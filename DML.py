# Emily Harms
# POL380 Term Project: Causes of Protectionism
# Double Machine learning

# NOTES

# Oct 22
# Results differ every time (as usual for ML) --> Probably a good idea to do bootstrapping (I will add this for final paper, is ok for now since just proposal) 

# import required modules

import doubleml as dml
from sklearn.ensemble import RandomForestRegressor
import pandas as pd


# Import the data

data = pd.read_csv('ProtectionismDataset.csv')

data.pop('Country') # Ditch country and year since I don't want them impacting results 
data.pop('Year') 

# Define independent and dependent variables 

dep_var = 'Tariff'

ind_vars = ['Exports', 'Unemployment', 'GDP_PerCapita', 'GDP_US', 'Inflation', 'NoParties']

results = {} # dictionary for storage

# Loop through independent variables

for var in ind_vars:
    measured_var = var
    other_vars = [v for v in ind_vars if v != measured_var]

    dml_data = dml.DoubleMLData(data, y_col = dep_var, d_cols = measured_var, x_cols = other_vars) # Create data structure

    # define nuisance learners with Random Forest 
    learner_l = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42) # predicting target from controls
    learner_m = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42) # predict treatment from controls 

    # Partial Linear Regression Model 
    dml_plr = dml.DoubleMLPLR(dml_data, ml_l = learner_l, ml_m = learner_m, n_folds = 5) 
    dml_plr.fit()

    results[measured_var] = dml_plr.summary

# Combine results into a single DataFrame

resultsDF = pd.concat(results)

resultsDF.to_csv('DML_Results.csv')

