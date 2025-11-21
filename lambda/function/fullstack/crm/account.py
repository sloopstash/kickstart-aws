##
# -*- coding: utf-8 -*-
##
##
# Account related functionalities.
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

# Get account by namespace.
def get_account(namespace):
  decimal_to_int_converter = lambda x: int(x) if isinstance(x,decimal.Decimal) else x
  response = DynamoDB.Table('accounts').query(
    IndexName='accounts_index_namespace',
    KeyConditionExpression=Key('namespace').eq(namespace),
    ExpressionAttributeNames={
      '#status':'status'
    },
    ProjectionExpression='id,namespace,organization,phone,#status,updated',
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
    if req_path=='/account':
      assert req_query_strings,'Required a valid query string parameters.'
      assert 'namespace' in req_query_strings,'Namespace query string parameter not found.'
      response = get_account(req_query_strings['namespace'])
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
