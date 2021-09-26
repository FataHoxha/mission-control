from boto3 import resource


# Create Client
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

# Create the Table
# Note: no need to define all the structure of the table, as dynamodb is noSQL.   
def create_table():
    table = dynamodb.create_table(
        TableName='Application',
        KeySchema=[
            {
                'AttributeName': 'name',
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
    return table

# once the table is created, can be retrieved from the resource
app_table = resource.Table('Application')

def fill_table():
    input = {'name': 'authentication', 'metadata': 'test_user@n26.com', 'config': 'some_file_on_aws'}

    # Insert Data
    app_table.put_item(Item=input)
    print('Successfully put item')

# get specific item based on application name
def get_item(name):

    response = app_table.get_item(
        Key = {
            'name'     : name
        },
        AttributesToGet=[
            'name' # valid types dont throw error
        ]
    )

    return response

def update_item(name, data:dict):

    response = app_table.update_item(
        Key = {
            'name': name
        },
        AttributeUpdates={
            'name': {
                'Value'  : data['name'],
                'Action' : 'PUT' # # available options -> DELETE(delete), PUT(set), ADD(increment)
            },
            'author': {
                'Value'  : data['author'],
                'Action' : 'PUT'
            }
        },
        ReturnValues = "UPDATED_NEW"  # returns the new updated values
    )
    return response

def delete_item(name):

    response = app_table.delete_item(
        Key = {
            'name': name
        }
    )

    return response