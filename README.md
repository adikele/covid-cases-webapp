# covid-cases-webapp
By Aditya Kelekar, updated: 6.4.2021

PROJECT DESCRIPTION: 
The purpose of this project is to develop software to visualize Covid-19 infection rates. 
Potential users are academicians, researchers and journalists. Such users can interact with the project’s website to create visual representations of Covid-19 data and save these as files. 
The data source is EU Open Data Portal: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data 
The project uses the following libraries: (i) matplotlib 3.3.0 (ii) pandas 1.1.0 (iii) flask 1.1.2

The project website can be found at: https://covid-19-visualizations.ey.r.appspot.com/ 
Currently website users can plot graphs for:
(i) Bargraphs of one user-entered country and four other countries from the same continent
(ii) Linegraphs of infections in three user-entered countries over a period of time

INSTALLATION AND RUNNING THE PROJECT:
On Linux and Mac:
Download this project from Github and run it like any other Flask Python project.
Here are the steps to download and run the project:

Step 1 : Install Python 3.7+ 

Step 2 : In your Terminal, first cd into the directory you would like to store the Covid project. 
Then type the following commands one after another in your Terminal:
```
mkdir covid-project && cd covid-project
python3 -m venv covid-venv
source covid-venv/bin/activate
git clone https://github.com/adikele/covid-cases-webapp
cd covid-cases-webapp
pip install -r requirements.txt
python app.py 
```

Your installation is successful if you have a message saying:
Serving Flask app "app" (lazy loading)
(more output)
Running on http://127.0.0.1:5000/

Step 3 : Leave the Terminal or minimize it but do not close the Terminal. 
Go to your browser and paste the URL: http://127.0.0.1:5000/
The site page displayed should have the title: COVID-19 PLOTS

Click on: Countries and Cases bar graphs

Scroll and select Bhutan, click on: Show results

Click on: Show bargraph

Your downloaded project is running successful if you see a bar graph with Bhutan and four other countries.

Note: If you want to exit from the project on your Terminal, either close or it press: Ctrl + C

TESTS:
Tested for different countries by running program and manually checking ouput. 

HOW TO GET IN TOUCH: 
Please write to me at adityakelekar@yahoo.com for contributions and suggestions. Thank you!
