# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 10:43:25 2017

@author: red7740
"""

import pandas as pd
import numpy as np
import re

data = pd.read_csv('C:/Users/red7740/Desktop/SharkAttacks/shark_attack_data.csv',encoding='latin-1')
del data['Date.1']
del data['Activity.1']
del data['Area.1']
del data['Location.1']
del data['Fatal?.1']
del data['Incident Type.1']
del data['Unnamed: 0']
data['Country'] = 'USA'
#data.Activity.fillna('',inplace=True)
#data.Sex.fillna('',inplace=True)

#make an age set
data.Age.fillna(0,inplace=True) #NaN vals -> 0
ages = pd.DataFrame(data['Age'].value_counts()).reset_index()
ages.columns = ['Age','Count']
unknownage = ages.iloc[0]
ages = ages[1:] #remove unkown age
ages = ages.sort_values('Age').reset_index()
del ages['index']


ages['Age'] = ages['Age'].str.replace(r'(.{2})or.*', r'\1')
ages['Age'] = ages['Age'].str.replace(r'(.{2})&.*', r'\1')
ages['Age'] = ages['Age'].str.replace(r'(.{2})\'s', r'\1')
ages['Age'] = ages['Age'].str.replace(r'(.{2})s', r'\1')
ages['Age'] = ages['Age'].str.replace(r'(6)[^0-9]', r'\1')
cats = ages[80:]
ages = ages[:80]
age_bins = {'Child':0,'Teen':0,'Young Adult':0,'Adult':0,'Seniors':0}
for i in ages['Age']:
    if int(i) < 10: 
        age_bins['Child'] += 1
    elif int(i) < 18:
        age_bins['Teen'] += 1
    elif int(i) < 25:
        age_bins['Young Adult'] += 1
    elif int(i) < 65:
        age_bins['Adult'] += 1
    else:
        age_bins['Seniors'] += 1

age_bins['Unknown'] = unknownage['Count']

#hack for categorical data cleanup -- can't automate
age_bins['Child'] += 1
age_bins['Teen'] += 7
age_bins['Young Adult'] += 1
age_bins['Seniors'] += 1

