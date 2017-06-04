from BeautifulSoup import BeautifulSoup as Soup
from tqdm import tqdm
import psycopg2
import requests
import xmltodict


class Updater():

	def update_data(self, data):
		for d in tqdm(data):
			self.cur.execute('UPDATE courses SET learning_domain=%s WHERE subject=%s AND catalog_nbr=%s',d)
		self.conn.commit()


class Lsld(Updater):

	base_url = 'http://www.depaul.edu/university-catalog/academic-handbooks/undergraduate/university-information/liberal-studies-program/liberal studies learning domains/Pages/%s.aspx'
	ld = ['arts-and-literature','philosophical-inquiry',
			'religious-dimensions','scientific-inquiry',
			'self-society-and-the-modern-world','understanding-the-past']

	def __init__(self):
		dsn = "postgres://tim:PASSWORD@35.188.136.193:5432/mocksched"
		self.conn = psycopg2.connect(dsn)
		self.cur = self.conn.cursor()

	def run(self):
		self.download()
		self.update_helper()

	def update_helper(self):
		self.update_data(self.learning_domains)

	def download(self):
		learning_domains = []
		for l in self.ld:
			url = self.base_url%l
			html = requests.get(url).content
			soup = Soup(html)
			for a in soup.findAll('a', {'class':'courseLink'}):
				content = a.text.split()
				if len(content) == 0:
					continue
				learning_domains.append([l,content[0],content[1]])
		self.learning_domains = learning_domains

if __name__ == '__main__':
	l = Lsld()
	l.run()

