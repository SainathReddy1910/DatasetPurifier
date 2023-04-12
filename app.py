import time
import pandas as pd
import numpy as np
from flask import Flask, render_template, url_for, request,send_file,redirect
from flask import *
# data-cleaning package
from datacleaning import DataCleaning
from distutils.log import debug
from fileinput import filename
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data', methods=['GET', 'POST'])
def data():
    f = request.files['file']
    send=request.form['send']
    print(send)
    path='static/'+f.filename
    f.save(path)  
    dp = DataCleaning(file_upload=path)
    cleaned_df = dp.start_cleaning()
    if send=='HTML':
        cleaned_df.to_html('purified.html',index=False)
        return send_file('purified.html',mimetype='text/html',as_attachment=True)
    elif send=='CSV':
        cleaned_df.to_csv('purified.csv',index=False)
        return send_file('purified.csv',mimetype='text/csv',as_attachment=True)
    elif send=='XML':
        # remove special character
        cleaned_df.columns = cleaned_df.columns.str.replace(' ', '')
        cleaned_df.to_xml('purified.xml')
        return send_file('purified.xml',mimetype='text/xml',as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 