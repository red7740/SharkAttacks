###############################################################################
# Shark Attacks  
# 
# Author(s): Roger Doles
#            Elizabeth Eakin
#            Nicholas Rupp
#
# Date: 10/27/17
#
###############################################################################

Abstract:
	
The Shark Attack Data Scrape project collects data on shark attack incidents in the 
United States from sharkattackdata.com. While not comprehensive, the data collected 
could be combined with data from additional sources to provide a more comprehensive
data set. 



Approach:

To collect the data, we deployed a simple bot that scrapes the root level of the site
for general information and click-through links. Those links are then followed to 
gather additional data points on each record. Once collected, we massage the data
into a useable form with numby and pandas. The resulting data set is then exported to 
a csv file for future analysis. 

Technical:

Sharkattackdata.com is JavaScript driven. As such, we utilize the Selenium package for 
calls to the site to allow the pageto render prior to collecting the html. We then parse
the html string with xpath for column headers and data points. The root level is 
compiled into a pandas dataframe separately from the details collected from the click-
throughs. The resulting dataframes are joined on the indices into a single dataframe 
that is exported to csv.

Our first approach used Chrome as the webdriver, consuming considerable resources in
the overhead of opening and closing the browser. This was mitigated by running the chrome
webdriver in headless mode, decreasing memory consumption and time required to complete 
the script. We intend to time the script and benchmark other headless webdrivers such as 
PhantomJS and NightmareJS.

  





