import ps
import requests
import config
import time

# Sometimes the DNS server blocks the etherscan api request, switch to VPN to get it working again
URL = "https://api.etherscan.io/v2/api"

results = {}

# for address in ps.ADDRESSES:
#     results[address] = {}
#     print("Address: ", address)

#     for chain_name, chain_data in config.CHAINS.items():
#         chain_id = chain_data["chainid"]
#         print("Chainid: ", chain_id)
#         results[address][chain_name] = {}

#         for token_name, token_data in chain_data["tokens"].items():
#             params = {
#                 "apikey": ps.api_key,
#                 "chainid": chain_id,
#                 "module": "account",
#                 "action": "tokenbalance",
#                 "contractaddress": token_data["address"],
#                 "address": address,
#                 "tag": "latest",
#             }

#             resp = requests.get(URL, params=params)
#             data = resp.json()

#             if data.get("status") == "1":
#                 balance_raw = int(data["result"])
#                 balance_clean = balance_raw / 10 ** token_data["decimals"]
#             else:
#                 balance_clean = None
#                 print(
#                     f"Error | {address} | {chain_name} | {token_name}: {data.get('message')}"
#                 )

#             results[address][chain_name][token_name] = balance_clean

# for address, chains in results.items():
#     print(f"\nAddress: {address}")

#     total_usdc = 0.0
#     total_usdt = 0.0

#     for chain, tokens in chains.items():
#         usdc = tokens.get("USDC")
#         usdt = tokens.get("USDT")

#         print(f"  Chain: {chain}")
#         print(f"    USDC = {usdc}")
#         print(f"    USDT = {usdt}")

#         if usdc is not None:
#             total_usdc += usdc
#         if usdt is not None:
#             total_usdt += usdt

#     print("\n  ---- Totals across all chains ----")
#     print(f"  Total USDC = {total_usdc}")
#     print(f"  Total USDT = {total_usdt}")
#     print(f"  Total Stablecoins (USDT + USDC) = {total_usdc + total_usdt}")



    # We iterate over the NAME (key), but use the ADDRESS (value) for the API
for name, address in ps.NAMED_ADDRESSES.items():
    results[name] = {}
    print(f"Fetching data for: {name}...")

    for chain_name, chain_data in config.CHAINS.items():
        chain_id = chain_data["chainid"]
        print("Chain ID: ", chain_id)
        results[name][chain_name] = {}

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

            try:
                resp = requests.get(URL, params=params, timeout=10)
                data = resp.json()

                if data.get("status") == "1":
                    balance_raw = int(data["result"])
                    balance_clean = balance_raw / 10 ** token_data["decimals"]
                else:
                    print("API error or no balance")
                    balance_clean = 0.0
                
                time.sleep(0.5) # Avoid rate limits

            except Exception:
                print("API ERROR")
                balance_clean = 0.0

            results[name][chain_name][token_name] = balance_clean


# UI SECTION - Using Names Only
for name, chains in results.items():
    print(f"\n{'#'*40}")
    print(f" PORTFOLIO: {name.upper()}")
    print(f"{'#'*40}")

    total_usdc = 0.0
    total_usdt = 0.0
    total_usdt0 = 0.0

    for chain, tokens in chains.items():
        usdc = tokens.get("USDC", 0.0)
        usdt = tokens.get("USDT", 0.0)
        usdt0 = tokens.get("USDT0", 0.0)
        
        total_usdc += usdc
        total_usdt += usdt
        total_usdt0 += usdt0
        
        # Nicely formatted table row
        print(f" {chain:10} | USDC: {usdc:,.2f} | USDT: {usdt:,.2f} | USDT0: {usdt0:,.2f}")

    print("-" * 40)
    print(f" {'TOTAL USDC:':<15} {total_usdc:,.2f}")
    print(f" {'TOTAL USDT:':<15} {total_usdt:,.2f}")
    print(f" {'TOTAL USDT0:':<15} {total_usdt0:,.2f}")
    print(f" {'GRAND TOTAL:':<15} ${(total_usdc + total_usdt + total_usdt0):,.2f}")