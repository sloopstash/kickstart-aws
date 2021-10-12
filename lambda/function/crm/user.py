##
# -*- coding: utf-8 -*-
##
##
# User related functionalities.
##

# Import community modules.
import os
import json
import decimal
import boto3
from boto3.dynamodb.conditions import Key,Attr
from botocore.exceptions import ClientError
from botocore.config import Config

# Environment variables.
REGION = os.environ['REGION']
DYNAMO_DB_ENDPOINT = os.environ['DYNAMO_DB_ENDPOINT']

# Initialize DynamoDB client.
DynamoDB = boto3.resource('dynamodb',region_name=REGION,endpoint_url=DYNAMO_DB_ENDPOINT,config=Config(
  connect_timeout=3,
  read_timeout=3,
  retries = {
    'max_attempts':1,
    'mode':'standard'
  }
))

# Get users by Account ID.
def get_users(account_id):
  decimal_to_int_converter = lambda x: int(x) if isinstance(x,decimal.Decimal) else x
  response = DynamoDB.Table('users').query(
    IndexName='users_index_account_id',
    KeyConditionExpression=Key('account_id').eq(int(account_id)),
    ExpressionAttributeNames={
      '#name':'name',
      '#status':'status'
    },
    ProjectionExpression='id,account_id,#name,email,#status,updated',
    Select='SPECIFIC_ATTRIBUTES'
  )
  if len(response['Items']) > 0:
    data = response['Items']
    for item in data:
      for key in item:
        item[key] = decimal_to_int_converter(item[key])
    response = {'status':'success','message':'Data found.','data':data}
  else:
    response = {'status':'success','message':'No data found.','data':[]}
  return response

# Handler for Lambda function.
def lambda_handler(event,context):
  req_path = event['path']
  req_query_strings = event['queryStringParameters']
  try:
    if req_path=='/users':
      assert req_query_strings,'Required a valid query string parameters.'
      assert 'account_id' in req_query_strings,'Account ID query string parameter not found.'
      response = get_users(req_query_strings['account_id'])
    else:
      raise Exception('Invalid path.')
  except AssertionError as error:
    return {
      'statusCode':200,
      'body':json.dumps({
        'status':'failure',
        'message':error.args[0]
      })
    }
  except ClientError as error:
    return {
      'statusCode':500,
      'body':json.dumps({
        'status':'failure',
        'message':str(error.response['Error']['Message'])
      })
    }
  except Exception as error:
    return {
      'statusCode':500,
      'body':json.dumps({
        'status':'failure',
        'message':'Internal server error.',
        'error':str(error)
      })
    }
  else:
    return {'statusCode':200,'body':json.dumps(response)}
