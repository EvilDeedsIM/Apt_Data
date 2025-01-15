import asyncio
import aiohttp
import bs4
import pandas as pd
import time
import datetime

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

# Функция для парсинга одной страницы
async def fetch_page(session, page_num):
    full_url = f'{url}page{page_num}.html'
    async with session.get(full_url) as response:
        page = await response.text()
        soup = bs4.BeautifulSoup(page, 'lxml')
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

# Основная функция для запуска асинхронных запросов
async def main():
    async with aiohttp.ClientSession() as session:
        page_num = 1
        full_df = pd.DataFrame()
        while True:
            print(page_num, end=' ', flush=True)
            table = await fetch_page(session, page_num)
            if table is None:
                break
            full_df = pd.concat([full_df, table], ignore_index=True)
            page_num += 1

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

# Замер времени
start_time = time.time()

# Запуск асинхронных задач
asyncio.run(main())

# Замер времени после выполнения
end_time = time.time()
execution_time = end_time - start_time
print(f"Script execution time: {execution_time:.2f} seconds")
