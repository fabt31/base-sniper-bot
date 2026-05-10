import asyncio
import json
from web3 import AsyncWeb3, WebSocketProvider
from eth_abi import decode as abi_decode

# Uniswap v3 Factory on Base
UNISWAP_FACTORY = "0x33128a8fC17869897dcE68Ed026d694621f6FDfD"
POOL_CREATED_SIG = "0x783cca1c0412dd0d695e784568c96da2e9c22ff989357a2e8b1d9b2b4e6b7118"
WETH = "0x4200000000000000000000000000000000000006"
USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
UNISWAP_ROUTER = "0x2626664c2603336E57B271c5C0b26F421741e481"

SWAP_ABI = [{"inputs":[{"components":[{"name":"tokenIn","type":"address"},{"name":"tokenOut","type":"address"},{"name":"fee","type":"uint24"},{"name":"recipient","type":"address"},{"name":"amountIn","type":"uint256"},{"name":"amountOutMinimum","type":"uint256"},{"name":"sqrtPriceLimitX96","type":"uint160"}],"name":"params","type":"tuple"}],"name":"exactInputSingle","outputs":[{"name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"}]

class Sniper:
    def __init__(self, ws_url: str, private_key: str, config: dict):
        self.ws_url = ws_url
        self.private_key = private_key
        self.config = config
        self.bought_tokens: dict = {}

    async def start(self):
        print("🔭 Sniper started — monitoring Base for new pools...")
        async with AsyncWeb3(WebSocketProvider(self.ws_url)) as w3:
            self.w3 = w3
            sub_id = await w3.eth.subscribe("logs", {
                "address": UNISWAP_FACTORY,
                "topics": [POOL_CREATED_SIG]
            })
            async for event in w3.socket.process_subscriptions():
                log = event.get("result", {})
                await self._handle_new_pool(log)

    async def _handle_new_pool(self, log: dict):
        try:
            topics = log.get("topics", [])
            if len(topics) < 3: return
            token0 = "0x" + topics[1][-40:]
            token1 = "0x" + topics[2][-40:]
            new_token = token0 if token0.lower() not in [WETH.lower(), USDC.lower()] else token1
            print(f"🆕 New pool detected! Token: {new_token}")

            if not await self._passes_filters(new_token):
                print(f"  ❌ Filters failed for {new_token}")
                return

            print(f"  ✅ Filters passed — executing buy for {self.config.get(buy_amount_eth, 0.05)} ETH")
            await self._execute_buy(new_token)
        except Exception as e:
            print(f"Error handling pool: {e}")

    async def _passes_filters(self, token: str) -> bool:
        # Placeholder: add real filter logic
        return True

    async def _execute_buy(self, token: str):
        account = self.w3.eth.account.from_key(self.private_key)
        amount = self.w3.to_wei(self.config.get("buy_amount_eth", 0.05), "ether")
        router = self.w3.eth.contract(address=UNISWAP_ROUTER, abi=SWAP_ABI)
        tx = await router.functions.exactInputSingle({
            "tokenIn": WETH, "tokenOut": token, "fee": 10000,
            "recipient": account.address, "amountIn": amount,
            "amountOutMinimum": 0, "sqrtPriceLimitX96": 0
        }).build_transaction({"from": account.address, "value": amount, "gas": 300000})
        signed = account.sign_transaction(tx)
        tx_hash = await self.w3.eth.send_raw_transaction(signed.rawTransaction)
        print(f"  🎯 Buy TX: {tx_hash.hex()}")
        self.bought_tokens[token] = {"amount": amount, "tx": tx_hash.hex()}

if __name__ == "__main__":
    config = {"buy_amount_eth": 0.05, "slippage_pct": 5}
    bot = Sniper("wss://base-mainnet.g.alchemy.com/v2/demo", "0x" + "0" * 64, config)
    asyncio.run(bot.start())