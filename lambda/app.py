# Import community modules.
import os
import json

# Import AWS SDK for python.
import boto3
from boto3.dynamodb.conditions import Key,Attr

# Constant values.
REGION = os.environ['REGION']
ENDPOINT = os.environ['ENDPOINT']
TABLES = ['prd_crm_accounts']
DynamoDB = boto3.resource('dynamodb',region_name=REGION,endpoint_url=ENDPOINT)

# Request handler
def main(event,context):
  try:
    table = event['queryStringParameters']['table']
    organization = event['queryStringParameters']['organization']
    if not table in TABLES:
      raise Exception('Table not exist.')
    response = DynamoDB.Table(table).query(
      KeyConditionExpression=Key('organization').eq(organization)
    )
    return {'statusCode':200,'body':json.dumps(response,indent=4)}
  except Exception as error:
    return {'statusCode':500,'body':json.dumps(str(error),indent=4)}