# Premium Refund Calculator
This calculator accurately calculates the unearned premium based on **SEVEN** input parameters by applying the actuarial reserving method.
**SIX** out of **SEVEN** parameters can be found in the database and one required manual input from the end-user.

### Table of Contents
<details>
    <summary>click to expand</summary>
    
* [Running RESTful API](#running-restful-api)
	* [1. Run directly on python](#1-run-directly-on-python)
	* [2. Run using docker container](#2-run-using-docker-container)
	* [Data format](#data-format)
    * [Definition of Parameters](#definition-of-parameters)
* [Running Web Application](#running-Web-application)
* [Calculation Methodology](#calculation-methodology)
	* [Summary](#summary)
	* [Start Day portion](#start-day-portion)
    * [Trip Duration portion](#trip-duration-portion)
    * [Lead Time portion](#lead-time-portion)
    

</details>


## Running RESTful API
The service on a  docker container or directly via python.
### 1. Run directly on python
You must have python3.7.4 and above install. Other required packages can be acquired via:<br>
`pip install -r requirements.txt`<br>

To run the service:<br>
`python run.py`

### 2. Run using docker container
First build the docker image by `docker build -t <image name> .`. 
Then simple run `docker run -p <port to map>:5000 <image name>`.



### Data format
The service take a json post request and returned the refund amount. The data **must** be in the the following structure:<br>
```
{"premium"     : $$$.$$,
'issue_date'   : 'yyyy-mm-dd HH:MM:SS',
'start_date'   : 'yyyy-mm-dd HH:MM:SS',
'end_date'     : 'yyyy-mm-dd HH:MM:SS',
'request_date' : 'yyyy-mm-dd HH:MM:SS',
'prd_grp_fin'  : 'E-comm',
'policy_id'    : 'XXXXX'}
```

Example to post a request via python is in `request.py`.

### Definition of Parameters:
1. `premium`      - The original GWP/Premium charged to the policyholders/customers.
2. `issue_date`   - The date when the policy is underwritten.
3. `start_date`   - The initial start date of the trip/journey.
4. `end_date`     - The expiry date of the policy or when the policy becomes ineffective.
5. `request_date` - The date in which refund begins to take effect.
6. `prd_grp_fin`  - Segmentation information provided by B.I.
7. `policy_id`    - The identifying id for the request policy. (This is for logging and debugging purpose)

## Calculation Methodology
All necessary function for calculation is in `calculator.py`.<br>

### Summary
When a policy is issued, the premium collected is earned on the term of the policy until it expired.
The earning has a unique pattern according to the risk involved within the policy term.

The reserving actuary has come out with a unique earning pattern for each `Product Group` to reflect each homogenous segment.
With this unique pattern, we can identify how much risk has expired or earned and how much is still in effect.
When a refund is needed, we can safely refund the portion that hasn't expired or earned yet.
Hence the proportion of refund is just `1-earned`.

<ins>The earned calculation are made up of :</ins>

1. Start Day portion
2. Trip Duration portion
3. Lead time portion

### Start Day portion
The start day portion is a constant set by the reserving actuary as:

| Product Group Finance | Start Day portion |
| --------------------- | ----------------- |
|      Ticket           | 0.360211775       |
|      E-comm           | 0.047960282       |
|      Corporate        | 0.                |
|      Cancellation     | 0.241505279       |
|      Trad & Other     | 0.054981764       |


### Trip Duration portion
Trip duration portion can either be earned on a pro-rata linear scale or a log scale.
The general rule of thumb is to use log scale when the trip duration is relatively long as compared to lead time; vice-versa on a linear scale when the trip duration is relatively short as compared to lead time.
The exact threshold can be found in the `calculator.py` which follows the reserving document.

### Lead Time portion
Lead time portion is calculated using a special formula:

![y](y.png)

where the coeficient n can be found in the documentation.

##### *Please contact the actuarial reserving team if you require a copy of the documentation.*
## 
<h6 align="center">
&copy; Quantuary 2020
</h6>
