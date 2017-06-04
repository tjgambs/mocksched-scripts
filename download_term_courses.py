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
		self.prepare()
		self.get_new()
		self.import_to_add()
		self.prepare()
		self.download()
		self.import_helper()

	def import_to_add(self):
		fields = '(title,subject,catalog_nbr,acad_career,description,prerequisites,modified,created)'
		self.import_data(self.to_add,'courses',fields)

	def import_helper(self):
		fields = '(stream,course_id)'
		self.import_data(self.term_courses,'term_courses',fields)

	def prepare(self):
		self.cur.execute("SELECT subject || ' ' || catalog_nbr, id FROM courses")
		self.key = dict((a[0],a[1]) for a in self.cur.fetchall())

	def get_terms(self):
		terms = requests.get('http://offices.depaul.edu/_layouts/DUC.SR.ClassSvc/DUClassSvc.ashx?action=getterms').json()
		return [a['strm'] for a in terms]

	def download(self):
		streams = self.get_terms()
		base_url = 'https://offices.depaul.edu/_layouts/DUC.SR.ClassSvc/DUClassSvc.ashx?action=searchclassbysubject&strm=%s'
		term_courses = []
		for s in streams:
			payload = requests.get(base_url%s).json()
			for p in payload:
				for i in p['classes']:
					term_courses.append([s,self.key[i['subject']+' '+i['catalog_nbr']]])
		self.term_courses = term_courses

	def get_new(self):
		streams = self.get_terms()
		base_url = 'https://offices.depaul.edu/_layouts/DUC.SR.ClassSvc/DUClassSvc.ashx?action=searchclassbysubject&strm=%s'
		to_add = []
		for s in streams:
			payload = requests.get(base_url%s).json()
			for p in payload:
				for i in p['classes']:
					try:
						a = self.key[i['subject']+' '+i['catalog_nbr']]
					except:
						to_add.append([
							i['descr'].title(),
							i.get('subject'),
							i.get('catalog_nbr'),
							None,
							None,
							None,
							None,
							None
						])
		self.to_add = to_add
		

if __name__ == '__main__':
	r = Rmp()
	r.run()

