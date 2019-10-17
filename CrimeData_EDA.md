Exploratory Data Analysis over Crime Data
_________________________________

Crime Data 2011 to current

File: Crimes_-_2001_to_present
_________________________________

Columns in the Dataset

Column Name	|	Type 	|	Description
-ID			number		Unique identifier
-Case Number		text		The Chicago Police Department RD Number (Records Division Number), 
						which is unique to the incident.
-Date			timestamp	Date when the incident occurred. this is sometimes a best estimate.
-Block			text		The partially redacted address where the incident occurred, placing 
						it on the same block as the actual address.
-IUCR			text		The Illinois Unifrom Crime Reporting code. This is directly linked to 
						the Primary Type and Description. See the list of IUCR codes 
						at https://data.cityofchicago.org/d/c7ck-438e.
-Primary Type		text		The primary description of the IUCR code.
-Description		text		The secondary description of the IUCR code, a subcategory of the primary description.
-Location Description	text		Description of the location where the incident occurred.
-Arrest			checkbox	Indicates whether an arrest was made.
-Domestic		checkbox	Indicates whether the incident was domestic-related as defined by the 
						Illinois Domestic Violence Act.
-Beat			text		Indicates the beat where the incident occurred. A beat is the smallest 
						police geographic area – each beat has a dedicated police beat car. 
						Three to five beats make up a police sector, and three sectors 
						make up a police district. The Chicago Police Department has 22
						police districts. See the beats at https://data.cityofchicago.org/d/aerh-rz74.
-District		text		Indicates the police district where the incident occurred. 
						See the districts at https://data.cityofchicago.org/d/fthy-xz3r.
-Ward			number		The ward (City Council district) where the incident occurred. See the wards 
						at https://data.cityofchicago.org/d/sp34-6z76.
-Community Area		text		Indicates the community area where the incident occurred. Chicago has 77 community areas. 
						See the community areas at https://data.cityofchicago.org/d/cauq-8yn6.
-FBI Code		text		Indicates the crime classification as outlined in the FBI's National Incident-Based Reporting System (NIBRS). 
						See the Chicago Police Department listing of these classifications 
						at http://gis.chicagopolice.org/clearmap_c
-X Coordinate		number		The x coordinate of the location where the incident occurred in State Plane Illinois East NAD 1983 projection. 
					This location is shifted from the actual location for partial redaction but falls on the same block.
-Y Coordinate		number		The y coordinate of the location where the incident occurred in State Plane Illinois East NAD 1983 projection. 
						This location is shifted from the actual location for partial redaction but falls on the same block.
-Year			number		Year the incident occureed.
-Updated On		timestamp	Date and time the record was last updated
-Latitude		number		The latitude of the location where the incident occurred. This location is shifted from the actual location 
						for partial redaction but falls on the same block.
-Longitude		number		The longitude of the location where the incident occurred. This location is shifted from the actual location 
						for partial redaction but falls on the same block.
-Location		location	The location where the incident occurred in a format that allows for creation of maps and other geographic 
						operations on this data portal. This location is shifted from the actual location for partial 
						redaction but falls on the same block.	

____________________________________________________________-

Exploratory Data Analysis Summary

Granularity: 	-Each record in the dataset represents a crime incident and related information
			such as location(in many different ways), crime type, case, etc.
		-It is important to note that due to the multiple ways to get locations
			there is lots of options to potentially geomapp our data 
Scope:		-The scope of the data includes recorded crimes in Chicago and all its districts.
			Since our objective is to analyze Chicago crimes the scope is broad enough to 
			provide us with our needed data.
Temporality:	-There are timestamps for the recorded incidents as well as updates
			The dataset begins in chronological order from 2011 to current (using API or latest dataset)
Faithfulness:	-Police Departments intention are to be transparent about crime and the reporting of the incidents
			due to their work to provide law enforcement to seek justice. This being said we are confident that
			the documenting of the incidents is accurate and upholding the high moral standard and interity
			of the Chicago Police Department.