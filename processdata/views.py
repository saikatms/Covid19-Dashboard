import json
from builtins import type

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader

from . import getdata, plots, maps
import pandas as pd


# Create your views here.


def index(request):
    report_dict = ind_report()
    trends_dict = trends()
    # growth_dict = growth_plot()
    daily_growth = daily_growth_plot()
    cases_dict = global_cases()
    statewise_pie_chart = statewise_sunburst()

    context = dict(report_dict, **trends_dict, **cases_dict,**statewise_pie_chart,**daily_growth)
    return render(request, template_name='index.html', context=context)





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
    lastupdatedtime=df['lastupdatedtime']
    df = {'Confirmed': Confirmed, 'Deaths': Deaths, 'Recovered': Recovered, "dailyrecovered": dailyrecovered,
          "dailyconfirmed": dailyconfirmed, "dailydeceased": dailydeceased, "active_cases": total_active,
          "actived_increases": active_increases,'lastupdatedtime':lastupdatedtime}

    death_rate = f'{(Deaths / Confirmed) * 100:.02f}%'

    report_dict = {"report": {'num_confirmed': df['Confirmed'],
                              'num_recovered': df['Recovered'],
                              'num_deaths': df['Deaths'],
                              'dailyconfirmed': df['dailyconfirmed'],
                              'dailydeceased': df['dailydeceased'],
                              'dailyrecovered': df['dailyrecovered'],
                              'actived_increases': df['actived_increases'],
                              'active_cases': df['active_cases'],
                              'death_rate': death_rate,
                              "lastupdatedtime":lastupdatedtime
                              }}

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


def state_growth_plot(statecode):
    state_plot_div = plots.state_daily_growth(statecode)
    return state_plot_div


def mapspage(request):
    plot_div = maps.usa_map()
    return render(request, template_name='pages/maps.html', context={'usa_map': plot_div})


def statewise_sunburst():
    plot_div = plots.statewie_pie_sunbrust()
    return {'sunbrust_plot': plot_div}

def distwise_sunburst(statecode):
    plot_div=plots.distwies_pie_sunbrust(statecode)
    return plot_div

def stateView(request, statecode):
    statedata=getdata.statewisedata()
    df_state=statedata.loc[statedata['statecode']==statecode]
    df_state=df_state.reset_index(drop=True)
    df=df_state.to_json(orient='records')
    json_data=json.loads(df)
    state_data=json_data[0]
    # df['active']=int(df[0]['active'])
    state_data['active_cases']=(int(json_data[0]['active']))
    state_data['num_confirmed']=(int(json_data[0]['confirmed']))
    state_data['num_deaths']=(int(json_data[0]['deaths']))
    state_data['num_recovered']=(int(json_data[0]['recovered']))
    state_data['dailyconfirmed']=(int(json_data[0]['deltaconfirmed']))
    state_data['dailydeceased']=(int(json_data[0]['deltadeaths']))
    state_data['dailyrecovered']=(int(json_data[0]['deltarecovered']))
    state_data['migratedother']=(int(json_data[0]['migratedother']))
    activeChanges=getdata.stateDailydata(statecode)
    state_data['activeChnge']=int(activeChanges)

    dist_data=dist_report(statecode)
    state_data['distwise_data']=dist_data

    daily_state_growth = state_growth_plot(statecode)
    state_data['state_growth_plot']=daily_state_growth

    dist_pie_chart = distwise_sunburst(statecode)
    state_data['dist_pie_chart']=dist_pie_chart

    return render(request, 'state.html', state_data)
    # pass
def dist_report(statecode):
    df = getdata.dist_data(statecode)
    return df[statecode]


