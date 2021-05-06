import json
file_kaggle_config = open('./config/kaggle.json', 'r', encoding='utf-8')
kaggle_config = json.load(file_kaggle_config)
import os
os.environ['KAGGLE_USERNAME'] = kaggle_config['username']
os.environ['KAGGLE_KEY'] = kaggle_config['key']
import kaggle
import animation
import pandas as pd
from datetime import datetime

RAW_PANDEMIC_DATA_PATH = './covid_data/raw/pandemic'
RAW_VACCINATION_DATA_PATH = './covid_data/raw/vaccination'
PANDEMIC_DAILY_DATA_FILENAME = 'worldometer_coronavirus_daily_data.csv'
VACCINATION_BY_MF_DATA_FILENAME = 'country_vaccinations_by_manufacturer.csv'

PANDEMIC_RAW_TO_USE_PATH = RAW_PANDEMIC_DATA_PATH + '/' + PANDEMIC_DAILY_DATA_FILENAME
VACCINATION_RAW_TO_USE_PATH = RAW_VACCINATION_DATA_PATH + '/' + VACCINATION_BY_MF_DATA_FILENAME

CACHE_DATA_PATH = './covid_data/cache'
PANDEMIC_BEF_VACC_FILENAME = 'pandemic_before.csv'
PANDEMIC_AFT_VACC_FILENAME = 'pandemic_after.csv'
VACC_SLICE_FILENAME = 'vaccination.csv'

PANDEMIC_BEF_VACC_PATH = CACHE_DATA_PATH + '/' + PANDEMIC_BEF_VACC_FILENAME
PANDEMIC_AFT_VACC_PATH = CACHE_DATA_PATH + '/' + PANDEMIC_AFT_VACC_FILENAME
VACC_SLICE_PATH = CACHE_DATA_PATH + '/' + VACC_SLICE_FILENAME

COUNTRY_LIST_PANDEMIC = ['Chile','France','Germany','Italy','USA']
COUNTRY_LIST_VACCINATION = ['Chile','France','Germany','Italy','United States']
VACC_TYPES = ['Johnson&Johnson', 'Moderna', 'Oxford/AstraZeneca', 'Pfizer/BioNTech', 'Sinovac']

def str2date(str_date: str) -> datetime: return datetime.strptime(str_date,'%Y-%m-%d') 

@animation.wait(animation = 'bar', text='Downloading the pandemic data from Kaggle')
def update_pandemic_raw_data():
    kaggle.api.dataset_download_files('josephassaker/covid19-global-dataset', path=RAW_PANDEMIC_DATA_PATH, force=True, unzip=True)

@animation.wait(animation = 'bar', text='Downloading the vaccination data from Kaggle')
def update_vaccination_raw_data():
    kaggle.api.dataset_download_files('gpreda/covid-world-vaccination-progress', path=RAW_VACCINATION_DATA_PATH, force=True, unzip=True)

@animation.wait(animation = 'bar', text='Generating Data for further computation')
def generate_data():
    # Read raw data
    file_pandemic = open(PANDEMIC_RAW_TO_USE_PATH, 'r', encoding='utf-8')
    file_vaccination = open(VACCINATION_RAW_TO_USE_PATH, 'r', encoding='utf-8')
    # df_pandemic = pd.read_csv(file_pandemic, usecols=['date','country','cumulative_total_cases'])
    df_pandemic = pd.read_csv(file_pandemic)
    df_vaccination = pd.read_csv(file_vaccination)
    df_pandemic = df_pandemic[df_pandemic['country'].isin(COUNTRY_LIST_PANDEMIC)]
    df_vaccination = df_vaccination[df_vaccination['location'].isin(COUNTRY_LIST_VACCINATION)]
    df_vaccination['location'] = df_vaccination['location'].map(lambda x: "USA" if x == "United States" else x)
    df_vaccination.columns = df_vaccination.columns.map(lambda x:"country" if x == 'location' else x)
    df_vacc_start = df_vaccination.groupby('country')['date'].min()
    # split the pandemic data
    for idx, (country, date) in enumerate(df_vacc_start.items()):
        df_same_country_operator = df_pandemic['country'] == country
        df_before_operator = df_pandemic['date'].map(str2date) < date
        df_nxt_bef_selector = df_same_country_operator & df_before_operator
        df_nxt_aft_selector = df_same_country_operator & ~df_before_operator
        df_bef_selector = df_nxt_bef_selector if idx == 0 else df_bef_selector | df_nxt_bef_selector
        df_aft_selector = df_nxt_aft_selector if idx == 0 else df_aft_selector | df_nxt_aft_selector

    df_pandemic_bef_vacc = df_pandemic[df_bef_selector]
    df_pandemic_aft_vacc = df_pandemic[df_aft_selector]

    # Don't pass file. Just pass the path, or otherwise unnecessary newlines are added.
    df_pandemic_bef_vacc.to_csv(PANDEMIC_BEF_VACC_PATH, index=None)
    df_pandemic_aft_vacc.to_csv(PANDEMIC_AFT_VACC_PATH, index=None)
    df_vaccination.to_csv(VACC_SLICE_PATH, index=None)

def get_slice_vacc_sum_by_types()->pd.DataFrame:
    file_vacc_slice = open(VACC_SLICE_PATH, 'r', encoding='utf-8')
    df_vaccination = pd.read_csv(file_vacc_slice)
    return df_vaccination.groupby('vaccine')['total_vaccinations'].sum()