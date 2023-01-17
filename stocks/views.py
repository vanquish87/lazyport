from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Stock, Stock_price
from .utils import instrumentList, scriptName, loginAngel, date_list, records_create_update, bulk_operations
from .scripts import scripts
from django.contrib import messages
from django.db.models.functions import Cast
from django.db.models import FloatField
import pandas as pd
from django.views.decorators.cache import cache_page



# Create your views here.
@login_required(login_url='login')
def add_stock(request):
    instrument_list = instrumentList()
    for scriptid in scripts:
        name, exch_seg = scriptName(scriptid, instrument_list)
        print(name, exch_seg)
        if Stock.objects.filter(scriptid=name).exists() is False:
            stock = Stock(scriptid=name, exchange=exch_seg)
            stock.save()
    context = {}
    return render(request, 'stocks/create-entry.html', context)



@login_required(login_url='login')
def search_stock(request):
    context = {}
    return render(request, 'stocks/search-results.html', context)



@login_required(login_url='login')
@cache_page(60 * 15)
def search_list(request):
    query = request.GET.get('q')
    if query:
        stocks = Stock.objects.filter(scriptid__icontains=query)
    else:
        stocks = Stock.objects.all()

    context = {'stocks': stocks}
    return render(request, 'stocks/search-list.html', context)



@login_required(login_url='login')
def stock_price_start(request):
    # need jwtToken & instrument_list first
    obj = loginAngel()
    instrument_list = instrumentList()

    fromdate = '2010-01-01'
    dates = date_list(fromdate)

    for i in range(len(dates)-1):
        fromdate = dates[i]
        todate = dates[i+1]

        scripts = Stock.objects.all().order_by().select_related('stockprice_set').values('id', 'scriptid')

        new_records, existing_records, msg = records_create_update(scripts=scripts, obj=obj, instrument_list=instrument_list, fromdate=fromdate, todate=todate)
        bulk_operations(new_records, existing_records)

    messages.info(request, 'All Stock prices are CREATED upto today!')

    return redirect('profile')



@login_required(login_url='login')
def stock_price_update(request):
    # need jwtToken & instrument_list first
    obj = loginAngel()
    instrument_list = instrumentList()

    scripts = Stock.objects.all().order_by().select_related('stockprice_set').values('id', 'scriptid')

    new_records, existing_records, msg = records_create_update(scripts=scripts, obj=obj, instrument_list=instrument_list, update=True)

    if msg:
        messages.info(request, msg)
    else:
        bulk_operations(new_records, existing_records)
        messages.info(request, 'All stock prices have been UPDATED as of today.')
    return redirect('index')



@login_required(login_url='login')
@cache_page(60 * 15)
def stock_chart(request, stock_id, scriptid):
    prices = Stock_price.objects.filter(stock=stock_id).annotate(closing_price_float=Cast('closing_price', FloatField())).values('date', 'closing_price_float')

    date_list = [x['date'].strftime('%Y-%m-%d') for x in prices]

    closing_price_list = [round(x['closing_price_float'], 2) for x in prices]

    df = pd.DataFrame({'date': date_list, 'closing_data': closing_price_list})

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Resample the dataframe to a weekly frequency and take the last value of each week's closing data
    df_weekly = df.resample('W-FRI').last()
    closing_data_weekly = df_weekly['closing_data'].tolist()

    dates_weekly = df_weekly.index.strftime("%Y-%m-%d").tolist()

    # Resample the dataframe to a monthly frequency and take the last value of each month's closing data
    df_monthly = df.resample('M').last()
    closing_data_monthly = df_monthly['closing_data'].tolist()

    dates_monthly = df_monthly.index.strftime("%Y-%m-%d").tolist()

    context = {
        'scriptid': scriptid,
        'date_list': date_list,
        'closing_price_list': closing_price_list,
        'dates_weekly': dates_weekly,
        'closing_data_weekly': closing_data_weekly,
        'dates_monthly': dates_monthly,
        'closing_data_monthly': closing_data_monthly,
    }

    return render(request, 'stocks/stock-chart.html', context)
