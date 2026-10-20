# Emily Harms
# POL380 Term Project: Causes of Protectionism
# Clean data from various sources to get consistent/usable formatting

# import required modules

import pandas as pd
import numpy as np

# Start with tariff data

TariffData = pd.read_csv('TariffData.csv', skiprows = 4)

TariffData = TariffData.drop(columns = ['Country Name', 'Indicator Name', 'Indicator Code']) # Get rid of columns we don't need

# Make a new DataFrame, where I will put the data I want to keep

ProtectionismData = pd.DataFrame()

# Make lists where I will store tariff data, for now

countries = []
years = []
tariffs = []

# Fill lists with tariff data

for row in range(len(TariffData)):
    for col in range(1, TariffData.shape[1]):
        tariff = TariffData.iloc[row, col]
        if pd.notna(tariff):
            countries.append(TariffData.iloc[row, 0])
            years.append(TariffData.columns[col])
            tariffs.append(tariff)

# Save data to the big dataset

ProtectionismData['Country'] = countries
ProtectionismData['Year'] = years
ProtectionismData['Tariff'] = tariffs

# Clean and add export data 

ExportData = pd.read_csv('ExportData.csv', skiprows = 4)

ExportPercent = []

for i in range(len(ProtectionismData)):
    code = ProtectionismData.loc[i, 'Country']
    year = str(ProtectionismData.loc[i, 'Year'])
    row = ExportData[ExportData['Country Code'] == code]
    if len(row)>0 and year in ExportData.columns:
        ExportPercent.append(row[year].iloc[0])
    else:
        ExportPercent.append(np.nan)

ProtectionismData['Exports'] = ExportPercent

ProtectionismData = ProtectionismData.dropna(subset = ['Exports']).reset_index(drop=True)

# Clean and add unemployment data

UnemploymentData = pd.read_csv('UnemploymentData.csv', skiprows = 4)

UnemploymentPercent = []

for i in range(len(ProtectionismData)):
    code = ProtectionismData.loc[i, 'Country']
    year = str(ProtectionismData.loc[i, 'Year'])
    row = UnemploymentData[UnemploymentData['Country Code'] == code]
    if len(row)>0 and year in UnemploymentData.columns:
        UnemploymentPercent.append(row[year].iloc[0])
    else:
        UnemploymentPercent.append(np.nan)

ProtectionismData['Unemployment'] = UnemploymentPercent

ProtectionismData = ProtectionismData.dropna(subset = ['Unemployment']).reset_index(drop=True)

# Clean and add GDP per capita data

GDPCapitaData = pd.read_csv('GDPData.csv', skiprows = 4)

GDPCapita = []

for i in range(len(ProtectionismData)):
    code = ProtectionismData.loc[i, 'Country']
    year = str(ProtectionismData.loc[i, 'Year'])
    row = GDPCapitaData[GDPCapitaData['Country Code'] == code]
    if len(row)>0 and year in GDPCapitaData.columns:
        GDPCapita.append(row[year].iloc[0])
    else:
        GDPCapita.append(np.nan)

ProtectionismData['GDP_PerCapita'] = GDPCapita

ProtectionismData = ProtectionismData.dropna(subset = ['GDP_PerCapita']).reset_index(drop=True)

# Clean and add GDP in US$ data

GDP_USData = pd.read_csv('GDP_US.csv', skiprows = 4)

GDP_US = []

for i in range(len(ProtectionismData)):
    code = ProtectionismData.loc[i, 'Country']
    year = str(ProtectionismData.loc[i, 'Year'])
    row = GDP_USData[GDP_USData['Country Code'] == code]
    if len(row)>0 and year in GDP_USData.columns:
        GDP_US.append(row[year].iloc[0])
    else:
        GDP_US.append(np.nan)

ProtectionismData['GDP_US'] = GDP_US

ProtectionismData = ProtectionismData.dropna(subset = ['GDP_US']).reset_index(drop=True)

# Clean and add inflation data

InflationData = pd.read_csv('InflationData.csv', skiprows = 4)

Inflation  = []

for i in range(len(ProtectionismData)):
    code = ProtectionismData.loc[i, 'Country']
    year = str(ProtectionismData.loc[i, 'Year'])
    row = InflationData[InflationData['Country Code'] == code]
    if len(row)>0 and year in InflationData.columns:
        Inflation.append(row[year].iloc[0])
    else:
        Inflation.append(np.nan)

ProtectionismData['Inflation'] = Inflation

ProtectionismData = ProtectionismData.dropna(subset = ['Inflation']).reset_index(drop=True)

# Clean and add protectionism data
# NOTE: this is not world bank data, so structure is a bit different

PartyData = pd.read_csv('NoParties.csv', delimiter = ';', decimal = ',')

NoParties = []

for i in range(len(ProtectionismData)):
    code = ProtectionismData.loc[i, 'Country']
    year = int(ProtectionismData.loc[i, 'Year'])

    match = PartyData[(PartyData['ccodealp'] == code) & (PartyData['year'] == year)]

    if len(match) > 0:
        NoParties.append(match['gol_enep'].iloc[0])
    else:
        NoParties.append(np.nan)

ProtectionismData['NoParties'] = NoParties
ProtectionismData = ProtectionismData.dropna(subset=['NoParties']).reset_index(drop=True)

# Save everything to a single csv file

ProtectionismData.to_csv('ProtectionismDataset.csv') 
