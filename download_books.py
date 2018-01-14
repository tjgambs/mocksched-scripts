from BeautifulSoup import BeautifulSoup as Soup
import requests
import time


class Parsing():

    def safe_find(self, soup, tag_name, dictionary, get_text_flag):
        try:
            return soup.find(tag_name, dictionary).text.encode('utf-8') if get_text_flag else soup.find(tag_name, dictionary)
        except:
            return ''

    def safe_find_all(self, soup, tag_name, dictionary):
        try:
            return soup.findAll(tag_name, dictionary)
        except:
            return []

class Books(Parsing):

    def __init__(self):
        ''' these need to be refreshed every once in a while '''
        self.cookies = {
            'TS015810ea_76': '088fa87ca9ab280094f2d1683cc0346656a6ee29f5b50ad70c44302d9208e6f8a8c706a9ebce25e14818bb36f03c25cf08180bd97487f800a1701b3502e63958eb99cc37cf714a39bfebe73b7825fd49a70eb99e82cd086e84e8e26b83bf2490b1db517f75755a23c338339a1db7a99302973b832c874394875a662bee9e0edb65b89edada89ca6ab09ce3228240cf1142db96eaac68ebba9bcfc8af8c1c55493927310233daf90945e5ba6143a4a3f8b1c81350222e8048858f6cae541f217a9e31b974755ecbc6c18844b8c25e4a7430adeb5b3d9fe448c9ce464bfbdb4ad75e3f06f82035ba2f0473ac52181efa5bd2343fdeea9ed8dee8bfcece32c1030590e7f332a2fdb0e183b44557b746b26d6305fd6e9d4e4d36bfdb677909de190c8e5f4f4d3930280b65d657277a206474',
            'flashMessage': '16551:false,',
            'CoreID6': '91378936185014965983736&ci=90222933',
            '_msuuid_518wse26072': 'E89BA83A-0EAB-4190-9ECE-B945FB1A7244',
            'BIGipServerBNCollege_WEBZ_http_pool': '875968266.20480.0000',
            '__utmt': '1',
            'cmTPSet': 'Y',
            'JSESSIONID': '0000Rt6vWLtSna74IjAuknrrkpV:prod-appz60',
            'WC_SESSION_ESTABLISHED': 'true',
            'WC_ACTIVEPOINTER': '-1%2C16551',
            'WC_USERACTIVITY_267400882': '267400882%2C16551%2Cnull%2Cnull%2C1496620813553%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2CESlsSvmMr3I%2FOMWLIsVfBI4CVs7kUYtGwAyIqL7Gugy6XwMzz9d9IKpk7sTu35VjflZcB%2FZ6Nlm3UqIOwO%2FOTQo%2BUIrWA0pHebItWVI8sWaZ58i%2BYfxImt9diTOEZh9OhBq31U5%2Fk0wK2LmN7i1yGW3Ldsd9XvGaMaqrsLQG0kULiDPEZ8wxY89R%2BEzMwsNDoqLAo4EaiYmDl5adxDx7j1PbPZwYARcTwQ80HIrqEDg%3D',
            'TS01825e4a': '013589168b8496b1fb24a65169bb812c4720afcf0d61c5f73f7f68087b4e8db66265ee6a8228417d30194d91e5074c0eae00151ace396ea23901c1b3c903a56a8ccd85c4d085dcf9848d0a4388afd50ceb715b05940ff038a4dcc7d3d8849721ea8137be7f926cc83bebedbc21e3b34ac115f2fc35',
            'TS015810ea_1': '01e8fc688d54d2f010db5b403fc00f9c9985b349b79142e73d865fe728e28b5c7854d25ae399fd1d4a3aa3af5d6fb9a9b106fc4a37',
            'TS015810ea_27': '01e8fc688d0fe9d830e7950791e534b8a45ced90c11904f99374dea9111a0453399515e3acc8d18ca2fe2138f0ad636510a69c7094',
            'TS014d5a24': '013589168bf2b6e40b94b995f6897e2bf3b0b1f91f61c5f73f7f68087b4e8db66265ee6a8238a5654f2f014ebc4707fc7b9c8befb8',
            '__utma': '168970354.543297142.1496598374.1496598374.1496598374.1',
            '__utmb': '168970354.168.9.1496601809508',
            '__utmc': '168970354',
            '__utmz': '168970354.1496598374.1.1.utmcsr=depaul.bncollege.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
            '__utmv': '168970354.store_084',
            'TS015810ea': '013589168bd2dc849b295601ae387eaf20a9ce1782ba2db390939e765de3d069208a9f64f8',
            'TS015810ea_30': '01e8fc688dbb86f4f17ac9ff91f586052163454bee1904f99374dea9111a0453399515e3ac0180b49041b0cf372cfc6a9705f4d504',
            '90222933_clogin': 'l=1496620813&v=1&e=1496622783571',
        }
        self.headers = {
            'Pragma': 'no-cache',
            'Origin': 'http://depaul-lincolnpark.bncollege.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control': 'no-cache',
            'Referer': 'http://depaul-lincolnpark.bncollege.com/webapp/wcs/stores/servlet/TBWizardView?catalogId=10001&langId=-1&storeId=16551',
            'Connection': 'keep-alive',
        }
        self.store_id = '16551'
        self.catalog_id = '10001'
        self.campus_id = '14704464'

    def get_terms(self):
        url = 'http://depaul-lincolnpark.bncollege.com/webapp/wcs/stores/servlet/TextBookProcessDropdownsCmd?campusId=%s&termId=&deptId=&courseId=&sectionId=&storeId=%s&catalogId=%s&langId=-1&dropdown=dept' % (self.campus_id,self.store_id,self.catalog_id)
        payload = requests.get(url,headers=self.headers,cookies=self.cookies).json()
        return payload

    def get_subjects(self, term):
        url = 'http://depaul-lincolnpark.bncollege.com/webapp/wcs/stores/servlet/TextBookProcessDropdownsCmd?campusId=%s&termId=%s&deptId=&courseId=&sectionId=&storeId=%s&catalogId=%s&langId=-1&dropdown=dept' % (self.campus_id,term,self.store_id,self.catalog_id)
        payload = requests.get(url,headers=self.headers,cookies=self.cookies).json()
        return payload

    def get_numbers(self, term, subject):
        url = 'http://depaul-lincolnpark.bncollege.com/webapp/wcs/stores/servlet/TextBookProcessDropdownsCmd?campusId=%s&termId=%s&deptId=%s&courseId=&sectionId=&storeId=%s&catalogId=%s&langId=-1&dropdown=dept' % (self.campus_id,term,subject,self.store_id,self.catalog_id)
        payload = requests.get(url,headers=self.headers,cookies=self.cookies).json()
        return payload

    def get_sections(self, term, subject, number):
        url = 'http://depaul-lincolnpark.bncollege.com/webapp/wcs/stores/servlet/TextBookProcessDropdownsCmd?campusId=%s&termId=%s&deptId=%s&courseId=%s&sectionId=&storeId=%s&catalogId=%s&langId=-1&dropdown=dept' % (self.campus_id,term,subject,number,self.store_id,self.catalog_id)
        payload = requests.get(url,headers=self.headers,cookies=self.cookies).json()
        return payload

    def get_soup(self, section_1):
        data = [
            ('storeId', self.store_id),
            ('catalogId', self.catalog_id),
            ('langId', '-1'),
            ('clearAll', ''),
            ('viewName', 'TBWizardView'),
            ('secCatList', ''),
            ('removeSectionId', ''),
            ('mcEnabled', 'N'),
            ('showCampus', 'false'),
            ('selectTerm', 'Select Term'),
            ('selectDepartment', 'Select Department'),
            ('selectSection', 'Select Section'),
            ('selectCourse', 'Select Course'),
            ('campus1', self.campus_id),
            ('section_1', section_1),
            ('section_2', ''),
            ('section_3', ''),
            ('section_4', ''),
            ('numberOfCourseAlready', '4'),
        ]
        url = 'http://depaul-lincolnpark.bncollege.com/webapp/wcs/stores/servlet/BNCBTBListView'
        html = requests.post(url, headers=self.headers, cookies=self.cookies, data=data).content
        soup = Soup(html)
        return soup

    def parse_books(self, section_1):
        books = []
        soup = self.get_soup(section_1)
        for s in soup.findAll('div',{'class':'book-list'}):
            try:
                title = s.find('div',{'class':'book_desc1 cm_tb_bookInfo'}).find('h1').text.replace('&#039;',"'")
                book_type = s.find('span',{'class':'recommendBookType'}).text
                author = s.find('i').text
                image_url = s.find('img',{'class':'noImageDisReq'})['src']
                edition = ' '.join(s.find('li',{'class':'book_c1'}).text.split()[1:])
                publisher = ' '.join(s.find('li',{'class':'book_c2'}).text.split()[1:])
                isbn = ' '.join(s.find('li',{'class':'book_c2_180616'}).text.split()[1:])
                books.append([
                    section_1,
                    title,
                    book_type,
                    author,
                    image_url,
                    edition,
                    publisher,
                    isbn
                ])
            except:
                continue
        return books


if __name__ == '__main__':
    b = Books()
    terms = b.get_terms()
    for term in terms[1:]:
        subjects = b.get_subjects(term['categoryId'])
        for subject in subjects:
            try:
                numbers = b.get_numbers(term['categoryId'],subject['categoryId'])
                for number in numbers:
                    sections = b.get_sections(term['categoryId'],subject['categoryId'],number['categoryId'])
                    # for section in sections:
                    #     print b.parse_books(section['categoryId'])
                print subject
                time.sleep(1)
            except Exception,e:
                print e



