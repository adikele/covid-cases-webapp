# covid-cases-webapp
By Aditya Kelekar, update:11.11.2020,

PROJECT DESCRIPTION: 
A web site, coded in Python 3.7 for displaying Covid-19 country-wise data taking its source from EU Open Data Portal.
Uses the following libraries: (i) matplotlib 3.3.0 (ii) pandas 1.1.0 (iii) flask 1.1.2
The web site is at: https://covid-19-visualizations.ey.r.appspot.com
This app is updated regularly, using the latest "COVID-19 cases worldwide" .csv file.
The .csv file has been downloaded from: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data 
(This project was initially conceived as a local app: https://github.com/adikele/covid-19-visualizations 1.8.2020 - 17.8.2020)

PROJECT PLAN: 
Stage 1 (completed 24.8.2020): App displays country bar graphs in a user-entered country + 4 other random countries for a fixed date

Stage 2 (completed 30.8.2020): App displays country line graphs showing the rise or decline of Covid-19 infections in 3 user-entered countries 

Stage 3 (completed 11.11.2020): Developing APIs for this project: first endpoint created

Stage 4 (11.11.2020 - ongoing): Extending program to store results in the cloud

Programs to display Covid-19 data taking its source from a .csv file with worldwide figures.

DESCRIPTION OF WEBSITE:
Countries and Cases bar graphs:
Bargraphs of one user-entered country and four other countries from the same continent as the user-entered country.
Spread of Infections in countries:
Linegraphs of infections in three user-entered countries over a period of time
Note: To calculate the number of infections, the data source of this program takes the cumulative number of new virus infections per 100000 inhabitants for every country. This cumulative number is during the 14 days prior to the compilation date of the .csv file. 

TESTS:
Tested for different countries by running program and manually checking ouput. 

HOW TO GET IN TOUCH: 
Please write to me at adityakelekar@yahoo.com for contributions and suggestions. Thank you!
