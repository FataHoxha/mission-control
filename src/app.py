
import db_utils 
import time
from flask import Flask, request, Response
from prometheus_client import Counter, Summary, Gauge, generate_latest, start_http_server

app = Flask(__name__)
# Register neccassy metrics to monitor webapp through endpoint /metrics
endpoint_request_counter = Counter('endpoint_request_counter', 'Requests per seconds per endpoint', ["endpoint", "method"])
err = Counter('error', 'Count of exceptions', ["endpoint", "method"])
overhaul_request_counter = Counter('overhaul_request_counter', 'Count total requests perseconds')
latency = Summary('request_latency_seconds', 'Request latency per seconds', ["endpoint", "method"])    

@app.route('/')
def index():
    # A new table is created when calling the index
    db_utils.create_table()
    return Response("This is a RESTful API for Application Version Control", status = 200)

@app.route('/fill_table',methods=["POST"])
def fill_table():
    ''' 
        This endpoint will fill the table with provided from an external json 
        
    '''

    # increase request count
    endpoint_request_counter.labels("/factorial/", request.method).inc()
    overhaul_request_counter.inc()
    
    # set monitor for request 
    with latency.labels("/fill_table/", request.method).time():
        # set monitor for errors
        with err.labels("/fill_table/", request.method).count_exceptions():
            res = ("Table Filled successfully {res}".format(res=db_utils.fill_table()))

    # return result
    return Response(res, status=200)


@app.route('/metrics')
def metrics():
    """
    Returns the metric calculated through prometheus_client
    
    /metrics/
    
    """
    return Response(generate_latest(), mimetype='text/plain; version=0.0.4; charset=utf-8')

 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # create a new table
    
    
   
   

