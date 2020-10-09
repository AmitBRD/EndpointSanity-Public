###How It Works:

this small script makes concurrent requests to a set of endpoints and compares the sha256 hash of the response body to ensure the return values are equivalent.


###to setup

update `auth.py`

set the following property:

```

BEARER_TOKEN="<YOUR_TOKEN_FROM_BLOCKSET_API>"

```

update the following properties in main.py:
```

PERIODIC_MS=15*1000 #ms - how often you want to run against the apis

Endpoints = ["https://api.blockset.com/", "http://api.blockset.com/"] - the endpoints you want to compare against

```

###to install:

`pip3.8 install -r requirements.txt`

###to run:

`python3.8 main.py`


Example Output:

```

Processing Api Calls:1602265999.338926
https://api.blockset.com/blocks?blockchain_id=bitcoinsv-mainnet&include_txs=True&max_page_size=20
https://api.blockset.com/blocks?blockchain_id=bitcoinsv-mainnet&include_txs=True&max_page_size=20&start_height=656148&end_height=656158
https://api.blockset.com/transactions?blockchain_id=bitcoinsv-mainnet&include_raw=True&max_page_size=20&include_transfers=True
https://api.blockset.com/transactions?blockchain_id=bitcoinsv-mainnet&include_raw=True&max_page_size=20&include_transfers=True&start_ts=1602179599&end_ts=1602265999
http://api.blockset.com/blocks?blockchain_id=bitcoinsv-mainnet&include_txs=True&max_page_size=20
http://api.blockset.com/blocks?blockchain_id=bitcoinsv-mainnet&include_txs=True&max_page_size=20&start_height=656148&end_height=656158
http://api.blockset.com/transactions?blockchain_id=bitcoinsv-mainnet&include_raw=True&max_page_size=20&include_transfers=True
http://api.blockset.com/transactions?blockchain_id=bitcoinsv-mainnet&include_raw=True&max_page_size=20&include_transfers=True&start_ts=1602179599&end_ts=1602265999
Unexpected error: HTTP 400: Bad Request <class 'tornado.httpclient.HTTPClientError'>
Unexpected error: HTTP 400: Bad Request <class 'tornado.httpclient.HTTPClientError'>
path: /blocks  matches
path: /blocks/block_range  matches
path: /transactions  matches
path: /transactions/time_range  matches
Completed Processing: 1602266000.022762


```


