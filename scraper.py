import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import os
from datetime import datetime


def scraper():
    url ='https://www.submarino.com.br/busca/s20-fe?c_legionRegion=310003&c_macroRegion=MG_INTERIOR&c_mesoRegion=3101&content=s20%20fe&filter=%7B%22id%22%3A%22wit%22%2C%22value%22%3A%22Smartphone%22%2C%22fixed%22%3Afalse%7D&oneDayDelivery=true&sortBy=relevance&source=nanook&testab=searchTestAB%3Dnew&limit=24&offset=0'

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

    site = requests.get(url,headers =headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    num_found = soup.find('span',class_='full-grid__TotalText-sc-fvrmdp-2 ENHXc').get_text().strip()
    index = num_found.find(' ')
    num_founded = num_found[0:index]
    num_found_int = int(num_founded)
    print(num_found + " encontrados hoje! ")

    i = 0
    while(i < num_found_int ):
        url_page = f'https://www.submarino.com.br/busca/s20-fe?c_legionRegion=310003&c_macroRegion=MG_INTERIOR&c_mesoRegion=3101&content=s20%20fe&filter=%7B%22id%22%3A%22wit%22%2C%22value%22%3A%22Smartphone%22%2C%22fixed%22%3Afalse%7D&oneDayDelivery=true&sortBy=relevance&source=nanook&testab=searchTestAB%3Dnew&limit=24&offset={i}'

        site = requests.get(url_page,headers =headers)
        soup = BeautifulSoup(site.content, 'html.parser')
        cells = soup.find_all('div', class_ ='src__Wrapper-sc-r60f4z-0 beBFQn')
        

    
        if not os.path.isfile('price_S20.csv'):
            with open ('price_S20.csv','a', newline='', encoding='UTF-8') as create:
                cabeçalho = "name" + ';' + "num_price" +';' +  "price_installments" + ';'+ "date" +';' + "site" +'\n'
                create.write(cabeçalho)



        with open ('price_S20.csv','a', newline='', encoding='UTF-8') as f:

            for cell in cells:
                
                name = cell.find('h3',class_='src__Name-sc-r60f4z-1 itcnES').get_text().strip()
                try:   
                    price = cell.find('span', class_='src__Text-sc-154pg0p-0 src__PromotionalPrice-sc-r60f4z-6 pXfdS').get_text().strip()
                    num_price = price[3:-3]
                except:
                    num_price = '0'
                try:
                    price_installments = cell.find('span',class_='src__PaymentDetails-sc-r60f4z-2 src__Installment-sc-r60f4z-3 kfHRvB').get_text().strip()
                except:
                    price_installments ='0'
                date_time = datetime.now()
                date = date_time.strftime('%d/%m/%Y')
                site = "submarino"
                
                line = name + ';' + num_price +';' +  price_installments + ';'+ date + ';' + site +'\n'
                f.write(line)
        
        i = i + 24


    table = pd.read_csv('price_S20.csv', sep = ';')

    min_price_line = table['num_price'].idxmin()
    today_date = datetime.now()
    today = date_time.strftime('%d/%m/%Y')
    min_data = table.loc[min_price_line, 'date']
    min_price = table.loc[min_price_line, 'num_price']
    if(min_data == today):
        print("Hoje é o melhor dia para compra!")

        print("O menor valor hoje é: ")
        print(min_price)
    else:
        print("Hoje não é o melhor dia para compra, o melho dia foi em: " + min_data)

print("------------   Iniciando scraper   -------------------")
buttom = int(input("Digite 1 para analizar se é o melhor momento para a compra:"))
if(buttom == 1):
    scraper()
else:
    print("Você escolheu não iniciar a busca, saindo.")

