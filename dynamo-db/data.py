##
# -*- coding: utf-8 -*-
##
##
# Manage DynamoDB data.
##

# Import community modules.
import sys
import json
import argparse
from time import time
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

# Configurations
data = parse_json('dynamodb/config/data.json')
config = parse_json('dynamodb/config/main.json')
schema = parse_json('dynamodb/config/schema.json')

# Initialize DynamoDB client.
DynamoDB = boto3.resource('dynamodb', region_name=config['region'], endpoint_url=config['endpoint'])

# Populate accounts data
def _populate_data(args):
  table = args.table_name
  for account in data['accounts']:
    try:
      account['created'] = account['updated'] = datetime.fromtimestamp(int(time())).strftime('%A, %b %d %Y, %H:%M%p')
      DynamoDB.Table(table).put_item(Item=account)
      print('Done creating account: '+account['organization'])
    except Exception as error:
      print(error)

# Parse CLI arguments.
cli = argparse.ArgumentParser(description='A CLI to manage DynamoDB table.')
cli_action = cli.add_subparsers(dest="action")

populate = cli_action.add_parser("populate")
populate.add_argument('-t',dest='table_name',type=str,required=True,help='Table name.')

args = cli.parse_args()

# Validates action.
if args.action == 'populate':
  _populate_data(args)
else:
  print("Invalid action.")