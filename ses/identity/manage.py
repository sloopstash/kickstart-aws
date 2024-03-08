##
# -*- coding: utf-8 -*-
##
##
# Manage SES identities.
##

# Import community modules.
import sys
import json
import argparse
import boto3

# Initialize SES client.
SES = boto3.client('ses',region_name='ap-south-1')

# Parse CLI arguments.
cli = argparse.ArgumentParser(description='A CLI to manage SES identities.')
cli.add_argument('-f',dest='sender',type=str,required=True,help='Email address of the sender.')
cli.add_argument('-t',dest='recipients',nargs='+',required=True,help='Email addresses of the recipients.')
cli.add_argument('-s',dest='subject',type=str,required=True,help='Subject.')
cli.add_argument('-m',dest='message',type=str,required=True,help='Message.')
args = cli.parse_args()

# Send email to recipients.
response = SES.send_email(
  Destination={'ToAddresses':args.recipients},
  Message={
    'Body':{'Text':{'Charset':'UTF-8','Data':args.message}},
    'Subject':{'Charset':'UTF-8','Data':args.subject},
  },
  Source=args.sender
)
print(json.dumps(response,indent=4))
