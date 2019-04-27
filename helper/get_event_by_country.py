import pandas as pd
import os

########################
# Load File
########################
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
all_loc = os.path.join(__location__,'..' ,'data/trend/all.csv')
death_loc = os.path.join(__location__,'..' ,'data/trend/death_by_country.csv')
incident_loc = os.path.join(__location__,'..' ,'data/trend/incident_by_country.csv')

country_all_df = pd.read_csv(all_loc)
death_df = pd.read_csv(death_loc,skiprows=[0])
incident_df = pd.read_csv(incident_loc,skiprows=[0])

########################
# Agg Death incident and Country information
########################
death_year = list(death_df.columns)
death_year.remove('Country')

death_df['Country_merge'] = death_df['Country'].apply(lambda x: x.replace(" ", "").lower())
country_all_df['Country_merge'] = country_all_df['name'].apply(lambda x: x.replace(" ", "").lower())

death_country_df = death_df.merge(country_all_df, left_on='Country_merge', right_on='Country_merge', how='inner')
death_country_extract_df = death_country_df[death_year+['Country']+['sub-region']+['region']].fillna(0)

death_by_years = []

def get_child_parent_list_by_year(year):
    # World
    world = [{
        'id': '0.0',
        'parent': '',
        'name': 'The World'
    }]

    # Region
    region_extract = death_country_extract_df['region'].unique()
    regions = []
    for idx, val in enumerate(region_extract):
        region = {'id':f'1.{idx}', 'parent':'0.0','name':val}
        regions.append(region)

    # Sub-region
    sub_region_extract = death_country_extract_df['sub-region'].unique()
    sub_regions = []

    for idx, val in enumerate(sub_region_extract):
        sub_region = {'id':f'2.{idx}','name':val}
        parent_index = (death_country_extract_df['sub-region'].values == val).argmax()
        print()
        parent_name = death_country_extract_df.loc[parent_index,'region']
        parent_id = list(filter(lambda x: x['name'] == parent_name, regions))[0]['id']
        sub_region['parent'] = parent_id
        sub_regions.append(sub_region)

    # Country by year
    country_extract = death_country_extract_df['Country']
    countries = []

    for idx, val in enumerate(country_extract):
        country = {'id':f'3.{idx}','name':val,'value':death_country_extract_df.loc[idx,year]}
        parent_name = death_country_extract_df.loc[idx,'sub-region']
        parent_id = list(filter(lambda x: x['name'] == parent_name, sub_regions))[0]['id']
        country['parent'] = parent_id
        countries.append(country)

    return world+regions+sub_regions+countries


def get_child_parent_list():

    child_parent_list_dic = {}

    for iYear in death_year:

        child_parent_list_dic[iYear] = get_child_parent_list_by_year(iYear)

    return child_parent_list_dic


