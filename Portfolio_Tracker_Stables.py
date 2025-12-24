# This Script is for tracking stablecoin balances across EVM chains (excl BSC and Base), Solana and Hypercore
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

    df_EVM = pd.DataFrame(rows)

    return df_EVM

def hyperliquid_dex():
    print("Fetching Hyperliquid clearinghouse and spot balances...")
    url = "https://api.hyperliquid.xyz/info"

    def get_user_balances(address):
        # 1. Fetch Perps Clearinghouse State (for Perps USDC)
        perp_payload = {"type": "clearinghouseState", "user": address}
        
        # 2. Fetch Spot Clearinghouse State (for Spot USDC, USDT, USDH)
        spot_payload = {"type": "spotClearinghouseState", "user": address}
        
        try:
            # Execute both calls
            perp_resp = requests.post(url, json=perp_payload).json()
            spot_resp = requests.post(url, json=spot_payload).json()

            # Extract Perps USDC (accountValue includes settled cash + unrealized PnL)
            perps_usdc = float(perp_resp.get('marginSummary', {}).get('accountValue', 0))

            # Initialize spot totals
            spot_stables = {"USDC": 0.0, "USDT": 0.0, "USDH": 0.0}
            
            # Parse spot balances (returns a list of coin objects)
            for item in spot_resp.get('balances', []):
                coin_name = item.get('coin')
                if coin_name in spot_stables:
                    spot_stables[coin_name] = float(item.get('total', 0))

            return perps_usdc, spot_stables
            
        except Exception as e:
            print(f"Error fetching Hyperliquid data for {address}: {e}")
            return 0.0, {"USDC": 0.0, "USDT": 0.0, "USDH": 0.0}

    results_list = []

    # Assuming ps.HYPERLIQUID_ADDRESSES is your dictionary of {name: address}
    for name, address in ps.HYPERLIQUID_ADDRESSES.items():
        print(f"Checking {name}...")
        
        perps_usdc, spot_stables = get_user_balances(address)
        
        # Sum USDC from both Perps and Spot
        total_usdc = perps_usdc + spot_stables["USDC"]
        total_usdt = spot_stables["USDT"]
        total_usdh = spot_stables["USDH"]

        # Calculate the single final value for the address
        grand_total = total_usdc + total_usdt + total_usdh

        results_list.append({
            "Name of address": name,
            "USDC Balance": total_usdc,
            "USDT Balance": total_usdt,
            "USDH Balance": total_usdh,
            "Total Stablecoin Balance": grand_total
        })

    # Create and return the DataFrame
    df = pd.DataFrame(results_list)
    return df

def solscan():
    print("Fetching token balances for all wallets...")

    # Solana Mainnet Token Mint Addresses
    USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    USDT_MINT = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
    RPC_URL = "https://api.mainnet-beta.solana.com"


    def get_token_balance(wallet_address, mint_address, rpc_url):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenAccountsByOwner",
            "params": [
                wallet_address,
                {"mint": mint_address},
                {"encoding": "jsonParsed"}
            ]
        }
        try:
            response = requests.post(rpc_url, json=payload).json()
            print(response)
            print()
            accounts = response.get('result', {}).get('value', [])
            
            if not accounts:
                return 0.0
                
            total_balance = sum(
                float(acc['account']['data']['parsed']['info']['tokenAmount']['uiAmount']) 
                for acc in accounts
            )
            return total_balance
        except Exception as e:
            print(f"Error fetching balance for {wallet_address}: {e}")
            return 0.0

    # 1. Create a list to store the data rows
    results_list = []

    # 2. Loop through the dictionary
    for name, address in ps.SOLANA_ADDRESSES.items():
        print(f"Checking {name}...")
        time.sleep(5)
        usdc_bal = get_token_balance(address, USDC_MINT, RPC_URL)
        time.sleep(5)
        usdt_bal = get_token_balance(address, USDT_MINT, RPC_URL)
        usdt0_bal = 0.0
        
        # Calculate total
        total_stable = usdc_bal + usdt_bal + usdt0_bal

        # Append data to the list
        results_list.append({
            "Name of address": name,
            "USDC balance": usdc_bal,
            "USDT balance": usdt_bal,
            "USDT0 balance": usdt0_bal,
            "Total stablecoin balance": total_stable
        })

    # 3. Create the DataFrame
    df_Solana = pd.DataFrame(results_list)
    return df_Solana

def export_to_csv(df_EVM, df_Solana, df_hl):

    combined_df = pd.concat([df_EVM, df_Solana, df_hl], axis=0, ignore_index=True)
    combined_df.to_csv(ps.portfolio_balances_fp, index=False)
    print("Data saved successfully to portfolio_balances.csv")


df_EVM = etherscan()

df_Solana = solscan()

df_hl = hyperliquid_dex()

export_to_csv(df_EVM, df_Solana, df_hl)