import ps
import requests
import config


# Sometimes the DNS server blocks the etherscan api request, switch to VPN to get it working again
URL = "https://api.etherscan.io/v2/api"

results = {}

for address in ps.ADDRESSES:
    results[address] = {}
    print("Address: ", address)

    for chain_name, chain_data in config.CHAINS.items():
        chain_id = chain_data["chainid"]
        print("Chainid: ", chain_id)
        results[address][chain_name] = {}

        for token_name, token_data in chain_data["tokens"].items():
            params = {
                "apikey": ps.api_key,
                "chainid": chain_id,
                "module": "account",
                "action": "tokenbalance",
                "contractaddress": token_data["address"],
                "address": address,
                "tag": "latest",
            }

            resp = requests.get(URL, params=params)
            data = resp.json()

            if data.get("status") == "1":
                balance_raw = int(data["result"])
                balance_clean = balance_raw / 10 ** token_data["decimals"]
            else:
                balance_clean = None
                print(
                    f"Error | {address} | {chain_name} | {token_name}: {data.get('message')}"
                )

            results[address][chain_name][token_name] = balance_clean

for address, chains in results.items():
    print(f"\nAddress: {address}")

    total_usdc = 0.0
    total_usdt = 0.0

    for chain, tokens in chains.items():
        usdc = tokens.get("USDC")
        usdt = tokens.get("USDT")

        print(f"  Chain: {chain}")
        print(f"    USDC = {usdc}")
        print(f"    USDT = {usdt}")

        if usdc is not None:
            total_usdc += usdc
        if usdt is not None:
            total_usdt += usdt

    print("\n  ---- Totals across all chains ----")
    print(f"  Total USDC = {total_usdc}")
    print(f"  Total USDT = {total_usdt}")