
'''
    Utilities class utilized to encapsulate helper functions
    and data for use by main application
'''
class Utilities:

    def __init__(self):
        self.area_names_dic , neighborhood_name_dic = Utilities.prepMaps()

    def prepMaps(self):
        code_pairs = [[float(p[0]), p[1]] for p in [pair.strip().split('\t') for pair in Utilities.area_names.strip().split('\n')]]
        area_name_dic = {float(k[0]): k[1] for k in code_pairs}

        code_pairs_neighborhoods = [[p[0], p[1]] for p in [pair.strip().split('\t') for pair in Utilities.neighborhood_Map.strip().split('\n')]]
        neighborhood_name_dic = {k[0]: k[1] for k in code_pairs_neighborhoods}

        return (area_name_dic,neighborhood_name_dic)



    crimes_list = [
        'THEFT',
        'BATTERY',
        'CRIMINAL DAMAGE',
        'ASSAULT',
        'NARCOTICS',
        'BURGLARY',
        'ROBBERY',
        'MOTOR VEHICLE THEFT',
        'HOMICIDE',
        'CRIM SEXUAL ASSAULT',
        'KIDNAPPING']

    noncriminal = ['NON - CRIMINAL', 'NON-CRIMINAL', 'NON-CRIMINAL (SUBJECT SPECIFIED)', 'GAMBLING']

    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dev']
    monthMap = {
        1 : 'Jan',
        2 : 'Feb',
        3 : 'Mar',
        4 : 'Apr',
        5 : 'May',
        6 : 'Jun',
        7 : 'Jul',
        8 : 'Aug',
        9 : 'Sep',
        10: 'Oct',
        11 : 'Nov',
        12 : 'Dec'
    }

    ##################
    #### MAPPING #####
    ##################

    ### community area name
    area_names = """
    01	Rogers Park	
    40	Washington Park
    02	West Ridge	
    41	Hyde Park
    03	Uptown	
    42	Woodlawn
    04	Lincoln Square	
    43	South Shore
    05	North Center	
    44	Chatham
    06	Lakeview	
    45	Avalon Park
    07	Lincoln Park	
    46	South Chicago
    08	Near North Side	
    47	Burnside
    09	Edison Park	
    48	Calumet Heights
    10	Norwood Park	
    49	Roseland
    11	Jefferson Park	
    50	Pullman
    12	Forest Glen	
    51	South Deering
    13	North Park	
    52	East Side
    14	Albany Park	
    53	West Pullman
    15	Portage Park	
    54	Riverdale
    16	Irving Park	
    55	Hegewisch
    17	Dunning	
    56	Garfield Ridge
    18	Montclare	
    57	Archer Heights
    19	Belmont Cragin	
    58	Brighton Park
    20	Hermosa	
    59	McKinley Park
    21	Avondale	
    60	Bridgeport
    22	Logan Square	
    61	New City
    23	Humboldt Park	
    62	West Elsdon
    24	West Town	
    63	Gage Park
    25	Austin	
    64	Clearing
    26	West Garfield Park 	
    65	West Lawn
    27	East Garfield Park	
    66	Chicago Lawn
    28	Near West Side	
    67	West Englewood
    29	North Lawndale	
    68	Englewood
    30	South Lawndale	
    69	Greater Grand Crossing
    31	Lower West Side	
    70	Ashburn
    32	Loop	
    71	Auburn Gresham	
    33	Near South Side	
    72	Beverly
    34	Armour Square	
    73	Washington Heights
    35	Douglas	
    74	Mount Greenwood
    36	Oakland	
    75	Morgan Park
    37	Fuller Park	
    76	O'Hare
    38	Grand Boulevard	
    77	Edgewater
    39	Kenwood	
    """

    ## neighborhood : community name
    neighborhood_Map = """
    Cabrini–Green	Near North Side	
    The Gold Coast	Near North Side	
    Goose Island	Near North Side	
    Magnificent Mile	Near North Side	
    Old Town	Near North Side	
    River North	Near North Side	
    River West	Near North Side	
    Streeterville	Near North Side	
    Loop	Loop	
    Near East Side	Loop	
    South Loop	Loop	
    West Loop Gate	Loop	
    Dearborn Park	Near South Side	
    Printer's Row	Near South Side	
    South Loop	Near South Side	
    Prairie Avenue Historic District	Near South Side	
    Horner Park	North Center	
    Roscoe Village	North Center	
    Boystown	Lake View	
    Lake View East	Lake View	
    Graceland West	Lake View	
    South East Ravenswood	Lake View	
    Wrigleyville	Lake View	
    Old Town Triangle	Lincoln Park	
    Park West	Lincoln Park	
    Ranch Triangle	Lincoln Park	
    Sheffield Neighbors	Lincoln Park	
    Wrightwood Neighbors	Lincoln Park	
    Belmont Gardens	Avondale	
    Chicago's Polish Village	Avondale	
    Kosciuszko Park	Avondale	
    Belmont Gardens	Logan Square	
    Bucktown	Logan Square	
    Kosciuszko Park	Logan Square	
    Palmer Square	Logan Square	
    East Rogers Park	Rogers Park	
    Arcadia Terrace	West Ridge	
    Peterson Park	West Ridge	
    West Rogers Park	West Ridge	
    Buena Park	Uptown	
    Argyle Street	Uptown	
    Margate Park	Uptown	
    Sheridan Park	Uptown	
    Ravenswood	Lincoln Square	
    Ravenswood Gardens	Lincoln Square	
    Rockwell Crossing	Lincoln Square	
    Edison Park	Edison Park	
    Big Oaks	Norwood Park	
    Old Norwood Park	Norwood Park	
    Oriole Park	Norwood Park	
    Union Ridge	Norwood Park	
    Gladstone Park	Jefferson Park	
    Edgebrook	Forest Glen	
    Old Edgebrook	Forest Glen	
    South Edgebrook	Forest Glen	
    Sauganash	Forest Glen	
    Wildwood	Forest Glen	
    Brynford Park	North Park	
    Hollywood Park	North Park	
    River's Edge	North Park	
    Sauganash Woods	North Park	
    Mayfair	Albany Park	
    North Mayfair	Albany Park	
    Ravenswood Manor	Albany Park	
    Schorsch Forest View	O'Hare	
    Andersonville	Edgewater	
    Edgewater Beach	Edgewater	
    Magnolia Glen	Edgewater	
    Lakewood/Balmoral	Edgewater	
    Belmont Central	Portage Park	
    Władysławowo	Portage Park	
    Six Corners	Portage Park	
    Avondale Gardens	Irving Park	
    Independence Park	Irving Park	
    Kilbourn Park	Irving Park	
    Little Cassubia	Irving Park	
    Old Irving Park	Irving Park	
    West Walker	Irving Park	
    The Villa	Irving Park	
    Belmont Heights	Dunning	
    Belmont Terrace	Dunning	
    Irving Woods	Dunning	
    Schorsch Village	Dunning	
    Montclare	Montclare	
    Belmont Central	Belmont Cragin	
    Hanson Park	Belmont Cragin	
    Belmont Gardens	Hermosa	
    Kelvyn Park	Hermosa	
    East Village	West Town	
    Noble Square	West Town	
    Polish Downtown	West Town	
    Pulaski Park	West Town	
    Smith Park	West Town	
    Ukrainian Village	West Town	
    Wicker Park	West Town	
    Galewood	Austin	
    The Island	Austin	
    West Garfield Park	West Garfield Park	
    Fifth City	East Garfield Park	
    Greektown	Near West Side	
    Little Italy	Near West Side	
    Tri-Taylor	Near West Side	
    Lawndale	North Lawndale	
    Homan Square	North Lawndale	
    Douglas Park	North Lawndale	
    Little Village	South Lawndale	
    Heart of Chicago	Lower West Side	
    Heart of Italy	Lower West Side	
    Pilsen	Lower West Side	
    East Pilsen	Lower West Side	
    Chinatown	Armour Square	
    Wentworth Gardens	Armour Square	
    Bridgeport, Chicago	Armour Square	
    Groveland Park	Douglas	
    Lake Meadows	Douglas	
    the Gap	Douglas	
    Prairie Shores	Douglas	
    South Commons	Douglas	
    Oakland	Oakland	
    Fuller Park	Fuller Park	
    Bronzeville	Grand Boulevard	
    Kenwood	Kenwood	
    South Kenwood	Kenwood	
    Washington Park	Washington Park	
    East Hyde Park	Hyde Park	
    Hyde Park	Hyde Park	
    West Woodlawn	Woodlawn	
    Jackson Park Highlands	South Shore	
    Bridgeport	Bridgeport	
    Grand Crossing	Greater Grand Crossing	
    Parkway Gardens	Greater Grand Crossing	
    Park Manor	Greater Grand Crossing	
    LeClaire Courts	Garfield Ridge	
    Sleepy Hollow	Garfield Ridge	
    Vittum Park	Garfield Ridge	
    Archer Heights	Archer Heights	
    Brighton Park	Brighton Park	
    McKinley Park 	McKinley Park	
    Back of the Yards	New City	
    Canaryville	New City	
    West Elsdon	West Elsdon	
    Gage Park	Gage Park	
    Chrysler Village	Clearing	
    Ford City	West Lawn	
    West Lawn	West Lawn	
    Lithuanian Plaza	Chicago Lawn	
    Marquette Park	Chicago Lawn	
    West Englewood	West Englewood	
    Englewood	Englewood	
    East Chatham	Chatham	
    West Chatham	Chatham	
    West Chesterfield	Chatham	
    Avalon Park	Avalon Park	
    Marynook	Avalon Park	
    Stony Island Park	Avalon Park	
    The Bush	South Chicago	
    Burnside	Burnside	
    Pill Hill	Calumet Heights	
    Fernwood	Roseland	
    Rosemoor	Roseland	
    Cottage Grove Heights	Pullman	
    London Towne	Pullman	
    Jeffrey Manor	South Deering	
    Trumbull Park	South Deering	
    Altgeld Gardens	Riverdale	
    Eden Green	Riverdale	
    Golden Gate	Riverdale	
    East Side	East Side	
    West Pullman	West Pullman	
    Hegewisch	Hegewisch	
    Beverly View	Ashburn	
    Mary Crest	Ashburn	
    Parkview	Ashburn	
    Scottsdale	Ashburn	
    Wrightwood	Ashburn	
    Auburn Gresham	Auburn Gresham	
    Beverly	Beverly	
    Brainerd	Washington Heights	
    Longwood Manor	Washington Heights	
    Princeton Park	Washington Heights	
    Mount Greenwood Heights	Mount Greenwood	
    Talley's Corner	Mount Greenwood	
    Beverly Woods	Morgan Park	
    Kennedy Park	Morgan Park	
    West Morgan Park	Morgan Park	
    """