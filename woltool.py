#!/usr/bin/env python3

import os
import re
import time
import json
import base64
import logging
import argparse
import datetime
import subprocess
import urllib.request

# Setup command line args
cmdline_parser = argparse.ArgumentParser(description='Polls sheet script to see if WOL was requested.')
cmdline_parser.add_argument('--url', required=True, action='store', help='Google script URL.')
cmdline_parser.add_argument('--retries', default=1, required=False, action='store', help='Number of times to retry. 0 for unlimited. Default is 1.')
cmdline_parser.add_argument('--interval', default=5, required=False, action='store', help='How many minutes to wait between retries.')
cmdline_parser.add_argument('--debug', required=False, action='store_true', help='Enable debug output.')
args = cmdline_parser.parse_args()

# Setup logger
logger = logging.getLogger(os.path.basename(__file__))
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
logger.setLevel(logging.INFO)
if args.debug: logger.setLevel(logging.DEBUG)

def sendWOL(name, mac):
    logger.debug("Sending wol for {name} - {mac}...".format(**locals()))
    try:
        output = subprocess.check_output("wakeonlan {mac}".format(**locals()), shell=True).decode("utf-8").strip()
        logger.debug(output)
        return output
    except Exception as e:
        logger.error("ERROR!: Could not send WOL to {name} - {mac}".format(**locals()))
        logger.error(e)
        return e

def sendStatus(data):
    try:
        url = args.url
        logger.debug("Posting status to {url}...".format(**locals()))
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        stringdata = json.dumps(data,sort_keys=True, indent=4, separators=(',', ': '))
        logger.debug(stringdata)
        stringdatabytes = stringdata.encode('utf-8')
        req.add_header('Content-Length', len(stringdatabytes))
        response = urllib.request.urlopen(req, stringdatabytes)
        logger.debug(response.read().decode('utf-8'))
    except Exception as e:
        logger.error("ERROR! Could not send status to {url}".format(**locals()))
        logger.error(e)
        exit(1)

retries = int(args.retries)
if retries == 0:
    retries = -1
while True:
    try:
        logger.debug("Loading {url}...".format(url=args.url))
        with urllib.request.urlopen(url=args.url) as url:
            response = url.read().decode()
        logger.debug(response)
        data = json.loads(response)
        for host in data:
            mac = data[host]["mac"]
            wake = data[host]["wake"]
            timestamp = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            if wake:
                if not mac:
                    logger.error("No MAC address was specified for {host}. Skipping.".format(**locals()))
                    data[host]["status"] = "[{timestamp}] No MAC address was specified. Skipping.".format(**locals())
                    data[host]["wake"] = "false"
                else:
                    status = sendWOL(host, mac)
                    data[host]["status"] = "[{timestamp}] {status}".format(**locals())
                    data[host]["wake"] = "false"
        sendStatus(data)
    except Exception as e:
        logger.error("ERROR! Could not load {url}".format(url=args.url))
        logger.error(e)
        exit(1)
    retries = retries - 1
    if retries == 0:
        break
    else:
        logger.debug("Sleeping for {interval} minutes...".format(interval=args.interval))
        time.sleep(int(args.interval) * 60)
