# Crserv

Crserv is a minimal microservice that provides realtime values of crptocurrencies.

# Features!

  - Retrieve real time values for crypto currencies.
  - Config symbols for desired crypto currencies and retrieval urls.

### Installation
Requires Python 2.7
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

python main.py -p <port> -c <config file location> -u <url file location>
```
### verify
```sh
127.0.0.1:<port>/currency/all
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
The status of server can be queried at `http://127.0.0.1:<port>/healthcheck`

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

 - Dockerize the application
 - Kubernetes depolyment donfig
 - Unit Tests

License
----

MIT

