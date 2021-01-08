##
# -*- coding: utf-8 -*-
##
##
# SES Service
##

# Import community modules.
import sys
import json
import argparse

# Import AWS SDK.
import boto3

# Initializing Amazon SES client.
SES = boto3.client('ses',region_name='us-west-2')

# Parsing commandline arguments.
parser = argparse.ArgumentParser()
parser.add_argument('-f',dest='sender',type=str,required=True,help='Sender email address.')
parser.add_argument('-t',dest='recipients',nargs='+',required=True,help='Recipients email address.')
parser.add_argument('-s',dest='subject',type=str,required=True,help='Subject.')
parser.add_argument('-m',dest='message',type=str,required=True,help='Message.')
args = parser.parse_args()

# Send a message to the recipients that you gave on the command line.
response = SES.send_email(
  Destination={'ToAddresses':args.recipients},
  Message={
    'Body':{'Text':{'Charset':'UTF-8','Data':args.message}},
    'Subject':{'Charset':'UTF-8','Data':args.subject},
  },
  Source=args.sender
)
print(json.dumps(response, indent=4))