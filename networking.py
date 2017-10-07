import requests
import parsing as ps
import golemio as io

login_page =  'https://sismobile.case.edu/app/profile/logintoapp'
search_page = "https://sis.case.edu/psc/P90SCWR_1/EMPLOYEE/P90SCWR/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL"
# TERM of YEAR is called as term_codes[TERM][YEAR - 2008]
term_codes = {'Fall'  :[2088, 2098, 2108, 2118, 2128, 2138, 2148, 2158, 2168, 2178],
              'Spring':[0000, 2091, 2101, 2111, 2121, 2131, 2141, 2151, 2161, 2171],
              'Summer':[2086, 2096, 2106, 2116, 2126, 2136, 2146, 2156, 2166, 2176]}

def get_session():
    return requests.session()

def logged_in(page_response):
    '''Checks if logged in given a page response'''
    return "ERP Student Information System Sign-in" not in page_response


def login(session, auth):
    '''Logs session into SIS'''
    result = session.get(search_page)
    if not logged_in(result.text):
        io.log('Logging into SIS')
        payload = {
            'username': auth[0],
            'password': auth[1],
            'loginAction': '',
            'institution': 'CASE1'
            }
        response = session.post(login_page, data=payload)
        if "incorrect" in response.text:
            io.log('Wrong username or password')
            return False
    return True


def search_classes(session, auth, course_subject='', catalog_number='', title_keyword='', term=''):
    '''
    Searches for classes given some criteria.
    Logs user in if not already logged in.
    Returns list of classes if everything works, otherwise returns empty list.
    term should be in the form "Fall 2018" for years from 2008 - 2017 and Fall, Summer, Spring
    '''
    try:
        if not login(session, auth):
            raise Exception("Login Error")

        io.log('Looking for ' + course_subject + catalog_number)
        query = {
            "course_subject": course_subject,
            "catalog_number": catalog_number,
            "title_keyword": title_keyword,
            "term":term_codes[term.split()[0]][int(term.split()[1]) - 2008] if term else ''
            }
        response = query_page(session, query)
        if response:
           return ps.parse_page(response.text)
        else:
            io.log("No response")
            return []
    except requests.exceptions.ConnectionError as e:
        io.log("Connection Error")
        return []


def query_page(session, query):
    '''
    Constructs and sends the POST request used to query the server.
    Returns response.
    '''
    payload = {
        'ICAction':'CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH',
        'CLASS_SRCH_WRK2_STRM$35$':query['term'],
        'SSR_CLSRCH_WRK_SUBJECT$0':query["course_subject"],
        'SSR_CLSRCH_WRK_CATALOG_NBR$1':query['catalog_number'],
        'SSR_CLSRCH_WRK_DESCR$10':query['title_keyword']
        }
    #io.log('Getting search page')
    response = session.post(search_page, data=payload)
    response = session.post(search_page, data={'ICAction':'#ICSave'})
    return response
