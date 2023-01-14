from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Stock
from .utils import instrumentList, scriptName
from .scripts import scripts


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

    context = {'stocks': stocks}
    return render(request, 'stocks/search-list.html', context)