import json
from datetime import time, date

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.graph_objs import Layout
from plotly.offline import plot

from . import getdata
from .getdata import daily_confirmed


def total_growth():
    """[summary] Plots cumulative growth in a logarithmic y-scale
    Reference: https://plotly.com/python/line-and-scatter/

    Returns:
        [plotly.graph_objs] -- [plot_div compatible with Django]
    """
    df = getdata.realtime_growth()
    dates = pd.to_datetime(df.index)
    layout = Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_type='log',
        xaxis_showgrid=False,
        template='plotly_dark',
        showlegend=False,
        font=dict(color='#8898aa'),
        height=310,
        margin=dict(t=0, l=10, r=10, b=0)
    )
    fig = go.Figure(layout=layout)

    fig.update_layout(
        updatemenus=[
            dict(
                type='dropdown',
                buttons=list([
                    dict(
                        args=[{'yaxis.type': 'log'}],
                        label='Logarithmic',
                        method='relayout'
                    ),
                    dict(
                        args=[{'yaxis.type': 'linear'}],
                        label='Linear',
                        method='relayout'
                    )
                ]),
                x=0.05,
                xanchor='auto',
                bgcolor='rgba(0,0,0,0)'
            ),
        ]
    )

    confirmed_trace = go.Scatter(x=dates, y=df.Confirmed, name='Confirmed', mode='lines', line=dict(width=4))
    recovered_trace = go.Scatter(x=dates, y=df.Recovered, name='Recovered', mode='lines', line=dict(width=4))
    deaths_trace = go.Scatter(x=dates, y=df.Deaths, name='Deaths', mode='lines', line=dict(width=4),
                              marker_color='#f5365c')

    fig.add_traces([confirmed_trace, deaths_trace, recovered_trace])
    plot_div = plot(fig, output_type='div', config={'displayModeBar': False})

    return plot_div


def daily_growth():
    """[summary] Plots daily data of confirmations and deaths, as stacked bar
    Reference: https://plotly.com/python/bar-charts/

    Returns:
        [plotly.graph_objs] -- [plot_div compatible with Django]
    """
    daily_cases = getdata.daily_confirmed()
    df_dailyCases = pd.DataFrame(daily_cases)
    daily_confirmed = df_dailyCases[["date", "dailyconfirmed"]]
    daily_confirmed['date'] = daily_confirmed['date'].astype(str) + ' 2020'
    daily_confirmed['date'] = pd.to_datetime(daily_confirmed.date)

    daily_deaths = df_dailyCases[["date", "dailydeceased"]]
    daily_deaths['date'] = daily_deaths['date'].astype(str) + ' 2020'
    daily_deaths['date'] = pd.to_datetime(daily_deaths.date)

    daily_recovered=df_dailyCases[["date","dailyrecovered"]]
    daily_recovered['date']=daily_recovered['date'].astype(str)+'2020'
    daily_recovered['date']=pd.to_datetime(daily_recovered.date)

    layout = Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(x=0.025, y=1), height=310,
                    margin=dict(t=0, l=15, r=10, b=0), barmode='stack')
    fig = go.Figure(layout=layout)
    daily_deaths_trace = go.Bar(x=daily_deaths.date, y=daily_deaths.dailydeceased, name='Deaths',
                                marker_color='#f5365c')
    daily_cases_trace = go.Bar(x=daily_confirmed.date, y=daily_confirmed.dailyconfirmed, name='Confirmed',
                               marker_color='#5603ad')
    daily_recovered_trace=go.Bar(x=daily_recovered.date,y=daily_recovered.dailyrecovered,name='Recovered',
                                 marker_color='#2fb307')
    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=7, label='W', step='day', stepmode='backward'),
                dict(count=14, label='2W', step='day', stepmode='backward'),
                dict(count=1, label='M', step='month', stepmode='backward'),
                dict(count=3, label='3M', step='month', stepmode='backward', ),
                dict(label='T', step='all')
            ]))
    )

    fig.update_yaxes(gridcolor='#fff')
    fig.add_traces([daily_cases_trace, daily_deaths_trace,daily_recovered_trace])
    plot_div = plot(fig, output_type='div', config={'displayModeBar': False})
    # print(plot_div)
    return plot_div


def state_daily_growth():
    daily_cases = getdata.statewise_daily()
    daily_cases_confirmed=daily_cases['data_confirmed']
    daily_cases_deaths=daily_cases['data_Death']
    daily_cases_recovered=daily_cases['data_Recovered']
    df_confirmed=pd.DataFrame(daily_cases_confirmed)
    df_deaths=pd.DataFrame(daily_cases_deaths)
    df_recovered=pd.DataFrame(daily_cases_recovered)
    df_confirmed = df_confirmed.drop('status', 1)
    df_deaths=df_deaths.drop('status',1)
    df_recovered=df_recovered.drop('status',1)
    df_confirmed['date'] = pd.to_datetime(df_confirmed.date)
    df_deaths['date']=pd.to_datetime(df_deaths.date)
    df_recovered['date']=pd.to_datetime(df_recovered.date)

    layout = Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(x=0.025, y=1), height=310,
                    margin=dict(t=0, l=15, r=10, b=0), barmode='stack')

    dicts={}
    for key in df_confirmed.keys():
        # print(key)
        fig = go.Figure(layout=layout)
        lists = []
        if key == "date":
            continue
        else:
            # print(key)
            daily_cases_trace = go.Bar(x=df_confirmed.date, y=df_confirmed[key], name="Confirmed", visible='legendonly')
            daily_deaths_trace=go.Bar(x=df_deaths.date,y=df_deaths[key],name="Deaths",marker_color='#f5365c')
            daily_recovered_trace=go.Bar(x=df_recovered.date,y=df_recovered[key],name="Recovered", marker_color='#2fb307')
            fig.update_xaxes(
                rangeselector=dict(
                    buttons=list([
                        dict(count=7, label='W', step='day', stepmode='backward'),
                        dict(count=14, label='2W', step='day', stepmode='backward'),
                        dict(count=1, label='M', step='month', stepmode='backward'),
                        dict(count=3, label='3M', step='month', stepmode='backward'),
                        dict(label='T', step='all')
                    ]))
            )

            fig.update_yaxes(gridcolor='#fff')
            fig.add_traces([daily_cases_trace,daily_deaths_trace,daily_recovered_trace])
            plot_div = plot(fig, output_type='div', config={'displayModeBar': False})
            dicts[key]=plot_div

    return dicts

