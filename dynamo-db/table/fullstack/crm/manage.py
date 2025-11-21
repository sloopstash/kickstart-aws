##
# -*- coding: utf-8 -*-
##
##
# Manage DynamoDB tables.
##

# Import community modules.
import json
import argparse
import decimal
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Return parsed JSON content.
def parse_json(Filename):
  File = open(Filename,'r')
  Content = File.read()
  Content = json.loads(Content)
  File.close()
  return Content

# Convert decimal value to integer value.
decimal_to_int_converter = lambda x: int(x) if isinstance(x,decimal.Decimal) else x

# Load configuration.
config = parse_json('crm/app/conf/aws/dynamo-db.conf')
schema = parse_json('dynamo-db/schema/crm/main.json')

# Initialize DynamoDB client.
DynamoDB = boto3.resource('dynamodb',region_name=config['region'],endpoint_url=config['endpoint'])

# Create DynamoDB tables.
def create_tables():
  for table in config['table']:
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
      break

  # Populate counter.
  try:
    DynamoDB.Table('counters').put_item(Item={'name':'ac','value':int(0)})
    DynamoDB.Table('counters').put_item(Item={'name':'u','value':int(0)})
    print('Done creating counters')
  except Exception as error:
    print(error)

# Delete DynamoDB table.
def delete_tables():
  for table in config['table']:
    try:
      DynamoDB.Table(table).delete()
      print('Done deleting table: '+table)
    except Exception as error:
      print(error)
      break

# Scan DynamoDB table.
def scan_table(args):
  table = args.table_name
  index = args.index_name
  if table in config['table']:
    if index:
      response = DynamoDB.Table(table).scan(IndexName=index)
    else:
      response = DynamoDB.Table(table).scan()
    for item in response['Items']:
      for key in item:
        item[key] = decimal_to_int_converter(item[key])
        if key in ['created','updated']:
          item[key] = datetime.fromtimestamp(int(item[key])).strftime('%Y-%m-%d %H:%M:%S')
    print(json.dumps(response['Items'],indent=4))
  else:
    print('Table not exist.')

# Query DynamoDB table.
def query_table(args):
  table = args.table_name
  index = args.index_name
  condition_key = args.key
  if condition_key in ['id','account_id','admin_uid']:
    condition_value = int(args.value)
  else:
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
    for item in response['Items']:
      for key in item:
        item[key] = decimal_to_int_converter(item[key])
        if key in ['created','updated']:
          item[key] = datetime.fromtimestamp(int(item[key])).strftime('%Y-%m-%d %H:%M:%S')
    print(json.dumps(response['Items'],indent=4))
  else:
    print('Table not exist.')

# Parse CLI arguments.
cli = argparse.ArgumentParser(description='A CLI to manage DynamoDB table.')
cli_action = cli.add_subparsers(dest="action")

create = cli_action.add_parser("create")

delete = cli_action.add_parser("delete")

scan = cli_action.add_parser("scan")
scan.add_argument('-t',dest='table_name',type=str,required=True,help='Table name.')
scan.add_argument('-i',dest='index_name',type=str,help='Index name.')

query = cli_action.add_parser("query")
query.add_argument('-t',dest='table_name',type=str,required=True,help='Table name.')
query.add_argument('-i',dest='index_name',type=str,help='Index name.')
query.add_argument('-k',dest='key',type=str,required=True,help='Key for condition expression.')
query.add_argument('-v',dest='value',type=str,required=True,help='Value for condition expression.')

args = cli.parse_args()

if args.action=='create':
  create_tables()
elif args.action=='delete':
  delete_tables()
elif args.action=='scan':
  scan_table(args)
elif args.action=='query':
  query_table(args)
else:
  print('Invalid action.')
