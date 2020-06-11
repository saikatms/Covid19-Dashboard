from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader

from . import getdata, plots, maps


# Create your views here.
def index(request):
    report_dict = ind_report()
    trends_dict = trends()
    # growth_dict = growth_plot()
    # daily_growth = daily_growth_plot()
    india_map_dict = india_map()
    cases_dict = global_cases()
    # ** growth_dict, ** daily_growth, ** cases_dict, ** world_map_dict
    # print(india_map_dict)

    # context = dict(report_dict, **trends_dict, **growth_dict, **cases_dict, **daily_growth, **world_map_dict)
    context = dict(report_dict, **trends_dict, **cases_dict)
    return render(request, template_name='index.html', context=context)


def ind_report():
    df = getdata.daily_report_india(date_string=None)
    Confirmed = int(df[0]['confirmed'])
    Deaths = int(df[0]['deaths'])
    Recovered = int(df[0]['recovered'])
    df = {'Confirmed': Confirmed, 'Deaths': Deaths, 'Recovered': Recovered}

    death_rate = f'{(Deaths / Confirmed) * 100:.02f}%'

    report_dict={"report":{'num_confirmed': df['Confirmed'],
        'num_recovered': df['Recovered'],
        'num_deaths': df['Deaths'],
        'death_rate': death_rate}}

    return report_dict["report"]


def trends():
    df = getdata.percentage_trends()
    return {
        'confirmed_trend': df['weekly_rate'].Confirmed,
        'deaths_trend': df['weekly_rate'].Deaths,
        'recovered_trend': df['weekly_rate'].Recovered,
        'death_rate_trend': df['weekly_rate'].Death_rate}


# def growth_plot():
#     plot_div = plots.total_growth()
#     return {'growth_plot': plot_div}
#
#
def global_cases():
    df = getdata.global_cases()
    return {'global_cases': df}
#
#
# def daily_growth_plot():
#     plot_div = plots.daily_growth()
#     return {'daily_growth_plot': plot_div}
#
#
def india_map():
    plot_div = maps.world_map()
    return {'world_map': plot_div}
#
#
# def mapspage(request):
#     plot_div = maps.usa_map()
#     return render(request, template_name='pages/maps.html', context={'usa_map': plot_div})
