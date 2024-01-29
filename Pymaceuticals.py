#!/usr/bin/env python
# coding: utf-8

# # Pymaceuticals Inc.
# ---
# 
# ### Analysis
# 
# - Add your analysis here.
#  

# In[50]:


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


# In[37]:


# Display the number of unique mice IDs in the data

unique_mouse_ids = combined_data['Mouse ID'].nunique()
unique_mouse_ids


# In[38]:


# check for any mouse ID with duplicate time points.

duplicate_ids = combined_data[combined_data.duplicated(subset=['Mouse ID', 'Timepoint'])]['Mouse ID'].unique()
duplicate_ids


# In[52]:


# Get the duplicate mice by ID number that shows up for Mouse ID and Timepoint. 
duplicate_mouse_data = Adjusted_df[Adjusted_df['Mouse ID'].isin(duplicate_ids)]

# Optional: Get all the data for the duplicate mouse ID. 
duplicate_mouse_data


# In[53]:


# Create a clean DataFrame by dropping the duplicate mouse by its ID.
# Mouse ID to be removed
duplicate_mouse_id = 'g989'

# Creating a clean DataFrame by dropping all data for the duplicate mouse ID
cleaned_data = Adjusted_df[Adjusted_df['Mouse ID'] != duplicate_mouse_id]
cleaned_data.head()


# In[55]:


# Checking the number of mice in the clean DataFrame.
unique_clean_mouse_ids = cleaned_data['Mouse ID'].nunique()
unique_clean_mouse_ids


# ## Summary Statistics

# In[84]:


#The mean of the tumor volume for each regimen is calculated using groupby.
mean = df.groupby('Drug Regimen')['Tumor Volume (mm3)'].mean()
mean


# In[77]:


# The median of the tumor volume for each regimen is calculated using groupby. 
median =df.groupby('Drug Regimen')['Tumor Volume (mm3)'].median()
median


# In[81]:


# The variance of the tumor volume for each regimen is calculated using groupby. 
variance =df.groupby('Drug Regimen')['Tumor Volume (mm3)'].var()
variance


# In[82]:


# The standard deviation of the tumor volume for each regimen is calculated using groupby. 
STD = df.groupby('Drug Regimen')['Tumor Volume (mm3)'].std()
STD   


# In[83]:


# The SEM of the tumor volume for each regimen is calculated using groupby. 
SEM = df.groupby('Drug Regimen')['Tumor Volume (mm3)'].sem()
SEM


# In[92]:


# A more advanced method to generate a summary statistics table of mean, median, variance, standard deviation,
# Using the aggregation method, produce the same summary statistics in a single line
summary_stats = cleaned_data.groupby('Drug Regimen')['Tumor Volume (mm3)'].agg(['mean', 'median', 'var', 'std', 'sem'])
summary_stats = summary_stats.rename(columns={'mean':'Mean Tumor Volume','median':'Median Tumor Volume','var':'Tumor Volume Variance','std':'Tumor Volume Std. Dev.','sem':'Tumor Volume Std. Err.'})      
summary_stats


# ## Bar and Pie Charts

# In[94]:


# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using Pandas.

# Create a bar plot using Pandas
regimen_counts.plot(kind='bar', title='Total Number of Rows for Each Drug Regimen')

# Add labels to the axes
plt.xlabel('Drug Regimen')
plt.ylabel('Number of Rows')

# Show the plot
plt.show()



# In[98]:


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
plt.ylabel('Number of Rows')
plt.title('Total Number of Rows for Each Drug Regimen')

# Display the plot
plt.show()


# In[99]:


# A pie plot showing the distribution of female versus male mice using Pandas is generated.

# Counting the number of female and male mice
sex_distribution = cleaned_data['Sex'].value_counts()

# Create a pie plot
sex_distribution.plot(kind='pie', title='Distribution of Female vs Male Mice', autopct='%1.1f%%')
plt.show()


# In[100]:


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

# In[110]:


# Calculate the final tumor volume of each mouse across four of the treatment regimens:  
# Capomulin, Ramicane, Infubinol, and Ceftamin
# Start by getting the last (greatest) timepoint for each mouse
# Merge this group df with the original DataFrame to get the tumor volume at the last timepoint



# A DatFrame that has the last timepoint for each mouse ID is created using groupby.
last_timepoint_df = cleaned_data.groupby('Mouse ID')['Timepoint'].max().reset_index()
last_timepoint_df


# In[111]:


# The index of the DataFrame is reset. 
last_timepoint_df.reset_index(drop=True, inplace=True)


# In[113]:


# The four treatment groups, Capomulin, Ramicane, Infubinol, and Ceftamin, are put in a list. 
treatment_groups = ['Capomulin', 'Ramicane', 'Infubinol', 'Ceftamin']
treatment_groups


# In[117]:


# Create an empty list to store tumor volume data:
tumor_vol_data = []


# In[118]:


# A "for" loop is used to display the interquartile range (IQR) and the outliers for each treatment group.


# List of the four treatment groups
treatments = ['Capomulin', 'Ramicane', 'Infubinol', 'Ceftamin']
tumor_vol_data = []

for treatment in treatments:
    # Locate the rows which contain mice on each drug and get the tumor volumes
    treatment_df = merged_data[merged_data['Drug Regimen'] == treatment]
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


# In[119]:


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


# In[106]:


# Group by 'Mouse ID' and find the maximum timepoint for each mouse
final_timepoints = filtered_df.groupby('Mouse ID')['Timepoint'].max().reset_index()
final_timepoints


# ## Line and Scatter Plots

# In[124]:


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


# In[125]:


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

# In[130]:


# Calculate the correlation coefficient and a linear regression model 
# for mouse weight and average observed tumor volume for the entire Capomulin regimen


import matplotlib.pyplot as plt

# Create a scatter plot of the average tumor volume vs. mouse weight
plt.scatter(mouse_grouped['Weight (g)'], mouse_grouped['Tumor Volume (mm3)'])

# Plot the linear regression line
regress_values = mouse_grouped['Weight (g)'] * slope + intercept
plt.plot(mouse_grouped['Weight (g)'], regress_values, "r-")

# Add labels and title to the plot
plt.xlabel('Weight (g)')
plt.ylabel('Average Tumor Volume (mm3)')
plt.title('Weight vs. Average Tumor Volume for Capomulin')
plt.show()

# Display the correlation coefficient and linear regression model results
print(f"The correlation coefficient between mouse weight and average tumor volume for the Capomulin regimen is: {correlation_coef:.2f}")
print(f"The linear regression model is: y = {slope:.2f}x + {intercept:.2f}")




# In[ ]:




