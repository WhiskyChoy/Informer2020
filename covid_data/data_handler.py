import json

from pandas import DataFrame
file_kaggle_config = open('./config/kaggle.json', 'r', encoding='utf-8')
kaggle_config = json.load(file_kaggle_config)
import os
os.environ['KAGGLE_USERNAME'] = kaggle_config['username']
os.environ['KAGGLE_KEY'] = kaggle_config['key']
import kaggle
import animation
import pandas as pd
from utils.io import FreqType, create_dir_not_exists, DatetimeConverter
from utils.augmentation import augment_time_acc, augment_time_new, augment_time, augment_time_new_fit_rate

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

create_dir_not_exists(RAW_PANDEMIC_DATA_PATH, RAW_VACCINATION_DATA_PATH, CACHE_DATA_PATH)

@animation.wait(animation = 'bar', text='Downloading the pandemic data from Kaggle')
def update_pandemic_raw_data():
    kaggle.api.dataset_download_files('josephassaker/covid19-global-dataset', path=RAW_PANDEMIC_DATA_PATH, force=True, unzip=True)

@animation.wait(animation = 'bar', text='Downloading the vaccination data from Kaggle')
def update_vaccination_raw_data():
    kaggle.api.dataset_download_files('gpreda/covid-world-vaccination-progress', path=RAW_VACCINATION_DATA_PATH, force=True, unzip=True)

# @animation.wait(animation = 'bar', text='Generating Data for further computation')
def generate_data(pandemic_data_type: str = 'cumulative', augmentation: bool = False):
    # Read raw data
    file_pandemic = open(PANDEMIC_RAW_TO_USE_PATH, 'r', encoding='utf-8')
    file_vaccination = open(VACCINATION_RAW_TO_USE_PATH, 'r', encoding='utf-8')
    if pandemic_data_type == 'all':
        df_pandemic = pd.read_csv(file_pandemic)
    if pandemic_data_type == 'cumulative':
        df_pandemic = pd.read_csv(file_pandemic, usecols=['date','country','cumulative_total_cases', 'active_cases', 'cumulative_total_deaths'])
    if pandemic_data_type == 'new':
        df_pandemic = pd.read_csv(file_pandemic, usecols=['date','country','daily_new_cases', 'daily_new_deaths'])
    
    df_pandemic = df_pandemic.fillna(0) # augmentation might need to use 0. Remember to assign the val

    df_vaccination = pd.read_csv(file_vaccination)
    df_pandemic = df_pandemic[df_pandemic['country'].isin(COUNTRY_LIST_PANDEMIC)]
    df_vaccination = df_vaccination[df_vaccination['location'].isin(COUNTRY_LIST_VACCINATION)]
    df_vaccination['location'] = df_vaccination['location'].map(lambda x: "USA" if x == "United States" else x)
    df_vaccination.columns = df_vaccination.columns.map(lambda x:"country" if x == 'location' else x)
    df_vacc_start = df_vaccination.groupby('country')['date'].min()
    # split the pandemic data
    for idx, (country, date) in enumerate(df_vacc_start.items()):
        df_same_country_operator = df_pandemic['country'] == country
        df_before_operator = df_pandemic['date'].map(DatetimeConverter().str2date) < date
        df_nxt_bef_selector = df_same_country_operator & df_before_operator
        df_nxt_aft_selector = df_same_country_operator & ~df_before_operator
        df_bef_selector = df_nxt_bef_selector if idx == 0 else df_bef_selector | df_nxt_bef_selector
        df_aft_selector = df_nxt_aft_selector if idx == 0 else df_aft_selector | df_nxt_aft_selector

    df_pandemic_bef_vacc = df_pandemic[df_bef_selector]
    df_pandemic_aft_vacc = df_pandemic[df_aft_selector]

    if augmentation:
        if pandemic_data_type == 'cumulative':
            print('Start augmenting the cumulative data before pandemic...')
            df_pandemic_bef_vacc = augment_time_acc(df_pandemic_bef_vacc, '%Y-%m-%d', '%Y-%m-%d %H:%M:%S', FreqType.Day, FreqType.Hour, ['cumulative_total_cases', 'active_cases','cumulative_total_deaths'])
            print('Start augmenting the cumulative after pandemic...')
            df_pandemic_aft_vacc = augment_time_acc(df_pandemic_aft_vacc, '%Y-%m-%d', '%Y-%m-%d %H:%M:%S', FreqType.Day, FreqType.Hour, ['cumulative_total_cases', 'active_cases','cumulative_total_deaths'])
        if pandemic_data_type == 'new':
            print('Start augmenting the daily data before pandemic...')
            df_pandemic_bef_vacc = augment_time_new(df_pandemic_bef_vacc, '%Y-%m-%d', '%Y-%m-%d %H:%M:%S', FreqType.Day, FreqType.Hour, ['daily_new_cases', 'daily_new_deaths'])
            print('Start augmenting the daily data after pandemic...')
            df_pandemic_aft_vacc = augment_time_new(df_pandemic_aft_vacc, '%Y-%m-%d', '%Y-%m-%d %H:%M:%S', FreqType.Day, FreqType.Hour, ['daily_new_cases', 'daily_new_deaths'])
        if pandemic_data_type == 'all':
            print('Start augmenting all data before pandemic...')
            df_pandemic_bef_vacc = augment_time(df_pandemic_bef_vacc, '%Y-%m-%d', '%Y-%m-%d %H:%M:%S', FreqType.Day, FreqType.Hour, ['daily_new_cases', 'daily_new_deaths'],  ['cumulative_total_cases', 'active_cases','cumulative_total_deaths'])
            print('Start augmenting all data after pandemic...')
            df_pandemic_aft_vacc = augment_time(df_pandemic_aft_vacc, '%Y-%m-%d', '%Y-%m-%d %H:%M:%S', FreqType.Day, FreqType.Hour, ['daily_new_cases', 'daily_new_deaths'],  ['cumulative_total_cases', 'active_cases','cumulative_total_deaths'])

    # Avoid NaN in the final output data
    df_vaccination = df_vaccination.fillna(0)

    # Don't pass file. Just pass the path, or otherwise unnecessary newlines are added.
    df_pandemic_bef_vacc.to_csv(PANDEMIC_BEF_VACC_PATH, index=False)
    df_pandemic_aft_vacc.to_csv(PANDEMIC_AFT_VACC_PATH, index=False)
    df_vaccination.to_csv(VACC_SLICE_PATH, index=False)

def split_data_by_country(df: DataFrame, store_path: str):
    group_data =  df.groupby('country')
    for name, group in group_data:
        group = group.drop(labels='country',axis=1)
        group.to_csv(store_path + '/' + name + '.csv', index=False)

def generate_pandemic_bef_by_country():
    file_pandemic_bef = open(PANDEMIC_BEF_VACC_PATH, 'r', encoding='utf-8')
    df_pandemic_bef = pd.read_csv(file_pandemic_bef)
    store_path = CACHE_DATA_PATH + '/pandemic_before'
    create_dir_not_exists(store_path)
    split_data_by_country(df_pandemic_bef, store_path)

def generate_pandemic_aft_by_country():
    file_pandemic_aft = open(PANDEMIC_AFT_VACC_PATH, 'r', encoding='utf-8')
    df_pandemic_aft = pd.read_csv(file_pandemic_aft)
    store_path = CACHE_DATA_PATH + '/pandemic_after'
    create_dir_not_exists(store_path)
    split_data_by_country(df_pandemic_aft, store_path)

def generate_pandemic_by_country():
    generate_pandemic_bef_by_country()
    generate_pandemic_aft_by_country()

def generate_all_data(pandemic_data_type: str = 'cumulative', augmentation: bool = False):
    generate_data(pandemic_data_type, augmentation)
    generate_pandemic_by_country()

def get_slice_vacc_sum_by_types()->pd.DataFrame:
    file_vacc_slice = open(VACC_SLICE_PATH, 'r', encoding='utf-8')
    df_vaccination = pd.read_csv(file_vacc_slice)
    return df_vaccination.groupby('vaccine')['total_vaccinations'].sum()