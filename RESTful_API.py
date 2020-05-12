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

app = Flask(__name__)
api = Api(app)


class calculate_api(Resource):
    def post(self):
        data = request.get_json(force=True)
        premium = data['premium']
        issue_date = datetime.strptime(data['issue_date'],'%Y-%m-%d %H:%M:%S.%f')
        start_date = datetime.strptime(data['start_date'],'%Y-%m-%d %H:%M:%S.%f')
        end_date = datetime.strptime(data['end_date'],'%Y-%m-%d %H:%M:%S.%f')
        request_date = datetime.strptime(data['request_date'],'%Y-%m-%d %H:%M:%S.%f')
    
        earned = cal.function(issue_date,start_date,end_date,request_date)
        refund = round(premium *(1-earned),2)


        return jsonify({'Refund Amount':refund})


api.add_resource(calculate_api, '/calculate_api')

if __name__ == "__main__":
    app.run(debug=True)
