from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, output_file, show
import Quandl

app = Flask(__name__)

app.stock = ''
app.closing = 0

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.stock = request.form['stock_name']
    
        mydata = Quandl.get("WIKI/"+app.stock, rows=30)
        
        dates = mydata.Close.index
        closing_price = mydata.Close.values
        app.closing = closing_price[0]
        
        f= open('check','w')
        print >>f, app.closing
        f.close()
        
        return redirect('/graph_page') 

@app.route('/graph_page')
def graph_page():
    
    return render_template('graph.html',stock_symbol = app.stock, closing = app.closing)

if __name__ == '__main__':
  app.run(port=33507)
