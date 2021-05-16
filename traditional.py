import pandas as pd
from fbprophet import Prophet

filename = 'USA.csv'

file_pandemic = open('./covid_data/cache/pandemic_before/'+filename, 'r', encoding='utf-8')
df = pd.read_csv(file_pandemic)