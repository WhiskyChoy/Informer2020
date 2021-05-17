import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt
from covid_data import country_list, feature_list, PANDAMIC_FORCAST_DIR_PATH, VACCINATION_WITH_PANDEMIC, DATA_FOR_LSP_PATH


def get_calculated_data(country: str, col_name: str):
    filename = country + '.csv'

    file_pandemic_bef_vacc = open(
        './covid_data/cache/pandemic_before/'+filename, 'r', encoding='utf-8')
    df = pd.read_csv(file_pandemic_bef_vacc)

    df['date'] = df['date'].apply(pd.to_datetime)

    df.columns = df.columns.map(lambda x: "ds" if x == 'date' else (
        "y" if x == col_name else x))

    file_pandemic_aft_vacc = open(
        './covid_data/cache/pandemic_after/'+filename, 'r', encoding='utf-8')

    df2 = pd.read_csv(file_pandemic_aft_vacc)

    df2['date'] = df2['date'].apply(pd.to_datetime)

    df2.columns = df2.columns.map(lambda x: "ds" if x == 'date' else (
        "y" if x == col_name else x))

    last_date_bef_vacc = df['ds'].max()
    last_date_aft_vacc = df2['ds'].max()

    periods = (last_date_aft_vacc - last_date_bef_vacc).days

    prophet = Prophet()
    prophet.fit(df)

    future = prophet.make_future_dataframe(
        periods=periods, include_history=False)
    forecast = prophet.predict(future)
    df3 = forecast[['ds', 'yhat']]
    df3 = df3[df3['ds'] > last_date_bef_vacc]

    return df, df2, df3


def draw_curve(country: str, col_name: str, description: str):
    df, df2, df3 = get_calculated_data(country, col_name)

    plt.figure(figsize=(12, 6))
    plt.plot('ds', 'y', data=df, color='black',
             label=f'{description} Before Vaccination')
    plt.plot('ds', 'y', data=df2, color='blue',
             label=f'Actual {description} After Vaccination')
    plt.plot('ds', 'yhat', data=df3, color='orange',
             label=f'Forecasted {description} After Vaccination')
    plt.legend()
    plt.show()


def draw_forecast():
    for country in country_list:
        draw_curve(country, 'cumulative_total_deaths',
                   'Cumulative Total Deaths')
        draw_curve(country, 'active_cases', 'Active Cases')
        draw_curve(country, 'cumulative_total_cases', 'Cumulative Total Cases')
        draw_curve(country, 'daily_new_cases', 'Daily New Cases')
        draw_curve(country, 'daily_new_deaths', 'Daily New Deaths')


def generate_forecast_data():

    for country in country_list:
        for idx, feature in enumerate(feature_list):
            _, _, df = get_calculated_data(country, feature)
            df.columns = df.columns.map(
                lambda x: "date" if x == 'ds' else (feature if x == 'yhat' else x))
            df_merge = df if idx == 0 else pd.merge(
                left=df_merge, right=df, left_on='date', right_on='date')
        df_merge.to_csv(PANDAMIC_FORCAST_DIR_PATH+country+'.csv', index=False)

def round_forecast():
    for country in country_list:

        df_file = open(
            PANDAMIC_FORCAST_DIR_PATH+country+'.csv', 'r', encoding='utf-8')
        df = pd.read_csv(df_file)
        for feature in feature_list:
            df[feature] = df[feature].map(lambda x: round(float(x)))
        df.to_csv(PANDAMIC_FORCAST_DIR_PATH+country+'.csv', index=False)

def set_date():
    for country in country_list:

            vacc_with_pan_file = open(
                VACCINATION_WITH_PANDEMIC+country+'.csv', 'r', encoding='utf-8')
            df_vacc_with_pan = pd.read_csv(vacc_with_pan_file)
            df_vacc_with_pan['date'] = df_vacc_with_pan['date'].apply(pd.to_datetime)
            df_vacc_with_pan.to_csv(VACCINATION_WITH_PANDEMIC+country+'.csv', index=False)


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

# set_date()
# generate_lsp_data()
