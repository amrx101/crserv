# Crserv

Crserv is a minimal microservice that provides realtime values of crypto-currencies.

# Features!

  - Retrieve real time values for crypto currencies.
  - Config symbols for desired crypto currencies and retrieval urls.

### Installation
Requires Python 2.7 & pip

Optional(Install pip)

```shell script
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
pip install virtualenv
sudo /usr/bin/easy_install virtualenv
```

```sh
pip install virtualenv
```
Test the installation
```sh
virtualenv --version
```
Create a virtualenv
```sh
cd crserv
virtualenv venv
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
pip install -r requirements.txt

python main.py -a <addr>-p <port> -c <config file location> -u <url file location>
```
### verify
```sh
<addr>:<port>/healthcheck
```

### API
GET `/currency/all`
```json
[
    {
        "last": "0.035979",
        "bid": "0.035980",
        "high": "0.036082",
        "feeCurrency": "BTC",
        "low": "0.035376",
        "ask": "0.035988",
        "fullName": "Ethereum",
        "open": "0.035811",
        "id": "ETH"
    }, 
    {
        "last": "10369.68",
        "bid": "10369.49",
        "high": "10399.13",
        "feeCurrency": "USD",
        "low": "10268.71",
        "ask": "10369.50",
        "fullName": "Bitcoin",
        "open": "10314.06",
        "id": "BTC"
    }
]
```

GET `/currency/BTCUSD`
```json
    {
        "last": "10369.68",
        "bid": "10369.49",
        "high": "10399.13",
        "feeCurrency": "USD",
        "low": "10268.71",
        "ask": "10369.50",
        "fullName": "Bitcoin",
        "open": "10314.06",
        "id": "BTC"
    }
```

### HealthCheck
The status of server can be queried at `http://<addr>:<port>/healthcheck`

A 200 OK response means server is up and functioning.

### Configs
The application requires 2 configs file to function, supplied as command line arguments.
Config 1: 
- `symbols.json`
- Contains the identifer of symbols


```json
[
  {"symbol":  "BTCUSD"},
  {"symbol": "ETHBTC"}
]
```

Config 2:
- `urls.json`
- Contains the urls to query the API.

```json
{
  "symbol": "https://api.hitbtc.com/api/2/public/symbol",
  "currency": "https://api.hitbtc.com/api/2/public/currency",
  "notifier": "wss://api.hitbtc.com/api/2/ws"
}
```

### Dependencies:
- `websocket_client`: Required because we need a Web Socket client to get notified by the server.
- `requests`: Simple HTTP library because we need to query the server to validate symbols and get meta info about them.
- `tornado`: We need a web-server to server our clients.

The default locations of the configs are `/etc/symbols.json` and `/etc/configs.json`. Reference config files are present in the `config` directory.

### Todos

 - TLS for server verification
 - Dockerize the application
 - Kubernetes deployment config
 - Unit Tests

License
----

MIT

