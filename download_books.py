from BeautifulSoup import BeautifulSoup as Soup
import requests


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
        self.cookies = cookies = {
            'TS015810ea_76': '088fa87ca9ab28009ce7634f2f5f53e597bbf772089e98bdce4e84612d5b08032e84940295160a04ad00ba54cdee7ff308a675131b87f8008047deaee2407df34741c78ce232d22385f9bc90a2f149d4ee45586dc4e63a2230ffa1a9dfdee92b5508856d2905661612e9f422dc81f0c3e1e9bf19fcafca8f9ab15079b580f1682aa275a77dbfb547668d70e684a3d24e60257c56b9f0bf37ba81cde536e274ce6153af1633617f4a72a4a21b342d2318ffe3b6ef1d98b2eef93d48e21ebdb7595886825ced44d5c43812aee63220ed80b822244c49394a139540d621b5c9d8e12ce72a865bcd484ae1bf6623581b5c6a047b480b454b6e56899d07d7d78bd57f163b83abb1763b115305fc2ad043bde0f21395f9ea0a3f99d951a319a45f4332e126a3207df07dcdd044e01ff9ef5374',
            'flashMessage': '16551:false,10551:false,',
            'BIGipServerBNCollege_WEBZ_http_pool': '859191050.20480.0000',
            'cmTPSet': 'Y',
            'CoreID6': '91378936185014965983736&ci=90222933',
            'JSESSIONID': '0000PJupCFJLojfmXJe448aCYXx:prod-appz02',
            'WC_SESSION_ESTABLISHED': 'true',
            'WC_USERACTIVITY_267358643': '267358643%2C16551%2Cnull%2Cnull%2C1496598373721%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2CeKoV%2Bj03gKX2TPevllojP74vT%2FrsUcolK03k%2F8US%2BXGJX0t9ct6Q1HPph%2F6fjz%2FtpYUEo%2FUnCtqE%2B0jitCnoHAjZdmI%2FqJKVyl%2B0Pxpxp5woukx4VIBuylJ1SaY4rQ5wvqv4kioa94eeMNTEHKunt06stTPE6k51045amBhEat6d5iIA62bxiziBjdo%2FrvgYoQgibiWuKNDM81G9Zfb0msDNU9nNowSskch4HXvSfNA%3D',
            'TS01825e4a': '013589168b94c514906c0efc6af5b947f7231bc34aab919958e7e0a9b12db2c7f58791eb1f3846391950091714e61dac85fab0c8ad3771b9ed0ec5a9d2a3f7b32d92f1983d685478c189101641b5095ad72ddaa95022ae12c3685268799e80bbcd090f8892de6a559c1330bceab1558ab6823cddf2',
            '_msuuid_518wse26072': 'E89BA83A-0EAB-4190-9ECE-B945FB1A7244',
            'TS014d5a24_77': '088fa87ca9ab28006d6cce0cdc4dcb1c5ba17a97de4781d0e0474ca1fc69725e83ea34359f2e21cce6860ce5b036e3c5085c3deba1823800f5961d2d94ded8e16407d5e4746e7266d45eaf7436e1bbcdec643c300fbd84f857bc7010fbab24c768b26c26148d5787aacafa23c3e4ae4a',
            'TS01beedce': '013589168b9f07d15941be0d1085e553c622c4e465bb2f5fbc1b4b96bcd71edd5a6e78a405',
            'WC_ACTIVEPOINTER': '-1%2C10551',
            'WC_USERACTIVITY_-1002': '-1002%2C10551%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2CsxzR97BJIOe2vKexBcRFDdaTaCq1D9e%2BdcLpHkFYNb1AKszHeY0CaALL8NQkPcwH3dzPJ5xbgydXgYsEefIioRntZdE%2F6cs20njOvweWP6PJVWgdcmCgDACDBuPHS6uHYEHkfEb83jkF8mjL1oAXCb00HJM71Tq3f3qt5hcoL9mTQJtMmhsAxAXQpKfOQxuzMsYj7rYzrDE3r%2FNXxjVNow%3D%3D',
            'WC_GENERIC_ACTIVITYDATA': '[1086025126%3Atrue%3Afalse%3A0%3ASzskSqBgrRvsUuTgYjCKkilw9Go%3D][com.ibm.commerce.context.entitlement.EntitlementContext|11002%2611002%26null%26-2000%26null%26null%26null][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][com.ibm.commerce.catalog.businesscontext.CatalogContext|10001%26null%26false%26false%26false][CTXSETNAME|Store][com.ibm.commerce.context.base.BaseContext|10551%26-1002%26-1002%26-1][com.ibm.commerce.context.audit.AuditContext|null][com.ibm.commerce.context.experiment.ExperimentContext|null][com.bncb.cms.context.BNCBCMSPreviewContext|null][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null][com.ibm.commerce.context.globalization.GlobalizationContext|-1%26USD%26-1%26USD]',
            'TS01971484': '013589168b3767e80923a972e40f1af78cd68c8240c1c28de7d9202e95ecd4e7534ba92bafb1aa9a94877fa243cf9230ba0825ee4720f513e08bb3703c91489c3646e8f04c0532a50a1aaeb15bfc1b3b07dec9bcc2',
            'TS015810ea_77': '088fa87ca9ab28007f65a70809c432ab3fd46a24439eb1692054c879611db51d87ad0b4ed0ac36e277cd739eeea1172008505651d5823800f39a43222c53e0c6106a597b873c6207cb370c5afe652987242e0aff00b858c029721aceefa26b0a0cb1ccb5491b61cb24ddbcba29587e96',
            '__utmt': '1',
            'TS015810ea_1': '01e8fc688d344381a61640b1adf75674c0a672272af5e0759de3e38a91bc2fb5003d90a75ccff7ae0ab2bca251f225fe71dac1a1de',
            'TS015810ea_27': '01e8fc688ddf85c9d41dcec1a627555850e1a6e79a2bce1f5000129f4b10fd20d4c84eb01dd1b9e6d4003746cfc35cf1377d0f457f',
            'TS014d5a24': '013589168b44c3d547a385034787c76f5d0b1bb272b758d45b25c9dc6ff1701d25f1cf1a8b77f833faf37dd36c7f637e1df74ec5f5',
            '__utma': '168970354.543297142.1496598374.1496598374.1496598374.1',
            '__utmb': '168970354.154.9.1496601809508',
            '__utmc': '168970354',
            '__utmz': '168970354.1496598374.1.1.utmcsr=depaul.bncollege.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
            '__utmv': '168970354.store_084',
            'TS015810ea': '013589168bedb47d2d9de7a6e3a61c53c51e03b6b261bc529f800a5e4acff8bead866c1c8d',
            'TS015810ea_30': '01e8fc688d901558ecc2b751a71326abcde3448c172bce1f5000129f4b10fd20d4c84eb01d52aa6aa0687d522f2e1ca1cdd001c677',
            '90222933_clogin': 'l=1496598373&v=1&e=1496608516936',
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
            numbers = b.get_numbers(term['categoryId'],subject['categoryId'])
            for number in numbers:
                sections = b.get_sections(term['categoryId'],subject['categoryId'],number['categoryId'])
                for section in sections:
                    print b.parse_books(section['categoryId'])



