import lxml
from bs4 import BeautifulSoup as bs
import golemio as io

def parse_page(page):
    '''
    Parses raw XML response page.
    Returns list of classes if the page is parsable.
    Otherwise returns empty list.
    Each element in the list is formatted as
    [Term, Status, Name, Title, Catalog #, Times, Room, Instructor, Dates, Enrl Cap, Enrl Cap]
    '''
    # uncomment to write every incoming page to a random file in temp/
    #io.write_page('temp/' + str(uuid.uuid4())[:5] + '.html', page)
    #io.log('Parsing page')
    if "The search returns no results that match the criteria specified." in page:
        io.log('No search results match criteria')
        return []

    soup = bs(page, 'lxml')
    term = soup.find_all('span', {'id':'DERIVED_CLSRCH_SSS_PAGE_KEYDESCR'})[0].text.split(' | ')[1]
    tables = soup.find_all('table',{'dir':'ltr', "class":"PSLEVEL1GRID"})
    if not tables:
        tables = soup.find_all('table',{'role':'presentation', 'class':"PSLEVEL1SCROLLAREABODY"})
        io.log('So few search results currently unsupported')
        return []         #no support for fewer than 20 results currently

    table = tables[0]
    contents = table.find_all('tr')

    return [[term] + parse_item(contents[i]) for i in range(1, len(contents))]


def parse_item(item):
    '''
    Parses individual table items which come in formatted as:
    [Name - Title, Catalog_number, Session, Days & Times, Room(Capacity),
                Instructor, Dates, Enrollment Cap, Enrolled, Fee, Select Class]
    They are returned as
    [Status, Name, Title, Catalog #, Times, Room, Instructor, Dates, Enrl Cap, Enrl Cap]
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


def format_line(line, display_array):
    '''Prints and formats a single line for output'''
    for i in range(len(line)):
        if display_array[i] != 0:
           if display_array[i] < len(line[i]):
               print(line[i][0:display_array[i]], end=' | ')
           else:
               print(line[i].ljust(display_array[i]), end=' | ')
    print()
