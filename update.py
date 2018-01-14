from tqdm import tqdm
from BeautifulSoup import BeautifulSoup as Soup
import psycopg2
import requests
import xmltodict
import re
import uuid


class Importer(object):

    def import_data(self, data, table, primary_keys, fields):
        chunks = self.chunks(data, 1000)
        upsert_text = self.generate_upsert_text(fields)
        for c in tqdm(chunks):
            args_str = ','.join(self.cur.mogrify(
                self.produce_s(len(x)), x) for x in c)
            self.cur.execute("INSERT INTO %s %s VALUES %s ON CONFLICT %s %s" % (
                table, fields, args_str, primary_keys, upsert_text, ))
            self.conn.commit()

    def produce_s(self, l):
        return '(%s)' % ','.join(['%s'] * l)

    def generate_upsert_text(self, fields):
        columns = tuple(fields[1:-1].split(','))
        updates = ','.join(['%s = excluded.%s' % (s, s) for s in columns])
        return 'DO UPDATE SET %s' % updates

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]


class Terms(Importer):

    def __init__(self):
        dsn = "postgres://tim:PASSWORD@35.188.136.193:5432/mocksched"
        self.conn = psycopg2.connect(dsn)
        self.cur = self.conn.cursor()
        self.terms = self.download_terms()

    @property
    def streams(self):
        return [x['strm'] for x in self.terms]

    def download_terms(self):
        url = 'http://offices.depaul.edu/_layouts/DUC.SR.ClassSvc/DUClassSvc.ashx?action=getterms'
        return requests.get(url).json()

    def update_db(self):
        fields = ['stream', 'description']
        primary_keys = ['stream']
        self.import_data(data=[(x['strm'], x['descr']) for x in self.terms],
                         table='terms',
                         primary_keys='(%s)' % ','.join(primary_keys),
                         fields='(%s)' % ','.join(fields))


class TermCourses(Importer):

    def __init__(self, terms, courses):
        dsn = "postgres://tim:PASSWORD@35.188.136.193:5432/mocksched"
        self.conn = psycopg2.connect(dsn)
        self.cur = self.conn.cursor()
        self.terms = terms
        self.courses = courses
        self.term_courses = self.download_term_courses()

    def download_term_courses(self):
        base_url = ('https://offices.depaul.edu/_layouts/DUC.SR.ClassSvc/DUClassSvc.ashx'
                    '?action=searchclassbysubject&strm=%s')
        term_courses = set()
        present_courses = self.courses.present_courses
        for stream in tqdm(self.terms.streams):
            payload = requests.get(base_url % stream).json()
            for p in payload:
                for i in p['classes']:
                    if i.get('descr') and i.get('subject') and i.get('catalog_nbr'):
                        seed_string = (
                            i['subject'] + i['catalog_nbr']).encode('utf8')
                        course_id = str(uuid.uuid3(
                            uuid.NAMESPACE_DNS, seed_string))
                        if not course_id in present_courses:
                            self.courses.courses.add((
                                course_id,
                                self.courses.format_title(i['descr']),
                                i['subject'],
                                i['catalog_nbr'],
                                self.courses.learning_domains.get(seed_string),
                                None,
                                None,
                                None,
                                None,
                                None
                            ))
                    term_courses.add((stream, course_id))
        return term_courses

    def update_db(self):
        fields = ['stream', 'course_id']
        primary_keys = ['stream', 'course_id']
        self.import_data(data=list(self.term_courses),
                         table='term_courses',
                         primary_keys='(%s)' % ','.join(primary_keys),
                         fields='(%s)' % ','.join(fields))


class Courses(Importer):

    def __init__(self):
        dsn = "postgres://tim:PASSWORD@35.188.136.193:5432/mocksched"
        self.conn = psycopg2.connect(dsn)
        self.cur = self.conn.cursor()
        self.learning_domains = self.get_learning_domains()
        self.courses = self.download_courses()

    @property
    def present_courses(self):
        return set(x[0] for x in self.courses)

    def update_db(self):
        fields = ['id', 'title', 'subject', 'catalog_nbr', 'learning_domain',
                  'acad_career', 'description', 'prerequisites', 'modified', 'created']
        primary_keys = ['id']
        self.import_data(data=list(self.courses),
                         table='courses',
                         primary_keys='(%s)' % ','.join(primary_keys),
                         fields='(%s)' % ','.join(fields))

    def download_courses(self):
        query_url = 'https://www.depaul.edu/university-catalog/_vti_bin/Lists.asmx'
        headers = {'Content-Type': "text/xml;charset='UTF-8'"}
        data = '''<soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' 
                                xmlns:xsd='http://www.w3.org/2001/XMLSchema' 
                                xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'>
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
        response = requests.post(query_url, headers=headers, data=data)
        class_list = [xmltodict.parse(x)['z:row'] for x in re.findall(
            r'<z:row.*?/>', response.content)]
        values = set()
        for c in class_list:
            if c.get('@ows_Title') and c.get('@ows_SUBJECT') and c.get('@ows_CATALOG_NBR'):
                seed_string = (c['@ows_SUBJECT'] +
                               c['@ows_CATALOG_NBR']).encode('utf8')
                course_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, seed_string))
                values.add((
                    course_id,
                    self.format_title(c['@ows_Title']),
                    c['@ows_SUBJECT'],
                    c['@ows_CATALOG_NBR'],
                    self.learning_domains.get(seed_string),
                    c.get('@ows_ACAD_CAREER'),
                    c.get('@ows_DESCR'),
                    c.get('@ows_Prerequisites'),
                    c.get('@ows_Modified'),
                    c.get('@ows_Created')))
        return values

    def format_title(self, title):
        title = title.title()
        romans = ['Viii', 'Vii', 'Vi', 'Iv', 'IIi', 'Ii']
        for r in romans:
            if r in title:
                return title.replace(r, r.upper())
        return title

    def get_learning_domains(self):
        base_url = ('http://www.depaul.edu/university-catalog/academic-handbooks/undergraduate/university-'
                    'information/liberal-studies-program/liberal studies learning domains/Pages/%s.aspx')
        ld = ['arts-and-literature',
              'philosophical-inquiry',
              'religious-dimensions',
              'scientific-inquiry',
              'self-society-and-the-modern-world',
              'understanding-the-past']
        learning_domains = {}
        for l in tqdm(ld):
            soup = Soup(requests.get(base_url % l).content)
            for a in soup.findAll('a', {'class': 'courseLink'}):
                content = a.text.split()
                if len(content):
                    learning_domains[content[0] + content[1]] = l
        return learning_domains


class Professors(Importer):

    def __init__(self):
        dsn = "postgres://tim:PASSWORD@35.188.136.193:5432/mocksched"
        self.conn = psycopg2.connect(dsn)
        self.cur = self.conn.cursor()
        self.professors = self.download_professors()

    @property
    def professor_ids(self):
        return [x[0] for x in self.professors]

    def download_professors(self):
        law_url = ('http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows=10000000&q=*%253A'
                   '*+AND+schoolid_s%253A5485&defType=edismax&qf=teacherfullname_t%255E1000+autosuggest&bf=pow('
                   'total_number_of_ratings_i%252C2.1)&sort=&siteName=rmp&rows=1000000000&start=0&fl=pk_id+'
                   'teacherfirstname_t+teacherlastname_t+averageratingscore_rf+averagehelpfulscore_rf+'
                   'averageclarityscore_rf+averageeasyscore_rf')
        law = requests.get(law_url).json()
        regular_url = ('http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows=1000000&q=*%253A'
                       '*+AND+schoolid_s%253A1389&defType=edismax&qf=teacherfullname_t%255E1000+autosuggest&bf=pow('
                       'total_number_of_ratings_i%252C2.1)&sort=&siteName=rmp&rows=1000000000&start=0&fl=pk_id+'
                       'teacherfirstname_t+teacherlastname_t+averageratingscore_rf+averagehelpfulscore_rf+'
                       'averageclarityscore_rf+averageeasyscore_rf')
        regular = requests.get(regular_url).json()
        complete = law['response']['docs'] + regular['response']['docs']
        return set((
            c.get('pk_id'),
            c.get('teacherfirstname_t'),
            c.get('teacherlastname_t'),
            c.get('averageratingscore_rf'),
            c.get('averagehelpfulscore_rf'),
            c.get('averageclarityscore_rf'),
            c.get('averageeasyscore_rf')
        ) for c in complete)

    def update_db(self):
        fields = ['id', 'first_name', 'last_name', 'overall_score', 'helpful_score',
                  'clarity_score', 'easy_score']
        primary_keys = ['id']
        self.import_data(data=list(self.professors),
                         table='professors',
                         primary_keys='(%s)' % ','.join(primary_keys),
                         fields='(%s)' % ','.join(fields))


class Reviews(Importer):

    def __init__(self, professors):
        dsn = "postgres://tim:PASSWORD@35.188.136.193:5432/mocksched"
        self.conn = psycopg2.connect(dsn)
        self.cur = self.conn.cursor()
        self.professor_ids = professors.professor_ids
        self.reviews = self.download_reviews()

    def download_reviews(self):
        reviews = []
        for tid in tqdm(self.professor_ids):
            page = 1
            while True:
                try:
                    url = 'http://www.ratemyprofessors.com/paginate/professors/ratings?tid=%s&page=%s' % (
                        tid, page)
                    response = requests.get(url).json()
                except Exception, e:
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
        return reviews

    def update_db(self):
        fields = ['id', 'professor_id', 'would_take_again', 'course', 'text_book_use', 'easy_color',
                  'teacher_grade', 'easy', 'clarity', 'useful_grouping', 'interest', 'sid', 'quality',
                  'status', 'attendance', 'teacher_rating_tags', 'overall_string', 'comments', 'date',
                  'taken_for_credit', 'online_class', 'not_help_count', 'helpful', 'teacher', 'help_color',
                  'easy_string', 'unuseful_grouping', 'overall', 'help_count', 'clarity_color']
        primary_keys = ['id']
        self.import_data(data=list(self.reviews),
                         table='reviews',
                         primary_keys='(%s)' % ','.join(primary_keys),
                         fields='(%s)' % ','.join(fields))


if __name__ == '__main__':
    terms = Terms()
    courses = Courses()
    term_courses = TermCourses(terms, courses)
    professors = Professors()
    reviews = Reviews(professors)
    courses.update_db()
    terms.update_db()
    term_courses.update_db()
    professors.update_db()
    reviews.update_db()
