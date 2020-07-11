import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+'\\'+'modules')
from create_database import write_tables
from first_table_connect import first_table
from first_cooks_distance import first_cook
from first_isolation_forest import first_forest
from first_z_score import first_z
from second_table_connect import second_table
from second_cooks_distance import second_cook
from second_isolation_forest import second_forest
from second_z_score import second_z
from third_table_connect import third_table
from third_isolation_forest import third_forest
from third_z_score import third_z

con = sqlite3.connect(dir_path+'\\'+'data'+'\\'+'Covid_Data.db')
curs = con.cursor()
write_tables(con, dir_path)


# First Example
# Single column just to try the basics, Isolation Forests require two columns of data, because why would you want to perform
# a forest model with a single column (except in this instance), so number of cases was doubled up.

# Selecting our data. Looks like the NYT data set has a few NULLs in it for FIPS codes. 

table = first_table(con)

# We know right away that this data is heavily left-skewed since only a few large counties have many cases.
# Most counties in America are pretty tiny compared to a place like LA County or Cook County with their entire population being less than the number of cases in either of these areas.
# Just to confirm suspicions of our data shape.

table['cases1'].plot.hist(bins=20)

first_z_outliers, first_z_speed = first_z(table)

first_forest_outliers, first_forest_speed = first_forest(table)


# Plotting our models to visualize the outliers

fig, axs = plt.subplots(1,2)
fig.suptitle('First Comparison')

# Plotting the z-score results
axs[0].scatter(table['cases1'], table['cases2'], c= 'b', marker = '+', label = 'Data')
axs[0].scatter(first_z_outliers['cases1'], first_z_outliers['cases2'], c= 'r', marker = '+', label = 'Outliers')
axs[0].set_title('z-scores')
axs[0].set_ylim(0,max(table['cases2']+.001))
axs[0].set_xlim(0,max(table['cases1']+.01))

# Plotting the Isolation Forest results
axs[1].scatter(table['cases1'], table['cases2'], c= 'b', marker = '+', label = 'Data')
axs[1].scatter(first_forest_outliers['cases1'], first_forest_outliers['cases2'], c= 'r', marker = '+', label = 'Outliers')
axs[1].set_title('Isolation Forest')
axs[1].set_ylim(0,max(table['cases2']+.001))
axs[1].set_xlim(0,max(table['cases1']+.01))

fig.show()

# Well we certainly sliced the biggest data points here, but it's a little hard to tell how effective each one was.
# For reference, it appears that the z-score method identified 38 points (1.2%), while the forest identified 62 points (2%, or exactly our contamination level)
print(len(first_z_outliers))
print(len(table))

# Speed check! Looks like applying z-scores is significantly faster than the forest

print(first_z_speed)
print(first_forest_speed)



# Second Example
# Bivariate data makes this a little more interesting. We can try using cook's distance, since it is possible to regress to variables now
# Let's compare county cases and deaths, controlled for total population and see how many outliers emerge


table = second_table(con)

second_z_outliers, second_z_speed = second_z(table)

second_forest_outliers, second_forest_speed = second_forest(table)

first_cooks_outliers, first_cooks_speed = first_cook(table)



# Plotting our models to visualize the outliers

fig, axs = plt.subplots(2,2)
fig.suptitle('Second Comparison')

# Plotting our Cook's Distance results
axs[1, 0].scatter(table['Case_Rate'], table['Death_Rate'], c= 'b', marker = '+', label = 'Data')
axs[1, 0].scatter(first_cooks_outliers['Case_Rate'], first_cooks_outliers['Death_Rate'], c= 'r', marker = '+', label = 'Outliers')
axs[1, 0].set_title('Cooks Distance')
axs[1, 0].set_ylim(0,max(table['Death_Rate']+.001))
axs[1, 0].set_xlim(0,max(table['Case_Rate']+.01))
axs[1, 0].set_xlabel('Case_Rate')
axs[1, 0].set_ylabel('Death_Rate')

# Plotting our z-score results
axs[0, 0].scatter(table['Case_Rate'], table['Death_Rate'], c= 'b', marker = '+', label = 'Data')
axs[0, 0].scatter(second_z_outliers['Case_Rate'], second_z_outliers['Death_Rate'], c= 'r', marker = '+', label = 'Outliers')
axs[0, 0].set_title('z-scores')
axs[0, 0].set_ylim(0,max(table['Death_Rate']+.001))
axs[0, 0].set_xlim(0,max(table['Case_Rate']+.01))
axs[0, 0].set_xlabel('Case_Rate')
axs[0, 0].set_ylabel('Death_Rate')

# Plotting our Isolation Forest results
axs[0, 1].scatter(table['Case_Rate'], table['Death_Rate'], c= 'b', marker = '+', label = 'Data')
axs[0, 1].scatter(second_forest_outliers['Case_Rate'], second_forest_outliers['Death_Rate'], c= 'r', marker = '+', label = 'Outliers')
axs[0, 1].set_title('Isolation Forest')
axs[0, 1].set_ylim(0,max(table['Death_Rate']+.001))
axs[0, 1].set_xlim(0,max(table['Case_Rate']+.01))
axs[0, 1].set_xlabel('Case_Rate')
axs[0, 1].set_ylabel('Death_Rate')

fig.show()


# Second speed test!

print(second_z_speed)
# .012 seconds
print(second_forest_speed)
# 4.41 seconds
print(first_cooks_speed)
# 3.54 seconds

# Surprising to see that the z-score is still so significantly faster, despite us tripling the necessary number of calculations



# Third Example
# We're not doing predictive modeling here, but it might be fun to throw in a related demographic variable. Let's add the percent of the county that works in food service for this example
# Once we start adding increased dimensionality, it becomes increasingly difficult to apply z-scores, and to visually see our outliers
# Had to divide it into two tables and merge to deal with null values, which the isolation forest does not like.
# Null values were replaced with a minimum value, since nulls in Census data indicate data that was just too small to be included without identifying particular individuals

table = third_table(con)

third_z_outliers, third_z_speed = third_z(table)

third_forest_outliers, third_forest_speed = third_forest(table)

second_cooks_outliers, second_cooks_speed = second_cook(table)



# Plotting our Cook's Distance results
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('Cooks Distance')
ax.set_xlabel('Percent_Food_Service')
ax.set_ylabel('Case_Rate')
ax.set_zlabel('Death_Rate')
sp = ax.scatter(table['Percent_Food_Service'], table['Case_Rate'], table['Death_Rate'], c='b', alpha = .4)
sp = ax.scatter(second_cooks_outliers['Percent_Food_Service'], second_cooks_outliers['Case_Rate'], second_cooks_outliers['Death_Rate'], c='r', alpha = 1)

fig.show()

# Plotting our z-score results
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('z-scores')
ax.set_xlabel('Percent_Food_Service')
ax.set_ylabel('Case_Rate')
ax.set_zlabel('Death_Rate')
sp = ax.scatter(table['Percent_Food_Service'], table['Case_Rate'], table['Death_Rate'], c='b', alpha = .4)
sp = ax.scatter(third_z_outliers['Percent_Food_Service'], third_z_outliers['Case_Rate'], third_z_outliers['Death_Rate'], c='r', alpha = 1)

fig.show()

# Plotting our Isolation Forest results
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('Isolation Forest')
ax.set_xlabel('Percent_Food_Service')
ax.set_ylabel('Case_Rate')
ax.set_zlabel('Death_Rate')
sp = ax.scatter(table['Percent_Food_Service'], table['Case_Rate'], table['Death_Rate'], c='b', alpha = .4)
sp = ax.scatter(third_forest_outliers['Percent_Food_Service'], third_forest_outliers['Case_Rate'], third_forest_outliers['Death_Rate'], c='r', alpha = 1)

fig.show()


# Third speed test!

print(third_z_speed)
print(third_forest_speed)
print(second_cooks_speed)

