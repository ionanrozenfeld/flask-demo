from flask import Flask, render_template, request, redirect, Markup
from bokeh.plotting import figure, output_file, show
import Quandl
from bokeh.plotting import figure
from bokeh.models import Range1d
from bokeh.embed import components
import datetime

app = Flask(__name__)

app.stock = ''
app.closing = 0
app.script = ''
app.div = Markup("<h1>hola</h1>")

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.stock = request.form['stock_name']
        
        #now = datetime.datetime.now()
        #today = 2"%s-%s-%s" % (now.year, now.month, now.day)
        #last_month = "%s-%s-%s" % (now.year, now.month-1, now.day)
        mydata = Quandl.get("WIKI/"+app.stock, rows = 30)
        
        dates = mydata.Close.index
        #dates = range(len(dates))
        closing_prices = list(mydata.Close.values)
        
        #f= open('check','w')
        #print >>f, app.closing
        #f.close()
        
        ##################################################
        ########Blokeh block##############################
        
        # select the tools we want
        TOOLS="pan,wheel_zoom,box_zoom,reset,save"
        
        # the red and blue graphs will share this data range
        #xr1 = Range1d(start=0, end=30)
        #yr1 = Range1d(start=0, end=30)
        
        # only the green will use this data range
        #xr2 = Range1d(start=0, end=30)
        #yr2 = Range1d(start=0, end=30)
        
        # build our figures
        p1 = figure(tools=TOOLS, plot_width=500, plot_height=500, x_axis_type="datetime", x_axis_label='Date', y_axis_label="Price ($)")
        p1.line(dates, closing_prices,line_width=3)
        p1.circle(dates, closing_prices, fill_color="red", size=6)
        
        # plots can be a single PlotObject, a list/tuple, or even a dictionary
        plots = {'Red': p1}
        
        script, div = components(plots)        
        app.script = script
        app.div = div.values()[0]
        ##################################################
        ##################################################

        
        return redirect('/graph_page') 

@app.route('/graph_page')
def graph_page():
    
    return render_template('graph.html',stock_symbol = app.stock, scr = Markup(app.script), diiv = Markup(app.div))

if __name__ == '__main__':
  app.run()
