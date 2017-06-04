from tqdm import tqdm
import psycopg2
import requests
import xmltodict


class Importer():

	def import_data(self, data, table, fields):
		chunks = self.chunks(data, 1000)
		for c in tqdm(chunks):
			args_str = ','.join(self.cur.mogrify(self.produce_s(len(x)), x) for x in c)
			self.cur.execute("INSERT INTO %s %s VALUES %s ON CONFLICT DO NOTHING" % (table, fields, args_str,))
			self.conn.commit()

	def produce_s(self, l):
		return '(%s)' % ','.join(['%s']*l)

	def chunks(self, l, n):
		for i in range(0, len(l), n):
			yield l[i:i + n]

class Rmp(Importer):

	def __init__(self):
		dsn = "postgres://tim:PASSWORD@35.188.136.193:5432/mocksched"
		self.conn = psycopg2.connect(dsn)
		self.cur = self.conn.cursor()

	def run(self):
		self.download()
		self.import_helper()

	def import_helper(self):
		fields = '(id,first_name,last_name,overall_score,helpful_score,clarity_score,easy_score)'
		self.import_data(self.ratings,'rate_my_professors',fields)

	def download(self):
		law = requests.get('http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows=10000000&q=*%253A*+AND+schoolid_s%253A5485&defType=edismax&qf=teacherfullname_t%255E1000+autosuggest&bf=pow(total_number_of_ratings_i%252C2.1)&sort=&siteName=rmp&rows=1000000000&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+averageratingscore_rf+averagehelpfulscore_rf+averageclarityscore_rf+averageeasyscore_rf').json()
		regular = requests.get('http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows=1000000&q=*%253A*+AND+schoolid_s%253A1389&defType=edismax&qf=teacherfullname_t%255E1000+autosuggest&bf=pow(total_number_of_ratings_i%252C2.1)&sort=&siteName=rmp&rows=1000000000&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+averageratingscore_rf+averagehelpfulscore_rf+averageclarityscore_rf+averageeasyscore_rf').json()
		complete = law['response']['docs'] + regular['response']['docs']
		ratings = []
		for c in complete:
			ratings.append([
					c.get('pk_id'),
					c.get('teacherfirstname_t'),
					c.get('teacherlastname_t'),
					c.get('averageratingscore_rf'),
					c.get('averagehelpfulscore_rf'),
					c.get('averageclarityscore_rf'),
					c.get('averageeasyscore_rf')
				])
		self.ratings = ratings

if __name__ == '__main__':
	r = Rmp()
	r.run()
