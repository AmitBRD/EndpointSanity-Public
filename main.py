from tornado.ioloop import IOLoop,PeriodicCallback
from tornado import httpclient
from urllib.parse import urlencode,urlparse
from tornado import gen
import hashlib
import json
import time
from collections import defaultdict
import functools
import sys
import auth

PERIODIC_MS=15*1000 #ms

headers = {"Authorization": "Bearer "+auth.BEARER_TOKEN}

blocks = "blocks"
txs = "transactions"
blockchains = "blockchains"
MAX_REQUEST_TIME=10
BLOCK_RANGE=10
MAX_PAGE_SIZE=20
TIME_RANGE=86400
Endpoints = ["https://api.blockset.com/", "http://api.blockset.com/"]

httpclient.AsyncHTTPClient.configure(None, defaults=dict(user_agent="MyUserAgent"))
http_client = httpclient.AsyncHTTPClient()


def height_range_spec(end_height):
  return urlencode({"start_height":end_height-BLOCK_RANGE, "end_height":end_height})
blockchain_id_spec = urlencode({'blockchain_id': 'bitcoinsv-mainnet'})
include_txs_spec = urlencode({"include_txs":True, 'max_page_size':MAX_PAGE_SIZE})
include_raw_spec = urlencode({"include_raw":True,'max_page_size':MAX_PAGE_SIZE,'include_transfers':True})

def time_range_spec(end_time):
  return urlencode({'start_ts':end_time-TIME_RANGE, 'end_ts':end_time})

async def asynchronous_fetch(url,sleep=0):
  await gen.sleep(sleep)
  print(url)
  try:
    response = await http_client.fetch(httpclient.HTTPRequest(url,headers=headers,request_timeout=MAX_REQUEST_TIME))
    return response.body
  except Exception as e:
    print("Unexpected error:", str(e), sys.exc_info()[0])
  return None

async def fetch_api(sleep=0):

  #get the current block height for the chain
  height = json.loads(str(await asynchronous_fetch(Endpoints[0]+blockchains+'/'+'bitcoinsv-mainnet',sleep=0.1),'utf-8'))
  print((height['block_height']))

  print("Processing Api Calls:" + str(time.time()))
 
  async_requests = []
  for endpoint in Endpoints:
    async_requests.extend([(endpoint+blocks,asynchronous_fetch(endpoint+blocks+"?"+"&".join([blockchain_id_spec,include_txs_spec]),sleep=0.)),#("?"+params if params else ""),sleep=0),
      (endpoint+blocks+"/block_range",asynchronous_fetch(endpoint+blocks+"?"+"&".join([blockchain_id_spec,include_txs_spec,height_range_spec(height['block_height'])]),sleep=0.)),
      (endpoint+txs,asynchronous_fetch(endpoint+txs+"?"+"&".join([blockchain_id_spec,include_raw_spec]),sleep=0)),
      (endpoint+txs+"/time_range",asynchronous_fetch(endpoint+txs+"?"+"&".join([blockchain_id_spec,include_raw_spec,time_range_spec(int(time.time()))]),sleep=0.))
      ])
  futures = dict(async_requests)
  results = {}
  
  #wait for them all to return in async
  results = await gen.multi(futures)
  
  hash_tuples = [(urlparse(api).path,hashlib.sha256(str(body).encode('utf-8')).hexdigest()) for api,body in results.items()]
  hashes = {}
  for key, value in hash_tuples:
    hashes.setdefault(key, []).append(value)

  for key,value in hashes.items():
    if not(all(elem == value[0] for elem in value)):
      print('path:',key,' does not match')
    else:
      print('path:',key,' matches') 

  #now groupby api endpoint and compare

  print('Completed Processing:',str(time.time()))
  return results


if __name__ == "__main__":
    io_loop = IOLoop.current()
    callback = functools.partial(fetch_api, sleep=0)
    scheduler = PeriodicCallback(callback, PERIODIC_MS)
    scheduler.start()
    io_loop.start()
