import pandas as pd
import feather
from Utilities import Utilities

class Preprocess_Feather():

    def __init__(self, filename):
        self.filename = filename
        self.file_df = pd.read_csv(filename, sep=',')

    def createFeather(self):
        # create cleaned dataframe and write as .feather
        eliminate_cols = ['location', 'latitude', 'longitude', 'x_coordinate', 'y_coordinate', 'updated_on', 'fbi_code',
                          'location_description', 'description']
        new_df = self.file_df.drop(columns=eliminate_cols)
        new_df['date'] = pd.to_datetime(new_df['date'])
        new_df = new_df[~new_df['primary_type'].isin(Utilities.noncriminal)]

        # create a feather dataframe formatted file
        feather.write_dataframe(new_df, 'crimeData.feather')
