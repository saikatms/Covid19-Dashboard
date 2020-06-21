import datetime
import json
import platform
import time
from urllib.request import urlopen

import pandas as pd

# Datasets scraped can be found in the following URL's:
# ¹ Johns Hopkins: https://github.com/CSSEGISandData/COVID-19
# ² Our World In Data: https://github.com/owid/covid-19-data/tree/master/public/data
# ³ New York Times: https://github.com/nytimes/covid-19-data

# Different styles in zero-padding in date depend on operating systems
from numpy import number

if platform.system() == 'Linux':
    STRFTIME_DATA_FRAME_FORMAT = '%-m/%-d/%y'
elif platform.system() == 'Windows':
    STRFTIME_DATA_FRAME_FORMAT = '%#m/%#d/%y'
else:
    STRFTIME_DATA_FRAME_FORMAT = '%-m/%-d/%y'


def daily_report(date_string=None):
    # Reports aggegrade data, dating as far back to 01-22-2020
    # If passing arg, must use above date formatting '01-22-2020'
    report_directory = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

    if date_string is None:
        yesterday = datetime.date.today() - datetime.timedelta(days=2)
        file_date = yesterday.strftime('%m-%d-%Y')
    else:
        file_date = date_string
    # print(report_directory + file_date + '.csv')
    df = pd.read_csv(report_directory + file_date + '.csv', dtype={"FIPS": str})
    return df


def daily_report_india(date_string=None):
    # Reports aggegrade data, dating as far back to 01-22-2020
    # If passing arg, must use above date formatting '01-22-2020'
    # report_directory = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
    report_directory = "https://api.covid19india.org/data.json";

    if date_string is None:
        yesterday = datetime.date.today() - datetime.timedelta(days=2)
        file_date = yesterday.strftime('%m-%d-%Y')
    else:
        file_date = date_string

    # df = pd.read_csv(report_directory + file_date + '.csv', dtype={"FIPS": str})
    json_url = urlopen(report_directory)
    df = json.loads(json_url.read())
    statewise_data = df['statewise']
    # cases_time_series=df['cases_time_series'][-1]
    # print(cases_time_series)
    # # print()
    return statewise_data



def todays_report(date_string=None):
    report_directory = "https://api.covid19india.org/data.json";

    if date_string is None:
        yesterday = datetime.date.today() - datetime.timedelta(days=2)
        file_date = yesterday.strftime('%m-%d-%Y')
    else:
        file_date = date_string

    # df = pd.read_csv(report_directory + file_date + '.csv', dtype={"FIPS": str})
    json_url = urlopen(report_directory)
    df = json.loads(json_url.read())
    live_data = df['statewise'][0]
    active_today=int(live_data['active'])
    yesterday_data= df['cases_time_series'][-1]
    active_yesterday=int(yesterday_data['totalconfirmed'])-(int(yesterday_data['totalrecovered'])+int(yesterday_data['totaldeceased']))
    # print(type(cases_time_series))
    # print(active_today,active_yesterday)
    increased=active_today-active_yesterday
    # print(increased)
    live_data['active_incrased']=increased
    return live_data



def confirmed_report():
    # Returns time series version of total cases confirmed globally
    report_directory = "https://api.covid19india.org/data.json";
    json_url = urlopen(report_directory)
    df = json.loads(json_url.read())
    cases_time_series = df['cases_time_series']
    return cases_time_series

    # df = pd.read_csv(
    #     'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    # return df


def deaths_report():
    # Returns time series version of total deaths globally
    report_directory = "https://api.covid19india.org/data.json";
    json_url = urlopen(report_directory)
    df = json.loads(json_url.read())
    cases_time_series = df['cases_time_series']
    return cases_time_series
    # df = pd.read_csv(
    #     'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    # return df


def recovered_report():
    # Return time series version of total recoveries globally
    report_directory = "https://api.covid19india.org/data.json";
    json_url = urlopen(report_directory)
    df = json.loads(json_url.read())
    cases_time_series = df['cases_time_series']
    return cases_time_series
    # df = pd.read_csv(
    #     'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    # return df
def active_report():
    report_directory = "https://api.covid19india.org/data.json";
    json_url = urlopen(report_directory)
    df = json.loads(json_url.read())
    cases_time_series = df['cases_time_series']
    return cases_time_series



def realtime_growth(date_string=None, weekly=False, monthly=False):
    """[summary]: consolidates all reports, to create time series of statistics.
    Columns excluded with list comp. are: ['Province/State','Country/Region','Lat','Long'].
    Args:
        date_string: must use following date formatting '4/12/20'.
        weekly: bool, returns df for last 8 weks
        monthly: bool, returns df for last 3 months
    Returns:
        [growth_df] -- [growth in series]
    """
    # df1 = confirmed_report()[confirmed_report().columns[4:]].sum()
    j_data = confirmed_report();
    df1 = pd.Series()
    for conf_data in j_data:
        date = time.strftime("%m/%d/%y", time.strptime(conf_data['date'] + '2020', "%d %B %Y"))
        df1[date] = conf_data['totalconfirmed']

    df2 = pd.Series()
    for conf_data in j_data:
        date = time.strftime("%m/%d/%y", time.strptime(conf_data['date'] + '2020', "%d %B %Y"))
        df2[date] = conf_data['totaldeceased']

    df3 = pd.Series()
    for conf_data in j_data:
        date = time.strftime("%m/%d/%y", time.strptime(conf_data['date'] + '2020', "%d %B %Y"))
        df3[date] = conf_data['totalrecovered']
    df4 = pd.Series()
    for conf_data in j_data:
        date = time.strftime("%m/%d/%y", time.strptime(conf_data['date'] + '2020', "%d %B %Y"))
        df4[date] = int(conf_data['totalconfirmed'])-(int(conf_data['totaldeceased'])+int(conf_data['totalrecovered']))
    growth_df = pd.DataFrame([])
    growth_df['Confirmed'], growth_df['Deaths'], growth_df['Recovered'],growth_df['active_cases_rate'] = df1, df2, df3,df4

    growth_df.index = growth_df.index.rename('Date')

    yesterday = (pd.Timestamp('now').date() - pd.Timedelta(days=1)).strftime("%m/%d/%y")
    if date_string is not None:
        return growth_df.loc[growth_df.index == date_string]

    if weekly is True:
        weekly_df = pd.DataFrame([])
        intervals = pd.date_range(end=yesterday, periods=8, freq='7D').strftime("%m/%d/%y").tolist()
        for day in intervals:
            weekly_df = weekly_df.append(growth_df.loc[growth_df.index == day])
        return weekly_df

    elif monthly is True:
        monthly_df = pd.DataFrame([])
        intervals = pd.date_range(end=yesterday, periods=3, freq='1M').strftime("%m/%d/%y").tolist()
        for day in intervals:
            monthly_df = monthly_df.append(growth_df.loc[growth_df.index == day])
        return monthly_df

    return growth_df


def percentage_trends():
    """[summary]: Returns percentage of change, in comparison to week prior.

    Returns:
        [pd.series] -- [percentage objects]
    """
    current = realtime_growth(weekly=True).iloc[-1]
    current = pd.to_numeric(current, downcast='integer')
    last_week = realtime_growth(weekly=True).iloc[-2]
    last_week = pd.to_numeric(last_week, downcast='integer')
    trends = round(number=((current - last_week) / last_week) * 100, ndigits=1)

    rate_change = round(((current.Deaths / current.Confirmed) * 100) - ((last_week.Deaths / last_week.Confirmed) * 100),
                        ndigits=2)
    trends_weekly = trends.append(pd.Series(data=rate_change, index=['Death_rate']))
    trends_dict = {"weekly_rate": trends_weekly}
    return trends_dict





def global_cases():
    """[summary]: Creates a table on total statistics of all countries,
    sorted by confirmations.
    Returns:
        [pd.DataFrame]
    """
    j_data = daily_report_india()
    df = pd.DataFrame(j_data)
    df = df.drop([0])
    df = df.groupby('state', as_index=False).sum()  # Dataframe mapper, combines rows where state value is the same
    df.sort_values(by=['confirmed'], ascending=False, inplace=True)
    return df

#
def usa_counties():
    """[summary]: Returns live cases of USA at county-level

    source:
        ³ nytimes
    Returns:
        [pd.DataFrame]
    """
    populations = pd.read_csv('https://raw.githubusercontent.com/balsama/us_counties_data/master/data/counties.csv')[
        ['FIPS Code', 'Population']]
    populations.rename(columns={'FIPS Code': 'fips'}, inplace=True)
    df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv',
                     dtype={"fips": str}).iloc[:, :6]
    df = pd.merge(df, populations, on='fips')
    df['cases/capita'] = (df.cases / df.Population) * 100000  # per 100k residents

    return df


def dist_data():
    report_directory="https://api.covid19india.org/state_district_wise.json"
    json_url=urlopen(report_directory)
    json_data=json.loads(json_url.read())
    dist_final={}
    for data in json_data:
        state=json_data[data]
        for dist in state:
            if dist=="districtData":
                dist_data=state[dist]
                dist_data_today = {}

                for d_data in dist_data:
                    # print(d_data)
                    dist_data_today[d_data] = dist_data[d_data]
            dist_final[state['statecode']]=dist_data_today
    return dist_final

def daily_confirmed():
    # returns the daily reported cases for respective date,
    # segmented globally and by country
    report_directory="https://api.covid19india.org/data.json";
    json_url=urlopen(report_directory)
    json_data=json.loads(json_url.read())
    df = json_data['cases_time_series']
    return df

# def daily_confirmed():
#     # returns the daily reported cases for respective date,
#     # segmented globally and by country
#     df = pd.read_csv('https://covid.ourworldindata.org/data/ecdc/new_cases.csv')
#     return df
#
#
# def daily_deaths():
#     # returns the daily reported deaths for respective date
#     df = pd.read_csv('https://covid.ourworldindata.org/data/ecdc/new_deaths.csv')
#     return df
