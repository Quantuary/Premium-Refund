import requests

url = 'http://localhost:5000/calculate_api'

r = requests.post(url,json={
                'policy_id'    : '111',
			    'request_date' : '2020-03-18',
			    'prd_grp_fin'  : 'E-comm',
                'premium'      : '192.72',
                'commission'   : '67.45',
                'issue_date'   : '2020-03-18',
                'start_date'   : '2020-03-18',
                'end_date'     : '2020-03-30',
                }
      		 )

print(r.json())
