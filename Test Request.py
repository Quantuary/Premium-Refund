import requests

url = 'http://localhost:5000/calculate_api'

r = requests.post(url,json={
                "premium"      : 250,
                'issue_date'   : '2020-01-11 08:15:27.12324',
			    'start_date'   : '2020-01-15 08:15:27.12324',
 			    'end_date'	   : '2020-01-31 08:15:27.12324',
			    'request_date' : '2020-01-15 08:15:27.12324',
			    #'PRD_GRP_FIN'  : 'E-comm'
                }
      		 )

print(r.json())
