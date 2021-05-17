from utils.io import create_dir_not_exists
import pandas as pd

country_list = ['USA', 'Chile', 'France', 'Germany', 'Italy']
feature_list = ['cumulative_total_deaths', 'active_cases',
                'cumulative_total_cases', 'daily_new_cases', 'daily_new_deaths']
vaccine_list = ['Pfizer/BioNTech','Moderna','Oxford/AstraZeneca','Sinovac','Johnson&Johnson']
PANDAMIC_FORCAST_DIR_PATH = './covid_data/cache/pandemic_forecast/'
VACCINATION_WITH_PANDEMIC = './covid_data/cache/vacc_with_pan/'
DATA_FOR_LSP_PATH = './covid_data/cache/for_lsp/'
LSP_PROBLEMS_PATH = './covid_data/cache/lsp_problems/'

create_dir_not_exists(PANDAMIC_FORCAST_DIR_PATH,
                      VACCINATION_WITH_PANDEMIC, DATA_FOR_LSP_PATH, LSP_PROBLEMS_PATH)