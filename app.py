# This module has functions for creating bargraphs and linegraphs
# The functions for bargraphs are written first, followed by those for linegraphs
# Bargraphs show countries and cases for:
# (i) 1 user-entered country + (ii) 4 random countries from same continent as user entered country
# Linegraphs plot number of case (yaxis) versus time (xaxis) for 3 user-entered countries
# .csv data file obtained from: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data
# Program created by Aditya Kelekar (adityakelekar@yahoo.com)
import io
import random
import pandas as pd
from flask import Flask, request, render_template, Response, jsonify
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

DATA_FILE = "EUOpenData_06_12_2020"
DATA_DATE = "06/12/2020"
NEXT_UPDATE_DATE = "13/12/2020"
NUMBER_OF_DAYS = 240
global x, y

app = Flask(__name__)


def read_input():
    print("At the prompt below, enter name of a country and press enter.")
    country = input("Enter country name: ")
    return country


def input_validataion(name_country, dict_all_countries):
    """
    Function takes name_country, a string.
    It queries the population api to check if name_country exists in database
    Function returns true if name_country exists, false otherwise
    """
    for country_list in dict_all_countries.values():
        if name_country in country_list:
            return True
    return False


def fetch_all_countries(df):
    """
    Function finds the list of countries from all the continents
    It takes a dataframe of the input data file
    Returns a dict with keys --> continents
                      values --> list of countries in the respective continents  
    """
    continents = ("Africa", "Europe", "America", "Oceania", "Asia")
    dict_all_countries = dict()
    for i in continents:
        df_current = df[(df["continentExp"] == i) & (df["dateRep"] == DATA_DATE)]
        dict_countries_current_continent = df_current.to_dict()
        list_countries_current_continent = list(
            dict_countries_current_continent["countriesAndTerritories"].values()
        )
        dict_all_countries[i] = list_countries_current_continent
    return dict_all_countries


def fetch_home_continent_data(df, country_sel):
    """
    Function finds the countries and cases for the home continent
    It takes (i) a dataframe of the input data file (ii) a string, country_sel
    Returns two lists: (i) a list of countries (ii) a list of cases
    """
    # determining the continent in which the selected country is situated
    dfc = df[
        (df["countriesAndTerritories"] == country_sel) & (df["dateRep"] == DATA_DATE)
    ]
    dict1 = dfc.to_dict()
    continent = list(dict1["continentExp"].values())
    continent = continent[0]

    # getting the list of countries from the same continent
    df2 = df[(df["continentExp"] == continent) & (df["dateRep"] == DATA_DATE)]
    dict2_countries_of_a_continent = df2.to_dict()
    list_countries = list(
        dict2_countries_of_a_continent["countriesAndTerritories"].values()
    )

    # extracting the number of Covid cases for the countries from the same continent
    list_cases = dict2_countries_of_a_continent[
        "Cumulative_number_for_14_days_of_COVID-19_cases_per_100000"
    ].values()

    return (list_countries, list_cases)


def random_countries(list_countries, country_sel):
    """  
    Function selects 4 random countries, none of which are to be the user-selected country
    It takes (i) a list of countries
    (ii) a string, country_sel
    Returns a list of 4 random countries 
    """
    list_countries_random = random.sample(list_countries, 4)
    if country_sel in list_countries_random:
        while True:
            list_countries_random = random.sample(list_countries, 4)
            if country_sel not in list_countries_random:
                break  # this way we always have 5 unique countries: 4 + 1
    return list_countries_random


def fetch_five_countries_data(dict_countries_cases, country_sel, list_countries_random):
    """
    Function creates a dict of countries and cases for 5 countries
    It takes (i) a dict of countries and cases (ii) a string, country_sel
    (iii) a list of 4 random countries 
    Returns a dict of countries and cases for 5 countries 
    """
    dict_fivecountries = dict()
    dict_fivecountries[country_sel] = dict_countries_cases[country_sel]

    for country in list_countries_random:
        dict_fivecountries[country] = dict_countries_cases[country]

    return dict_fivecountries


# plotting countries and cases:
def create_figure(countries, cases):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.bar(countries, cases, color="blue")
    axis.set_ylabel("Persons infected in last 14 days (source: EU Open Data)")
    axis.set_title(
        f"Cumulative number (14 days) of COVID-19 cases per 100000 persons \n Data updated on: {DATA_DATE}  Next update: {NEXT_UPDATE_DATE}"
    )
    return fig


# NOTE: processing functions for linegraphs start from here..
def creating_date_list(df, n):
    df1 = df[df["countriesAndTerritories"] == "Afghanistan"]
    dict1_one_country = df1.to_dict()
    date_list = list(dict1_one_country["dateRep"].values())
    newlistdate_list = date_list[:n]  # take the last "n" days
    newlistdate_list.reverse()  # reverse the list, now list ends with latest date
    return newlistdate_list


def fetch_all_continent_data(df):
    """
    Function finds the countries and cases for all continents
    It takes a dataframe of the input data file 
    Returns two things: (i) a list of countries 
    (ii) a dict with keys --> countries 
                   values --> list of cases for each of the days recorded since Dec 2019
    """
    # extracting the countries from all continents:
    df3 = df[(df["dateRep"] == DATA_DATE)]
    dict3_countries_of_all_continent = df3.to_dict()
    countries_list = list(
        dict3_countries_of_all_continent["countriesAndTerritories"].values()
    )
    z = len(countries_list)  # getting the number of countries

    dict_countries_cases = dict()
    for i in range(z):
        df_current = df[df["countriesAndTerritories"] == countries_list[i]]
        dict_current = df_current.to_dict()
        dict_countries_cases[countries_list[i]] = list(
            dict_current[
                "Cumulative_number_for_14_days_of_COVID-19_cases_per_100000"
            ].values()
        )

    return countries_list, dict_countries_cases


def fetch_three_countries_data(
    dict_countries_cases, country_sel1, country_sel2, country_sel3, n
):
    """
    Function creates a dict of countries and cases for 3 countries
    It takes (i) a dict of countries and cases (ii) 3 strings, names of countries
    (iii) an integer, number of days for which data is desired.
    Returns a dict of countries and cases for 3 countries
    """
    # creating a dict of countries and cases for the 3 countries
    dict_threecountries = dict()
    dict_threecountries[country_sel1] = dict_countries_cases[country_sel1]
    dict_threecountries[country_sel2] = dict_countries_cases[country_sel2]
    dict_threecountries[country_sel3] = dict_countries_cases[country_sel3]

    # within the dict, "process" the list of case numbers
    for i in dict_threecountries.keys():
        abc_real_list = dict_threecountries[i]
        newabc_real_list = abc_real_list[:n]  # take the last "n" days
        newabc_real_list.reverse()  # reverse the list, now list ends with latest cases
        dict_threecountries[i] = newabc_real_list

    return dict_threecountries


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api_info")
def api_info():
    return render_template("api_info.html")

@app.route("/country_form")
def country_form():
    df = pd.read_csv(DATA_FILE)
    dict_all_countries = fetch_all_countries(df)
    list_all_countries = []
    for i in dict_all_countries.values():
        for j in i:
            list_all_countries.append(j)
    list_all_countries_sorted = sorted(list_all_countries)
    return render_template("country_form.jinja2", options=list_all_countries_sorted)


@app.route("/countries_result", methods=["POST"])
def countries_result():
    global x
    global y
    country_sel = request.form["country_name"]

    df = pd.read_csv(DATA_FILE)

    list_countries, list_cases = fetch_home_continent_data(df, country_sel)

    dict_continent = dict(zip(list_countries, list_cases))

    list_countries_random = random_countries(list_countries, country_sel)

    dict_fivecountries = fetch_five_countries_data(
        dict_continent, country_sel, list_countries_random
    )

    x = dict_fivecountries.keys()
    y = dict_fivecountries.values()

    fig = create_figure(x, y)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return render_template("countries_result.jinja2", result=dict_fivecountries.keys())


@app.route("/plot.png")
def plot():
    global x
    global y
    fig = create_figure(x, y)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


# NOTE: template and graph functions for linegraphs start from here..
# plotting countries and cases over time:
def create_figure_linegraphs(newlistdate_list, dict_three_countries):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    for i in dict_three_countries.keys():
        axis.plot(newlistdate_list, dict_three_countries[i], label=i)
    axis.set_xticks(
        ["15/04/2020", "15/05/2020", "15/06/2020", "15/07/2020", "15/08/2020", "15/09/2020", "15/10/2020", "15/11/2020"]
    )
    z = ["mid-April", "mid-May", "mid-June", "mid-July", "mid-Aug", "mid-Sept", "mid-Oct", "mid-Nov"]
    axis.set_xticklabels(z)
    axis.set_ylabel("Cumulative number of new virus infections per 100000 inhabitants")
    axis.set_xlabel("Year 2020 (last update: 6th Dec 2020)")  
    axis.set_title("Covid-19 infections - Country Graphs (source: EU Open Data)")
    axis.legend(loc="best")
    return fig


@app.route("/linegraphs_form")
def linegraphs_form():
    df = pd.read_csv(DATA_FILE)
    dict_all_countries = fetch_all_countries(df)
    list_all_countries = []
    for i in dict_all_countries.values():
        for j in i:
            list_all_countries.append(j)
    list_all_countries_sorted = sorted(list_all_countries)
    return render_template("linegraphs_form.jinja2", options=list_all_countries_sorted)


@app.route("/plot_linegraphs.png", methods=["POST"])
def plot_linegraphs():
    global x
    global y
    
    country_sel1 = request.form["country_name1"]
    country_sel2 = request.form["country_name2"]
    country_sel3 = request.form["country_name3"]

    df = pd.read_csv(DATA_FILE)

    list_countries, dict_countries_cases = fetch_all_continent_data(df)

    dict_three_countries = fetch_three_countries_data(
        dict_countries_cases, country_sel1, country_sel2, country_sel3, NUMBER_OF_DAYS
    )

    newlistdate_list = creating_date_list(df, NUMBER_OF_DAYS)

    fig = create_figure_linegraphs(newlistdate_list, dict_three_countries)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


@app.route('/api/v1/bargraph/country', methods=['GET'])
def api_id():
    '''
    Provides an endpoint
    Returns a dictionary with:
    keys --> user-entered country + 4 other random countries from the same continent as user-entered country
    values --> ”number of cases” for each of the countries 
    '''
    if 'id' in request.args:
        id = str(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    df = pd.read_csv(DATA_FILE)
    country_sel = id
    dict_all_countries = fetch_all_countries (df)
    list_countries, list_cases = fetch_home_continent_data(df, country_sel)
    dict_continent = dict(zip(list_countries, list_cases)) 
    list_countries_random = random_countries(list_countries, country_sel)
    dict_fivecountries = fetch_five_countries_data(dict_continent, country_sel, list_countries_random)
    return jsonify(dict_fivecountries)


if __name__ == '__main__':
    app.debug = True
    app.run()
