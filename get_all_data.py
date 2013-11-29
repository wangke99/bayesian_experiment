import argparse
from pandas import DataFrame
import pandas as pd
import os

parser = argparse.ArgumentParser(description="download historical data based on configuration file")

parser.add_argument('-c', '--config', help="data configuration file", required=False, type=str, default='sp500')
parser.add_argument('-d', '--data', help='data directory', required=False, type=str, default='data/raw' )
parser.add_argument('-o', '--output', help='output file', required=False, type=str, default='data/sp500.txt')

args = parser.parse_args()


tickers = 'config/data/'+args.config + '.txt'
data = args.data
output = args.output

tickers = pd.read_csv(tickers, header=None)

tickers.columns = ['ticker']

for each in list(tickers['ticker']):
    command_string = 'python get_data.py -t '+each
    os.system(command_string)

tickers['location'] = tickers['ticker'].map(lambda x: data+'/'+x+'.csv')

data = DataFrame(columns=['Date','Open','High','Low','Close','Volume','Adj Close', 'Ticker'])

for each in tickers.itertuples():
    t = each[1]
    l = each[2]
    print '[INFO] processing data for %s at %s' % (t, l)
    d = pd.read_csv(l, sep=',', encoding='utf-8')
    d['Ticker'] = t
    data = data.append(d)

print data
data.to_csv(output, sep=',', index=False, encoding='utf-8')
print '[INFO] data generated at '+output
