import requests, datetime
import bs4
import pandas as pd
import time
import concurrent.futures

url = 'https://www.ss.lv/ru/real-estate/flats/riga/all/sell/'
date_now = f'{datetime.datetime.now().date()}'
symbol = '€'

cols = ['Date',
        'District',
        'Street',
        'Rooms',
        'm2',
        'Floor',
        'Serie',
        'Price']

# Собираем страницы параллельно
def fetch_page(page_num):
    full_url = f'{url}page{page_num}.html'
    page = requests.get(full_url)
    soup = bs4.BeautifulSoup(page.text, 'lxml')
    for b in soup.find_all('b'):
        b.replaceWithChildren()
    
    btn = soup.find_all('button', {'class': 'navia'})[0]
    btn_text = btn.get_text()
    if btn_text == '1' and page_num != 1:
        return None

    df = pd.read_html(full_url, header=0, flavor='bs4', index_col=False)
    table = df[4]
    table = table.iloc[:, 3:]
    return table

# Замер времени
start_time = time.time()

# Запуск параллельных запросов
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(fetch_page, range(1, 100)))  # Диапазон страниц

# Собираем все данные
full_df = pd.concat([table for table in results if table is not None], ignore_index=True)

# Обработка данных
district_street_cols = full_df.iloc[:, 0].str.split(' ', n=1, expand=True)
full_df.drop(full_df.columns[0], axis=1, inplace=True)
full_df.insert(0, 0, district_street_cols[0])
full_df.insert(1, 1, district_street_cols[1])
full_df['date'] = date_now
date_col = full_df.pop('date')
full_df.insert(0, 'date', date_col)
full_df.columns = cols
full_df['Price'] = full_df['Price'].str.split(' ', n=1, expand=True)[0].str.replace(',', '').astype(int)

print(full_df)

# Сохранение в CSV
path = f'./csv/{date_now}.csv'
full_df.to_csv(path, index=False)

# Замер времени после выполнения
end_time = time.time()
execution_time = end_time - start_time
print(f"Script execution time: {execution_time:.2f} seconds")
