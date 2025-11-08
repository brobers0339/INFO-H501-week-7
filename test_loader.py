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
        
        expected = {
            'Museum of Modern Art': (40.7614327, -73.9776216),
            'USS Alabama Battleship Memorial': (30.3314265, -87.9512903)
        }
        
        # Tolerance in degrees (~0.01 degrees ≈ 1.1 km). Adjust if you need stricter/looser checks.
        delta = 0.05

        # Ensure we have results for each requested location and assert closeness
        for _, row in geo_df.iterrows():
            name = row.get('location')
            lat = row.get('latitude')
            lon = row.get('longitude')

            # Ensure geocoding returned values
            self.assertIsNotNone(lat, f"Latitude for '{name}' should not be None")
            self.assertIsNotNone(lon, f"Longitude for '{name}' should not be None")

            if name in expected:
                exp_lat, exp_lon = expected[name]
                # Use assertAlmostEqual with delta to compare floating point values
                self.assertAlmostEqual(lat, exp_lat, delta=delta,
                                       msg=f"Latitude for '{name}' not within {delta} degrees of expected")
                self.assertAlmostEqual(lon, exp_lon, delta=delta,
                                       msg=f"Longitude for '{name}' not within {delta} degrees of expected")
            else:
                # If an unexpected location appears, at least ensure latitude/longitude are floats
                self.assertIsInstance(lat, float)
                self.assertIsInstance(lon, float)


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
        self.assertTrue(df['latitude'].isnull().all() and df['longitude'].isnull().all(),
                          "DataFrame should contain None for latitude and longitude of invalid locations.")
        
if __name__ == "__main__":
    unittest.main(exit=False)
