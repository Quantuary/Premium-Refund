#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 21:26:00 2020

@author: marcus
"""

from flask_restful import Resource, Api
from flask import Flask, request, jsonify
from datetime import datetime
import calculator as cal
import cx_Oracle

app = Flask(__name__)
api = Api(app)


class calculate_api(Resource):
    def post(self):
        data = request.get_json(force=True)
        premium = data['premium']
        issue_date = datetime.strptime(data['issue_date'],'%Y-%m-%d %H:%M:%S')
        start_date = datetime.strptime(data['start_date'],'%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(data['end_date'],'%Y-%m-%d %H:%M:%S')
        request_date = datetime.strptime(data['request_date'],'%Y-%m-%d %H:%M:%S')
        prd_grp_fin = data['prd_grp_fin']
        POLICY_ID = data['policy_id']
        
        if request_date>end_date:
            result = jsonify({'Sorry, your requested date is after policy expired! No Premium is will be refund'})
        
        elif request_date<issue_date:
            result =  jsonify({'You cannot request a refund prior to the policy issued date'})
            
        else:
            earned = cal.function(issue_date,start_date,end_date,request_date,prd_grp_fin)
            refund = round(premium *(1-earned),2)    
            result = jsonify({'Refund Amount':refund})
        
# =============================================================================
#         SQL database injection is place here 
# =============================================================================
        connection = cx_Oracle.connect("aXXXX","XXXX", cx_Oracle.makedsn("auwphprx-scan.maau.group",1521,"Dwin"))
        cursor=connection.cursor()
        
        ls = [tuple(x) for x in df.values]
        
        column_str = ','.join(list(df))
        insert_str = ','.join([':'+each for each in list(df)])
        final_str = "INSERT INTO %s (%s) VALUES (%s)" % \
                  ("ML_REFUND",column_str,insert_str)
       
        cursor.executemany(final_str,ls)
        connection.commit()   
        connection.close()
        
        return result

api.add_resource(calculate_api, '/calculate_api')

if __name__ == "__main__":
    app.run(debug=True,port=5001)
