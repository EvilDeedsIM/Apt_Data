import time
import datetime
import pandas as pd

date_now = f'{datetime.datetime.now().date()}'

full_df = pd.DataFrame()
full_df['date'] = date_now

path = f'ss/All/csv/{date_now}.csv'
full_df.to_csv(path, index=False)
