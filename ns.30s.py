#!/usr/bin/python3

# Metadata allows your plugin to show up in the app, and website.
#
#  <xbar.title>Nightscout Blood Glucose Value</xbar.title>
#  <xbar.version>v1.0</xbar.version>
#  <xbar.author>Peter Wallman</xbar.author>
#  <xbar.author.github>petwall</xbar.author.github>
#  <xbar.desc>Reads the current bg value and direction arrow from your Nightscout server</xbar.desc>
#  <xbar.image>http://www.hosted-somewhere/pluginimage</xbar.image>
#  <xbar.dependencies>python</xbar.dependencies>
#  <xbar.abouturl>http://url-to-about.com/</xbar.abouturl>

import urllib.request
import requests
import hashlib

#######################################################
# Change this to fit your Nightscout setup
#######################################################

NIGHTSCOUT_URL = "https://your.nightscout.url"
API_SECRET = "your api secrect"
MMOL = True # set to False if you prefer mgdl instead

#######################################################

# you should not have to change this
API_ENDPOINT = "/api/v1/entries.json"

def sha1_hash(string):
    encoded_string = string.encode()
    sha1 = hashlib.sha1()
    sha1.update(encoded_string)
    hex_digest = sha1.hexdigest()
    return hex_digest

def arrow(direction):
    arrows = {
        "Flat": "→",
        "SingleUp": "↑",
        "DoubleUp": "↑↑",
        "DoubleDown": "↓↓",
        "SingleDown": "↓",
        "FortyFiveDown": "↘",
        "FortyFiveUp": "↗"
    }
    return arrows.get(direction, direction)

# ping a stable host just to check if we have an internet connection
def connect(host='http://google.com'):
  try:
    urllib.request.urlopen(host) #Python 3.x
    return True
  except:
    return False

if (connect() is False):
  print("[no connection]")
else:
  nightscout_url = NIGHTSCOUT_URL
  nightscout_url.rstrip('/') # in case we have a trailing slash
  nightscout_url += API_ENDPOINT

  # Set up the parameters and headers
  params = {'count': '1'}
  headers = {'API-SECRET': sha1_hash(API_SECRET)}

  # Make the GET request
  response = requests.get(nightscout_url, params=params, headers=headers)

  # Check if the request was successful
  if response.status_code == 200:
      # Parse the JSON response
      data = response.json()
      if data:
          # Assuming the data is in the expected format, extract the relevant information
          glucose_value = data[0].get('sgv')
          direction = data[0].get('direction')
          if (MMOL):
            glucose_value = glucose_value * 0.0555
            print(f"{glucose_value:.1f} {arrow(direction)}")
          else:
            print(f"{glucose_value} {arrow(direction)}")
      else:
          print("[no data]")
  else:
      print("[error:"+ str(response.status_code)+"]")
