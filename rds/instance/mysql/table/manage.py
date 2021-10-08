##
# -*- coding: utf-8 -*-
##
##
# Manage MySQL tables.
##

# Import community modules.
import json
import argparse
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
config = parse_json('rds/conf/main.conf')

# Initialize MySQL connection.
connection = create_engine(
  'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
    config['username'],config['password'],config['endpoint'],str(config['port']),config['database']),
  pool_size=10,pool_recycle=3600,max_overflow=0,echo=False,echo_pool=False
).connect()
connection.execution_options(autocommit=False)

# Create MySQL tables.
def create_tables():
  with open('rds/instance/mysql/table/schema.sql') as file:
    sql = file.read()
    queries = sql.split(';')
    for query in queries:
      try:
        connection.execute(query)
      except OperationalError as error:
        print(error)

# Delete MySQL tables.
def delete_tables():
  tables = [
    'accounts',
    'users'
  ]
  for table in tables:
    try:
      connection.execute('DROP TABLE IF EXISTS '+table)
      print('Deleted table: '+table)
    except OperationalError as error:
      print(error)

# Query MySQL table records.
def query_tables(args):
  query = """SELECT * FROM {} USE INDEX ({}) WHERE {}='{}'""".format(args.table_name,args.index_name,args.key,args.value)
  records = connection.execute(query).fetchall()
  results = []
  for row in records:
    row = dict(row)
    row['created'] = str(row['created'])
    row['updated'] = str(row['updated'])
    results.append(row)
  print(json.dumps(results,indent=2))

# Parse CLI arguments.
cli = argparse.ArgumentParser(description='A CLI to manage MySQL table.')
cli_action = cli.add_subparsers(dest="action")

create = cli_action.add_parser("create")

delete = cli_action.add_parser("delete")

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
elif args.action=='query':
  query_tables(args)
else:
  print('Invalid action.')
