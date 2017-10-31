###############################################################################
# Shark Attack Data Scrape 
# 
# Author(s): Roger Doles
#            Elizabeth Eakin
#            Nicholas Rupp
#
# Date: 10/27/17
#
# Purpose: Scrape shark attack data from sharkattackdata.com
#
###############################################################################

import lxml
from urllib import request
from lxml import etree
import pandas as pd
import numpy as np
from selenium import webdriver # to allow js to load page before scrape

# Globals
baseurl = r'http://www.sharkattackdata.com'
headurl = r'http://www.sharkattackdata.com/place/united_states_of_america'
webDriverLoc = "C:/Users/red7740/Downloads/chromedriver.exe" # Change to your own path

# Add options arguments for Chrome
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600') # I don't think this is necessary anymore

#Helper Function -- Should put this into a separate file...
def getHTML(url):
    '''
    Returns inner html after JS executes from giver url
    '''
    # Load the page and scrape for data
    browser = webdriver.Chrome(executable_path="C:/Users/red7740/Downloads/chromedriver.exe",chrome_options=options)#added headless
    browser.get(url)
    innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
    browser.close()
    return innerHTML


# Get headings and main attack data from root url 
myETree = lxml.etree.HTML(getHTML(headurl))
heads = myETree.xpath('//thead/tr/th')
attacks = myETree.xpath('//tbody/tr/td')
links = myETree.xpath('//tbody/tr/td/a/@href')

#convert column names to list
headings=[]
for h in heads:
    headings.append(h.text)

#convert data to list
data=[]
for a in attacks:
    data.append(a.text)

#convert links to list
links = list(links)

# Fix heading value 
headings.pop()
headings.append('url')

# Massage Data into a pandas dataframe
#get some sizes...
ncols = len(headings) 
nrows = int(len(data)/len(headings))

#Start with data -> numpy array -> reshape -> dataframe
data = np.array(data) #list-> numpy array
data = data.reshape(nrows,ncols)# reshape array
data = pd.DataFrame(data) #np.array -> dataframe
    
#loop through urls to details section and grab data
detail_data = [] # data
detail_headers = [] # column names
count = 0 #counter for loop progress to display in console

for url in links: # slice links for demo or debug. remove slice for full executable        
    # Get and parse html string
    myETree = lxml.etree.HTML(getHTML(baseurl+url))
    # xpath for data
    dat = myETree.xpath('//tbody/tr/td')
    
    #convert data to list
    details=[]
    for d in dat:
        details.append(d.text)
        
    #append details of each record to data list
    detail_data.append(details)
    
    # First time through loop - grab headers
    if count == 0: #change count var to boolean if count-print removed
        # xpath for data
        dat = myETree.xpath('//tbody/tr/th')
        #convert data to list
        detail_headers=[]
        for d in dat:
            detail_headers.append(d.text)
            
    #print progress tracking for debugging - can remove when deployed
    count += 1
    if (count % 50) == 0:
        print("Status: record " + str(count) + " completed. " + str(nrows - count) + " remaining")
        
# details -> dataframe     
detail_data = pd.DataFrame(detail_data)
detail_data.columns = detail_headers

#detail_data = pd.DataFrame(detail_data)
parent_data = pd.DataFrame(data.iloc[:,:6])
parent_data.columns = headings

#merge details onto parent attack data
shark_attack_data = pd.concat([parent_data, detail_data], axis=1) # links -> last column in data frame

# Export data to permanant storage
shark_attack_data.to_csv('./shark_attack_data.csv',)

