#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:58:13 2020

@author: marcus
"""

from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api
from datetime import datetime
import calculator as cal
import cx_Oracle
import pandas as pd

app = Flask(__name__)
api = Api(app)

            

def SQL_retrieve(policy_id):
    connection = cx_Oracle.connect("user","XXXX", cx_Oracle.makedsn("auwphprx-scan.maau.group",1521,"Dwin"))
    p_master = pd.read_sql_query(
        '''
        select 
        PLAN_ID, ISSUE_DATE, START_DATE, END_DATE
        from MIDAS_MV_REPLICATE.MV_POLICY_MASTER
        where POLICY_ID='%s'
          ''' %(policy_id) , con=connection)
    
    p_premium = pd.read_sql_query(
        '''
        select 
        CALCULATED_PREMIUM, ADDITIONAL_LOADING, COMMISSION, TOTAL_OWING
        from MIDAS_MV_REPLICATE.MV_POLICY_PREMIUM 
        where POLICY_ID='%s'
          ''' %(policy_id) , con=connection)
    
    plan_com = pd.read_sql_query(
        '''
        select 
        RATE
        from MIDAS_MV_REPLICATE.MV_PLAN_COMMISSION 
        where PLAN_ID='%s'
            and 
          ''' %(p_master["PLAN_ID"]) , con=connection)
        


      
    p_premium['CALCULATED_PREMIUM']+p_premium['ADDITIONAL_LOADING']
    
    connection.close()
    return p_master['ISSUE_DATE'], p_master['START_DATE'], p_master['END_DATE'] 
    
# =============================================================================
#     
#     connection = cx_Oracle.connect("aXXXX","XXXX", cx_Oracle.makedsn("auwphprx-scan.maau.group",1521,"Dwin"))
#         cursor=connection.cursor()
#         
#         ls = [tuple(x) for x in df.values]
#         
#         column_str = ','.join(list(df))
#         insert_str = ','.join([':'+each for each in list(df)])
#         final_str = "INSERT INTO %s (%s) VALUES (%s)" % \
#                   ("ML_REFUND",column_str,insert_str)
#        
#         cursor.executemany(final_str,ls)
#         connection.commit()   
#         connection.close()
# 
# =============================================================================
def compute(request_date,prd_grp_fin,policy_id):
    if request_date>end_date:
        msg='Sorry, your requested date is after policy expired! No Premium is will be refund'  
    elif request_date<issue_date:
        msg='You cannot request a refund prior to the policy issued date'    
    else:
        
        earned = cal.function(issue_date,start_date,end_date,request_date,prd_grp_fin)
        refund = round(premium *(1-earned),2)
        msg = refund 
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
    #premium = float(request.form['premium'])
    #issue_date = datetime.strptime(request.form['issue_date'],'%Y-%m-%d')
    #start_date = datetime.strptime(request.form['start_date'],'%Y-%m-%d')
    #end_date = datetime.strptime(request.form['end_date'],'%Y-%m-%d')
    request_date = datetime.strptime(request.form['request_date'],'%Y-%m-%d')
    prd_grp_fin = request.form['prd_grp_fin']
            
    msg = compute(request_date,prd_grp_fin,policy_id)
    
    return render_template('index.html', refund_amount='$ {}'.format(msg))

class calculate_api(Resource):
    def post(self):
        data = request.get_json(force=True)
        policy_id = data['policy_id']
        #premium = data['premium']
        #issue_date = datetime.strptime(data['issue_date'],'%Y-%m-%d %H:%M:%S')
        #start_date = datetime.strptime(data['start_date'],'%Y-%m-%d %H:%M:%S')
        #end_date = datetime.strptime(data['end_date'],'%Y-%m-%d %H:%M:%S')
        request_date = datetime.strptime(data['request_date'],'%Y-%m-%d %H:%M:%S')
        prd_grp_fin = data['prd_grp_fin']
        
        msg = compute(request_date,prd_grp_fin,policy_id)
        
        return jsonify({'Refund Amount':msg})

api.add_resource(calculate_api, '/calculate_api')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False, port=5000)
