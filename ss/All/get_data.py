import bs4, requests, datetime, csv

url = 'https://www.ss.lv/ru/real-estate/flats/riga/all/sell/'
date_now = f'{datetime.datetime.now().date()}'
symbol = '€'

fields = ['Date',
        'District',
        'Street',
        'Rooms',
        'm2',
        'Floor',
        'Serie',
        'Price',
        ]
apartments = []

# districts = ['centre', 
#             'agenskalns',
#             'aplokciems',
#             'bergi',
#             'bierini',
#             'bolderaya',
#             'breksi',
#             'vecaki',
#             'vecdaugava',
#             'vecmilgravis',
#             'vecriga',
#             'voleri',
#             'grizinkalns',
#             'darzciems',
#             'daugavgriva',
#             'dzeguzhkalns',
#             'dreilini',
#             'zakusala',
#             'ziepniekkalns',
#             'zolitude',
#             'ilguciems',
#             'imanta',
#             'katlakalns',
#             'kengarags',
#             'kipsala',
#             'kliversala',
#             'kundzinsala',
#             'mangali',
#             'mangalsala',
#             'mezhapark',
#             'mezhciems',
#             'plyavnieki',
#             'purvciems',
#             'krasta-st-area',
#             'maskavas-priekshpilseta',
#             'sarkandaugava',
#             'teika',
#             'tornjakalns',
#             'chiekurkalns',
#             'shampeteris-pleskodale',
#             'shkirotava',
#             'yugla',
#             'jaunciems',
#             ]

page_num = 1


def add_to_array(array, data):
    array.append(data)

while True:
    page = requests.get(url + f'page{page_num}.html')
    soup = bs4.BeautifulSoup(page.text, 'lxml')

    for b in soup.find_all('b'):
        b.replaceWithChildren()

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
            col_data_arr = [x for x in col.contents if getattr(x, 'name', None) != 'br']
            if len(col_data_arr) > 1:
                for c in col_data_arr:
                    if symbol in c:
                        c = c.replace(symbol, '').strip()
                    if len(c) > 0:
                        c = c.replace(',', '')
                        add_to_array(row_arr, c)
            else:
                c = col_data_arr[0]
                if symbol in c:
                        c = c.replace(symbol, '').strip()
                        c = c.replace(',', '')
                add_to_array(row_arr, c)

        apartments.append(row_arr)
        # print(row_arr)

    page_num += 1
    # break

print(len(apartments))


path = f'./csv/{date_now}.csv'
with open(path, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fields)
    writer.writerows(apartments)

# comment
