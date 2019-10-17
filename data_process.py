import pandas as pd
import json
import csv

name_map = {'hanson park': 'belmont cragin', 
			'edgebrook': 'forest glen', 
			'old edgebrook': 'forest glen',
			'south edgebrook': 'forest glen',
			'sauganash': 'forest glen',
			'wildwood': 'forest glen',
			'belmont gardens': 'hermosa',
			'kelvyn park': 'hermosa',
			'lakeview': 'lake view',
			'the loop': 'loop',
			'new east side': 'loop',
			'south loop': 'loop',
			'dearborn park': 'near south side',
			"printer's row": 'near south side',
			'south loop nss': 'near south side',
			'prairie district': 'near south side',
			'little italy': 'near west side',
			'tri-taylor': 'near west side',
			'horner park': 'north center',
			'roscoe village': 'north center',
			'schorsch forest view': 'ohare',
			'south lawndale / little village': 'south lawndale',
			'brainerd': 'washington heights',
			'longwood manor': 'washington heights',
			'princeton park': 'washington heights',
			'east village': 'west town',
			'noble square': 'west town',
			'polish downtown': 'west town',
			'pulaski park': 'west town',
			'smith park': 'west town',
			'ukrainian village': 'west town',
			'wicker park': 'west town'}

with open('chicago_communities.geojson') as f:
	geo = f.read()
	geojson = json.loads(geo)

def process_crime():
	df = pd.read_csv('crime_data.csv')
	crime_type = list(set(df['primary_type'].values))
	codes = list(set(df['community_area'].values))
	years = [i for i in range(2011, 2019)]
	records = []
	for co in codes:
		for y in years:
			rec = [co, y]
			for t in crime_type:
				count = 0
				curr = df.loc[(df['community_area']==co) & (df['year']==y) & (df['primary_type']==t), 'count']

				if len(curr.values) != 0:
				    count = curr.values[0]
				    
				rec.append(count)

			records.append(rec)
	cols = ['community', 'year'] + crime_type
	return pd.DataFrame(records, columns=cols)

def process_realestate():
	names = [geojson['features'][k]['properties']['community'].lower() for k in range(len(geojson['features']))]
	code_name_dict = {}
	for c in geojson['features']:
		code_name_dict[int(c['properties']['area_numbe'])] = c['properties']['community'].lower()
	realestate = []
	with open('ppsf.csv', encoding='utf-16') as re_file:
		next(re_file)
		reader = csv.reader(re_file, delimiter='\t')

		for row in reader:
			realestate.append(row)
	#Duplicate neighborhood 'south loop' because it belongs to both 'loop' and 'near south side'
	southloop = []
	for row in realestate:
		if row[0].replace('Chicago, IL - ', '').lower() == 'south loop':
			southloop = row.copy()
			break
	southloop[0] = 'south loop nss'
	realestate.append(southloop)

	#Lowercase community names
	for row in realestate:
		row[0] = row[0].replace('Chicago, IL - ', '').lower()

	#Transform neighborhood name to community name
	for row in realestate:
		if row[0] in name_map.keys():
			row[0] = name_map[row[0]]

	#Get all community names from real estate file
	communities = []
	for row in realestate[1:]:
		communities.append(row[0])

	#Get communities that exist both in real estate file and in geojson file
	duplicate = list(set(communities).intersection(names))
	duplicate.sort()

	#Get headers
	headers = realestate[0]
	headers[0] = 'Community'

	#Create data frame
	re_df = pd.DataFrame(realestate[1:], columns=headers)
	re_df = re_df.loc[re_df['Community'].isin(duplicate),:]


	#Cast price into float
	for i in range(1, len(headers)):
		re_df[headers[i]] = pd.to_numeric(re_df[headers[i]])

	#Group by neighborhood and get average price
	re_df = re_df.groupby('Community', as_index=False).agg('mean')

	#Set index to 'Community' column, prepare for transpose
	re_df.set_index('Community')

	#Transpose
	re_df = re_df.T

	#Get new column names, to be community name
	cols = re_df.iloc[0]
	#Reset df from the 1st price row
	re_df = re_df[1:]
	#Reset column names
	re_df.columns = cols

	#Add new column 'year' to be same as index column (now to be month)
	re_df['year'] = re_df.index

	#Get year array from the df
	years = re_df['year'].values

	#Trim this array so that only year remains
	temp = []
	for y in years:
		temp.append(y[-4:])
	re_df['year'] = temp

	#Cast data back to float
	for c in re_df.columns:
		re_df[c] = pd.to_numeric(re_df[c])

	#Group by year, then take average price in that year
	re_df = re_df.groupby('year', as_index=False).agg('mean')
	return re_df