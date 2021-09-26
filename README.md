# Mission Control Center (MCC) 

## Description

The goal of this simple API is to update and display versioned changes of application informations stored into database


## API

The API includes three endpoints which with main functionalities: get all applications, get specifc app and versioning, update application

`/get-applications`

`/get-application/<app_name>`

`/update-application/<app_name`

`/metrics`
This endpoint exposes the metrics 

## Setup
To run the API, simply run the docker container.
TODO: add testing script + path

This will start the Flask, DynamoDB services.

```
	docker-compose build
	docker-compose up  
```

## Run the web app
After starting the container, you can start using the endpoints.
The Web App will be available locally at the path: `http://localhost:5000/`


## Testing
The endpoints can be tested inside the container as follow
TODO: add testing script + path
