from flask import Flask,render_template,request,redirect,session

import requests as rq
import simplejson as json
import pandas as pd
import quandl as qd
import numpy as np

from bokeh.plotting import figure, show, output_file
from bokeh.embed import components,file_html
 
app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
    return redirect('/symbolpage')

@app.route('/symbolpage', methods=['GET'])
def retrievesymbol():
    return render_template('Symbolpage.html')

def retrievestocklink(asymbol):
    mydata = qd.get('WIKI/' + str(asymbol), start_date = '2017-04-01', end_date = '2017-04-30', authtoken='EHRdSDYVebxuv_oz13ut')
    df= pd.DataFrame(mydata)
    dfreset = df.reset_index()
    return dfreset

def makegraph(asymbol):
    gooddf=retrievestocklink(asymbol)
    sf = figure(title='Stock Price for '+ asymbol +' during April 2017')
    sf.xaxis.axis_label = 'April 2017 days'
    sf.yaxis.axis_label = 'Closing Price ($)'
    sf.xaxis.major_label_text_color = None
    sf.line(x=np.array(gooddf['Date'].values), y=np.array(gooddf['Close'].values),line_width=4, legend='Close')
    return sf

@app.route('/stockgraph', methods=['POST'])
def stockgraph():
    app.vars['stocksymbol'] = request.form['stocksymbol']
    madegraph=makegraph(app.vars['stocksymbol'])
    thescript, thediv = components(madegraph)
    return render_template('stockgraph.html', script=thescript, div=thediv)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)