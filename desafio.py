import requests
import pandas as pd 
from lxml import html
import os 
import sys
import json
# Para identificar o repositório em que o arquivo do programa se encontra e salvando os arquivos nos formatos CSV e JSON
repository = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')


# Classe do Crawler cotendo os metodos a serem usados
class Crawler_table(): 


# Começa extração das informações da pagina alvo 1 e retorna em formato de Data Frame     
    def extractionPaginaAlvo_1(self):

        df = pd.DataFrame(columns=['Storage','CPU', 'Memory','Bandwidth', 'Price'])
        response = requests.get('https://www.vultr.com/products/cloud-compute/#pricing')
        content_web = html.fromstring(response.content)
        
        if response.status_code == 200:
# Seleciona qual tabela que o usuário deseja via xpath
            div_table = '//div[@class = "pt__body js-body"]'
            table = content_web.xpath(div_table)[0]
# Seleciona qual linha que o usuário deseja  via xpath
            div_rows = table.xpath('./div')
                
            for link in range(0,len(div_rows)):
# Inicio da extração dos textos da tabela desejada e sendo convertidos em Data Frame
                data = []
                div_content = div_rows[link].xpath('./div[@class = "pt__row-content"]')[0]

                divs_texto = div_content.xpath('./div')
                
                data.append(divs_texto[1].text_content().strip())
                data.append(divs_texto[2].text_content().strip())
                data.append(divs_texto[3].text_content().strip().split('Ram')[0])
                data.append(divs_texto[4].text_content().strip().split('Bandwidth')[0])
                data.append(divs_texto[5].text_content().strip().split('\n')[0])
                
                df.loc[link] = data
        else:
            print("Infelizmente não foi possível extrair os dados, verifique os seletores se estão corretos")
        return df    
    
# Começa extração das informações da pagina alvo 2 e retorna em formato de Data Frame     
    def extractionPaginaAlvo_2(self):

        df = pd.DataFrame(columns=['Memory','vCPUs', 'SSD Disk','Transfer', '$/MO'])
        response = requests.get('https://www.digitalocean.com/pricing/')
        content_web = html.fromstring(response.content)
        
        if response.status_code == 200:
# Seleciona qual tabela que o usuário deseja via xpath
            select_table = '//ul[@class = "priceBox"]'
            table = content_web.xpath(select_table)[0]
# Seleciona qual tlinha que o usuário deseja via xpath
            rows_table = table.xpath('.//li[@class = "priceBoxItem"]')

            for link in range(0,len(rows_table)):
# Inicio da extração dos textos da tabela desejada e sendo convertidos em Data Frame
                content_table = rows_table[link].xpath('.//a/div/ul/li')
                money_table = rows_table[link].xpath('.//a/div/div')
                rows_table = table.xpath('.//li[@class = "priceBoxItem"]')
                #print(money_table[0].text_content())
                data = []
                data.append(content_table[0].text_content().split("/")[0])
                data.append(content_table[0].text_content().split("/")[1])
                data.append(content_table[1].text_content().split("SSD")[0])
                data.append(content_table[2].text_content().split("transfer")[0])
                data.append(money_table[0].text_content().split("/")[0])
                df.loc[link] = data
        else:
            print("Infelizmente não foi possível extrair os dados, verifique os seletores se estão corretos")
        return df


# Metodo para salvar o arquivo no formato JSON. 
    def Save_Json(self,df):
        print("Favor colocar o nome do arquivo, sem .json")
        name = input()
        dic = df.to_dict()
        with open(repository+'/'+name+'.json', 'w') as data:
            json.dump(dic, data,indent=4)
        print("##########################################")
        print("Arquivo salvo no formato JSON com sucesso")
        print("##########################################")
# Metodo para salvar o arquivo no formato CSV. 
    def Save_CSV(self,df):
        print("Favor colocar o nome do arquivo, sem .csv")
        name = input()
        df.to_csv(repository+'/'+name+'.csv',index=False)
        print("#########################################")
        print("Arquivo salvo no formato CSV com sucesso")
        print("#########################################")


# Metodo para printar na tela o conteudo extraido. 
    def Print_info(self,df):
        print(df,"\n")
        
          

# Metodo para o usuario selecionar qual opcao que ele deseja
    def Menu(self):
        df_pagina1 = self.extractionPaginaAlvo_1()
        df_pagina2 = self.extractionPaginaAlvo_2()
        if not df_pagina1.empty and not df_pagina2.empty:
            action = -1
            while action != 0: 
                print("Selecione qual opção deseja executar:")
                action = input("1 para imprimir os dados\n2 para Salvar em CSV\n3 para Salvar em json\n0 para sair\nDigite sua opção: ")
                if action != "0":
                    pagina = input("Qual site deseja fazer WebScrapping?\n1 para a página alvo Vultr\n2 para a página alvo Digital Ocean: ")
                
                if action == "1" and pagina == "1":
                    self.Print_info(df_pagina1)
                elif action == "2" and pagina == "1":
                    self.Save_CSV(df_pagina1)
                elif action == "3" and pagina == "1":
                    self.Save_Json(df_pagina1)
                elif action == "1" and pagina == "2":
                    self.Print_info(df_pagina2)
                elif action == "2" and pagina == "2":
                    self.Save_CSV(df_pagina2)
                elif action == "3" and pagina == "2":
                    self.Save_Json(df_pagina2)                 
                elif action == "0":
                    return None
                else:
                    print("Não existe essa opção, favor colocar as opções desejada novamente\n")
        else:
            print("Infelizmente não foi possível extrair os dados, verifique os seletores se estão corretos")
        

if __name__ == "__main__":
# Cria-se uma instancia da classe e executa as acoes que o usuario deseja
    Extract_Data = Crawler_table()
    Extract_Data.Menu()