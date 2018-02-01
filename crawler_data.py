import time

from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

from database import Base, engine, session
from database import *

from config import URL

from selenium.webdriver.common.by import By
from lxml import etree, html
from lxml.cssselect import CSSSelector

import re


def find_by_xpath(element_source,xpath_expression):
	root = html.fromstring(element_source)
	return root.xpath(xpath_expression)


def get_articles(soup):
	
	resultados = soup.findAll("div",{"ng-repeat": "td in resultado.tesesDissertacoes"})

	articles = []

	for div in resultados:

		campos =[]

		for tag in div.findAll("div", {"class": "col-md-11 ng-binding"}):
			campos = tag.text.split('\n\t\t\t')


		articles.append(campos)

		print ('Obtendo %s' %campos[2])
		#break

	#for a in articles:
		#print (a[1])
		#print (a[5])

	return  articles


def craw():

	display = Display(visible=0, size=(800, 600))
	display.start()
	driver = webdriver.Chrome()
	driver.get(URL)

	#print (driver.title)

	form = driver.find_element(By.XPATH, '//INPUT[@type="text"]')
	form.send_keys('"chuva intensa"')
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
		nxt = driver.find_element(By.XPATH, '//A[@href=""][text()="%s"]' %p)
		nxt.click()

		soup = BeautifulSoup(driver.page_source, 'html.parser')

		time.sleep(5) 

		articles = articles + get_articles(soup)

	print(u'Trabalhos capturados %s' %str(len(articles)))
	
	#articles = get_articles(soup)
	#print(soup.prettify())

	#links = soup.findAll("a", {"class": "ng-scope"})
	#
	#for a in links:
	#   print (a['href'])

	driver.close()


if __name__ == "__main__":
	craw()  
