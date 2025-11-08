import unittest
import pandas as pd
from loader import *

class TestLoader(unittest.TestCase):
    def test_valid_locations(self):
        
        '''
        Test valid locations with functions from loader.py file.

        This function serves as a test under the TestLoader class to test valid locations using the
        functions within the loader.py file to ensure the functions are working properly.       
        '''
        test_locations = ['Museum of Modern Art', 'USS Alabama Battleship Memorial']
        loader = Loader(test_locations)
        geo = loader.get_geolocator()
        geo_df = loader.build_geo_dataframe(geo)
        
        expected = {
            'Museum of Modern Art': (40.7614327, -73.9776216),
            'USS Alabama Battleship Memorial': (30.3314265, -87.9512903)
        }
        
        #Acceptable variance in latitude and longitude
        delta = 0.5

        for _, row in geo_df.iterrows():
            name = row.get('location')
            lat = row.get('latitude')
            lon = row.get('longitude')

            # Ensure geocoding returned values
            self.assertIsNotNone(lat, f"Latitude for '{name}' should not be None")
            self.assertIsNotNone(lon, f"Longitude for '{name}' should not be None")

            #For each expected location, check if the latitude and longitude are within the acceptable ranges
            if name in expected:
                exp_lat, exp_lon = expected[name]
                self.assertAlmostEqual(lat, exp_lat, delta=delta,
                                       msg=f"Latitude for '{name}' not within {delta} degrees of expected")
                self.assertAlmostEqual(lon, exp_lon, delta=delta,
                                       msg=f"Longitude for '{name}' not within {delta} degrees of expected")


    def test_invalid_location(self):
        '''
        Test invalid locations with functions from the loader.py file.

        This function serves as a test under the TestLoader class to test invalid locations 
        using the functions within the loader.py file to ensure the functions are working
        properly.
        '''
        loader = Loader(['asdfqwer1234'])
        geolocator = loader.get_geolocator()
        result = loader.fetch_location_data(geolocator, ["asdfqwer1234"])
        df = loader.build_geo_dataframe(geolocator)
        
        # Check that the invalid location returns None values
        self.assertTrue(any(value is None for value in result.values()), 
                          "A nonexistent location should have an empty result.")
        
if __name__ == "__main__":
    unittest.main(exit=False)
