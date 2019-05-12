import fix_yahoo_finance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import scipy.stats


def get_stocks_nasdaq(file, _start_date):
    df = pd.read_csv(file)
    symbols = df['Symbol']
    years = df['IPOyear']
    cutting_year = int(_start_date[0:4]) - 1
    number_stock = min(len(symbols), len(years))
    _stocks = []
    for i in range(number_stock):
        if not pd.isna(years[i]):
            if int(years[i]) <= cutting_year:
                _stocks.append(symbols[i])
    return _stocks


def get_stocks_returns(_symbol, _start_date, _end_date, _price_label):
    _symbol = _symbol
    _start_date = _start_date
    _end_date = _end_date
    _price_label = _price_label

    try:
        _stock = yf.Ticker(_symbol)
        _data = _stock.history(start=_start_date, end=_end_date)
        used_data = _data[_price_label]
        ret = []
        for i in range(len(used_data)-1):
            result = (used_data[i+1]-used_data[i])/used_data[i]
            if not np.isnan([result]).any():
                ret.append(result)
        return ret
    except:
        return []


def cal_density_real_data(_data, _bins='auto'):
    _frequency, _bins = np.histogram(_data, bins=_bins, density=True)
    return [_frequency, _bins]


if __name__ == "__main__":
    file_name = 'companylist.csv'
    start_date = '2012-01-01'
    end_date = '2018-01-01'
    price_label = 'Close'
    # stocks = get_stocks_nasdaq(file_name, start_date)
    stocks = ['^IXIC']

    data = []
    i = 0
    for stock in stocks:
        data = data + get_stocks_returns(stock, start_date, end_date, price_label)
        i += 1
        print("current/total: %d/%d " % (i, len(stocks)))

    mu = np.mean(data)
    sigma = np.sqrt(np.var(data))
    data_normalized = (data-mu)/sigma
    [frequency, bins] = cal_density_real_data(data_normalized)

    x = np.linspace(min(bins), max(bins), len(bins[1:]))

    matplotlib.rcParams.update({'font.size': 14})
    nasdaq, = plt.plot(bins[1:], frequency, 'b-', label='Nasdaq daily returns')
    gau, = plt.plot(x, scipy.stats.norm.pdf(x), 'g--', label='Gaussian samples')
    plt.legend(handles=[nasdaq, gau], loc='best', fontsize='small')
    plt.savefig('1.png', bbox_inches='tight', dpi=300)
    plt.show()
