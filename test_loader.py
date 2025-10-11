import unittest
import pandas as pd
from loader import *

class TestLoader(unittest.TestCase):
    def test_valid_locations(self):
        
        '''
        Test valid locations with functions from loader.py file.

        This function serves as a test under the TestLoader class to test valid locations using the
        functions within the loader.py file to ensure the functions are working properly.

        Returns
        -------
            pandas DataFrame:
               Dataframe containing found geolocation data where the given location name, latitude, longitude, 
                and location type are all columns.        
        '''
        test_locations = ['Museum of Modern Art', 'USS Alabama Battleship Memorial']
        loader = Loader(test_locations)
        geo = loader.get_geolocator()
        geo_df = loader.build_geo_dataframe(geo)
        return geo_df

    def test_invalid_location(self):
        '''
        Test invalid locations with functions from the loader.py file.

        This function serves as a test under the TestLoader class to test invalid locations 
        using the functions within the loader.py file to ensure the functions are working
        properly.

        Returns
        -------
            pandas DataFrame:
                Dataframe containing found geolocation data where the given location name, latitude, longitude, 
                and location type are all columns. If the location doesn't exist or cannot be found, None
                types are returned for these categories besides the location given name. The function also
                tests to ensure that None types are found within the results of the location data and filled
                in to the dataframe properly.
        '''
        loader = Loader(['asdfqwer1234'])
        geolocator = loader.get_geolocator()
        result = loader.fetch_location_data(geolocator, ["asdfqwer1234"])
        df = loader.build_geo_dataframe(geolocator)
        self.assertTrue(any(value is None for value in result.values()), 
                          "A nonexistent location should have an empty result.")
        return df
    
if __name__ == "__main__":
    unittest.main(exit=False)
