from flask import Flask, render_template, request, redirect, Markup
from bokeh.plotting import figure, output_file, show
from bokeh.models import Range1d
from bokeh.embed import components
import time
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
            app.stock_name = mydata.json()['dataset']['name']
            data = mydata.json()['dataset']['data']        
            dates, closing_prices = zip(*[(time.strptime(i[0], '%Y-%m-%d'),i[1]) for i in data])
            dates = np.array(dates)
            dates = pd.DatetimeIndex(dates)
            dates = "Date"
            
            #f=open("aaa",'w')
            #print >>f, dates
            #print >>f, closing_prices
            #f.close()
            
            ##################################################
            ########Bokeh block##############################
        
            # select the tools we want
            TOOLS="pan,wheel_zoom,box_zoom,reset,save"
        
            p1 = figure(tools=TOOLS, plot_width=500, plot_height=500, x_axis_type="datetime", x_axis_label='Date', y_axis_label="Price ($)")
            p1.line(dates.index, closing_prices,line_width=3)
            p1.circle(dates.index, closing_prices, fill_color="red", size=6)
        
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
