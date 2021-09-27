import boto3
import db_utils
import unittest 
from botocore.exceptions import ClientError
from moto import mock_dynamodb2 

@mock_dynamodb2
class TestDynamoDB(unittest.TestCase):

    def setUpDynamoDB(self):
        """
        Set dynamoDB resource and add mocked table
        """

        self.table = db_utils.create_table()
        self.table = db_utils.fill_table()()

    def deleteTable(self):
        """
        Delete dynamoDB table after test run
        """
        self.table.delete()
    
    def test_table_name(self):
        """
        Test if table exist and if name is correct
        """
        self.assertIn('Application', self.table.name) 

    def test_update_application(self):
        """
        Test UPDATE
        """

        result = db_utils.update_item_versioning('ai_app')
        
        self.assertEqual(200, result['ResponseMetadata']['HTTPStatusCode'])
    
    def test_get_app(self):
        """
        Test GET application, for specific name, and assert result correctness 
        """
        result = db_utils.get_item('ai_app')

        self.assertEqual('ai_app', result['name'])
        self.assertEqual("tes.user@n26.com", result['owner'])
        self.assertEqual("somewhere_in_s3", result['app_config'])

if __name__ == '__main__':
    unittest.main()
