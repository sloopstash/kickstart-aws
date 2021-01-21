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
config = parse_json('dynamodb/config/main.json')
schema = parse_json('dynamodb/config/schema.json')

# Initialize DynamoDB client.
DynamoDB = boto3.resource('dynamodb', region_name=config['region'], endpoint_url=config['endpoint'])

# Create table
def _create_table(args):
  table = args.table_name
  if table in config['tables']:
    try:
      if schema[table].has_key('GlobalSecondaryIndexes'):
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
  if table in config['tables']:
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
  if table in config['tables']:
    response = DynamoDB.Table(table).scan()
    print(json.dumps(response, indent=4))
  else:
    print('Table not exist.')

# Query table
def _query_table(args):
  table = args.table_name
  organization = args.organization
  if table in config['tables']:
    response = DynamoDB.Table(table).query(
      KeyConditionExpression=Key('organization').eq(organization)
    )
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

query = cli_action.add_parser("query")
query.add_argument('-t',dest='table_name',type=str,required=True,help='Table name.')
query.add_argument('-o',dest='organization',type=str,required=True,help='Organization name.')

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