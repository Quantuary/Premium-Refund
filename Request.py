import requests

url = 'http://localhost:5000/calculate_api'

r = requests.post(url,json={
                'premium'      : 250,
                'issue_date'   : '2020-01-11 08:15:27',
			    'start_date'   : '2020-01-15 08:15:27',
 			    'end_date'	   : '2020-01-31 08:15:27',
			    'request_date' : '2020-01-14 08:15:27',
			    'prd_grp_fin'  : 'E-comm',
                'policy_id'    : '123456'
                }
      		 )

print(r.json())
