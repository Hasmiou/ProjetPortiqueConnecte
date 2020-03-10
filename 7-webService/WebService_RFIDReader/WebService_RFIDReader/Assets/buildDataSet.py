﻿#Import library

import pandas as pd
#import numpy as np

#parameters
appData=''
token=''
executed=False

#Import Data
n=['TimesTamp', 'ECP', 'Antenna', 'RSSI']
p=appData+'/11-RawData/'+token+'.csv'
d=','

def importData(path, delimit,cols):
    return pd.read_csv(path, sep=delimit,names=cols)

data=importData(p,d,n)

# TYPAGE DES CHAMPS
def typage(data):
    data['ECP']=data['ECP'].astype(str)
    data['TimesTamp']=data['TimesTamp'].astype('int64')
    data['RSSI']=data['RSSI'].astype('float64')
    data['Antenna']=data['Antenna'].astype('int64')
    data['FP']=data['FP'].astype('int64')
    return data

data=typage(data)

#Build DataSet
from scipy.stats import variation 

def generateDataSet(data, groupedBy):
    grouped_df = data.groupby(groupedBy) #On groupe les données par ..."Etiquetes"
    
    dataSet = pd.DataFrame({}) #Création d'une nouvelle dataFrame
    
    #Création des variables intermédiaire pour la récupération des champs
    ecp=pd.Series(grouped_df.ECP.unique().index,name="ECP")
    fp=pd.Series(grouped_df.FP.max(),name="FP")
    rc= pd.Series(grouped_df.ECP.count(),name="readcount")
    minRSSI= pd.Series(grouped_df.RSSI.min(),name="minRssi")
    maxRSSI= pd.Series(grouped_df.RSSI.max(),name="maxRssi")
    mean=pd.Series(grouped_df.RSSI.mean(),name="meanRssi")
    startTime=pd.Series(grouped_df.TimesTamp.min(),name="startTime")
    endTime=pd.Series(grouped_df.TimesTamp.max(),name="endTime")
    #diff=pd.Series(grouped_df.RSSI.diff,name="difference")
    
    #Mise à jour des champs de la dataFrame
    dataSet['ECP']=ecp.values
    dataSet['RC']=rc.values
    dataSet['MIN']=minRSSI.values
    dataSet['MAX']=maxRSSI.values
    dataSet['MEAN']=mean.values
    dataSet['START']=startTime.values
    dataSet['END']=endTime.values
    dataSet['DURATION']=endTime.values-startTime.values
    cv={}
    a1={}
    a2={}
    a3={}
    a4={}
    for key, item in grouped_df:
        cv[key]=variation(grouped_df['RSSI'].get_group(key).values,axis=0)
        a1[key]=0
        a2[key]=0
        a3[key]=0
        a4[key]=0
        for a in grouped_df['Antenna'].get_group(key).values:
            if(a==1): a1[key]+=1
            if(a==2): a2[key]+=1
            if(a==3): a3[key]+=1
            if(a==4): a4[key]+=1
                
    dataSet['CV']=pd.Series(cv).values
    dataSet['A1']=pd.Series(a1).values
    dataSet['A2']=pd.Series(a2).values
    dataSet['A3']=pd.Series(a3).values
    dataSet['A4']=pd.Series(a4).values
    dataSet['FP']=fp.values
    
    return dataSet

dataSet=generateDataSet(data,'ECP')

#Export Data
def exportData(data, path):
    data.to_csv(path, index = None, header=False)

#Export allinOne
exportPath = appData+'/2-DataSet/'+token+'.csv'
exportData(dataSet, exportPath)

executed=True
