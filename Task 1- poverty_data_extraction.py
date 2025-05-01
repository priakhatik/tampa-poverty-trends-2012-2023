#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd
import time

# Target years
years = list(range(2012, 2024))  # 2012 to 2023

# Florida State FIPS code
state_fips = '12'

# Counties you want (focus counties)
target_counties = [
    'Hillsborough County, Florida',
    'Pinellas County, Florida',
    'Pasco County, Florida',
    'Polk County, Florida',
    'Sarasota County, Florida',
    'Manatee County, Florida',
    'Citrus County, Florida'
]

# Initialize a DataFrame
poverty_data = pd.DataFrame()

for year in years:
    print(f"Fetching data for {year}...")
    url = f"https://api.census.gov/data/{year}/acs/acs1/subject"
    params = {
        'get': 'NAME,S1701_C03_001E',
        'for': 'county:*',
        'in': f'state:{state_fips}'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        
        # Filter only target counties
        df = df[df['NAME'].isin(target_counties)]
        
        # Clean up
        df = df[['NAME', 'S1701_C03_001E']]
        df['S1701_C03_001E'] = pd.to_numeric(df['S1701_C03_001E'], errors='coerce')
        df = df.set_index('NAME').T
        df['Year'] = year
        
        poverty_data = pd.concat([poverty_data, df])
        
        # Avoid slamming Census servers
        time.sleep(1)
    else:
        print(f"Failed to fetch data for {year}")

# Reorder columns: Year first
poverty_data = poverty_data.set_index('Year')
poverty_data = poverty_data.rename(columns={
    'Hillsborough County, Florida': 'Hillsborough',
    'Pinellas County, Florida': 'Pinellas',
    'Pasco County, Florida': 'Pasco',
    'Polk County, Florida': 'Polk',
    'Sarasota County, Florida': 'Sarasota',
    'Manatee County, Florida': 'Manatee',
    'Citrus County, Florida': 'Citrus'
})

poverty_data.index.name = 'Year'

# Save to Excel
output_filename = "florida_poverty_data_2012_2024.xlsx"
poverty_data.to_excel(output_filename)

print(f"\n✅ Data extraction completed and saved to '{output_filename}'")


# ## Note: "2020 data was unavailable due to COVID-related disruptions, and 2024 ACS data is not yet released; script includes 2012–2023 only."
# 
