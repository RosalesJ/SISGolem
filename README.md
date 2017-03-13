# SISGolem
A little minion that will do your SIS checking for you.

### Installation
Simply clone the repository
```
git clone https://github.com/RosalesJ/SISGolem
cd SISGolem
```

### Requirements
* Beautiful Soup 4
* lxml

### Setup
Change the custom fields at the top of SISGolem.py.
You should at the very least change the authentication field and the class_file field.

### Usage
To check SIS for classes given criteria call:
```
search_classes(session, auth, course_subject=subject, catalog_number=number, title_keyword=keyword, term=term)
```  
* ```session```: The session started at the beginning of the main method
* ```auth```: the authentication field defined at the beginning of SISGolem.py
* ```subject``` (Optional): Format as ```"EECS"```, ```"MATH"```, ```"CHEM"```. Might cause issues if left blank
* ```number``` (Optional): Format as ```"123456"```. Might cause issues if used currently.
* ```keyword``` (Optional): Also might cause issues if used currently.
* ```term```(Optional): Formatted as ```"Fall 2016"```, ```"Spring 2016"```. If left blank will return results for the current term.

To check SIS for a list of classes call:
```
check_classes(session, auth, class_list, term='')
```
* ```session```: The session started at the beginning of the main method
* ```auth```: the authentication field defined at the beginning of SISGolem.py
* ```class_list```: Formatted as```['EECS 340', 'MATH 380', 'USSO 290']```
* ```term``` (Optional): Formatted as ```"Fall 2016"```, ```"Spring 2016"```. If left blank will return results for the current ter
