# csv2ics
Create ics calendar file on **current year** from csv data file

usage:

```
csv2ics [-h] [-s CSV_FILE_NAME] [-d ICS_FILE_NAME] [-t CALENDAR_TITLE] [-e CALENDAR_EVENT]
```

Create ics calendar file from csv data file

options:

    -h, --help         show this help message and exit
    -s CSV_FILE_NAME   Input data file in csv format. Default value: data.csv
    -d ICS_FILE_NAME   Output data file in ics format. Default value: calendar.ics
    -t CALENDAR_TITLE  Calendar title. Default value: Calendar
    -e CALENDAR_EVENT  Event title. Default value: Birthday

csv row example:

    Садьдо Жанна Игоревна;Горячий цех;Инженер;2.01.
    Николаев Николай Николаевич;Складской терминал;Водитель погрузчика;21.05.1911
    James Smith;Blacksmith Workshop;Worker;12.03.1982    


Compile to one file:
```
nuitka --standalone --onefile csv2ics.py 
```