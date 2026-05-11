import httpx, asyncio

async def send_alert(bot_token: str, chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"})

def format_buy_alert(token: str, amount_eth: float, tx_hash: str) -> str:
    return f"🎯 <b>Sniped!</b>\nToken: <code>{token}</code>\nAmount: {amount_eth} ETH\nTX: <code>{tx_hash[:20]}...</code>"

def format_sell_alert(token: str, pnl_pct: float, tx_hash: str) -> str:
    emoji = "✅" if pnl_pct > 0 else "❌"
    return f"{emoji} <b>Sold</b>\nToken: <code>{token}</code>\nPnL: {pnl_pct:+.1f}%\nTX: <code>{tx_hash[:20]}...</code>"
