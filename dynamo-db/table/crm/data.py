##
# -*- coding: utf-8 -*-
##
##
# Manage DynamoDB data.
##

# Import community modules.
import json
import argparse
from time import time
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Return parsed JSON content.
def parse_json(Filename):
  File = open(Filename,'r')
  Content = File.read()
  Content = json.loads(Content)
  File.close()
  return Content

# Load data and configuration.
dataset = parse_json('crm/data/main.json')
config = parse_json('crm/app/conf/aws/dynamo-db.conf')
schema = parse_json('dynamo-db/schema/crm/main.json')

# Initialize DynamoDB client.
DynamoDB = boto3.resource('dynamodb',region_name=config['region'],endpoint_url=config['endpoint'])

# Get counter
def get_counter(name):
  counter = DynamoDB.Table('counters').update_item(
    Key={'name':name},
    UpdateExpression='SET #value=#value+:increment',
    ExpressionAttributeValues={':increment':1},
    ExpressionAttributeNames={'#value':'value'},
    ReturnValues='ALL_NEW'
  )['Attributes']['value']
  return counter

# Populate data into DynamoDB table.
def populate_data(args):
  table = args.table
  data = dataset[args.entity]
  data_count = len(data)
  for item in data:
    try:
      date_time = int(time())
      if table == 'accounts':
        user_id = get_counter('u')
        DynamoDB.Table(table).put_item(Item={
          'id':item['id'],
          'admin_uid':user_id,
          'namespace':item['namespace'],
          'organization':item['organization'],
          'email':item['email'],
          'phone':item['phone'],
          'status':int(0),
          'created':date_time,
          'updated':date_time
        })
        DynamoDB.Table('users').put_item(Item={
          'id':user_id,
          'account_id':item['id'],
          'name':item['name'],
          'email':item['email'],
          'password':item['password'],
          'status':int(0),
          'created':date_time,
          'updated':date_time
        })
      elif table == 'users':
        user_id = get_counter('u')
        DynamoDB.Table(table).put_item(Item={
          'id':user_id,
          'account_id':item['account_id'],
          'name':item['name'],
          'email':item['email'],
          'password':item['password'],
          'status':int(0),
          'created':date_time,
          'updated':date_time
        })
    except Exception as error:
      print(error)
      break
  print('Done populating data.')

# Parse CLI arguments.
cli = argparse.ArgumentParser(description='A CLI to manage DynamoDB data.')
cli_action = cli.add_subparsers(dest='action')

populate = cli_action.add_parser('populate')
populate.add_argument('-t',dest='table',type=str,required=True,help='Name of the DynamoDB table.')
populate.add_argument('-e',dest='entity',type=str,required=True,help='Entity data.')

args = cli.parse_args()

if args.action=='populate':
  populate_data(args)
else:
  print('Invalid action.')
