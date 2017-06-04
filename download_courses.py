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


class Descriptions(Importer):

	def __init__(self):
		dsn = "postgres://tim:PASSWORD@35.188.136.193:5432/mocksched"
		self.conn = psycopg2.connect(dsn)
		self.cur = self.conn.cursor()

	def run(self):
		self.download()
		self.import_helper()

	def import_helper(self):
		fields = '(title,subject,catalog_nbr,acad_career,description,prerequisites,modified,created)'
		self.import_data(self.courses,'courses',fields)

	def download(self):
		headers = {'Content-Type': "text/xml;charset='UTF-8'"}
		data = '''<soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'>
					<soap:Body>
						<GetListItems xmlns='http://schemas.microsoft.com/sharepoint/soap/'>
							<listName>Courses</listName>
							<viewName></viewName>
							<query>
								<Query></Query>
							</query>
							<viewFields>
								<ViewFields>
									<FieldRef Name='Title' />
									<FieldRef Name='SUBJECT' />
									<FieldRef Name='CATALOG_NBR' />
									<FieldRef Name='ACAD_CAREER' />
									<FieldRef Name='DESCR' />
									<FieldRef Name='Prerequisites' />
								</ViewFields>
							</viewFields>
							<rowLimit>0</rowLimit>
							<queryOptions>
								<QueryOptions></QueryOptions>
							</queryOptions>
						</GetListItems>
					</soap:Body>
				</soap:Envelope>'''
		payload = requests.post('https://www.depaul.edu/university-catalog/_vti_bin/Lists.asmx', headers=headers, data=data).content
		class_list = xmltodict.parse(payload)['soap:Envelope']['soap:Body']['GetListItemsResponse']['GetListItemsResult']['listitems']['rs:data']['z:row']
		courses = []
		for c in class_list:
			courses.append([
					c['@ows_Title'].title(),
					c.get('@ows_SUBJECT'),
					c.get('@ows_CATALOG_NBR'),
					c.get('@ows_ACAD_CAREER'),
					c.get('@ows_DESCR'),
					c.get('@ows_Prerequisites'),
					c.get('@ows_Modified'),
					c.get('@ows_Created')
				])
		self.courses = courses


if __name__ == '__main__':
	d = Descriptions()
	d.run()




