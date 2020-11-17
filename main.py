from bs4 import BeautifulSoup as bs4
import urllib.request, json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dt
from sklearn.metrics import r2_score

def get_values(amount , obj):
    
    with urllib.request.urlopen(f"http://api.nbp.pl/api/exchangerates/rates/a/{obj}/last/{amount}/?format=json") as url:
        data = json.loads(url.read().decode())
        values = []
        date=[]
        #print(data)
        for f in range(0,amount):
            values.append(data['rates'][f]['mid'])
            date.append(data['rates'][f]['effectiveDate'])
        x = np.array([date, values])
        return x
def create_plot(table):
    x = []
    for f in range(0,np.size(table[0])):
        x.append(f)

    model = np.poly1d(np.polyfit(x, table[1].astype('f'), len(x)))
    line = np.linspace(1, x[-1], len(x)-1)
    score = r2_score(table[1].astype('f'), model(x))

    fig = plt.figure()
    ax1 = fig.add_subplot()
    
    ax1.plot(table[1].astype('f'), 'o-c', ms=5, label='Real Data')
    plt.plot(line, model(line), label='Polynomial regression')   
    
    ax1.set_title('Kurs USD')
    ax1.set_xlabel('Data')
    ax1.set_ylabel('Notowanie')
    ax1.text(4, 1
    , 'R^2 = {0}'.format(score), ha='left')
    ax1.legend()
    plt.show()
    print('R^2 = {0}'.format(score))
    print('Next predicted value = {0}'.format(model(len(x)+1)))


table = get_values(90, 'usd')
create_plot(table)
