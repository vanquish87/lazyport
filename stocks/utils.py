import requests, time
from smartapi import SmartConnect
from decouple import config
import pyotp, requests
from datetime import datetime, timedelta
from .models import Stock_price


def instrumentList():
    instrument_list =  requests.get('https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json').json()
    return instrument_list


# then we need a symboltoken with the help of scriptid
# this is search from hash Table ie, JSON O(1)
def scriptName(scriptid, instrument_list):
    # get SCRIPTID from database of eq_stocks and convert them into stock_symbol
    stock_symbol = str(scriptid) + str('-EQ')
    for data in instrument_list:
        if data['symbol'] == stock_symbol:
            # print(data)
            # print(data['token'])
            # print(data['name'])
            # print(data['exch_seg'])
            return data['name'], data['exch_seg']


def loginAngel():
    obj = SmartConnect(api_key=config('API_KEY'))

    ENABLE_TOTP = config('ENABLE_TOTP')
    totp = pyotp.TOTP(ENABLE_TOTP)
    totp_now =totp.now()

    data = obj.generateSession(config('CLIENTCODE'),config('PASSWORD'),totp_now)
    return obj


# json of all the instrumentList from Angel_API
# we need instrument_list only once O(1) via requests
def instrumentList():
    instrument_list =  requests.get('https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json').json()
    return instrument_list


# then we need a symboltoken with the help of scriptid
# this is search from hash Table ie, JSON O(1)
def scriptToken(scriptid, instrument_list):
    # get SCRIPTID from database of eq_stocks and convert them into stock_symbol
    stock_symbol = str(scriptid) + str('-EQ')
    for data in instrument_list:
        if data['symbol'] == stock_symbol:
            # print(data)
            # print(data['token'])
            # print(data['name'])
            # print(data['exch_seg'])
            return data['token']


# historical data
# Max Days in one Request ONE_DAY = 2000, refer to smartapi docs
# scriptid = 'INFY', fromdate = '2022-05-05', todate = '2022-05-06'
def historical_angel(symboltoken, fromdate, todate, obj):
    try:
        historicParam={
        "exchange": "NSE",
        "symboltoken": symboltoken,
        "interval": "ONE_DAY",
        "fromdate": f"{fromdate} 09:00",
        "todate": f"{todate} 15:30"
        }
        return obj.getCandleData(historicParam)
    except Exception as e:
        print("Historic Api failed: {}".format(e.message))


# this is the main function to be called
def getDataAPI(scriptid, fromdate, todate, jwtToken, instrument_list):
    # this is search from hash Table ie, JSON O(1)
    symboltoken = scriptToken(scriptid, instrument_list)

    # it will give:
    # {'status': True, 'message': 'SUCCESS', 'errorcode': '', 'data': [['2023-01-02T00:00:00+05:30', 181.0, 189.3, 180.85, 187.7, 2692157], ['2023-01-03T00:00:00+05:30', 188.55, 194.35, 187.55, 190.2, 4258536], ['2023-01-04T00:00:00+05:30', 190.7, 192.6, 184.4, 186.65, 2161857], ['2023-01-05T00:00:00+05:30', 187.0, 188.65, 181.2, 188.1, 2510756]]}
    candle_data = historical_angel(symboltoken, fromdate, todate, jwtToken)
    closing_list = candle_data['data']

    return closing_list


# creating list of dates to current date to adjust to Angel API limit of 500 days
def date_list(fromdate):
    fromdate = '2010-01-01'
    fromdate_object = datetime.strptime(fromdate, '%Y-%m-%d')

    now = datetime.now()

    dates = [fromdate]

    while fromdate_object < now:
        fromdate_object = fromdate_object + timedelta(days=490)
        dates.append(fromdate_object.strftime('%Y-%m-%d'))

        if fromdate_object > now:
            dates.append(now.strftime('%Y-%m-%d'))

    return dates


def records_create_update(scripts, fromdate, todate, obj, instrument_list):
    print(fromdate, todate)
    # Create a list to hold the new Stock_price records
    new_records = []
    # Create a list to hold the existing Stock_price records that need to be updated
    existing_records = []

    for i in scripts:
        print(f'Fetching {i.id} of {len(scripts)}.')
        closing_list = getDataAPI(i, fromdate, todate, obj, instrument_list)
        # iterate through data and create or update stock_prices
        for row in closing_list:
            try:
                date = row[0]
                closing_price = round(row[4], 2)
                if not isinstance(closing_price, (float, int)):
                    raise ValueError(f"closing_price {closing_price} should be a decimal for {i.scriptid} on {date} ")
            except Exception as e:
                print(f"Error: {e}")
                continue

            date_object = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
            date_for_database = date_object.date()

            # Check if the Stock_price record already exists
            existing_record = Stock_price.objects.filter(stock=i, date=date_for_database).first()
            if existing_record:
                # If the record exists, add it to the list of existing records that need to be updated
                existing_record.closing_price = closing_price
                existing_records.append(existing_record)
            else:
                # If the record does not exist, create a new Stock_price record
                new_record = Stock_price(stock=i, date=date_for_database, closing_price=closing_price)
                new_records.append(new_record)

        time.sleep(0.15)

    return new_records, existing_records