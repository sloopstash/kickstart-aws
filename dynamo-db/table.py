##
# -*- coding: utf-8 -*-
##
##
# Manage DynamoDB tables.
##

# Import community modules.
import sys
import json
import argparse
from datetime import datetime

# Import AWS SDK for python.
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Returns parsed json content.
def parse_json(Filename):
  File = open(Filename,'r')
  Content = File.read()
  Content = json.loads(Content)
  File.close()
  return Content

# configurations
config = parse_json('dynamo-db/conf/main.conf')
schema = parse_json('dynamo-db/conf/schema.conf')

# Initialize DynamoDB client.
DynamoDB = boto3.resource('dynamodb', region_name=config['region'], endpoint_url=config['endpoint'])

# Create table
def _create_table(args):
  table = args.table_name
  if table in config['table']:
    try:
      if 'GlobalSecondaryIndexes' in schema[table]:
        DynamoDB.create_table(
          TableName=table,
          KeySchema=schema[table]['KeySchema'],
          GlobalSecondaryIndexes=schema[table]['GlobalSecondaryIndexes'],
          AttributeDefinitions=schema[table]['AttributeDefinitions'],
          ProvisionedThroughput=schema[table]['ProvisionedThroughput']
        )
        print('Done creating table: '+table)
      else:
        DynamoDB.create_table(
          TableName=table,
          KeySchema=schema[table]['KeySchema'],
          AttributeDefinitions=schema[table]['AttributeDefinitions'],
          ProvisionedThroughput=schema[table]['ProvisionedThroughput']
        )
        print('Done creating table: '+table)
    except Exception as error:
      print(error)
  else:
    print('Table not exist.')

# Delete table
def _delete_table(args):
  table = args.table_name
  if table in config['table']:
    try:
      DynamoDB.Table(table).delete()
      print('Done deleting table: '+table)
    except Exception as error:
      print(error)
  else:
    print('Table not exist.')

# Scaning table
def _scan_table(args):
  table = args.table_name
  index = args.index_name
  if table in config['table']:
    if index:
      response = DynamoDB.Table(table).scan(IndexName=index)
    else:
      response = DynamoDB.Table(table).scan()
    items = []
    for item in response['Items']:
      item = dict(item)
      item['id'] = int(item['id'])
      item['updated'] = datetime.fromtimestamp(item['updated']).strftime('%Y-%m-%d %H:%M:%S')
      items.append(item)
    response['Items'] = items
    print(json.dumps(response, indent=4))
  else:
    print('Table not exist.')

# Query table
def _query_table(args):
  table = args.table_name
  index = args.index_name
  condition_key = args.key
  condition_value = args.value
  if table in config['table']:
    if index:
      response = DynamoDB.Table(table).query(
        IndexName=index,
        KeyConditionExpression=Key(condition_key).eq(condition_value)
      )
    else:
      response = DynamoDB.Table(table).query(
        KeyConditionExpression=Key(condition_key).eq(condition_value)
      )
    items = []
    for item in response['Items']:
      item = dict(item)
      item['id'] = int(item['id'])
      item['updated'] = datetime.fromtimestamp(item['updated']).strftime('%Y-%m-%d %H:%M:%S')
      items.append(item)
    response['Items'] = items
    print(json.dumps(response, indent=4))
  else:
    print('Table not exist.')

# Parse CLI arguments.
cli = argparse.ArgumentParser(description='A CLI to manage DynamoDB table.')
cli_action = cli.add_subparsers(dest="action")

create = cli_action.add_parser("create")
create.add_argument('-t',dest='table_name',type=str,required=True,help='Table name.')

delete = cli_action.add_parser("delete")
delete.add_argument('-t',dest='table_name',type=str,required=True,help='Table name.')

scan = cli_action.add_parser("scan")
scan.add_argument('-t',dest='table_name',type=str,required=True,help='Table name.')
scan.add_argument('-i',dest='index_name',type=str,help='Index name.')

query = cli_action.add_parser("query")
query.add_argument('-t',dest='table_name',type=str,required=True,help='Table name.')
query.add_argument('-i',dest='index_name',type=str,help='Index name.')
query.add_argument('-k',dest='key',type=str,required=True,help='Key for condition expression.')
query.add_argument('-v',dest='value',type=str,required=True,help='Value for condition expression.')

args = cli.parse_args()

# Validates action.
if args.action == 'create':
  _create_table(args)
elif args.action == 'delete':
  _delete_table(args)
elif args.action == 'scan':
  _scan_table(args)
elif args.action == 'query':
  _query_table(args)
else:
  print('Invalid action.')