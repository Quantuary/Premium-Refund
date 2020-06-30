#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:58:13 2020

@author: marcus
"""
import os
os.chdir(r"/home/marcus/Documents/Premium-Refund-master")
from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api
from datetime import datetime
import calculator as cal
import SQL
app = Flask(__name__)
api = Api(app)


def compute(request_date,prd_grp_fin,policy_id, issue_date=None, end_date=None, start_date=None, premium=None, commission=None):
   try:
       if (premium==None) or (issue_date==None) or (end_date==None) or (start_date==None) or (commission==None):
           issue_date, end_date, start_date, premium, commission = SQL.retrieve(policy_id)
       else:
           issue_date = datetime.strptime(issue_date,'%Y-%m-%d') 
           start_date = datetime.strptime(start_date,'%Y-%m-%d')  
           end_date = datetime.strptime(end_date,'%Y-%m-%d') 
           premium = float(premium)
           commission = float(commission)

       if request_date>end_date:
           msg='Sorry, your requested date is after policy expired! No Premium is refunded'  
       elif request_date<issue_date:
           msg='You cannot request a refund prior to the policy issued date'  
       else:    
            earned = cal.function(issue_date,start_date,end_date,request_date,prd_grp_fin)
            Premium_refunded = round(premium*(1-earned),2)
            returned_commission = round(commission *(1-earned),2)
            
            if Premium_refunded < round(premium,2):
                refund_type = 'partial refund'
            else :
                refund_type = 'full refund'
            
            msg = {'POLICY_ID'          : policy_id,
                   'ISSUE_DATE'         : issue_date,
                   'START_DATE'         : start_date,
                   'END_DATE'           : end_date,
                   'REQUEST DATE'       : request_date,
                   'PRD_GRP_FIN'        : prd_grp_fin,
                   'ORIGINAL_PREMIUM'   : premium,
                   'COMMISSION'         : commission,
                   'REFUND_PERCENT'     : (1-earned),
                   'PREMIUM_REFUND'     : Premium_refunded,
                   'RETURNED_COMMISSION': returned_commission, 
                   'REFUND_TYPE'        : refund_type,
                   'PROCESS_DATE'       : datetime.now()
                    }
            
   except:
       msg = SQL.retrieve(policy_id)  
   return msg
        

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate',methods=['POST'])
def calculate():
    '''
    For rendering results on HTML GUI
    '''
    policy_id = request.form['policy_id']
    premium = request.form['premium'] or None
    commission = request.form['commission'] or None
    issue_date = request.form['issue_date'] or None
    start_date = request.form['start_date'] or None
    end_date = request.form['end_date'] or None
    request_date = datetime.strptime(request.form['request_date'],'%Y-%m-%d')
    prd_grp_fin = request.form['prd_grp_fin']
            
    msg = compute(request_date,prd_grp_fin,policy_id, issue_date=issue_date, end_date=end_date, start_date=start_date, premium=premium, commission=commission)
    
    return render_template('index.html', 
                           #refund_amount='Refund Amount ${}'.format(msg['premium refunded']),
                                          data_dump = msg)

class calculate_api(Resource):
    def post(self):
        data = request.get_json(force=True)
        policy_id = data['policy_id']
        premium = data['premium'] or None
        commission = data['commission'] or None
        issue_date = data['issue_date'] or None
        start_date = data['start_date'] or None
        end_date = data['end_date'] or None
        request_date = datetime.strptime(data['request_date'],'%Y-%m-%d')
        prd_grp_fin = data['prd_grp_fin']
        
        msg = compute(request_date,prd_grp_fin,policy_id, issue_date=issue_date, end_date=end_date, start_date=start_date, premium=premium, commission=commission)
        
        return jsonify(msg)

api.add_resource(calculate_api, '/calculate_api')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False, port=5000)
