import boto3


# Create connection
dynamodb = boto3.resource('dynamodb', 
                          endpoint_url='http://localhost:8000', 
                          region_name='eu-west-1',
                          aws_access_key_id='test_key',
                          aws_secret_access_key='test_key' )

# Create the Table
# Note: no need to define all the structure of the table, as dynamodb is noSQL.   
def create_table():
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

table = dynamodb.Table('Application')

def fill_table():
    #recall existing table
    table = dynamodb.Table('Application')
    # create input to fillin 
    # TODO: input from external json
    input = {'name': 'authentication', 'owner': 'test_user@n26.com', 'config': 'some_file_on_aws'}

    # Insert Data
    response = table.put_item(Item=input)

    return response

def list_items():
    # return all items, applications, contained in a table
    response = table.get_item(
        Key = {
            'name'     : name
        },
        AttributesToGet=[
            'name' # valid type
        ]
    )

    return response

# get specific item based on application name
def get_item(name):
    # return only a specific item, application
    response = table.get_item(
        Key = {
            'name'     : name
        },
        AttributesToGet=[
            'name' # valid type
        ]
    )

    return response


def update_item(name, data:dict):

    response = table.update_item(
        Key = {
            'name': name
        },
        AttributeUpdates={
            'name': {
                'Value'  : data['name'],
                'Action' : 'PUT' # # available options -> DELETE(delete), PUT(set), ADD(increment)
            },
            'owner': {
                'Value'  : data['owner'],
                'Action' : 'PUT'
            }
        },
        ReturnValues = "UPDATED_NEW"  # returns the new updated values
    )
    return response

def update_item_versioning(name, data:dict):
    '''ref: https://aws.amazon.com/blogs/database/implementing-version-control-using-amazon-dynamodb/'''

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
    response = table.delete_item(
        Key = {
            'name': name
        }
    )

    return response