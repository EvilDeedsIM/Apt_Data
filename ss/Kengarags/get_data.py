import bs4, requests, datetime, csv

url = 'https://www.ss.lv/ru/real-estate/flats/riga/kengarags/sell/'
date_now = f'{datetime.datetime.now().date()}'
symbol = '€'

fields = ['Date', 'Street', 'Rooms', 'm2', 'Floor', 'Serie', f'{symbol}/m2', 'Price']
apartments = []

page_num = 1

while True:
    page = requests.get(url + f'page{page_num}.html')
    soup = bs4.BeautifulSoup(page.text, 'lxml')

    btn = soup.find_all('button', {'class': 'navia'})[0]
    btn_text = btn.get_text()
    if btn_text == '1' and page_num != 1:
        break

    form = soup.find_all('form', {'id': 'filter_frm'})[0]
    table = form.find_all('table')[2]
    rows = table.find_all('tr')[1:-1]

    for row in rows:
        cols = row.find_all('td')[3:]
        row_arr = []
        row_arr.append(date_now)
        for col in cols:
            txt = col.get_text()
            
            if symbol in txt:
                txt = txt.replace(symbol, '').strip()
            row_arr.append(txt)
        apartments.append(row_arr)

    page_num += 1

print(len(apartments))


path = f'./csv/{date_now}.csv'
with open(path, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fields)
    writer.writerows(apartments)

