import csv
from datetime import datetime

def log(event):
    '''Logs a string event, currently prints to command line'''
    # if verbose == 2:
    print(str(datetime.now().strftime('%H:%M:%S')) + ' ::: ' + str(event))

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


def read_csv(file_path):
    class_list = []
    with open(file_path) as file:
        reader = csv.reader(file)
        for row in reader:
            for element in row:
                if element.startswith(u'\ufeff'):
                    element = element[1:]
                    if element:
                        for e in element.split('\t'):
                            if e:
                                class_list.append(e)
    return class_list

def output(classes, display_dict):
    '''Writes classes in a pretty box given a list of classes and the display dict'''
    # if verbose >= 1 :
    display_array = [x[1] for x in display_dict]
    width =  sum(display_array) + 3*len([x for x in display_array if x]) - 1
    if classes:
        print('-'*width)
        open_classes = [x for x in classes if x[1] == "Open"]
        format_line([x[0] for x in display_dict], display_array)
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
