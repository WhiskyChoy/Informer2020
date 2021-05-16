from datetime import timedelta
from utils.io import FreqType, DatetimeConverter, get_freq_rate
from pandas import DataFrame
from itertools import islice
from math import floor
from tqdm import tqdm
from random import random

def augment_time(df: DataFrame, source_formatter: str, target_formatter: str, source_freq: FreqType, target_freq: FreqType, total_cols: list=None, item_cols: list=None, date_col: str = 'date', aug_method_type: str = 'linear'):
    if not (total_cols is None and item_cols is None):
        if aug_method_type == 'linear':
            str2date = DatetimeConverter(source_formatter).str2date
            date2str = DatetimeConverter(target_formatter).date2str
            freq_rate = get_freq_rate(source_freq, target_freq)
            seconds_num = get_freq_rate(source_freq+1, FreqType.Second)
            new_df = DataFrame(columns=df.columns)
            current_row = df.iloc[0]
            tqdm_bar = tqdm(total=df.shape[0])
            for _, next_row in islice(df.iterrows(), 1, None):
                current_date = current_row[[date_col]] # Need [] to wrap date_col
                current_totals = None
                next_totals = None
                totals_gap = None
                if item_cols is not None:
                    current_items = current_row[item_cols]
                    avg = current_items // freq_rate
                    left = current_items % freq_rate
                if total_cols is not None:
                    current_totals = current_row[total_cols]
                    next_totals = next_row[total_cols]
                    totals_gap = next_totals - current_totals
                for i in range(freq_rate):
                    new_row = current_row.copy()
                    new_row[[date_col]] = (current_date.map(str2date) + i * timedelta(seconds=seconds_num)).map(date2str)
                    if total_cols is not None:
                        new_row[total_cols] = (current_totals + i * totals_gap / freq_rate).map(floor)
                    if item_cols is not None:
                        new_row[item_cols] = avg if i != freq_rate - 1 else avg + left
                    new_df = new_df.append(new_row,  ignore_index=True)
                current_row = next_row
                tqdm_bar.update(1)
            tqdm_bar.close()
            return new_df

def augment_time_acc(df: DataFrame, source_formatter: str, target_formatter: str, source_freq: FreqType, target_freq: FreqType, total_cols: list=None, date_col: str = 'date', aug_method_type: str = 'linear'):
    if total_cols is not None:
        if aug_method_type == 'linear':
            str2date = DatetimeConverter(source_formatter).str2date
            date2str = DatetimeConverter(target_formatter).date2str
            freq_rate = get_freq_rate(source_freq, target_freq)
            seconds_num = get_freq_rate(source_freq+1, FreqType.Second)
            new_df = DataFrame(columns=df.columns)
            current_row = df.iloc[0]
            tqdm_bar = tqdm(total=df.shape[0]-1)
            for _, next_row in islice(df.iterrows(), 1, None):
                current_date = current_row[[date_col]] # Need [] to wrap date_col
                current_totals = current_row[total_cols]
                next_totals = next_row[total_cols]
                totals_gap = next_totals - current_totals
                for i in range(freq_rate):
                    new_row = current_row.copy()
                    new_row[[date_col]] = (current_date.map(str2date) + i * timedelta(seconds=seconds_num)).map(date2str)
                    new_row[total_cols] = (current_totals + i * totals_gap / freq_rate).map(floor)
                    new_df = new_df.append(new_row,  ignore_index=True)
                current_row = next_row
                tqdm_bar.update(1)
            tqdm_bar.close()
            return new_df

def augment_time_new(df: DataFrame, source_formatter: str, target_formatter: str, source_freq: FreqType, target_freq: FreqType, item_cols: list=None, date_col: str = 'date', aug_method_type: str = 'linear'):
    if item_cols is not None:
        if aug_method_type == 'linear':
            str2date = DatetimeConverter(source_formatter).str2date
            date2str = DatetimeConverter(target_formatter).date2str
            freq_rate = get_freq_rate(source_freq, target_freq)
            seconds_num = get_freq_rate(source_freq+1, FreqType.Second)
            new_df = DataFrame(columns=df.columns)
            tqdm_bar = tqdm(total=df.shape[0])
            for _, current_row in df.iterrows():
                current_date = current_row[[date_col]] # Need [] to wrap date_col
                current_items = current_row[item_cols]
                avg = current_items // freq_rate
                upper = avg + 1
                counter = current_items % freq_rate
                for i in range(freq_rate):
                    new_row = current_row.copy()
                    new_row[[date_col]] = (current_date.map(str2date) + i * timedelta(seconds=seconds_num)).map(date2str)
                    rand = random()
                    if rand > 0.1 and counter.all() > 0:
                        counter -= 1
                        new_row[item_cols] = upper
                    else:
                        new_row[item_cols] = avg
                    new_df = new_df.append(new_row,  ignore_index=True)
                tqdm_bar.update(1)
            tqdm_bar.close()
            return new_df

def augment_time_rigorous(df: DataFrame, source_formatter: str, target_formatter: str, source_freq: FreqType, target_freq: FreqType, item_cols: list=None, date_col: str = 'date', aug_method_type: str = 'linear'):
    if item_cols is not None:
        if aug_method_type == 'linear':
            str2date = DatetimeConverter(source_formatter).str2date
            date2str = DatetimeConverter(target_formatter).date2str
            freq_rate = get_freq_rate(source_freq, target_freq)
            seconds_num = get_freq_rate(source_freq+1, FreqType.Second)
            new_df = DataFrame(columns=df.columns)
            tqdm_bar = tqdm(total=df.shape[0])
            for _, current_row in df.iterrows():
                current_date = current_row[[date_col]] # Need [] to wrap date_col
                current_items = current_row[item_cols]
                avg = current_items // freq_rate
                upper = avg + 1
                counter = current_items % freq_rate
                for i in range(freq_rate):
                    new_row = current_row.copy()
                    new_row[[date_col]] = (current_date.map(str2date) + i * timedelta(seconds=seconds_num)).map(date2str)
                    rand = random()
                    if rand > 0.1 and counter.all() > 0:
                        counter -= 1
                        new_row[item_cols] = upper
                    elif i < freq_rate - 1:
                        new_row[item_cols] = avg
                    else:
                        new_row[item_cols] = avg + counter
                    new_df = new_df.append(new_row,  ignore_index=True)
                tqdm_bar.update(1)
            tqdm_bar.close()
            return new_df


def augment_time_new_fit_rate(df: DataFrame, source_formatter: str, target_formatter: str, source_freq: FreqType, target_freq: FreqType, item_cols: list=None, date_col: str = 'date', aug_method_type: str = 'linear'):
    if item_cols is not None:
        if aug_method_type == 'linear':
            str2date = DatetimeConverter(source_formatter).str2date
            date2str = DatetimeConverter(target_formatter).date2str
            freq_rate = get_freq_rate(source_freq, target_freq)
            seconds_num = get_freq_rate(source_freq+1, FreqType.Second)
            new_df = DataFrame(columns=df.columns)
            tqdm_bar = tqdm(total=df.shape[0])
            for _, current_row in df.iterrows():
                current_date = current_row[[date_col]] # Need [] to wrap date_col
                current_items = current_row[item_cols]
                avg = current_items // freq_rate
                upper = avg + 1
                counter = current_items % freq_rate
                rate = counter / freq_rate
                for i in range(freq_rate):
                    new_row = current_row.copy()
                    new_row[[date_col]] = (current_date.map(str2date) + i * timedelta(seconds=seconds_num)).map(date2str)
                    rand = random()
                    if rand > rate.all() and counter.all() > 0:
                        counter -= 1
                        new_row[item_cols] = upper
                    elif i < freq_rate - 1:
                        new_row[item_cols] = avg
                    else:
                        new_row[item_cols] = avg + counter
                    new_df = new_df.append(new_row,  ignore_index=True)
                tqdm_bar.update(1)
            tqdm_bar.close()
            return new_df