##
# -*- coding: utf-8 -*-
##

# Import community modules.
import os
import json
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key,Attr

# Environment variables.
REGION = os.environ['REGION']
DYNAMO_DB_ENDPOINT = os.environ['DYNAMO_DB_ENDPOINT']

# Initialize DynamoDB client.
DynamoDB = boto3.resource('dynamodb',region_name=REGION,endpoint_url=DYNAMO_DB_ENDPOINT)

# Handler for Lambda function.
def lambda_handler(event,context):
  try:
    organization = event['queryStringParameters']['organization']
    query = DynamoDB.Table('prd_crm_users').query(
      IndexName='prd_crm_users_index_organization',
      KeyConditionExpression=Key('organization').eq(organization)
    )
    items = query['Items']
    users = []
    for item in items:
      item = dict(item)
      item['id'] = int(item['id'])
      item['updated'] = datetime.fromtimestamp(item['updated']).strftime('%Y-%m-%d %H:%M:%S')
      users.append(item)
    if 'requestContext' in event and 'apiId' in event['requestContext']:
      return {'statusCode':200,'body':json.dumps(users,indent=2)}
    else:
      return {'statusCode':200,'body':users}
  except Exception as error:
    return {'statusCode':500,'body':str(error)}
