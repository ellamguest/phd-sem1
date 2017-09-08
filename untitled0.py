#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 21:33:57 2017

@author: emg
"""

import pandas as pd

surveys_df = pd.read_csv("/Users/emg/Desktop/data_carpentry/surveys.csv")

surveys_df
which prints contents like above


type(surveys_df)
# this does the same thing as the above!
surveys_df.__class__

surveys_df.dtypes
which returns:

surveys_df.columns
surveys_df.shape

surveys_df.head()
surveys_df.head(15)
surveys_df.tail()

surveys_df.columns.values

pd.unique(surveys_df['species_id'])



### CHALLENGE - STATISTICS
# 1) Create a list of unique plot ID’s found in the surveys data. Call it plot_names. How many unique plots are there in the data? How many unique species are in the data?
plot_names = pd.unique(surveys_df['plot_id'])
len(plot_names)

# 2) What is the difference between len(plot_names) and surveys_df['plot_id'].nunique()?
len(plot_names) == surveys_df['plot_id'].nunique()
    

surveys_df['weight'].describe()

surveys_df['weight'].min()
surveys_df['weight'].max()
surveys_df['weight'].mean()
surveys_df['weight'].std()
surveys_df['weight'].count()

# Group data by sex
grouped_data = surveys_df.groupby('sex')
# summary statistics for all numeric columns by sex
grouped_data.describe()
# provide the mean for each numeric column by sex
grouped_data.mean()

###Challenge - Summary Data

# 1) How many recorded individuals are female F and how many male M
grouped_data.count()
# 2) What happens when you group by two columns using the following syntax and then grab mean values:
grouped_data2 = surveys_df.groupby(['plot_id','sex'])
grouped_data2.mean()

# 3) Summarize weight values for each plot in your data. HINT: you can use the following syntax to only create summary statistics for one column in your data by_plot['weight'].describe()
Did you get #3 right?

A Snippet of the Output from challenge 3 looks like:

	plot
	1     count    1903.000000
	      mean       51.822911
	      std        38.176670
	      min         4.000000
	      25%        30.000000
	      50%        44.000000
	      75%        53.000000
	      max       231.000000
         ...
Quickly Creating Summary Counts in Pandas
Let’s next count the number of samples for each species. We can do this in a few ways, but we’ll use groupby combined with a count() method.

# count the number of samples by species
species_counts = surveys_df.groupby('species_id')['record_id'].count()
print(species_counts)
Or, we can also count just the rows that have the species “DO”:

surveys_df.groupby('species_id')['record_id'].count()['DO']
Challenge - Make a list

What’s another way to create a list of species and associated count of the records in the data? Hint: you can perform count, min, etc functions on groupby DataFrames in the same way you can perform them on regular DataFrames.
Basic Math Functions
If we wanted to, we could perform math on an entire column of our data. For example let’s multiply all weight values by 2. A more practical use of this might be to normalize the data according to a mean, area, or some other value calculated from our data.

# multiply all weight values by 2
surveys_df['weight']*2
Quick & Easy Plotting Data Using Pandas
We can plot our summary stats using Pandas, too.

# make sure figures appear inline in Ipython Notebook
%matplotlib inline
# create a quick bar chart
species_counts.plot(kind='bar');
Weight by Species Plot Weight by species plot

We can also look at how many animals were captured in each plot:

total_count = surveys_df.groupby('plot_id')['record_id'].nunique()
# let's plot that too
total_count.plot(kind='bar');
Challenge - Plots

Create a plot of average weight across all species per plot.
Create a plot of total males versus total females for the entire dataset.
Summary Plotting Challenge

Create a stacked bar plot, with weight on the Y axis, and the stacked variable being sex. The plot should show total weight by sex for each plot. Some tips are below to help you solve this challenge:

For more on Pandas plots, visit this link.
You can use the code that follows to create a stacked bar plot but the data to stack need to be in individual columns. Here’s a simple example with some data where ‘a’, ‘b’, and ‘c’ are the groups, and ‘one’ and ‘two’ are the subgroups.
d = {'one' : pd.Series([1., 2., 3.], index=['a', 'b', 'c']),'two' : pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
pd.DataFrame(d)
shows the following data

      one  two
  a    1    1
  b    2    2
  c    3    3
  d  NaN    4
We can plot the above with

# plot stacked data so columns 'one' and 'two' are stacked
my_df = pd.DataFrame(d)
my_df.plot(kind='bar',stacked=True,title="The title of my graph")
Stacked Bar Plot

You can use the .unstack() method to transform grouped data into columns for each plotting. Try running .unstack() on some DataFrames above and see what it yields.
Start by transforming the grouped data (by plot and sex) into an unstacked layout, then create a stacked plot.

Solution to Summary Challenge



Key Points

