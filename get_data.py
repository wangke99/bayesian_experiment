import argparse
import requests
import datetime

parser = argparse.ArgumentParser(description="download historical data from yahoo finance")

parser.add_argument('-t','--ticker', help="company ticker", required=True, type=str)
parser.add_argument('-a', '--from_month', help='from month', required=False, type=int, default=1)
parser.add_argument('-b', '--from_day', help='from day', required=False, type=int, default=1)
parser.add_argument('-c', '--from_year', help='from year', required=False, type=int, default=2011)
parser.add_argument('-d', '--to_month', help='to month', required=False, type=int, default=11)
parser.add_argument('-e', '--to_day', help='to day', required=False, type=int, default=28)
parser.add_argument('-f', '--to_year', help='to year', required=False, type=int, default=2013)
parser.add_argument('-o', '--output', help='output directory', required=False, type=str, default='data/raw/')

args = parser.parse_args()


ticker = args.ticker
from_month = args.from_month
from_day = args.from_day
from_year = args.from_year
to_month = args.to_month
to_day = args.to_day
to_year = args.to_year

output = args.output

try:
    start = datetime.date(from_year, from_month, from_day)
except:
    print '[ERROR] Invalid start date'
    quit()

try:
    end = datetime.date(to_year, to_month, to_day)
except:
    print '[ERROR] Invalid end date'
    quit()

def format_date(s):
    s = str(s)
    if len(s) == 1:
        return '0'+s
    else:
        return s
    
from_month = format_date(from_month)
from_day = format_date(from_day)
to_month = format_date(to_month)
to_day = format_date(to_day)
from_year = str(from_year)
to_year = str(to_year)

url = 'http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s' % (ticker, from_month, from_day, from_year, to_month, to_day, to_year)

print '[INFO] getting historical data for ' + ticker

r = requests.get(url)

if r.status_code != 200:
    print '[ERROR] Cannot get Yahoo data'
    print r.status_code
    quit()

output = output+ticker+'.csv'
    
f = open(output, 'w')
f.write(r.text)
f.close()