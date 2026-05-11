from dataclasses import dataclass
import httpx, asyncio

BASESCAN_API = "https://api.basescan.org/api"

@dataclass
class FilterResult:
    passed: bool; reasons: list

async def check_contract_verified(address: str, api_key: str) -> bool:
    async with httpx.AsyncClient() as client:
        r = await client.get(BASESCAN_API, params={"module":"contract","action":"getsourcecode","address":address,"apikey":api_key}, timeout=10)
        data = r.json()
        if data.get("status") == "1" and data["result"][0].get("SourceCode"):
            return True
    return False

async def run_filters(token: str, config: dict) -> FilterResult:
    reasons = []
    if config.get("require_verified"):
        verified = await check_contract_verified(token, config.get("basescan_key", ""))
        if not verified: reasons.append("Contract not verified on Basescan")
    return FilterResult(passed=len(reasons) == 0, reasons=reasons)
