from django.shortcuts import render
import requests
from datetime import datetime
import plotly.express as px


def home(request):
    global list
    re = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&x_cg_api_key=CG-Wdt1LGaFii5mRzqGyZoJm3MC')
    list = re.json()
    return render(request,'Home.html',{'p': list})
def coin(request,name):
    coin_name = name
    for i in list:
        if (i['name'] == coin_name) :
            re= requests.get('https://api.coingecko.com/api/v3/coins/{}/market_chart?vs_currency=usd&days=7'.format(i['id']))
            data=re.json()
            ts =[ datetime.fromtimestamp(x[0]/1000) for x in data['prices']]
            pr=[ y[1] for y in data['prices']]
            # print(datetime.fromtimestamp(1545730073))
            # for t in range(len(ts)):
            #     ts[t]=datetime.fromtimestamp(ts[t]/1000)
            df={'ts':ts,'pr': pr}
            fig = px.line(df,x=ts,y=pr,title="7 Day's History ",labels={'x':"Date and Time",'y':"Price in $"})
            fig.update_layout(title={'font_size':25,'xanchor': 'center','x':0.5})
            chart = fig.to_html()
            return render(request,'coin.html',{'c':i,'chart':chart,'data':data})
    return render(request,'coin.html',{'c':list})
