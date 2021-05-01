from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import getcwd
import csv

def get_html(url):
	options = Options()
	options.headless = True
	driver = webdriver.Chrome(executable_path=getcwd() + '/chromedriver', options=options)
	driver.get(url)
	time.sleep(10)
	html = driver.page_source
	driver.quit()

	return html

def get_data(html):
	soup = BeautifulSoup(html, 'lxml')
	objects = soup.find('div', class_='sportName').find_all('div', class_='event__match event__match--twoLine')
	data = []

	for i in objects:
		try:
			home_player = i.find('div', class_='event__participant event__participant--home').text.strip()
		except:
			home_player = i.find('div', class_='event__participant event__participant--home fontBold').text.strip()
		
		try:
			away_player = i.find('div', class_='event__participant event__participant--away').text.strip()
		except:
			away_player = i.find('div', class_='event__participant event__participant--away fontBold').text.strip()

		try:
			home_score = i.find('div', class_='event__score event__score--home').text.strip()
		except:
			home_score = ''

		try:
			away_score = i.find('div', class_='event__score event__score--away').text.strip()
		except:
			away_score = ''

		data.append([home_player, home_score, away_player, away_score])

	return data
 
def write_csv(data):
	with open('flashscore.csv', 'a', newline = '') as file:
		writer = csv.writer(file, delimiter = ';')
		for i in data:
			writer.writerow((i[0], i[1]))
			writer.writerow((i[2], i[3]))
			writer.writerow((''))

			print(i[0], ' & ', i[2], ' parsed!')



def main():
	url = 'https://www.flashscore.com/table-tennis/'

	write_csv(get_data(get_html(url)))
	

if __name__ == '__main__':
	main()