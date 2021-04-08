import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import logging
import sys
import os
from send_email import SendMail
city = 'Essen'

try:
	os.remove(f'{city}_old.csv')
	os.rename(f'{city}.csv',f'{city}_old.csv')
except:
	pass

headers = {'User-Agent': 'Mozilla/5.0'}
class payload:
	def __init__(self, position,city):
		self.formdata = {'umkreis': -1,
			'WAS': 'Immobilienmakler',

			'WO': city,
			'position': position,
			'anzahl': 10,
			'sortierung': 'relevanz'}

session = requests.Session()

def get_status(c):
	l = json.load(open('codes.json'))
	s = list(filter(lambda person: person['code'] == 200, l))
	return s[0]['phrase']

def GetTotal():
	r = session.post('https://www.gelbeseiten.de/AjaxSuche',headers=headers,data=payload(1,city).formdata)
	json_data = json.loads(r.text)
	return	json_data['gesamtanzahlTreffer']
total = GetTotal()

def Scrape(position, s):
	r = s.post('https://www.gelbeseiten.de/AjaxSuche',headers=headers,data=payload(position,city).formdata)
	json_data = json.loads(r.text)
	html = json_data['html']
	soup = BeautifulSoup(html,'html.parser')
	articles = soup.select('article')
	fdatas = []
	for article in articles:
		fdata = dict()
		fdata['heading'] = article.find('h2').get_text()
		links = article.find_all("a", string="Webseite")
		if(links):
			website = links[0]['href']
			fdata['website'] = website
		else:
			website = 'n.a'
		print(fdata)
		fdatas.append(fdata)
	return fdatas

i = 1 
alldf = []

while i <= total:
	
	d = Scrape(i,session)
	df = pd.DataFrame(d)
	alldf.append(df)

	fdf = pd.concat(alldf)
	print(fdf)
	fdf.to_csv(f'{city}.csv')
	i = i + 10 
	print('\n')

df = pd.read_csv(f'{city}.csv')

for i in range(0,len(df)):
	url = df.loc[i,'website']
	print(i)
	try:
		r = requests.get(url)
		stts = get_status(r.status_code)
		df.loc[i,'code'] = r.status_code
		df.loc[i,'status'] = stts
	except Exception as e :
		print(e)
		df.loc[i,'status'] = 'Not Found'
		df.loc[i,'code'] = 404
	logging.info(f"{i} - HTTP {df.loc[i,'code']} Found for {url}")
	print(df)
	df.to_csv(f'{city}.csv')


SendMail()