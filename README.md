# base-sniper-bot

> Token Launch Sniper for Base L2

Monitor Base for new token pool creations on Uniswap v3 and Aerodrome, and execute instant buy orders when a new listing matches your criteria. Built with anti-rug filters.

## Features
- 🔭 Real-time new pool detection (WebSocket)
- ⚡ Sub-second execution via private RPC
- 🛡️ Built-in rug pull filters (liquidity lock check, ownership renounced)
- 💰 Configurable buy amount and slippage
- 📊 Auto sell at target profit (take-profit)
- 🚫 Blacklist known scam deployers
- 📱 Telegram alerts on buy/sell

## Safety Filters (applied before buying)
- ✅ LP must be > $10k
- ✅ Owner renounced or no mint function
- ✅ Contract verified on Basescan
- ✅ No transfer tax > 5%
- ✅ Max wallet > 1%

## Setup
```bash
git clone https://github.com/fabt31/base-sniper-bot
cd base-sniper-bot
pip install -r requirements.txt
cp config.example.yml config.yml
python main.py
```

## Configuration
```yaml
rpc_ws: wss://base-mainnet.g.alchemy.com/v2/YOUR_KEY
private_key: "0x..."
buy_amount_eth: 0.05
slippage_pct: 5
take_profit_pct: 100   # sell at 2x
stop_loss_pct: 50      # sell at -50%
min_liquidity_usd: 10000
filters:
  require_renounced: true
  max_tax_pct: 5
```

## Disclaimer
Sniping bots carry extreme financial risk including total loss of funds. Use only funds you can afford to lose.

## License
MIT