from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader

from . import getdata, plots, maps


# Create your views here.




def index(request):
    report_dict = ind_report()
    trends_dict = trends()
    district_datas= dist_report()
    growth_dict = growth_plot()
    daily_growth = daily_growth_plot()
    #daily_state_growth=state_growth_plot()
    cases_dict = global_cases()
    world_map_dict = world_map()
    #
    # context = dict(report_dict, **trends_dict, **growth_dict, **cases_dict, **daily_growth, **world_map_dict)daily_state_growth
    context = dict(report_dict, **trends_dict, **cases_dict,**district_datas,**daily_growth)
    return render(request, template_name='index.html', context=context)


def dist_report():
    df=getdata.dist_data()
    return {"district_cases":df}

def ind_report():
    df = getdata.todays_report(date_string=None)
    Confirmed = int(df['confirmed'])
    Deaths = int(df['deaths'])
    Recovered = int(df['recovered'])
    dailyconfirmed = int(df['deltaconfirmed'])
    dailydeceased = int(df['deltadeaths'])
    dailyrecovered = int(df['deltarecovered'])
    total_active = int(df['active'])
    active_increases = int(df['active_incrased'])
    df = {'Confirmed': Confirmed, 'Deaths': Deaths, 'Recovered': Recovered, "dailyrecovered": dailyrecovered,
          "dailyconfirmed": dailyconfirmed, "dailydeceased": dailydeceased, "active_cases": total_active,
          "actived_increases": active_increases}

    death_rate = f'{(Deaths / Confirmed) * 100:.02f}%'

    report_dict = {"report": {'num_confirmed': df['Confirmed'],
                              'num_recovered': df['Recovered'],
                              'num_deaths': df['Deaths'],
                              'dailyconfirmed': df['dailyconfirmed'],
                              'dailydeceased': df['dailydeceased'],
                              'dailyrecovered': df['dailyrecovered'],
                              'actived_increases': df['actived_increases'],
                              'active_cases': df['active_cases'],
                              'death_rate': death_rate}}

    return report_dict["report"]


def trends():
    df = getdata.percentage_trends()
    return {
        'confirmed_trend': df['weekly_rate'].Confirmed,
        'deaths_trend': df['weekly_rate'].Deaths,
        'recovered_trend': df['weekly_rate'].Recovered,
        'death_rate_trend': df['weekly_rate'].Death_rate,
        'active_cases_rate': df['weekly_rate'].active_cases_rate}


def growth_plot():
    plot_div = plots.total_growth()
    return {'growth_plot': plot_div}


def global_cases():
    df = getdata.global_cases()
    return {'global_cases': df}



def daily_growth_plot():
    plot_div = plots.daily_growth()
    # print(plot_div)
    return {'daily_growth_plot': plot_div}

def state_growth_plot():
    state_plot_div=plots.state_daily_growth()

    return {'daily_growth_state_plot': state_plot_div}


def mapspage(request):
    plot_div = maps.usa_map()
    return render(request, template_name='pages/maps.html', context={'usa_map': plot_div})

def world_map():
    plot_div = maps.world_map()
    return {'world_map': plot_div}
