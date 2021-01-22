# Import community modules.
import os
import json
from datetime import datetime

# Import AWS SDK for python.
import boto3
from boto3.dynamodb.conditions import Key,Attr

# Constant values.
REGION = os.environ['REGION']
ENDPOINT = os.environ['ENDPOINT']
DynamoDB = boto3.resource('dynamodb',region_name=REGION,endpoint_url=ENDPOINT)

# Request handler
def lambda_handler(event,context):
  try:
    organization = event['queryStringParameters']['organization']
    response = DynamoDB.Table('prd_crm_users').query(
      IndexName='prd_crm_users_index_organization',
      KeyConditionExpression=Key('organization').eq(organization)
    )
    items = []
    for item in response['Items']:
      item = dict(item)
      item['id'] = int(item['id'])
      item['updated'] = datetime.fromtimestamp(item['updated']).strftime('%Y-%m-%d %H:%M:%S')
      items.append(item)
    response['Items'] = items
    return {'statusCode':200,'body':json.dumps(response,indent=4)}
  except Exception as error:
    return {'statusCode':500,'body':json.dumps(str(error),indent=4)}