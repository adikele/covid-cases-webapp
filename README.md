# covid-cases-webapp
A web application, coded in Python 3.7 and flask, for displaying Covid-19 country-wise data taking its source from EU Open Data Portal.
The web app is at: https://covid-19-visualizations.ey.r.appspot.com

By Aditya Kelekar, dt:24.8.2020, 
(This project was initially conceived as a local app: https://github.com/adikele/covid-19-visualizations 1.8.2020 - 17.8.2020)

PROJECT PLAN: 
Stage 1 (completed 24.8.2020): App displays country bar graphs in a user-entered country + 4 other random countries for a fixed date

Stage 2 (completed 30.8.2020): App displays country line graphs showing the rise or decline of Covid-19 infections in 3 user-entered countries 

Stage 3 (in the works): Developing APIs for this project

PROJECT DESCRIPTION: Programs to display Covid-19 data taking its source from a .csv file with worldwide figures.

DESCRIPTION OF COMPLETED WORK:
A bar graph showing the cumulative number of new virus infections per 100000 inhabitants is plotted for any user-entered country. 
The cumulative number is during the 14 days prior to the compilation date of the .csv file. 
The program also shows the data for four other countries, picked randomly, from the same continent as the user-entered country.

SPECIFICATIONS:
This program uses python 3.7 and the following libraries: (i) matplotlib 3.3.0 (ii) pandas 1.1.0 (iii) flask 1.1.2
This app will be updated on a weekly basis, using the latest "COVID-19 cases worldwide" .csv file.
The .csv file has been downloaded from: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data 

TESTS:
Tested for different countries by running program and manually checking ouput. 

HOW TO GET IN TOUCH: 
Please write to me at adityakelekar@yahoo.com for contributions and suggestions. Thank you!
