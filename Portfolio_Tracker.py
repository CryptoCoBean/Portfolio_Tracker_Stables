import ps

import requests

ADDRESS = "0x21B3Ca06d377457b4002A73dFb2a530867dceef5"
CHAIN_ID = 1  # Ethereum Mainnet

url = f"https://api.etherscan.io/v2/api"

params = {
    "apikey": ps.api_key,
    "chainid": CHAIN_ID,
    "module": "account",
    "action": "balance",
    "address": ADDRESS,
    "tag": "latest"
}

resp = requests.get(url, params=params)
data = resp.json()
print(data)