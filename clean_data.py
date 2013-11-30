from pandas import DataFrame
import pandas as pd
from math import log
from dateutil import parser as ps
import argparse

parser = argparse.ArgumentParser(description="transform data into the desired log return format")

parser.add_argument('-i','--inputfile', help="input file", required=False, type=str, default='data/sp500.txt')
parser.add_argument('-o', '--outputfile', help='output file', required=False, type=str, default='data/cleaned_sp500.txt')

args = parser.parse_args()


inputfile = args.inputfile
output = args.outputfile


print '[INFO] reading input file at '+inputfile

raw = pd.read_csv(inputfile, sep=',', encoding='utf-8')

clean_data = DataFrame(columns=['ticker', 'date', 'volume', 'daily_log'])

grpd = raw.groupby(['Ticker'])

for name, data in grpd:
    data = data[['Date', 'Ticker', 'Volume', 'Adj Close']]
    data.columns = ['date', 'ticker', 'volume', 'close']

    d = [0] + list(data['close'])
    d = d[:len(data['close'])]

    data['pre_close'] = d

    data = data[data['pre_close'] != 0]
    data['daily_return'] = data['close']/data['pre_close']
    data['daily_log'] = data['daily_return'].map(log)
    data['daily_return'] = data['daily_return'] - 1
    data['date'] = data['date'].apply(ps.parse)
    data = data.sort(['date']).reset_index()
    data = data[['ticker', 'date', 'volume', 'daily_log']]

    clean_data = clean_data.append(data, ignore_index=True)
    
print '[INFO] generating result at ' + output

clean_data.to_csv(output, sep=',', index=False, encoding='utf-8')
