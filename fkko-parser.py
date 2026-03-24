import requests
from bs4 import BeautifulSoup
import polars as pl


df = pl.DataFrame(
    data={ 'code': [], 'name': [], 'link': [] },
    schema={ 'code': pl.String, 'name': pl.String, 'link': pl.String }
)
for n in range(1, 455+1):
    url = f'https://rpn.gov.ru/fkko/nav-more-fkko/page-{n}/'
    rows = BeautifulSoup(requests.get(url).text, 'lxml').find_all('div', class_='registryCard__itemTableRow')
    for row in rows[1:]:
        code = row.find('div', class_='registryCard__itemTableCol _code').text.strip()
        name = row.find('a', class_='fkko-item').text.strip()
        link = row.find('a', class_='fkko-item').attrs['href'].strip()
        newrow = pl.DataFrame({'code': code, 'name': name, 'link': link})
        df.extend(newrow)
    print(f'DEBUG: Done with page #{n}')
    print(df)

df.write_csv('fkko.csv', separator='\t', include_header=True)