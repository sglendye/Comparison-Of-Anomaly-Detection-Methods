# Introduction:

In many examples that I’ve seen online or otherwise, dealing with anomalies is viewed more of as a necessary chore than an analysis in its own right. It is approached at times with a “let’s get this over with” attitude whereby researchers quickly try to isolate outlying points to eliminate, or to eliminate everything around them, with little exploration into why their method for selecting these points may or may not be appropriate. I too am guilty of having made this mistake. While it may be easy to fall back onto whichever method is most familiar, easiest to implement, or most trendy at the time, the method used for selecting anomalous points can have serious downstream repercussions and may heavily bias the end results of an analysis.

In this analysis, I compare three of my favorite methods for anomaly detection, all of which function very differently “under the hood”. The models are evaluated based on accuracy - as defined by the ever so scientific "eyeballing it"; speed of execution – since as with all modeling, the tradeoff between time to execute and how robust it needs to be should never be forgotten; and most importantly, which points are selected. It may sound nice to pick out outliers in the nebulous, but in practicality, the underlying mathematics of different methods are quite different and in addition to the above metrics, your model selection should be driven by the goal of your project.

The three models that were selected for this analysis are:

•	The isolation forest. For those not familiar, this is an ensemble tree method to isolate points far from the norm. A "contamination score" can be implemented to name the rough percentage that we expect the forest to find, and in this case we will say that ~2% of the points are outliers. We'll also tell the forest to create 1000 decision trees.

•	The Cook's Distance, used with (multiple) linear regression. This method uses the residuals of points to score how much they impact the regression line. A typical "outlier" (used here for simplicity's sake) is 4/n, where n is the number of observations.

•	The humble standard score. While z-scores may be associated with introductory statistics classes due to their simplicity and sensitivity to data shape, they are certainly the most common outlier metric used. Furthermore, they can serve their purpose well when used appropriately. For simplicity's sake here, we'll use the traditional 3 standard deviations away as our outlier metric. For multi-dimensional data, we'll take an average of the standard scores (with all of the assumptions that may entail).

The specific data used is the number of Covd-19 cases and deaths in each United States county on 7/3/2020, giving us 3052 observations to work with. In conjunction with our Covid data, I merge on some Census data from the American Community Survey in the final section to keep things interesting. To be honest, the data selection for this project is entirely arbitrary, as we are not testing any one hypothesis. However, I decided that Covid data would be timely and interesting to visualize for our models.

The simple tests for comparing these models will be identifying outliers along one dimension, two dimensions, and three dimensions. Why such low dimensionality? Z-scores, despite arguably being the most commonly used metric are pretty difficult to scale up. Furthermore, I personally thought that it may be interesting to attempt to define a line where it may be beneficial to switch between models, and I suspect that this begins in three dimensional space.

<br/>

# Contents of This Repository:

<br/>

## Data:
The data is a number of raw csv files pulled for this project. The ACS_5yr_demo is an extract from the Census’ ACS data containing demographics such as age, race, etc. for each county, while the ACS_5yr_industry file contains specific breakdowns of labor categories for each county. As noted above, the NYT_historical data is a pull from the Covid-19 dataset that the New York Times is maintaining on their github. 

Source data for the Census: https://data.census.gov/cedsci/

Source data for NYT: https://github.com/nytimes/covid-19-data?fbclid=IwAR1xa3rM45z5RWDZt0ubH4vYEgbNNgiH9jz-VGebd3htK_xOFo5BCn8gPZU


## Modules:

The *Modules* folder contains a module for each of the analyses performed. In hindsight, it may have made sense to refactor some of these into class modules or to at least group them together based on function. However, in their current iteration they should at least represent an easy to follow workflow with each function clearly defined by their position in the analysis. The first-second-third titles denote which exercise in the analysis the functions are called for, and the name of the function describes either which model is being called or, in the case of the table connects, which data set is being produced from our database. The *create_database* module is unique in that is the first function called in the analysis, which creates a working database from the data located in the data folder. If the database does not yet exist, it creates it, and then it performs checks to make sure that the requisite tables are included. If they are not, they are written in from the appropriate data file(s).

## Analysis Files:

The analysis files are all iterations of the analysis performed. 

The .ipynb notebook and the html are the same file, with the html version of the notebook being published for readers who do not have Jupyter. These files contain similar theoretical rationale behind the project in their introductory section, and demonstrating the results of the analysis. They contain sections demonstrating plots used for the eyeball test and also provide indications of the speed tests performed with each of the models. Finally, these files also provide some analysis with my observations on how the models are comparing under each degree of dimensionality and why they may or may not be behaving as they do. 

The *Perform_Analysis* module is the python file that I used to run the analysis. It produces our SQLite database, should the database not already exist, and then proceeds to call each of the other functions in the *Modules* folder to perform the analysis. Should you wish to replicate my results, simply download or clone the repository and leave the folder structure intact for this module to serve its purpose.

