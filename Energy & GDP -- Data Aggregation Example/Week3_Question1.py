import numpy as np
import pandas as pd

# Read the first excel file.  Exclude header and footer and use relevant columns.
energy = pd.read_excel('Energy Indicators.xls', index_col=None,
             names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'],
             usecols='C:F', skiprows=17, skip_footer=38)

# Set missing data to NaN
energy = energy.replace('...', np.NaN)

# Eliminate parentheticals and footnotes from country names
energy['Country'] = energy['Country'].str.replace(r" \(.*\)", "")
energy['Country'] = energy['Country'].str.replace(r"\d", "")

# Use more common country names
energy = energy.replace(['Republic of Korea', 'United States of America', 'United Kingdom of Great Britain and Northern Ireland', 'China, Hong Kong Special Administrative Region'], ['South Korea', 'United States', 'United Kingdom', 'Hong Kong'])

# Convert energy petajoules to gigajoules
energy['Energy Supply'] *= 1000000

# Read GDP file and update country names
GDP = pd.read_csv('world_bank.csv', skiprows=4)
GDP = GDP.replace(['Korea, Rep.', 'Iran, Islamic Rep.', 'Hong Kong SAR, China'], ['South Korea', 'Iran', 'Hong Kong'])

# Read ScimEn file, using only the top 15 ranked countries
ScimEn = pd.read_excel('scimagojr-3.xlsx')
ScimEn = ScimEn[ScimEn['Rank'] < 16]

# Join into a single dataframe, and select the relevant columns
df = pd.merge(energy, GDP, how='inner', left_on='Country', right_on='Country Name')
df = pd.merge(df, ScimEn, how='inner', left_on='Country', right_on='Country')
df = df[['Country', 'Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document',
         'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010',
        '2011', '2012', '2013', '2014', '2015']]

# Index based on the country name
df = df.set_index('Country')

print(df)