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
        client = make_client()
        params = {'id': 1235, 'state': 'DONE!'}
        # params = {'message_group_uuid': "dba1f675-4793-4ad8-aa25-29c37b9eada6": my_user_uuid, 'state': 'DONE!'}
        # resp = client.execute(gql(update_appsync_obj),

        get_appsync_obj = f"""query listCrdDdbDynamoDBTable1NK2LU7KGZSIPS {{
            listCrdDdbDynamoDBTable1NK2LU7KGZSIPS(filter: {{message_group_uuid: {{eq: "{message_group_uuid}"}}}}) {{
                items {{
                message_group_uuid
                pk
                sk
                user_uuid
                user_display_name
                user_handle
                message
                }}
            }}
        }}
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

# Function to test our mutation in AppSync works
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

        last_sent_at = item['sk']
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
# AppSync.list_messages(appsync,"dba1f675-4793-4ad8-aa25-29c37b9eada6")
# query_messages()