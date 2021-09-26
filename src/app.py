
from flask import Flask, request, Response
import db_utils as dynamodb

app = Flask(__name__)


    
@app.route('/get-applications')
def get_items():
    res = ("Content is {table}".format(table=get_items()))

    # return result
    return Response(res, status=200)


@app.route('/')
def index():
    return Response("This is a RESTful App for Application Version control", status = 200)
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # create a new table
    dynamodb.create_table()

    # fill table with some entries 
    # TODO: add fill from external JSON
    dynamodb.add_items()
    
   
   

