#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:58:13 2020

@author: marcus
"""

from flask import Flask, request, render_template
from datetime import datetime
import calculator as cal
import cx_Oracle

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate',methods=['POST'])
def calculate():
    '''
    For rendering results on HTML GUI
    '''
    policy_id = request.form['policy_id']
    premium = float(request.form['premium'])
    issue_date = datetime.strptime(request.form['issue_date'],'%Y-%m-%d')
    start_date = datetime.strptime(request.form['start_date'],'%Y-%m-%d')
    end_date = datetime.strptime(request.form['end_date'],'%Y-%m-%d')
    request_date = datetime.strptime(request.form['request_date'],'%Y-%m-%d')
    prd_grp_fin = request.form['prd_grp_fin']
            
    if request_date>end_date:
        return render_template('index.html', refund_amount='Sorry, your requested date is after policy expired! No Premium is will be refund')
     
    elif request_date<issue_date:
        return render_template('index.html', refund_amount='You cannot request a refund prior to the policy issued date')
            
    else:
        earned = cal.function(issue_date,start_date,end_date,request_date,prd_grp_fin)
        refund = round(premium *(1-earned),2)
    
        return render_template('index.html', refund_amount='Eligible Refund Amount $ {}'.format(refund))
        #return print(int_features)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
