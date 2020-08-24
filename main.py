import io
import random

import pandas as pd
import random
from flask import Flask, request, render_template, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

DATA_FILE = "EUOpenData_24_8_2020"
DATA_DATE = "24.8.2020"
NEXT_UPDATE_DATE = "31.8.2020"
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
        df_current = df[(df["continentExp"] == i) & (df["dateRep"] == "28/07/2020")]
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
        (df["countriesAndTerritories"] == country_sel) & (df["dateRep"] == "28/07/2020")
    ]
    dict1 = dfc.to_dict()
    continent = list(dict1["continentExp"].values())
    continent = continent[0]

    # getting the list of countries from the same continent
    df2 = df[(df["continentExp"] == continent) & (df["dateRep"] == "28/07/2020")]
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
    axis.set_ylabel("Persons infected in last 14 days")
    axis.set_title(f"Cumulative number (14 days) of COVID-19 cases per 100000 persons \n Data updated on: {DATA_DATE} Next update: {NEXT_UPDATE_DATE}")
    return fig


@app.route("/")
def index():
    return render_template("index.jinja2")


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


if __name__ == "__main__":
    app.server(host="0.0.0.0", port=8080, debug=True)
