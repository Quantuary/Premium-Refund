import requests

url = 'http://localhost:5000/calculate_api'

r = requests.post(url,json={
                'policy_id'    : '50427782',
			    'request_date' : '2020-01-12',
			    'prd_grp_fin'  : 'Cancellation',
                'premium'      : '192.72',
                'commission'   : '67.45',
                'issue_date'   : '2020-01-01',
                'start_date'   : '2020-01-15',
                'end_date'     : '2020-01-30',
                'policy_id'    : '50427782'
                }
      		 )

print(r.json())
