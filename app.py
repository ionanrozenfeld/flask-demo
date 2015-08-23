from flask import Flask, render_template, request, redirect, Markup
from bokeh.plotting import figure, output_file, show
from bokeh.models import Range1d
from bokeh.embed import components
import time
import datetime
import requests
import simplejson as json
import numpy as np
import pandas as pd

app = Flask(__name__)

app.stock = ''
app.script = ''
app.div = ''

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        app.script = ''
        app.div = ''
        app.stock_symbol = ''
        app.stock_name = ''

        return render_template('index.html')
    else:
        
        app.stock_symbol = request.form['stock_symbol']
        
        mydata = requests.get("https://www.quandl.com/api/v3/datasets/WIKI/"+app.stock_symbol+".json?rows=30&column_index=4")

        if 'quandl_error' in mydata.json():
            app.script = ''
            app.div = ''
            
            return render_template('error_page.html', stock_symbol = app.stock_symbol)
        else:        
            data = mydata.json()['dataset']['data']        
            dates, closing_prices = zip(*[(time.strptime(i[0], '%Y-%m-%d'),i[1]) for i in data])
            dates = [datetime.datetime(i.tm_year,i.tm_mon,i.tm_mday) for i in dates]
            dates = np.array(dates)
            dates = pd.DatetimeIndex(dates)
            dates = list(dates)
            app.stock_name = mydata.json()['dataset']['name']
            extra_text_index = app.stock_name.find("Prices, Dividends, Splits and Trading Volume")
            if extra_text_index != -1:
                app.stock_name = app.stock_name[0:extra_text_index-1]
            
            ##################################################
            ########Bokeh block##############################
        
            # select the tools we want
            TOOLS="pan,wheel_zoom,box_zoom,reset,save"
        
            p1 = figure(tools=TOOLS, plot_width=500, plot_height=500, x_axis_type="datetime", x_axis_label='Date', y_axis_label="Price ($)")
            p1.line(dates, closing_prices,line_width=3)
            p1.circle(dates, closing_prices, fill_color="red", size=6)
        
            plots = {'Red': p1}
        
            script, div = components(plots)        
            app.script = script
            app.div = div.values()[0]
            ##################################################
            ##################################################

            return redirect('/graph_page') 
            
@app.route('/graph_page')
def graph_page():
    return render_template('graph.html',stock_symbol = app.stock_symbol, stock_name = app.stock_name, scr = Markup(app.script), diiv = Markup(app.div))

if __name__ == '__main__':
  app.run()
