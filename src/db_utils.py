'''
    ref: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html
'''

import boto3
import json
from botocore.exceptions import ClientError
from decimal import Decimal



# Create connection
dynamodb = boto3.resource('dynamodb', 
                          endpoint_url='http://localhost:8000', 
                          region_name='eu-west-1',
                          aws_access_key_id='test_key',
                          aws_secret_access_key='test_key' )


def create_table():
    # Create the Table
    # Note: no need to define all the structure of the table, as dynamodb is noSQL

    dynamodb.create_table(
        TableName='Application',
        KeySchema=[
            {
                'AttributeName': 'name', # we assume that the name of the app is unique, so we can use it as id
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

# table created
table = dynamodb.Table('Application')


def fill_table():
    # fills an existing table with json data, stored in ./data/applicationdata

    with open("/data/applicationdata.json") as json_file:
        application_list = json.load(json_file, parse_float=Decimal)

    for app in application_list:
        name = app['name']
        owner = app['owner']
        print("Loading applications from json:", name , owner)
        table.put_item(Item=app)


def get_item(name):
    # return only a specific item, given the name 

    try:
        response = table.get_item(
                Key={'name': name}
            )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


def get_items():
    # return all items, applications, contained in a table

    try:
        response = dynamodb.scan(
                TableName='Application'
            )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response

def update_item_versioning(name, data:dict):

    # Update the item that has the latest version and content
    response = table.update_item(
        Key={
            'PK': name,
            'SK': 'v0'
        },
        # Atomic counter -> increment the latest version
        UpdateExpression='SET Latest = if_not_exists(Latest, :defaultval) + :incrval, #owner = :owner, #config = :config',
        ExpressionAttributeNames={
            '#owner': 'owner',
            '#config': 'config'
        },
        ExpressionAttributeValues={
            ':owner': data['owner'],
            ':config': data['config'], 
            ':defaultval': 0,
            ':incrval': 1
        },
        # return attributes values after the update
        ReturnValues='UPDATED_NEW'  
    )

    # Get the updated version
    latest_version = response['Attributes']['Latest']

    # Add the new item with the latest version
    latest_response = table.put_item(
        Item={
            'PK': name,
            'SK': 'v' + str(latest_version),
            'owner': data['owner'],
            'config': data['config']
        }
    )

    return latest_response

def delete_item(name):
    # permanently delete an item, application, from the table
    try:
        response = table.delete_item(
            Key = {
                'name': name
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response