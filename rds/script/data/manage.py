##
# -*- coding: utf-8 -*-
##
##
# Manage MySQL data.
##

# Import community modules.
import os
import sys
import json
import boto3
import argparse
import pandas as pd
from time import time
from datetime import datetime
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import InvalidRequestError,IntegrityError,OperationalError

# Return parsed JSON content.
def parse_json(Filename):
  File = open(Filename,'r')
  Content = File.read()
  Content = json.loads(Content)
  File.close()
  return Content

# Load configuration.
config = parse_json('rds/instance/mysql/conf/main.conf')
dataset = parse_json('rds/instance/mysql/data/dataset.json')

# Initialize MySQL connection.
connection = create_engine(
  'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
    config['username'],config['password'],config['endpoint'],str(config['port']),config['database']),
  pool_size=10,pool_recycle=3600,max_overflow=0,echo=False,echo_pool=False
).connect()
connection.execution_options(autocommit=False)


_add_account_query = """INSERT INTO accounts (id,admin_uid,namespace,organization,email,phone,status,created,updated) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
_add_user_query = """INSERT INTO users (account_id,name,email,password,status,created,updated)
                     VALUES (%s,%s,%s,%s,%s,%s,%s)"""

# Populate data.
def populate_data(args):
  table = args.table
  data = dataset[args.entity]
  data_count = len(data)
  try:
    transaction = connection.begin()
    for item in data:
      try:
        date_time = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
        if table == 'accounts':
          connection.execute(
            _add_account_query,
            (item['id'],int(0),item['namespace'],item['organization'],
            item['email'],item['phone'],int(0),date_time,date_time)
          )
          query = connection.execute(
            _add_user_query,
            (item['id'],item['name'],item['email'],item['password'],int(0),date_time,date_time)
          )
          user_id = query.lastrowid
          connection.execute(
            """UPDATE accounts SET admin_uid=%s,updated=%s WHERE id=%s""",
            (user_id,date_time,item['id'])
          )
        elif table == 'users':
          connection.execute(
            _add_user_query,
            (item['account_id'],item['name'],item['email'],item['password'],int(0),date_time,date_time)
          )
        else:
          raise Exception('Table not exist.')
      except Exception as error:
        raise Exception(error)
    transaction.commit()
  except IntegrityError as error:
    transaction.rollback()
    print('Record already exists.')
    print(error)
  except Exception as error:
    transaction.rollback()
    print(error)
  else:
    print('Done populating data.')

# Parse CLI arguments.
cli = argparse.ArgumentParser(description='A CLI to manage MySQL table.')
cli_action = cli.add_subparsers(dest="action")

populate = cli_action.add_parser("populate")
populate.add_argument('-t',dest='table',type=str,required=True,help='Name of the MySQL table.')
populate.add_argument('-e',dest='entity',type=str,required=True,help='Entity data.')

args = cli.parse_args()

if args.action=='populate':
  populate_data(args)
else:
  print('Invalid action.')
