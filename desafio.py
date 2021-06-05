import requests
import pandas as pd 
from lxml import html

class Crawler:

    df = pd.DataFrame(columns=['Storage','CPU', 'Memory','Bandwidth', 'Price'])
    response = requests.get('https://www.vultr.com/products/cloud-compute/#pricing')
    text = html.fromstring(response.content)

    if response.status_code == 200:
        try:
            div_table = '//div[@class = "pt__body js-body"]'
            table = text.xpath(div_table)[0]
            div_rows = table.xpath('./div')

            for link in range(0,len(div_rows)):
                data = []
                div_content = div_rows[link].xpath('./div[@class = "pt__row-content"]')[0]

                divs_texto = div_content.xpath('./div')

                data.append(divs_texto[1].text_content().strip())
                data.append(divs_texto[2].text_content().strip())
                data.append(divs_texto[3].text_content().strip().split('Ram')[0])
                data.append(divs_texto[4].text_content().strip().split('Bandwidth')[0])
                data.append(divs_texto[5].text_content().strip().split('\n')[0])

                df.loc[link] = data

        except:
            pass

        print(df)




if __name__ == "__dev__":
    teste = Crawler()