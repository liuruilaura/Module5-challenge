#!/usr/bin/env python
# coding: utf-8

# # Pymaceuticals Inc.
# ---
# 
# ### Analysis
# 
# - Add your analysis here.
#  

# In[92]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st

# Study data files
mouse_metadata_path = "data/Mouse_metadata.csv"
study_results_path = "data/Study_results.csv"

# Read the mouse data and the study results
mouse_metadata = pd.read_csv(mouse_metadata_path)
study_results = pd.read_csv(study_results_path)

# Combine the data into a single DataFrame
combined_data = pd.merge(mouse_metadata, study_results, on='Mouse ID')

# Adjust Column orders:
desired_column_order = ['Mouse ID', 'Timepoint', 'Tumor Volume (mm3)', 'Metastatic Sites','Drug Regimen','Sex','Age_months','Weight (g)']
Adjusted_df = combined_data[desired_column_order]

Adjusted_df.head()


# In[93]:


# Display the number of unique mice IDs in the data

unique_mouse_ids = combined_data['Mouse ID'].nunique()
unique_mouse_ids


# In[94]:


# check for any mouse ID with duplicate time points.

duplicate_ids = combined_data[combined_data.duplicated(subset=['Mouse ID', 'Timepoint'])]['Mouse ID'].unique()
duplicate_ids


# In[95]:


# Get the duplicate mice by ID number that shows up for Mouse ID and Timepoint. 
duplicate_mouse_data = Adjusted_df[Adjusted_df['Mouse ID'].isin(duplicate_ids)]

# Optional: Get all the data for the duplicate mouse ID. 
duplicate_mouse_data


# In[96]:


# Create a clean DataFrame by dropping the duplicate mouse by its ID.
# Mouse ID to be removed
duplicate_mouse_id = 'g989'

# Creating a clean DataFrame by dropping all data for the duplicate mouse ID
cleaned_data = Adjusted_df[Adjusted_df['Mouse ID'] != duplicate_mouse_id]
cleaned_data.head()


# In[97]:


# Checking the number of mice in the clean DataFrame.
unique_clean_mouse_ids = cleaned_data['Mouse ID'].nunique()
unique_clean_mouse_ids


# ## Summary Statistics

# In[98]:


#The mean of the tumor volume for each regimen is calculated using groupby.
mean = cleaned_data.groupby('Drug Regimen')['Tumor Volume (mm3)'].mean()
mean


# In[99]:


# The median of the tumor volume for each regimen is calculated using groupby. 
median =cleaned_data.groupby('Drug Regimen')['Tumor Volume (mm3)'].median()
median


# In[100]:


# The variance of the tumor volume for each regimen is calculated using groupby. 
variance =cleaned_data.groupby('Drug Regimen')['Tumor Volume (mm3)'].var()
variance


# In[101]:


# The standard deviation of the tumor volume for each regimen is calculated using groupby. 
STD = cleaned_data.groupby('Drug Regimen')['Tumor Volume (mm3)'].std()
STD   


# In[102]:


# The SEM of the tumor volume for each regimen is calculated using groupby. 
SEM = cleaned_data.groupby('Drug Regimen')['Tumor Volume (mm3)'].sem()
SEM


# ## Bar and Pie Charts

# In[103]:


# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using Pandas.

# Create a bar plot using Pandas
regimen_counts.plot(kind='bar', title='Total Observed Timepoints for Each Drug Regimen')

# Add labels to the axes
plt.xlabel('Drug Regimen')
plt.ylabel('Mouse Timepoints')

# Show the plot
plt.show()



# In[104]:


# A bar plot showing the total number of timepoints for all mice tested for each drug regimen using pyplot is generated. 

import numpy as np
import matplotlib.pyplot as plt

# Counting the occurrences of each drug regimen
regimen_counts = cleaned_data['Drug Regimen'].value_counts()

# Setting up x-axis and tick locations
x_axis = np.arange(len(regimen_counts))
tick_locations = [value for value in x_axis]

# Creating the bar plot
plt.bar(x_axis, regimen_counts)
plt.xticks(tick_locations, regimen_counts.index, rotation='vertical')

# Adding labels and title
plt.xlabel('Drug Regimen')
plt.ylabel('Mouse Timepoints')


# Display the plot
plt.show()


# In[105]:


# A pie plot showing the distribution of female versus male mice using pyplot is generated. # Counting the number of female and male mice

sex_distribution = cleaned_data['Sex'].value_counts()
import matplotlib.pyplot as plt

# Data for pie chart
sizes = sex_distribution.values
labels = sex_distribution.index

# Creating the pie chart
plt.pie(sizes, labels=labels, autopct='%1.1f%%')

# Adding a title
plt.title('Distribution of Female vs Male Mice')

# Show the plot
plt.show()


# ## Quartiles, Outliers and Boxplots

# In[106]:


# Calculate the final tumor volume of each mouse across four of the treatment regimens:  
# Capomulin, Ramicane, Infubinol, and Ceftamin
# Start by getting the last (greatest) timepoint for each mouse
# Merge this group df with the original DataFrame to get the tumor volume at the last timepoint



# A DatFrame that has the last timepoint for each mouse ID is created using groupby.
last_timepoint_df = cleaned_data.groupby('Mouse ID')['Timepoint'].max().reset_index()
last_timepoint_df


# In[107]:


# The index of the DataFrame is reset. 
last_timepoint_df.reset_index(drop=True, inplace=True)


# In[108]:


# The four treatment groups, Capomulin, Ramicane, Infubinol, and Ceftamin, are put in a list. 
treatment_groups = ['Capomulin', 'Ramicane', 'Infubinol', 'Ceftamin']
treatment_groups


# In[109]:


# Create an empty list to store tumor volume data:
tumor_vol_data = []


# In[110]:


# A "for" loop is used to display the interquartile range (IQR) and the outliers for each treatment group.


# List of the four treatment groups
treatments = ['Capomulin', 'Ramicane', 'Infubinol', 'Ceftamin']
tumor_vol_data = []

for treatment in treatments:
    # Locate the rows which contain mice on each drug and get the tumor volumes
    treatment_df = cleaned_data[cleaned_data['Drug Regimen'] == treatment]
    tumor_volumes = treatment_df['Tumor Volume (mm3)']

    # Add subset
    tumor_vol_data.append(tumor_volumes)

    # Calculate the IQR and quantitatively determine if there are any potential outliers
    quartiles = tumor_volumes.quantile([.25, .5, .75])
    lowerq = quartiles[0.25]
    upperq = quartiles[0.75]
    iqr = upperq - lowerq
    lower_bound = lowerq - (1.5 * iqr)
    upper_bound = upperq + (1.5 * iqr)
    outliers = tumor_volumes[(tumor_volumes < lower_bound) | (tumor_volumes > upper_bound)]

    # Display results
    print(f"{treatment} Regimen:")
    print(f"  IQR: {iqr}")
    print(f"  Lower Bound: {lower_bound}")
    print(f"  Upper Bound: {upper_bound}")
    if not outliers.empty:
        print(f"  Potential outliers: {outliers.values}")
    else:
        print("  No potential outliers found")
    print("\n")


# In[111]:


# A box plot is generated that shows the distribution of the final tumor volume for all the mice in each treatment group.#

import matplotlib.pyplot as plt
# Treatment group names for plot labels
treatment_groups = ['Capomulin', 'Ramicane', 'Infubinol', 'Ceftamin']

# Create the box plot
plt.boxplot(tumor_vol_data, labels=treatment_groups, flierprops=dict(marker='o', markerfacecolor='r', markersize=8))

# Add titles and labels
plt.title('Final Tumor Volume by Treatment')
plt.ylabel('Final Tumor Volume (mm3)')
plt.xlabel('Drug Regimen')

# Show the plot
plt.show()


# In[112]:


# Group by 'Mouse ID' and find the maximum timepoint for each mouse
final_timepoints = cleaned_data.groupby('Mouse ID')['Timepoint'].max().reset_index()
final_timepoints


# ## Line and Scatter Plots

# In[113]:


# Generate a line plot of tumor volume vs. time point for a single mouse treated with Capomulin

import matplotlib.pyplot as plt

# Assuming 'cleaned_data' is your DataFrame and it has 'Drug Regimen', 'Mouse ID', 'Timepoint', and 'Tumor Volume (mm3)' columns
# Step 1: Filter the data for Capomulin treatment
capomulin_data = cleaned_data[cleaned_data['Drug Regimen'] == 'Capomulin']

# Step 2: Select a single mouse 
mouse_id = 'l509'  # select mouse ID as of "l509", the one used in Starter code
mouse_data = capomulin_data[capomulin_data['Mouse ID'] == mouse_id]

# Step 3: Plot tumor volume over time for that single mouse
plt.plot(mouse_data['Timepoint'], mouse_data['Tumor Volume (mm3)'], marker='o')

# Adding a title and labels
plt.title(f'Capomulin treatment of mouse l509')
plt.xlabel('Timepoint (Days)')
plt.ylabel('Tumor Volume (mm3)')

# Show the plot
plt.show()


# In[114]:


# Generate a scatter plot of mouse weight vs. the average observed tumor volume for the entire Capomulin regimen


import matplotlib.pyplot as plt

# Assuming 'cleaned_data' is your DataFrame and it contains 'Drug Regimen', 'Mouse ID', 'Tumor Volume (mm3)', and 'Weight (g)' columns

# Step 1: Filter the data for the Capomulin regimen
capomulin_data = cleaned_data[cleaned_data['Drug Regimen'] == 'Capomulin']

# Step 2: Group by mouse ID to calculate the average tumor volume
avg_tumor_vol = capomulin_data.groupby('Mouse ID')['Tumor Volume (mm3)'].mean()

# Step 3: Merge this with the mouse weight data
mouse_weight = capomulin_data.groupby('Mouse ID')['Weight (g)'].mean()  # assuming the weight does not change
avg_tumor_vol = avg_tumor_vol.reset_index()
mouse_weight = mouse_weight.reset_index()
capomulin_summary = pd.merge(avg_tumor_vol, mouse_weight, on='Mouse ID')

# Step 4: Generate the scatter plot
plt.scatter(capomulin_summary['Weight (g)'], capomulin_summary['Tumor Volume (mm3)'])

# Adding a title and labels
plt.title('Average Tumor Volume vs. Mouse Weight for the Capomulin Regimen')
plt.xlabel('Weight (g)')
plt.ylabel('Average Tumor Volume (mm3)')

# Show the plot
plt.show()




# ## Correlation and Regression

# In[115]:


# Calculate the correlation coefficient and a linear regression model 
# for mouse weight and average observed tumor volume for the entire Capomulin regimen


correlation = st.pearsonr(capomulin_summary['Weight (g)'], capomulin_summary['Tumor Volume (mm3)'])
print(f"The correlation coefficient between mouse weight and average tumor volume is {correlation[0]:.2f}")



# In[120]:


# Plot the different factors in a scatter plot

from scipy.stats import linregress

x_values = capomulin_summary['Weight (g)']
y_values = capomulin_summary['Tumor Volume (mm3)']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(0,50),fontsize=15,color="red")
plt.xlabel('Weight (g)')
plt.ylabel('Average Tumor Volume (mm3)')
print(f"The r-squared is: {rvalue**2}")
plt.show()


# In[ ]:




