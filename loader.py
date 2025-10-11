'''
Script to load geographical data into a pandas DataFrame, and save it as a CSV file.
'''
from geopy.geocoders import Nominatim
import pandas as pd

class Loader():
    def __init__(self, locations):
        self.locations = locations

    def get_geolocator(self, agent='h501-student'):
        """
        Initiate a Nominatim geolocator instance given an `agent`.

        Parameters
        ----------
        agent : str, optional
            Agent name for Nominatim, by default 'h501-student'
        """
        return Nominatim(user_agent=agent)

    def fetch_location_data(self, geolocator, loc):
        try:
            location = geolocator.geocode(loc)
        except:
            print(f"-- {e} --:\n\t-->", loc)
            return None
    
        if location is None:
            return {"location": loc, "latitude" : None, "longitude" : None, "Type" : None}
        return {"location": loc, "latitude": location.latitude, "longitude": location.longitude, "type": location.raw.get('type')}

    def build_geo_dataframe(self, geolocator):
        geo_data = [self.fetch_location_data(geolocator, loc) for loc in self.locations]
        
        return pd.DataFrame(geo_data)


if __name__ == "__main__":
    locations = ["Museum of Modern Art", "iuyt8765(*&)", "Alaska", "Franklin's Barbecue", "Burj Khalifa"]
    loader = Loader(locations)
    df = loader.build_geo_dataframe()

    df.to_csv("./geo_data.csv")
