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
from time import mktime
from datetime import datetime,timedelta

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
dataset = parse_json('dynamo-db/conf/data.json')
config = parse_json('dynamo-db/conf/main.conf')
schema = parse_json('dynamo-db/conf/schema.conf')

# Initialize DynamoDB client.
DynamoDB = boto3.resource('dynamodb', region_name=config['region'], endpoint_url=config['endpoint'])

# Populate data
def _populate_data(args):
  table = args.table_name
  data = dataset[args.entity]
  data_count = len(data)

  def past_date_timestamp(index):
    no_of_elapsed_days = data_count - index
    past_dt = datetime.now() - timedelta(days=no_of_elapsed_days)
    return int(mktime(past_dt.timetuple()))

  for index in range(data_count):
    try:
      data[index]['id'] = int(data[index]['id'])
      data[index]['updated'] = past_date_timestamp(index)
      DynamoDB.Table(table).put_item(Item=data[index])
      print('Done creating item: '+data[index]['name'])
    except Exception as error:
      print(error)

# Parse CLI arguments.
cli = argparse.ArgumentParser(description='A CLI to manage DynamoDB table.')
cli_action = cli.add_subparsers(dest="action")

populate = cli_action.add_parser("populate")
populate.add_argument('-t',dest='table_name',type=str,required=True,help='Table name.')
populate.add_argument('-e',dest='entity',type=str,required=True,help='User entity.')

args = cli.parse_args()

# Validates action.
if args.action == 'populate':
  _populate_data(args)
else:
  print("Invalid action.")