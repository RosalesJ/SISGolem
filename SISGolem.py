import re
import csv
import time
import uuid
import lxml
import requests
import tempfile
from datetime import datetime
from bs4 import BeautifulSoup as bs
from collections import OrderedDict

classes_file = '/Users/cobyrosales/Documents/School/Classes.csv'
login_page =  'https://sismobile.case.edu/app/profile/logintoapp'
search_page = "https://sis.case.edu/psc/P90SCWR_1/EMPLOYEE/P90SCWR/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL"
authentication = ('Username', 'Password')

#[Status, Name, Title, Catalog Number, Times, Room, Instructor, Dates, Cap, Enrolled]
display_array = [6, 9, 20, 0, 20, 0, 10, 0, 0, 0]
seconds_between_requests = 20

def log(event):
    '''Logs a string event, currently prints to command line'''
    print(str(datetime.now().strftime('%H:%M:%S')) + ' ::: ' + str(event))


def logged_in(page_response):
    '''Checks if logged in given a page response'''
    return "ERP Student Information System Sign-in" not in page_response


def login(session, auth):
    '''Logs session into SIS'''
    log('Logging into SIS')
    payload = {
        'username': auth[0],
        'password': auth[1],
        'loginAction': '',
        'institution': 'CASE1'
    }
    response = session.post(login_page, data=payload)
    try:
        if "incorrect" in response.text:
            log('Wrong username or password')
            return False
    except Exception as e:
        log('Exception Raised while logging in:')
        log(str(e))
        log("Authentication Error")
        return False
    return True


def search_classes(session, auth, course_subject='', catalog_number='', title_keyword=''):
    '''
    Searches for classes given some criteria.
    Logs user in if not already logged in.
    Returns list of classes if everything works, otherwise returns empty list.
    '''
    try:
        response = session.get(search_page)
        if not logged_in(response.text):
            if not login(session, auth):
                raise Exception("Login Error")
            else:
                log("Logged into SIS")

            response = session.get(search_page).text

        query = {
            "course_subject": course_subject,
            "catalog_number": catalog_number,
            "title_keyword": title_keyword
            }
        response = query_page(session, query)
        if response:
           return parse_page(response.text)
        else:
            log("No response")
            return []
    except requests.exceptions.ConnectionError as e:
        log("Connection Error")
        return []


def query_page(session, query):
    '''
    Constructs and sends the POST request used to query the server.
    Returns response.
    '''
    payload = {
        'ICAction':'CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH',
        'SSR_CLSRCH_WRK_SUBJECT$0':query["course_subject"],
        'SSR_CLSRCH_WRK_CATALOG_NBR$1':query['catalog_number'],
        'SSR_CLSRCH_WRK_DESCR$10':query['title_keyword']
        }
    #log('Getting search page')
    response = session.post(search_page, data=payload)
    response = session.post(search_page, data={'ICAction':'#ICSave'})
    return response


def parse_page(page):
    '''
    Parses raw XML response page.
    Returns list of classes if the page is parsable.
    Otherwise returns empty list.
    '''
    # uncomment to write every incoming page to a random file in temp/
    #write_page('temp/' + str(uuid.uuid4())[:5] + '.html', page)
    #log('Parsing page')
    if "The search returns no results that match the criteria specified." in page:
        log('No search results match criteria')
        return []

    soup = bs(page, 'lxml')
    tables = soup.find_all('table',{'dir':'ltr', "class":"PSLEVEL1GRID"})
    if not tables:
        tables = soup.find_all('table',{'role':'presentation', 'class':"PSLEVEL1SCROLLAREABODY"})
        log('So few search results currently unsupported')
        return []         #no support for fewer than 20 results currently

    table = tables[0]
    contents = table.find_all('tr')

    return [parse_item(contents[i]) for i in range(1, len(contents))]


def parse_item(item):
    '''
    Parses individual table items which come in formatted as:
    [Name - Title, Catalog_number, Session, Days & Times, Room(Capacity),
                Instructor, Dates, Enrollment Cap, Enrolled, Fee, Select Class]
    They are returned as
    [Status, Name, Title, Catalog #, Times, Room, Instructor, Dates, Cap, Enrolled]
    '''
    cls = []
    if item:
        elements = [x.text for x in item('span')]
        name = re.sub('[^a-zA-Z0-9- \.]', '', elements[0]).split(' - ')
        number = elements[1][elements[1].find("(")+1:elements[1].find(")")]
        cls.append(item('img')[0]['alt'])  # Status
        cls.append(name[0])                # name
        cls.append(name[1])                # title
        cls.append(number)                 # catalog number
        cls = cls + elements[3:9]          # times, room, instructor, dates, cap, enrolled
    return cls


def output(classes, display_array):
    '''Writes classes in a pretty box given a list of classes and the display array'''
    width =  sum(display_array) + 3*len([x for x in display_array if x]) - 1
    if classes:
        print('-'*width)
        open_classes = [x for x in classes if x[0] == "Open"]
        format_line(['Status', 'Name', 'Title', 'Cat #', 'Times', 'Room',
                        'Instructor', 'Dates', 'Enr Cap', 'Enr Tot'], display_array)
        print('-'*width)
        try:
            for line in classes:
                format_line(line, display_array)
        except Exception as e:
            log(str(e))
            log("Error in error print")

        print('-'*width)
        print("Total Results: " + str(len(classes)))
        print("Total Closed: " + str(len(classes) - len(open_classes)))
        print("Total Open: " + str(len(open_classes)))
        print('-'*width)


def format_line(line, display_array):
    '''Prints and formats a single line for output'''
    for i in range(len(line)):
        if display_array[i] != 0:
           if display_array[i] < len(line[i]):
               print(line[i][0:display_array[i]], end=' | ')
           else:
               print(line[i].ljust(display_array[i]), end=' | ')
    print()


def write_page(file_path, response):
    '''Write raw text response to file at file_path'''
    log("Writing page to " + file_path)
    with open(file_path, 'w') as file:
        file.write(response)


def write_csv(file_path, classes):
    '''Write class list classes to csv file at file_path'''
    log("Writing classes to " + file_path)
    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(classes)


def check_classes(session, auth, class_list):
    '''
    Checks if a list of classes given by class_list are available on SIS
    Returns list of classes currently available on SIS
    '''
    subjects = {cls[:4] : [y[5:] for y in class_list if y[:4] == cls[:4]] for cls in class_list}
    available_classes = []
    try:
        for subject in subjects:
            log('Looking for ' + subject)
            classes = search_classes(session, authentication, course_subject=subject)
            if not classes:
                log('No results')
            else:
                for cls in classes:
                    if cls[1] in class_list:
                        #log('Available class: ' + cls[1])
                        available_classes.append(cls)
    except Exception as e:
        log(str(e))
        return []
    return available_classes


def monitor_classes(session, auth, class_list):
    '''
    Periodically checks if a list of classes given by class_list are available on SIS
    Prints new classes as they become available
    '''
    working_classes = OrderedDict()
    try:
        while True:
            classes = check_classes(session, auth, class_list)
            if classes:
                new_classes = []
                for cls in classes:
                    if cls[7] not in working_classes:
                        working_classes[cls[7]] = cls
                        new_classes.append(cls)
                if(new_classes):
                    output(new_classes, display_array)
                log("New Classes: " + str(len(new_classes)))
                log("Old Classes: " + str(len(working_classes) - len(new_classes)))

                #output([x for x in working_classes.values()], display_array)
                time.sleep(seconds_between_requests)
    except KeyboardInterrupt:
        print()
        log("Exit")


def main():
    class_list = []
    with open(classes_file) as file:
        reader = csv.reader(file)
        for row in reader:
            for element in row:
                if element.startswith(u'\ufeff'):
                    element = element[1:]
                if element:
                    class_list.append(element)

    session = requests.session()

    classes = check_classes(session, authentication, class_list)
    write_csv('temp/classes.csv', classes)
    output(classes, display_array)


if __name__ == '__main__':
    main()
