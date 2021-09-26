
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
    ''' 
        Route: http://localhost:5000/
    '''
    
    return Response("This is a RESTful API for Application Version Control", status = 200)

@app.route('/create_and_fill_table', methods=["POST"])
def create_and_fill_table():
    ''' 
        This endpoint will create and fill the table with data provided from an external json stored in src/data
        Route: http://localhost:5000/create_and_fill_table/
    '''

    # increase request count
    endpoint_request_counter.labels("/create_and_fill_table/", request.method).inc()
    overhaul_request_counter.inc()
    
    # set monitor for request 
    with latency.labels("/create_and_fill_table/", request.method).time():
        # set monitor for errors
        with err.labels("/create_and_fill_table/", request.method).count_exceptions():
            db_utils.create_table()
            res = ("Table Created & Filled successfully {res}".format(res=db_utils.fill_table()))

    # return result
    return Response(res, status=200)

@app.route('/get_app/<name>', methods=["GET"])
def get_item(name):
    ''' 
        Returns Application data for a given application name
        
        Route: http://localhost:5000/get_app/<name>

    '''

    # increase request count
    endpoint_request_counter.labels("/get_app/", request.method).inc()
    overhaul_request_counter.inc()
    
    # set monitor for request 
    with latency.labels("/get_app/", request.method).time():
        # set monitor for errors
        with err.labels("/get_app/", request.method).count_exceptions():
            res = ("Application data for {name}: {res}".format(name=name, res=db_utils.get_item(name)))

    # return result
    return Response(res, status=200)

@app.route('/get_apps/', methods=["GET"])
def get_items():
    ''' 
        Returns all the Application data in the table
        Route: http://localhost:5000/get_apps/
    '''

    # increase request count
    endpoint_request_counter.labels("/get_apps/", request.method).inc()
    overhaul_request_counter.inc()
    
    # set monitor for request 
    with latency.labels("/get_apps/", request.method).time():
        # set monitor for errors
        with err.labels("/get_apps/", request.method).count_exceptions():
            res = ("Application data available in the table: {res}".format(res=db_utils.get_items()))

    # return result
    return Response(res, status=200)

@app.route('/update_app/<name>', methods=['PUT'])
def update_item_versioning(name):
    ''' 
        Delets an item, application, given then name in input
        Route: http://localhost:5000/update_app/<name>
    '''
    # data = {
    #     'owner': 'tes.user@n26.com',
    #     'app_config': 'somewhere_in_s3'
    # }
    # increase request count
    endpoint_request_counter.labels("/update_app/", request.method).inc()
    overhaul_request_counter.inc()
    
    # set monitor for request 
    with latency.labels("/update_app/", request.method).time():
        # set monitor for delete_app
        with err.labels("/update_app/", request.method).count_exceptions():
            res = ("Application {name} removed from table! {res}".format(name=name, res=db_utils.update_item_versioning(name , data)))

    # return result
    return Response(res, status=200)

@app.route('/delete_app/<name>', methods=['DELETE'])
def delete_item(name):
    ''' 
        Delets an item, application, given then name in input
        Route: http://localhost:5000/delete_app/<name>
    '''

    # increase request count
    endpoint_request_counter.labels("/delete_app/", request.method).inc()
    overhaul_request_counter.inc()
    
    # set monitor for request 
    with latency.labels("/delete_app/", request.method).time():
        # set monitor for delete_app
        with err.labels("/delete_app/", request.method).count_exceptions():
            res = ("Application {name} removed from table! {res}".format(name=name, res=db_utils.delete_item(name)))

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
    
    
   
   

