Currently this project gets the stablecoin balances from EVM chains, Solana and Hypercore (perps and Spot).

For EVM chains, base and bsc is excluded as they are premier features of the Etherscan API, more chains can be added in the config file.

The ps file has the following variables in the following structure:

  api_name = 'REDACTED'
  
  api_key = 'REDACTED'
  
  NAMED_ADDRESSES = {
      "Name #1": "REDACTED", 
      "Name #2": "REDACTED",
  }
  
  SOLANA_ADDRESSES = {
      "Name #1": "REDACTED", 
      "Name #2": "REDACTED",
  }
  
  HYPERLIQUID_ADDRESSES = {
      "Name #1": "REDACTED", 
      "Name #2": "REDACTED",
  }
  
  portfolio_balances_fp = r'REDACTED'
