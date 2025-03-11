import time
import datetime

date_now = f'{datetime.datetime.now().date()}'

path = f'ss/All/csv/{date_now}.csv'
date_now.to_csv(path, index=False)
