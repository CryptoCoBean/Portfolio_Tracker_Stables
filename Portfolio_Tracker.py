import ps
import requests
import config
import time
import pandas as pd

def etherscan():
    # Sometimes the DNS server blocks the etherscan api request, switch to VPN to get it working again
    URL = "https://api.etherscan.io/v2/api"

    results = {}

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
    return results

def exporting_data(results): # UI SECTION - Using Names Only
    # Terminal output
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

    # Exporting to CSV
    rows = []

    for name, chains in results.items():
        # Initialize totals per wallet
        total_usdc = 0.0
        total_usdt = 0.0
        total_usdt0 = 0.0

        for chain, tokens in chains.items():
            total_usdc += tokens.get("USDC", 0.0)
            total_usdt += tokens.get("USDT", 0.0)
            total_usdt0 += tokens.get("USDT0", 0.0)

        grand_total = total_usdc + total_usdt + total_usdt0
            
        # Append one row per wallet
        rows.append({
            "Name of address": name,
            "USDC balance": total_usdc,
            "USDT balance": total_usdt,
            "USDT0 balance": total_usdt0,
            "Total stablecoin balance": grand_total
        })

    df = pd.DataFrame(rows)
    df.to_csv(ps.portfolio_balances_fp, index=False)

    print("Data saved successfully to portfolio_balances.csv")

def hyperliquid_dex():
    print("This is all the token balances on the Hyperliquid DEX ")

def solscan():
    print("This function is for all the tokens on solana address' ")

results = etherscan()
exporting_data(results)