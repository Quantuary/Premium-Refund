#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 21:28:36 2020

@author: marcus
"""
from flask import Flask, request, jsonify, render_template
from datetime import datetime
import numpy as np

app = Flask(__name__)

def y(a,b,lead_time,time_used):
    n = 2* np.log(
                (1+np.sqrt(
                        1-4*np.exp(-a*lead_time-b)*(1-np.exp(-a*lead_time-b)) 
                    
                    ))/
                 (2*np.exp(-a*lead_time-b))
                 )
    
    y = (np.exp(n*time_used/lead_time)-1)/(
                                            np.exp(n)-1)
    return y
    

def function(issue_date,start_date,end_date,request_date):
    
    a = 0.00231666274238708
    b = 1.75607152635351
    
    lead_time = (start_date-issue_date).days
    duration = (end_date-start_date).days
    time_used = (request_date-issue_date).days
    
    startday_portion = 0.048
    LT_TT = lead_time/duration 
    
    if LT_TT>5:
        alpha = -0.170799706
        coef = 0.988104113
        duration_portion =(alpha*np.log(min(55.3,LT_TT)+coef
                                        )
                            )*(1-startday_portion)
    else:
        alpha = 0.071940917
        duration_portion = (1-alpha*LT_TT)*(1-startday_portion)
    
    lead_time_portion = 1-duration_portion-startday_portion
    
    if time_used<lead_time:
        earned = y(a,b,lead_time,time_used) * lead_time_portion
        
    elif time_used<=lead_time:
        earned = y(a,b,lead_time,time_used) * lead_time_portion + startday_portion
    
    elif time_used>lead_time:
        earned = lead_time_portion + startday_portion + duration_portion/duration*(time_used-lead_time)
    
    return earned


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate',methods=['POST'])
def calculate():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [x for x in request.form.values()]
    premium = float(int_features[0])
    issue_date = datetime.strptime(int_features[1],'%Y-%m-%d').date()
    start_date = datetime.strptime(int_features[2],'%Y-%m-%d').date()
    end_date = datetime.strptime(int_features[3],'%Y-%m-%d').date()
    request_date = datetime.strptime(int_features[4],'%Y-%m-%d').date()
    
    earned = function(issue_date,start_date,end_date,request_date)
    refund = round(premium *(1-earned),2)


    return render_template('index.html', refund_amount='Eligible Refund Amount $ {}'.format(refund))
    #return print(int_features)

@app.route('/calculate_api',methods=['POST'])
def calculate_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)

    output = prediction[0]
    return jsonify({'Result':output})


if __name__ == "__main__":
    app.run(debug=True)
