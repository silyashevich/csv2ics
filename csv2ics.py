from argparse import ArgumentParser
from csv import reader
from datetime import datetime, timedelta
from os.path import isfile
from sys import exit, exc_info
from uuid import uuid4
parser = ArgumentParser(prog='csv2ics', description='Create ics calendar file from csv data file')
parser.add_argument("-s", dest="csv_file_name", default='data.csv', type=str,
                    help='Input data file in csv format. Default value: data.csv')
parser.add_argument("-d", dest="ics_file_name", default='calendar.ics', type=str,
                    help='Output data file in ics format. Default value: calendar.ics')
parser.add_argument("-t", dest="calendar_title", default='Calendar', type=str,
                    help='Calendar title. Default value: Calendar')
parser.add_argument("-e", dest="calendar_event", default='Birthday', type=str,
                    help='Event title. Default value: Birthday')
args = parser.parse_args()
if not isfile(args.csv_file_name):
    exit(f'Error: {args.csv_file_name} not found or not a file!')
with open(args.csv_file_name, newline='') as csvfile:
    rows = list(reader(csvfile, delimiter=';'))
    if len(rows) == 0 or not all(map(lambda _: len(_) == 4, rows)):
        exit(f'Error: {args.csv_file_name} contains wrong data!')
    try:
        with open(f'{args.ics_file_name}', mode='w') as icsfile:
            current_year = datetime.now().year
            calendar_header = f'BEGIN:VCALENDAR\n' \
                              f'PRODID:-//silyashevich//Sergey Ilyashevich//EN\n' \
                              f'VERSION:2.0\n' \
                              f'CALSCALE:GREGORIAN\n' \
                              f'METHOD:PUBLISH\n' \
                              f'X-WR-TIMEZONE:Europe/Moscow\n' \
                              f'X-WR-CALNAME:{args.calendar_title}\n'
            icsfile.write(calendar_header)
            for row in rows:
                event_date_start = datetime.strptime(f'{".".join(map(lambda s: str(s).zfill(2), row[-1].split(".")[:2] + [current_year]))}', '%d.%m.%Y')
                event_date_end = event_date_start + timedelta(days=1)
                event_start = ''.join(map(lambda s: str(s).zfill(2), [event_date_start.year, event_date_start.month, event_date_start.day]))
                event_end = ''.join(map(lambda s: str(s).zfill(2), [event_date_end.year, event_date_end.month, event_date_end.day]))
                event_location = f'{row[1]} - {row[2]}'
                event_summary = f'{args.calendar_event}: {row[0]}'
                event_uid = str(uuid4())
                calendar_event = f'BEGIN:VEVENT\n' \
                                 f'CLASS:PUBLIC\n' \
                                 f'DTSTART;VALUE=DATE:{event_start}\n' \
                                 f'DTEND;VALUE=DATE:{event_end}\n' \
                                 f'SEQUENCE:0\n' \
                                 f'LOCATION:{event_location}\n' \
                                 f'SUMMARY;LANGUAGE=ru:{event_summary}\n' \
                                 f'TRANSP:TRANSPARENT\n' \
                                 f'UID:{event_uid}\n' \
                                 f'X-MICROSOFT-CDO-BUSYSTATUS:FREE\n' \
                                 f'END:VEVENT\n'
                icsfile.write(calendar_event)
            calendar_footer = f'END:VCALENDAR\n'
            icsfile.write(calendar_footer)
    except IOError as e:
        exit(f'Error: I/O error {e.errno}: {e.strerror}')
    except Exception as ex:
        exit(f'Error: {exc_info()[0]}')
