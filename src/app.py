
from flask import Flask, request, Response
import db_utils 

app = Flask(__name__)


    



@app.route('/')
def index():
    # A new table is created when calling the index
    db_utils.create_table()
    db_utils.fill_table()
    return Response("This is a RESTful API for Application Version Control", status = 200)
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # create a new table
    
    
   
   

