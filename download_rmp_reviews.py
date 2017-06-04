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
		fields = '(id,professor_id,would_take_again,course,text_book_use,easy_color,teacher_grade,easy,clarity,useful_grouping,interest,sid,quality,status,attendance,teacher_rating_tags,overall_string,comments,date,taken_for_credit,online_class,not_help_count,helpful,teacher,help_color,easy_string,unuseful_grouping,overall,help_count,clarity_color)'
		self.import_data(self.reviews,'rate_my_professors_reviews',fields)

	def download(self):

		self.cur.execute('SELECT id FROM rate_my_professors')
		tids = [tid[0] for tid in self.cur.fetchall()]
		reviews = []
		for tid in tqdm(tids):
			page = 1
			while True:
				try:
					response = requests.get('http://www.ratemyprofessors.com/paginate/professors/ratings?tid=%s&page=%s'%(tid,page)).json()
				except Exception,e:
					print e
					break
				for j in response['ratings']:
					reviews.append([
							j.get('id'),
							tid,
							j.get('rWouldTakeAgain'),
							j.get('rClass'),
							j.get('rTextBookUse'),
							j.get('easyColor'),
							j.get('teacherGrade'),
							j.get('rEasy'),
							j.get('rClarity'),
							j.get('usefulGrouping'),
							j.get('rInterest'),
							j.get('sId'),
							j.get('quality'),
							j.get('rStatus'),
							j.get('attendance'),
							j.get('teacherRatingTags'),
							j.get('rOverallString'),
							j.get('rComments'),
							j.get('rDate'),
							j.get('takenForCredit'),
							j.get('onlineClass'),
							j.get('notHelpCount'),
							j.get('rHelpful'),
							j.get('teacher'),
							j.get('helpColor'),
							j.get('rEasyString'),
							j.get('unUsefulGrouping'),
							j.get('rOverall'),
							j.get('helpCount'),
							j.get('clarityColor')
						])
				if response['remaining'] == 0:
					break
				page += 1
		self.reviews = reviews

if __name__ == '__main__':
	r = Rmp()
	r.run()
