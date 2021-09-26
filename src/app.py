
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


@app.route('/metrics')
def metrics():
    """
    Returns the metric calculated through prometheus_client
    
    /metrics/
    
    """
    return Response(generate_latest(), mimetype='text/plain; version=0.0.4; charset=utf-8')

@app.route('/')
def index():
    # A new table is created when calling the index
    db_utils.create_table()
    db_utils.fill()
    return Response("This is a RESTful API for Application Version Control", status = 200)
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # create a new table
    
    
   
   

