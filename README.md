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
Customize the necessary fields in ```settings.xml```. To begin it is enough to change the default username and password.

### Usage
Call sisgolem from the command line. It can get you a select few classes:

```
$ sisgolem EECS340 MATH308 PHYS221
20:30:14 ::: Logging into SIS
20:30:17 ::: Logged into SIS
20:30:20 ::: Looking for PHYS
20:30:33 ::: Looking for MATH
20:30:45 ::: Looking for EECS
--------------------------------------------------------------------
Status | Name      | Title                  | Times                |
--------------------------------------------------------------------
Open   | PHYS 221  | Introduction to Modern | MWF 3:20PM - 4:10PM  |
Open   | PHYS 221  | Introduction to Modern | Th 10:00AM - 10:50AM |
Open   | PHYS 221  | Introduction to Modern | Th 1:00PM - 1:50PM   |
Open   | MATH 308  | Introduction to Abstra | MWF 9:30AM - 10:20AM |
Closed | EECS 340  | Algorithms             | MW 12:45PM - 2:00PM  |
--------------------------------------------------------------------
Total Results: 5
Total Closed: 1
Total Open: 4
--------------------------------------------------------------------
```
Or tell you what a class does over time:
```
$ sisgolem EECS340 --terms fall2013 spring2014 fall2014 spring
2015 fall2015 spring2016
------------------------------------------------------------------
Term        | Name      | Instructor         | EnrlCap | EnrlTot |
------------------------------------------------------------------
Fall 2013   | EECS 340  | Mehmet Koyuturk    | 60      | 54      |
Spring 2014 | EECS 340  | Vincenzo Liberator | 30      | 29      |
Fall 2014   | EECS 340  | Mehmet Koyuturk    | 60      | 68      |
Spring 2015 | EECS 340  | Vincenzo Liberator | 50      | 50      |
Fall 2015   | EECS 340  | Mehmet Koyuturk    | 40      | 39      |
Fall 2015   | EECS 340  | Vincenzo Liberator | 40      | 33      |
Spring 2016 | EECS 340  | Mehmet Koyuturk    | 40 (40) | 43 (48) |
Spring 2016 | EECS 340  | Mehmet Koyuturk    | 40 (40) | 5 (48)  |
------------------------------------------------------------------
```
Or read and write classes from files:
```
sisgolem --input ~/Documents/School/Classes.csv --output tem
p/output.csv
20:53:05 ::: Logging into SIS
20:53:08 ::: Logged into SIS
20:53:12 ::: Looking for MATH
20:53:24 ::: Looking for EECS
20:53:38 ::: Classes not found
EECS 337
20:53:38 ::: Writing classes to temp/output.csv
-------------------------------------------------------------
Status | Name      | Times                | Room            |
-------------------------------------------------------------
Closed | MATH 303  | MWF 11:40AM - 12:30P | To Be Scheduled |
Closed | EECS 325  | MW 3:20PM - 4:35PM   | To Be Scheduled |
Closed | EECS 440  | TuTh 10:00AM - 11:15 | To Be Scheduled |
-------------------------------------------------------------
Total Results: 3
Total Closed: 3
Total Open: 0
-------------------------------------------------------------
```
SISGolem is pretty flexible.
## Arguments
##### Classes
The core compitency of SISGolem and it's main argument. SISGolem can look up an arbitrary number of classes, so go crazy.
```
$ sisgolem EECS132 EECS223 MATH121 MATH121 MATH122 MATH233 CHEM111
```
* Classes shoud be formatted as ```EECS132```, ```math122```, ```phys121``` with no spaces
* Classes are case insensitive
* A class with no course number will return all classes under subject. so ```$ sisgolem MATH``` will return all math classes
* Classes can be left blank in the case that classes are being read from an input file
##### Term
SISGolem can check classes in an arbitrary number of terms using the argument ```-t TERMS [TERMS ...], --terms TERMS [TERMS ...]```.
```
$ sisgolem eecs132 eecs223 -t spring2012 fall2013
```
* Terms should be formatted as ```spring2013```, ```summer2012```, ```fall2016```, for any year between 2008 and current year
* Terms are case insensitive
* Term defaults to current term if not specified
* When multiple terms and classes are specified all classes will be returned in all terms.

If used, terms should be specified after classes. Otherwise SISGolem won't know where the terms finish and the classes start. For example:
```
$ sisgolem -t spring2012 fall2013 eecs132 eecs223
```
Will mistake ```eecs132 and eecs223``` as terms. The intended behaviour is achieved using the example at the beginning of this section.
##### Authentication
SISGolem uses the username and password defined in ```settings.xml``` by default, but they can be overridden from the command line using the ```-a [AUTH], --auth [AUTH]``` where ```AUTH``` is in the form ```username:password```.
```
$ sisgolem -a jxr450:password EECS132
```
##### Input/Output
You can configure input and output files for SISGolem to push and pull classes from. Use the arguments ```-o [OUTPUT], --output [OUTPUT]  ``` and ```-i [INPUT], --input``` where ```OUTPUT, INPUT``` are the paths to output/input csv files. If either is left blank then SISGolem will use the default input/output files.
```
$ sisgolem -i -o
```
Will take classes from the default input, and output results to the default output. Both defaults are defined in ```settings.xml```.

If arguments are left blank they should be specified before the classes, otherwise the first class might be mistaken as an input or output. For example:
```
$ sisgolem -i MATH380 MATH303
```
The intent is to use the default input, and search for ```MATH380``` and ``` MATH303```, but ```MATH380``` will be mistaken as the input file and sisgolem will throw a file not found error. The intended behaviour is achieved with.
```
$ sisgolem MATH380 MATH303 -i
```

##### Verbosity
Control what SISGolem will tell you during and after searching for classes by using the ```-v {0,1,2}, --verbose {0,1,2}``` argument. This argument can only take on three values.
* 0 : Completely quiet. No console output.
* 1 : Disabled log output. Only final class diplay enabled.
* 2 : (Default) Both log and final display are enabled.
```
$ sisgolem -v 1 MATH121
-------------------------------------------------------------------
Term       | Status | Name      | Title    | Times                |
-------------------------------------------------------------------
Fall 2017  | Open   | MATH 121  | Calculus | MWF 9:30AM - 10:20AM |
Fall 2017  | Open   | MATH 121  | Calculus | Tu 11:30AM - 12:20PM |
-------------------------------------------------------------------
Total Results: 2
Total Closed: 0
Total Open: 2
--------------------------------------------------------------------
```
