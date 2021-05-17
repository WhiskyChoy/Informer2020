from utils.io import DatetimeConverter
from scipy.linalg import lstsq
from scipy.special import softmax
import pandas as pd
from covid_data import country_list, feature_list, VACCINATION_WITH_PANDEMIC, PANDAMIC_FORCAST_DIR_PATH, DATA_FOR_LSP_PATH, vaccine_list, LSP_PROBLEMS_PATH
from datetime import datetime, timedelta
import numpy as np
np.set_printoptions(suppress=True)

start_date = datetime(2021, 1, 13)
end_date = datetime(2021, 4, 30)
date_list = [start_date + timedelta(days=x) for x in range(0, (end_date-start_date).days)]

def generate_lsp_data():
    for country in country_list:

        vacc_with_pan_file = open(
            VACCINATION_WITH_PANDEMIC+country+'.csv', 'r', encoding='utf-8')
        df_vacc_with_pan = pd.read_csv(vacc_with_pan_file)
        df_vacc_with_pan.columns = df_vacc_with_pan.columns.map(
            lambda x: x+'_real' if x in feature_list else x)

        pan_forcast_file = open(
            PANDAMIC_FORCAST_DIR_PATH+country+'.csv', 'r', encoding='utf-8')
        df_pan_forcast = pd.read_csv(pan_forcast_file)
        df_pan_forcast.columns = df_pan_forcast.columns.map(
            lambda x: x+'_forecast' if x in feature_list else x)

        df_merge = pd.merge(left=df_vacc_with_pan, right=df_pan_forcast, left_on='date', right_on='date')
        df_merge.to_csv(DATA_FOR_LSP_PATH+country+'.csv', index=False)

def get_lsp_data(country: str)->pd.DataFrame:
    lsp_file = open(
    DATA_FOR_LSP_PATH+country+'.csv', 'r', encoding='utf-8')
    df_lsp = pd.read_csv(lsp_file)
    df_lsp['date'] = df_lsp['date'].apply(pd.to_datetime)
    return df_lsp

def save_lsp_data(df: pd.DataFrame, country: str):
    df.to_csv(DATA_FOR_LSP_PATH+country+'.csv', index=False)


def align_lsp_data_date():
    for idx, country in enumerate(country_list):
        df = get_lsp_data(country)
        df_date = df['date']
        max_start = df_date.min() if idx == 0 else max(max_start, df_date.min())
        min_end = df_date.max() if idx == 0 else min(min_end, df_date.max())
    for country in country_list:
        df = get_lsp_data(country)
        df = df[(df['date']> max_start) & (df['date'] < min_end)]
        save_lsp_data(df, country)

def generate_lsp_problems(target_list: list = ['cumulative_total_cases', 'cumulative_total_deaths']):
    converter = DatetimeConverter()
    dfs = []
    target_list_delta = list(map(lambda x: x+'_delta', target_list))
    final_target_list = ['date'] + target_list_delta + vaccine_list
    for country in country_list:
        df = get_lsp_data(country)
        for feature in target_list:
            df[feature+'_forecast'] -= df[feature+'_real']
            df.columns = df.columns.map(lambda x: '_'.join(x.split('_')[:-1])+'_delta' if x == feature+'_forecast' else x)
        df = df[final_target_list]
        dfs.append(df)
    for idx, date in enumerate(date_list):
        for jdx, df in enumerate(dfs):
            # Get row
            df_row = df.iloc[[idx]]
            df_result =  df_row if jdx == 0 else pd.concat([df_result, df_row], ignore_index=True)
        df_result.to_csv(LSP_PROBLEMS_PATH + converter.date2str(date) + '.csv', index=False)
    pass

def get_one_lsp_problem(date: datetime):
    converter = DatetimeConverter()
    date_str = converter.date2str(date)
    lsp_problem_file = open(
    LSP_PROBLEMS_PATH+date_str+'.csv', 'r', encoding='utf-8')
    df_lsp_problem = pd.read_csv(lsp_problem_file)
    df_lsp_problem['date'] = df_lsp_problem['date'].apply(pd.to_datetime)
    return df_lsp_problem

def solve_lsp(date: datetime, target_list: list = ['cumulative_total_cases', 'cumulative_total_deaths'], target_vaccine_list: list = vaccine_list):
    target_list_delta = list(map(lambda x: x+'_delta', target_list))
    df_lsp_problem = get_one_lsp_problem(date)
    # Define A
    A = df_lsp_problem[target_vaccine_list]
    # Define B
    B = df_lsp_problem[target_list_delta]
    # Solve LSP
    X, _, _, _ = lstsq(A, B)
    X_original = np.round(X, 2)
    X_softmax = np.round(softmax(X, axis=0),2)
    print(X_original)
    print(X_softmax)
    return X_original, X_softmax

solve_lsp(datetime(2021, 4, 13))