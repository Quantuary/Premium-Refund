#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 21:28:36 2020

@author: marcus
"""

import numpy as np

parm_startday = {
                "Ticket"       : 0.360211775,
                "E-comm"       : 0.047960282,
                "Corporate"    : 0.,
                "Cancellation" : 0.241505279,
                "Trad & Other" : 0.054981764
                }

alpha_linear ={"E-comm"       : 0.071940917,
                "Trad & Other" : 0.104720535}
                
alpha_log ={"E-comm"       : -0.170799706,
            "Trad & Other" : -0.185327377,
            "Cancellation" : -0.098980333}

coef_log ={"E-comm"       : 0.988104113,
            "Trad & Other" : 0.910074186,
            "Cancellation" : 0.397359904}


def earn_LT(a,b,lead_time,time_used):
    if lead_time==0:
        y=0
    else:
        n = 2* np.log(
                (1+np.sqrt(
                        1-4*np.exp(-a*lead_time-b)*(1-np.exp(-a*lead_time-b)) 
                    
                    ))/
                 (2*np.exp(-a*lead_time-b))
                 )
    
        y = (np.exp(n*time_used/lead_time)-1)/(
                                            np.exp(n)-1)
    return y

def log_or_linear(LT_TT,startday_portion,prd_grp_fin):
    
    if LT_TT>5:
        alpha = alpha_log[prd_grp_fin]
        coef = coef_log[prd_grp_fin]
        duration_portion =(alpha*np.log(min(55.3,LT_TT))+coef
                                      )*(1-startday_portion)
    else:
        alpha = alpha_linear[prd_grp_fin]
        duration_portion = (1-alpha*LT_TT)*(1-startday_portion)
    return duration_portion


def earn_duration(LT_TT,startday_portion,prd_grp_fin):

    if prd_grp_fin == "E-comm":
        duration_portion=log_or_linear(LT_TT,startday_portion,prd_grp_fin)
        
    elif prd_grp_fin == "Trad & Other":
        duration_portion=log_or_linear(LT_TT,startday_portion,prd_grp_fin)
    
    elif prd_grp_fin == "Cancellation":
        if LT_TT>0.1:
            alpha = alpha_log[prd_grp_fin]
            coef = coef_log[prd_grp_fin]
            duration_portion =(alpha* np.log(min(55.3,LT_TT) )+coef
                                      )*(1-startday_portion)
        else: # required confirmation from reserving!
            duration_portion = 1 *(1-parm_startday[prd_grp_fin])
            
    elif prd_grp_fin == "Corporate":
        duration_portion=1
    
    return duration_portion
    
        
def function(issue_date,start_date,end_date,request_date,prd_grp_fin):
    
    a = 0.002316663
    b = 1.756071526
    
    lead_time = (start_date-issue_date).days
    duration = (end_date-start_date).days
    time_used = (request_date-issue_date).days
    
    startday_portion = parm_startday[prd_grp_fin]

    if prd_grp_fin != "Ticket":
        LT_TT = lead_time/duration 
        duration_portion = earn_duration(LT_TT,startday_portion,prd_grp_fin)
        lead_time_portion = max((1-duration_portion-startday_portion),0) # prevent leadtime portion going negative due to error
        

        y = earn_LT(a,b,lead_time,time_used)
        if time_used<=lead_time:
            earned = y * lead_time_portion
            
        elif time_used>lead_time:
            earned = lead_time_portion + startday_portion + duration_portion/duration*(time_used-lead_time)
    
    elif prd_grp_fin == "Ticket":
        duration_portion=0
        lead_time_portion = 1-duration_portion-startday_portion
        
        if time_used<lead_time:
            x = time_used/lead_time
            y = (895.43283*x**10 - 2973.34742*x**9 + 3160.22821*x**8 - 
                 2683.4742*x**6 + 2399.6224*x**5 - 985.8713*x**4 + 208.5337*x**3 - 21.1719*x**2 + 0.9768*x)
            
            earned = y*lead_time_portion
        else:
            earned = lead_time_portion + startday_portion 
    return earned
