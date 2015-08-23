from flask import Flask, render_template, request, redirect, Markup
from bokeh.plotting import figure, output_file, show
import Quandl
from bokeh.plotting import figure
from bokeh.models import Range1d
from bokeh.embed import components
import datetime

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
        return render_template('index.html')
    else:
        app.script = ''
        app.div = ''
        app.stock = ''
        
        app.stock = request.form['stock_name']
        
        try:
            mydata = Quandl.get("WIKI/"+app.stock, rows = 30)
            dates = mydata.Close.index
            closing_prices = list(mydata.Close.values)
            
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
            
        except:
            app.script = ''
            app.div = ''
            
            return render_template('error_page.html', stock_symbol = app.stock)
                    

@app.route('/graph_page')
def graph_page():
    return render_template('graph.html',stock_symbol = app.stock, scr = Markup(app.script), diiv = Markup(app.div))

if __name__ == '__main__':
  app.run()
