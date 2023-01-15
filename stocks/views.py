from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Stock, Stock_price
from .utils import instrumentList, scriptName, loginAngel, date_list, records_create_update
from .scripts import scripts
from django.db import transaction
from django.db.models.functions import Cast
from django.db.models import FloatField


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

        scripts = Stock.objects.all().order_by()

        new_records, existing_records = records_create_update(scripts, fromdate, todate, obj, instrument_list)

        # Use the transaction.atomic decorator to ensure that the bulk create and update operations are atomic
        with transaction.atomic():
            Stock_price.objects.bulk_create(new_records)
            Stock_price.objects.bulk_update(existing_records, ['closing_price'])

    return redirect('profile')


def stock_chart(request, stock_id):
    prices = Stock_price.objects.filter(stock=stock_id).annotate(closing_price_float=Cast('closing_price', FloatField())).values('date', 'closing_price_float')
    date_list = list(map(lambda x: x['date'].strftime('%Y-%m-%d'), prices))
    closing_price_list = [round(x['closing_price_float'], 2) for x in prices]

    context = {
        'date_list': date_list,
        'closing_price_list': closing_price_list
    }

    return render(request, 'stocks/stock-chart.html', context)


