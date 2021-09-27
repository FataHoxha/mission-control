# Mission Control Center (MCC) 

## Description

The goal of this API is to provide endpoints which can be used to display versioned changes of applications stored in a dynamodb


## API

The API includes several endpoints which cover the following functionalities: get all applications, get specifc app and versioning, update application

### setup the database and fill with data

`/create_and_fill_table`

### Crud operations
GET
`/get_app/<name>` -> read a single item
`/get_apps/` -> read all the items items in the table

DELETE
`/delete_app/<name>`

UPDATE with versioning
`/update_app/<name>`


### metrics
`/metrics`
This endpoint exposes the metrics to monitor the staus of the api

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
```
	docker exec -i -t mission-control_web_1 bash
	python3 src/test_db.py
```