README
________________________________
Author: Cesar Lazcano

Files:
-main file:	Crime_app.py
-preprocessor:  Preprocess_Feather.py
-Util file:	Utilities.py
-additional:    < crime csv and/or .feather>

Description:
This folder contains a Dash app that will run a localhost server, visit to view webpage.
The webpage contains visualizations of Chicago crime data from years covered by the the original 
crime csv file. I personally chose 2014-2018 combined into a single csv for most current results.
The app itself reads a compressed .feather file created from the csv. On first run if .feather is missin
the app will run preprocess and create the .feather file from csv. From thereon forward it will load
from existing .feather file.

The app is interactive with the year and the crime types. I have set initial values 
for the user:
	burglary, assault, robbery
I chose these defaults because when tied with neighborhoods in the project this can reflect personal safety
best with minimal filters. 
 
___________________________________________
RUN DIRECTION

cmd: 
python Crime_App.py <your_cimedata.csv>

___________________________________________

