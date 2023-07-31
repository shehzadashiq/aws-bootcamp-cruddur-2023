import boto3
import sys
import uuid
import os
import botocore.exceptions
from datetime import datetime, timedelta, timezone

import json
import os

from boto3 import Session as AWSSession
from requests_aws4auth import AWS4Auth

from gql import gql
from gql.client import Client
from gql.transport.requests import RequestsHTTPTransport


class AppSync:
    def client():
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        aws = AWSSession(aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                        region_name=os.getenv('AWS_DEFAULT_REGION'))
        credentials = aws.get_credentials().get_frozen_credentials()
        auth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            aws.region_name,
            'appsync',
            session_token=credentials.token,
        )
        transport = RequestsHTTPTransport(url=os.getenv('APPSYNC_ENDPOINT'),
                                        headers=headers,
                                        auth=auth)
        client = Client(transport=transport,
                        fetch_schema_from_transport=True)
        return client

    def test_mutation(self):
        client = make_client()
        params = {'id': 1235, 'state': 'DONE!'}
        # resp = client.execute(gql(update_appsync_obj),


        # get_appsync_obj="""query listCrdDdbDynamoDBTable1NK2LU7KGZSIPS {
        #     listCrdDdbDynamoDBTable1NK2LU7KGZSIPS(filter: {message_group_uuid: {eq: "dba1f675-4793-4ad8-aa25-29c37b9eada6"}}) {
        #         items {
        #         message_group_uuid
        #         pk
        #         sk
        #         }
        #     }
        #     }"""

        get_appsync_obj="""query listCrdDdbDynamoDBTable1NK2LU7KGZSIPS {
            listCrdDdbDynamoDBTable1NK2LU7KGZSIPS(filter: {message_group_uuid: {eq: "dba1f675-4793-4ad8-aa25-29c37b9eada6"}}) {
                items {
                message_group_uuid
                pk
                sk
                user_display_name
                user_handle
                message
                user_uuid
                }
            }
            }
            """          

        response = client.execute(gql(get_appsync_obj),
                            variable_values=json.dumps({'input': params}))

        print("Response")                            
        print(response)

        items = response['listCrdDdbDynamoDBTable1NK2LU7KGZSIPS']['items']

        print("Raw Items")
        print(items)
        

        results = []
        for item in items:
            last_sent_at = item['sk']['S']
            results.append({
                'uuid': item['message_group_uuid']['S'],
                'display_name': item['user_display_name']['S'],
                'handle': item['user_handle']['S'],
                'message': item['message']['S'],
                'created_at': last_sent_at
            })
        return results

    def list_message_groups(client,my_user_uuid):
        client = make_client()
        params = {'id': 1235, 'state': 'DONE!'}
        # params = {'message_group_uuid': "dba1f675-4793-4ad8-aa25-29c37b9eada6": my_user_uuid, 'state': 'DONE!'}
        # resp = client.execute(gql(update_appsync_obj),

        get_appsync_obj="""query listCrdDdbDynamoDBTable1NK2LU7KGZSIPS {
            listCrdDdbDynamoDBTable1NK2LU7KGZSIPS(filter: {message_group_uuid: {eq: "dba1f675-4793-4ad8-aa25-29c37b9eada6"}}) {
                items {
                message_group_uuid
                pk
                sk
                user_uuid
                user_display_name
                user_handle
                message
                }
            }
            }
            """          

        response = client.execute(gql(get_appsync_obj),
                            variable_values=json.dumps({'input': params}))

        print("Response Generated from AppSync GQL Query")                            
        print(response)

        # Create an array from response items
        items = response['listCrdDdbDynamoDBTable1NK2LU7KGZSIPS']['items']

        # print("Raw Items")
        # print(items)
        
        # Parse Results and return items
        results = []
        for item in items:
            last_sent_at = item['sk']
            results.append({
                'uuid': item['message_group_uuid'],
                'display_name': item['user_display_name'],
                'handle': item['user_handle'],
                'message': item['message'],
                'created_at': last_sent_at
            })
        return results

    
    def list_messages(client,message_group_uuid):
        year = str(datetime.now().year)
        # table_name = os.getenv("DDB_MESSAGE_TABLE")
        table_name="CrdDdbDynamoDBTable1NK2LU7KGZSIP"
        query_params = {
        'TableName': table_name,
        'KeyConditionExpression': 'pk = :pk AND begins_with(sk,:year)',
        'ScanIndexForward': False,
        'Limit': 20,
        'ExpressionAttributeValues': {
            ':year': {'S': year },
            ':pk': {'S': f"MSG#{message_group_uuid}"}
        }
        }

        response = client.query(**query_params)
        items = response['Items']
        items.reverse()
        results = []
        for item in items:
            created_at = item['sk']['S']
            results.append({
                'uuid': item['message_uuid']['S'],
                'display_name': item['user_display_name']['S'],
                'handle': item['user_handle']['S'],
                'message': item['message']['S'],
                'created_at': created_at
            })
        return results
    def create_message(client,message_group_uuid, message, my_user_uuid, my_user_display_name, my_user_handle):
        created_at = datetime.now().isoformat()
        message_uuid = str(uuid.uuid4())

        record = {
        'pk':   {'S': f"MSG#{message_group_uuid}"},
        'sk':   {'S': created_at },
        'message': {'S': message},
        'message_uuid': {'S': message_uuid},
        'user_uuid': {'S': my_user_uuid},
        'user_display_name': {'S': my_user_display_name},
        'user_handle': {'S': my_user_handle}
        }
        # insert the record into the table
        # table_name = os.getenv("DDB_MESSAGE_TABLE")
        table_name="CrdDdbDynamoDBTable1NK2LU7KGZSIP"
        response = client.put_item(
        TableName=table_name,
        Item=record
        )
        # print the response
        print(response)
        return {
        'message_group_uuid': message_group_uuid,
        'uuid': my_user_uuid,
        'display_name': my_user_display_name,
        'handle':  my_user_handle,
        'message': message,
        'created_at': created_at
        }
    def create_message_group(client, message,my_user_uuid, my_user_display_name, my_user_handle, other_user_uuid, other_user_display_name, other_user_handle):
        table_name = os.getenv("DDB_MESSAGE_TABLE")

        message_group_uuid = str(uuid.uuid4())
        message_uuid = str(uuid.uuid4())
        now = datetime.now(timezone.utc).astimezone().isoformat()
        last_message_at = now
        created_at = now

        my_message_group = {
        'pk': {'S': f"GRP#{my_user_uuid}"},
        'sk': {'S': last_message_at},
        'message_group_uuid': {'S': message_group_uuid},
        'message': {'S': message},
        'user_uuid': {'S': other_user_uuid},
        'user_display_name': {'S': other_user_display_name},
        'user_handle':  {'S': other_user_handle}
        }

        other_message_group = {
        'pk': {'S': f"GRP#{other_user_uuid}"},
        'sk': {'S': last_message_at},
        'message_group_uuid': {'S': message_group_uuid},
        'message': {'S': message},
        'user_uuid': {'S': my_user_uuid},
        'user_display_name': {'S': my_user_display_name},
        'user_handle':  {'S': my_user_handle}
        }

        message = {
        'pk':   {'S': f"MSG#{message_group_uuid}"},
        'sk':   {'S': created_at },
        'message': {'S': message},
        'message_uuid': {'S': message_uuid},
        'user_uuid': {'S': my_user_uuid},
        'user_display_name': {'S': my_user_display_name},
        'user_handle': {'S': my_user_handle}
        }

        items = {
        table_name: [
            {'PutRequest': {'Item': my_message_group}},
            {'PutRequest': {'Item': other_message_group}},
            {'PutRequest': {'Item': message}}
        ]
        }

        try:
            # Begin the transaction
            response = client.batch_write_item(RequestItems=items)
            return {
                'message_group_uuid': message_group_uuid
            }
        except botocore.exceptions.ClientError as e:
            print(e)

####-----------------------------------------

# get_appsync_obj="""query listCrdDdbDynamoDBTable1NK2LU7KGZSIPS {
#   listCrdDdbDynamoDBTable1NK2LU7KGZSIPS {
#     items {
#       message_group_uuid
#       pk
#       sk
#     }
#   }
# }"""

def make_client():
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    aws = AWSSession(aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                     region_name=os.getenv('AWS_DEFAULT_REGION'))
    credentials = aws.get_credentials().get_frozen_credentials()

    auth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        aws.region_name,
        'appsync',
        session_token=credentials.token,
    )

    transport = RequestsHTTPTransport(url=os.getenv('APPSYNC_ENDPOINT'),
                                      headers=headers,
                                      auth=auth)
    client = Client(transport=transport,
                    fetch_schema_from_transport=True)
    return client

# get_appsync_obj and update_appsync_obj are GraphQL queries in string form.
# You can make one using AppSync's query sandbox and copy the text over.

# from .queries import get_appsync_obj
# , update_appsync_obj

# def test_get():
#     # get_appsync_obj is a GraphQL query in string form.
#     # You can use the query strings from AppSync schema.
#     client = make_client()
#     params = {'id': 1235}
#     resp = client.execute(gql(get_appsync_obj),
#                           variable_values=json.dumps(params))
#     return resp


def test_mutation():
    client = make_client()
    params = {'id': 1235, 'state': 'DONE!'}

    get_appsync_obj="""query listCrdDdbDynamoDBTable1NK2LU7KGZSIPS {
        listCrdDdbDynamoDBTable1NK2LU7KGZSIPS(filter: {message_group_uuid: {eq: "dba1f675-4793-4ad8-aa25-29c37b9eada6"}}) {
            items {
            message_group_uuid
            pk
            sk
            user_uuid
            user_display_name
            user_handle
            message
            }
        }
        }
        """  


    # resp = client.execute(gql(update_appsync_obj),
    resp = client.execute(gql(get_appsync_obj),
                          variable_values=json.dumps({'input': params}))
    return resp

# Driver function for test
def query_messages():
    print("Result: ", test_mutation())


    response = test_mutation()

    print(response)

    # List of items

    items = response['listCrdDdbDynamoDBTable1NK2LU7KGZSIPS']['items']
    
    print(items)

    results = []
    
    for item in items:
        # print(item)
        # print(item['pk'])
        # print(item['message_group_uuid'])
        # print(item['sk'])
        # print(item['user_display_name'])
        # print(item['user_handle'])
        # print(item['message'])

        last_sent_at = item['sk'
        ]
        results.append({
            'uuid': item['message_group_uuid'],
            'display_name': item['user_display_name'],
            'handle': item['user_handle'],
            'message': item['message'],
            'created_at': last_sent_at
        })

    # return results

    print ("Results")
    print(results)

# Test functions only used from command line, comment out when being used in GUI otherwise the backend container will crash
appsync = AppSync()
# AppSync.list_message_groups(appsync,"4fa2d4e6-11f3-4b39-9ec8-a421d4faaa0a")
# query_messages()