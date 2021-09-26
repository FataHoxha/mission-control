
from flask import Flask, request, Response

app = Flask(__name__)


    
@app.route('/get-applications')
def get_items():
    return Response("This will return all the availabel apps", status = 200)


if __name__ == '__main__':
    app.run()

@app.route('/')
def index():
    
    return Response("This is a RESTful App for Application Version control", status = 200)
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
   
   

