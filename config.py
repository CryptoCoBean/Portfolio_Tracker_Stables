CHAINS = {
    "ethereum": {
        "chainid": 1,
        "tokens": {
            "USDC": {
                "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "decimals": 6,
            },
            "USDT": {
                "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "decimals": 6,
            },
        },
    },

    "base": {
        "chainid": 8453,
        "tokens": {
            "USDC": {
                # Native USDC on Base
                "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                "decimals": 6,
            },
            "USDT": {
                "address": "0xfde4C962512720E773E50422119c2992dADC9B0d",
                "decimals": 6,
            },
            "USDT0": {
                "address": "0xfde4C962512720E773E50422119c2992dADC9B0d",
                "decimals": 6,
            },
        },
    },

    "arbitrum": {
        "chainid": 42161,
        "tokens": {
            "USDC": {
                # Native USDC (not USDC.e)
                "address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
                "decimals": 6,
            },
            "USDT": {
                "address": "0x55d398326f99059fF775485246999027B3197955",
                "decimals": 6,
            },
            "USDT0": {
                "address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
                "decimals": 6,
            },
        },
    },

    "bsc": {
        "chainid": 56,
        "tokens": {
            "USDC": {
                "address": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
                "decimals": 18,  # BSC USDC uses 18 decimals
            },
            "USDT": {
                "address": "0x55d398326f99059fF775485246999027B3197955",
                "decimals": 18,
            },
        },
    },
    "hyperevm": {
        "chainid": 999,
        "tokens": {
            "USDC": {
                "address": "0xb88339CB7199b77E23DB6E890353E22632Ba630f",
                "decimals": 6,
            },
            "USDT": {
                # USDT0 on HyperEVM
                "address": "0xB8CE59FC3717ada4C02eaDF9682A9e934F625ebb",
                "decimals": 6,
            },
        },
    },
}
