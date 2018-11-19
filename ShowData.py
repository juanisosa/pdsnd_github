import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


df = pd.read_csv(CITY_DATA['new york city'])

print(df.groupby(['Birth Year']).size())
