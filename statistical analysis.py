import kneed as kn
import pandas as pd
import math as math
import numpy as np
import matplotlib.pyplot as plt


##### DATA #####

# Import the data
raw_data = pd.read_csv('Chocolate LCA - Main.csv', header=1)

# Extract the data per kg cocoa for boundaries = cradle to farm gate and EIP = [AD, GW, ODP, AC, EU CED ]
data = raw_data[['Country***', 'Agriculture type*', 'AD (kg Sb eq) .1', 'GW (kg CO2 eq) .1',
     'ODP (kg CF11 eq).1', 'AC (kg SO2 eq).1', 'EU (kg PO4 eq).1', 'CED (MJ).1']].loc[(raw_data['Boundaries / production phase ******'] == 'Cradle to farm gate')]

data = data.replace(0, float('nan')) # Replace 0 values with NaN

# List of the student quantile for n = 2 to 30 and alpha = 0.025
t_arr = np.array([12.71, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.16, 2.145, 2.131, 2.12, 2.11, 2.101, 2.093, 2.086, 2.08, 2.074, 2.069, 2.064, 2.06, 2.056, 2.052, 2.048, 2.045])

n_arr = np.arange(2, 31)

def my_funky_function(indicator, country):
    dico = {'AD': 'AD (kg Sb eq) .1', 'GW': 'GW (kg CO2 eq) .1', 'ODP': 'ODP (kg CF11 eq).1', 'AC': 'AC (kg SO2 eq).1', 'EU': 'EU (kg PO4 eq).1', 'CED': 'CED (MJ).1'}
    # Extract the data for the given indicator
    data_indicator = data[dico[indicator]]
    mean = np.nanmean(data_indicator) # mean of the indicator values forthe entire population

    # Extract the data for the given country and the given indicator
    data_indicator_country = data[dico[indicator]].loc[data['Country***'] == country]
    var = np.nanvar(data_indicator_country, ddof = 1) # std deviation for the indicator values of the partial sample NB: ddof = 1 for sample std deviation
    
    # Calculates the order of magnitude for the EIP indicator
    m = 10**((-1)*math.ceil(abs(math.log10(mean)))) 

    # Calculates the IC values 
    IC = (t_arr * (var / np.sqrt(n_arr)) )/ m

    # Knee location and save graph
    knee = kn.KneeLocator(n_arr, IC, S= 1, curve='convex', direction='decreasing', interp_method='interp1d')
    knee.plot_knee()
    plt.savefig('/home/lisa/Documents/Cours archives/APT 2A/Stage/UB/Rapport de stage/Images/knee_' + indicator + '_' + country + '.png') # Specific to my computer
    
    knee_value = knee.knee
    table_data = np.concatenate([n_arr, IC], axis=0).reshape(2, 29).T

    # Convert the table data to a pandas dataframe and save as csv
    table = pd.DataFrame(table_data, columns=['n', 'IC'])
    table.to_csv('/home/lisa/Documents/Cours archives/APT 2A/Stage/UB/Rapport de stage/knee_'+indicator+'_'+country+'.csv', index=False) # Specific to my computer

    return knee_value, table

# Example of use
my_funky_function('AD', 'Peru')
