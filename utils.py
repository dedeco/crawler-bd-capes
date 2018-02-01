
import datetime
import time

def datestring_to_date(datestr, formatstr="%d/%m/%Y"):
    try:
        dt = time.strptime(datestr, formatstr)
    except ValueError:
        dt = None

    if dt:
        dd = datetime.date(*dt[:3])
    else:
        dd = None

    return dd

from database import Base, engine, session
from database import *

def save_articles(articles):

	print(u'Salvando os artigos no sqlite (ver config.py)...')  

	trabalhos = []

	for a in articles:
		t = Trabalho() 
		for key, value in a.items():
			setattr(t, key, value)
		trabalhos.append(t)

	session.add_all(trabalhos)
	session.commit()

import csv

def export_to_csv():

	print(u'Exportando para csv...')
	
	file = './trabalhos.csv'

	q = session.query(Trabalho)

	with open(file, 'w', encoding='latin1') as csvfile:
		outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)

		outcsv.writerow(['titulo','autor','data','tamanho','tipo', \
							'area','instituicao','local','programa','resumo',\
							'pavavras_chaves','abstract'])  

		for r in q.all():
			outcsv.writerow([r.titulo,r.autor,r.data,r.tamanho,r.tipo, \
							r.area,r.instituicao,r.local,r.programa,r.resumo,\
							r.pavavras_chaves,r.abstract])    

def limpa_unicode(astr, force_encoding=False, encoding='latin-1', encoding_method='replace'):
    if not astr:
        return None

    s = astr
    s = s.replace(u'\u200b', u'')
    s = s.replace(u'\u2010', u'-')
    s = s.replace(u'\u2011', u'-')
    s = s.replace(u'\u2012', u'-')
    s = s.replace(u'\u2013', u'-')
    s = s.replace(u'\u2014', u'-')
    s = s.replace(u'\u2015', u'-')
    s = s.replace(u'\u2022', u'*')
    s = s.replace(u'\u2021', u'|')
    s = s.replace(u'\u2030', u'%0')
    s = s.replace(u'\u2122', u'TM')
    s = s.replace(u'\u2018', u"'")
    s = s.replace(u'\u2019', u"'")
    s = s.replace(u'\u201a', u"'")
    s = s.replace(u'\u201b', u"'")
    s = s.replace(u'\u201c', u'"')
    s = s.replace(u'\u201d', u'"')
    s = s.replace(u'\u201e', u'"')
    s = s.replace(u'\u201f', u'"')
    s = s.replace(u'\u255a', u'"')
    s = s.replace(u'\u20ac', u'Euro')
    s = s.replace(u'\uf066', u'')
    
    if force_encoding:
        ts = s.encode(encoding, encoding_method)
        s = unicode(ts, encoding)

    return s