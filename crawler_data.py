from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#from selenium.webdriver.common import WebDriverException

from bs4 import BeautifulSoup

from lxml import html

import time

import re

import argparse

from utils import datestring_to_date, limpa_unicode, save_articles, export_to_csv

from config import URL

def find_by_xpath(element_source,xpath_expression):
	root = html.fromstring(element_source)
	return root.xpath(xpath_expression)

def get_articles(soup):
	
	resultados = soup.findAll("div",{"ng-repeat": "td in resultado.tesesDissertacoes"})

	articles = []

	for div in resultados:

		campos ={}

		dados =  div.find("div", {"class": "col-md-11 ng-binding"})
		aux = dados.text.split('\n\t\t\t')

		campos['autor'] = aux[1]
		campos['titulo'] = aux[2]
		campos['data'] = datestring_to_date(aux[3])
		campos['tamanho'] = aux[4]
		campos['tipo'] = aux[5]
		campos['area'] = aux[6]
		campos['instituicao'] = aux[7]
		campos['local'] = aux[8]

		a = div.find("a", {"class": "ng-scope"})
		if a:
			campos['link'] = a['href']
		else:
			campos['link'] = ''

		articles.append(campos)

	return  articles

def get_info_link(articles, driver):

	for a in articles:
		if a['link']:
			driver.get(a['link'])
			soup = BeautifulSoup(driver.page_source, 'html.parser')
			resumo = soup.find("span",{"id": "resumo"})
			palavras = soup.find("span",{"id": "palavras"})
			abstract = soup.find("span",{"id": "abstract"})

			if resumo:
				a['resumo'] = limpa_unicode(resumo.text)
			if palavras:
				a['pavavras_chaves'] = palavras.text			
			if abstract:
				a['abstract'] = limpa_unicode(abstract.text)

			time.sleep(1) 

	return articles

def craw(keyword, all_info):

	display = Display(visible=0, size=(800, 600))
	display.start()
	driver = webdriver.Chrome()

	#try:
	driver.get(URL)

	form = driver.find_element(By.XPATH, '//INPUT[@type="text"]')
	form.send_keys(str(keyword))
	form.click()
	form.send_keys(Keys.ENTER)

	time.sleep(1) 

	soup = BeautifulSoup(driver.page_source, 'html.parser')

	qty = soup.find("h3",{"class": "mb0 ng-binding"})
	num = re.findall('\d+', qty.text)

	qty = int(num[0])
	pag = 20 # paginacao

	print(u'Buscando %s resultados... (cada página com %s resultados)' %(str(qty),str(pag)))

	articles = []
	
	for p in range(1,(int(qty/pag) +2)):
		print(u'Buscando página %s ...' %p)     

		if p ==1:
			xpath = '//A[@href=""][text()="1"][text()="1"]'
		else:
			xpath ='//A[@href=""][text()="%s"]' %p

		#print (xpath)

		nxt = driver.find_element(By.XPATH, xpath)
		nxt.click()

		time.sleep(5) 

		soup = BeautifulSoup(driver.page_source, 'html.parser')

		r = get_articles(soup)
		print ('Primeiro artigo da pagina...%s' %r[0]['titulo'])
		articles = articles + r

	print(u'Trabalhos capturados %s' %str(len(articles)))  

	if all_info:
		print(u'Obtendo informações de cada link do artigo ...')  
		get_info_link(articles, driver)

	#except WebDriverException:
	#	print ('Erro no crawler. Tente novamente')
	#	return None

	driver.close()

	return articles

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("keyword", help=u"Informe a palavra chave para pesquisar. Se for duas ou mais palavras, \
						 use aspas para restringir os resultados")
	parser.add_argument("all_info", help=u"Pegar informações complementares do artigo como resumo, palavras chaves \
						 e abstract.", type=bool, default=False)
	args = parser.parse_args()

	keyword =  '"{0}"'.format(args.keyword)

	articles = craw(keyword, args.all_info) 

	if articles:
		save_articles(articles)
		export_to_csv() 
