import pandas as pd
import numpy as np
import math
from sklearn.linear_model import LinearRegression

########################
# Load File
########################

##Aggregating malaria death and child mortality rate data
malaria=pd.read_csv("data/trend/death_by_country_tracy.csv")
child=pd.read_csv("data/trend/child.csv")
child_death=child[child["Uncertainty bounds*"]=="Median"]
child_death.rename(columns={'Country':'Country Name'}, inplace=True)


malaria_child=pd.merge(malaria, child_death, on='Country Name', how='inner')
malaria_child=malaria_child.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
malaria_child["Feature"]=malaria_child["U5MR.2017"]
malaria_child["Malaria_Num_Death"]=malaria_child["Num Death 2017"]
malaria_child=malaria_child[["Country Name","Feature","Malaria_Num_Death"]]


#Aggregating malaria death data and GDP data
gdp=pd.read_csv("data/trend/GDP_by_country.csv")
malaria_gdp=pd.merge(malaria, gdp, on='Country Name', how='inner')
malaria_gdp=malaria_gdp.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
malaria_gdp["Feature"]=malaria_gdp["2017"]
malaria_gdp["Malaria_Num_Death"]=malaria_gdp["Num Death 2017"]
malaria_gdp= malaria_gdp[["Country Name","Feature","Malaria_Num_Death"]]

#Aggregating malaria death and Percipitation
p=pd.read_csv("data/trend/Precipitation.csv")
match=pd.read_csv("data/trend/code_match.csv")
percipitation=pd.merge(p, match, on='ISO_3DIGIT', how='inner')
malaria_percipitation=pd.merge(malaria, percipitation, on='Country Name', how='inner')
malaria_percipitation["Feature"]=malaria_percipitation["Annual_precip"]
malaria_percipitation["Malaria_Num_Death"]=malaria_percipitation["Num Death 2017"]
malaria_percipitation= malaria_percipitation[["Country Name","Feature","Malaria_Num_Death"]]
malaria_percipitation=malaria_percipitation.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

########################
# Data export
########################

def regress_child():
    malaria_child_17=LinearRegression()
    malaria_child_17.fit(malaria_child["Feature"].values.reshape(-1, 1),malaria_child["Malaria_Num_Death"].values.reshape(-1, 1))
    
    malaria_child_17_coef=malaria_child_17.coef_[0][0]
    malaria_child_17_intercept=malaria_child_17.intercept_[0]
    regress_child={}
    child.dict=malaria_child.to_dict()
    line_values={}
    line_values={"coef": malaria_child_17_coef, "intercept":malaria_child_17_intercept}
    regress_child={"scatter": child.dict, "line": line_values}
    return regress_child

def regress_gdp():
    malaria_gdp_17=LinearRegression()
    malaria_gdp_17.fit(malaria_gdp["Feature"].values.reshape(-1, 1),malaria_gdp["Malaria_Num_Death"].values.reshape(-1, 1))
    
    malaria_gdp_17_coef=malaria_gdp_17.coef_[0][0]
    malaria_gdp_17_intercept=malaria_gdp_17.intercept_[0]

    regress_gdp={}
    gdp.dict=malaria_gdp.to_dict()
    line_values={}
    line_values={"coef": malaria_gdp_17_coef, "intercept": malaria_gdp_17_intercept}
    regress_gdp={"scatter": gdp.dict, "line": line_values}
    
    return regress_gdp
   
def regress_rain():
    malaria_percipitation_17=LinearRegression()
    malaria_percipitation_17.fit(malaria_percipitation["Feature"].values.reshape(-1, 1),malaria_percipitation["Malaria_Num_Death"].values.reshape(-1, 1))

    malaria_percipitation_17_coef= malaria_percipitation_17.coef_[0][0]
    malaria_percipitation_17_intercept=malaria_percipitation_17.intercept_[0]

    regress_rain={}
    raining_dict=malaria_percipitation.to_dict()
    line_values={}
    line_values={"coef": malaria_percipitation_17_coef, "intercept": malaria_percipitation_17_intercept}
    regress_rain={"scatter": raining_dict, "line": line_values}
    
    return  regress_rain
