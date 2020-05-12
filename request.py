import requests

url = 'http://localhost:5000/calculate_api'

r = requests.post(url,json={'issue_date'   : 2020-01-31,
			    'start_date'   : 2020-02-04,
 			    'end_date'	   : 2020-02-28
			    'request_date' : 2020-02-14
			    'PRD_GRP_FIN'  : 'E-comm'}
      		 )

print(r.json())
