#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:03:36 2020

@author: marcus
"""

import cx_Oracle
import pandas as pd

def retrieve(policy_id):
    connection = cx_Oracle.connect("actuary","XXXX", cx_Oracle.makedsn("auwphprx-scan.maau.group",1521,"Dwin"))

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
    CALCULATED_PREMIUM, ADDITIONAL_LOADING, DISCOUNT, COMMISSION, TOTAL_OWING 
    from MIDAS_MV_REPLICATE.MV_POLICY_PREMIUM 
    where POLICY_ID='%s'
      ''' %(policy_id) , con=connection)
    
    connection.close()
    
    
    if p_premium.empty==True :
        return 'The following policy id is not found'
    else:
        issue_date = p_master["ISSUE_DATE"][0]
        end_date = p_master["END_DATE"][0]
        start_date = p_master["START_DATE"][0]
        calculated_premium=p_premium['CALCULATED_PREMIUM'][0]
        additional_loading=p_premium['ADDITIONAL_LOADING'][0]
        discount   = p_premium['DISCOUNT'][0]
        commission = p_premium['COMMISSION'][0]
        
        if calculated_premium==0:
            premium = additional_loading - discount
        else:
            premium = calculated_premium
        return issue_date, end_date, start_date, premium, commission
    