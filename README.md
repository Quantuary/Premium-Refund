## Premium Refund Calculator
This calculator accurately calculate the unearned premium based on **SIX** input parameters by applying the company reserving method.

### Prerequisites
You must have python3.7.4 and above install. Other required packages can be aquired via:<br>
`pip install -r requirements.txt`.

### Parameter required are:
**FIVE** out of **SIX** parameters can be to drawn directly from the data. 
1. Premium - The original GWP/Premmium charged to the policyholders/customers.
2. Issue Date - The date when the policy is underwritten.
3. Start Date - The initial start date of the trip/journey.
4. End Date - The expiry date of the policy or when the policy become ineffective.
5. Request Date - The date in which refund begain to take effect from.
6. Product Group Finance - Segmentation information provided by B.I.



### Running Web Application
`python webapp.py`

### Running RESTful API as a service
`python RESTful_API.py`

### Data format
Data format **POST** to API must follow a json format as below:<br>
{
"premium"      : 250,<br>
'issue_date'   : 'yyyy-mm-dd HH:MM:SS',<br>
'start_date'   : 'yyyy-mm-dd HH:MM:SS',<br>
'end_date'     : 'yyyy-mm-dd HH:MM:SS',<br>
'request_date' : 'yyyy-mm-dd HH:MM:SS',<br>
'prd_grp_fin'  : 'E-comm'<br>
}<br>

Test example is in `request.py`
