import os
import sys
import json
import requests
import urllib.parse
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, BalanceAllowanceParams, OrderArgs
from py_clob_client.order_builder.constants import BUY, SELL

# Configuration
KEY = os.getenv("POLYMARKET_KEY")
HOST = "https://clob.polymarket.com"
CHAIN_ID = 137

def get_proxy_wallet(signer_address):
    """Auto-detect the Proxy Wallet (Funder) address via Gamma API."""
    try:
        url = f"https://gamma-api.polymarket.com/public-profile?address={signer_address.lower()}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json().get("proxyWallet")
    except Exception as e:
        print(f"Warning: Proxy detection failed ({e})")
    return None

def get_client():
    if not KEY:
        print("Error: POLYMARKET_KEY not set.")
        return None, None
        
    try:
        tmp_client = ClobClient(HOST, key=KEY, chain_id=CHAIN_ID)
        signer_addr = tmp_client.get_address()
        funder = os.getenv("POLYMARKET_FUNDER") or get_proxy_wallet(signer_addr)
        
        creds_raw = tmp_client.create_or_derive_api_creds()
        if isinstance(creds_raw, dict):
            creds = ApiCreds(
                api_key=creds_raw['apiKey'],
                api_secret=creds_raw['secret'],
                api_passphrase=creds_raw['passphrase']
            )
        else:
            creds = creds_raw
            
        sig_type = 1 if funder and funder.lower() != signer_addr.lower() else None
        client = ClobClient(HOST, key=KEY, chain_id=CHAIN_ID, creds=creds, funder=funder, signature_type=sig_type)
        return client, funder
    except Exception as e:
        print(f"Auth Error: {e}")
        return None, None

def show_portfolio():
    client, funder = get_client()
    if not client: return
    
    signer_addr = client.get_address()
    print(f"🔑 Signer: {signer_addr}")
    print(f"🏦 Funder: {funder or 'Self (EOA)'}")
    
    # 1. Fetch Cash Balance (CLOB)
    cash = 0.0
    try:
        sig_type = 1 if funder and funder.lower() != signer_addr.lower() else 0
        params = BalanceAllowanceParams(asset_type="COLLATERAL", signature_type=sig_type)
        res = client.get_balance_allowance(params=params)
        cash = float(res.get('balance', '0')) / 1e6
        print(f"💵 Available Cash: ${cash:.2f} USDC")
    except Exception as e:
        print(f"Cash fetch failed: {e}")

    # 2. Fetch Holdings & P&L (Data API)
    holdings_value = 0.0
    if funder:
        try:
            print("\n📊 Current Positions:")
            url = f"https://data-api.polymarket.com/positions?user={funder}"
            r = requests.get(url, timeout=10)
            positions = r.json()
            
            if not positions:
                print("No open positions.")
            else:
                for p in positions:
                    title = p.get('title', 'Unknown')
                    outcome = p.get('outcome', 'N/A')
                    size = float(p.get('size', 0))
                    avg_price = float(p.get('avgPrice', 0))
                    cur_price = float(p.get('curPrice', 0))
                    pnl_val = float(p.get('cashPnl', 0))
                    pnl_pct = float(p.get('percentPnl', 0))
                    cur_val = float(p.get('currentValue', 0))
                    holdings_value += cur_val
                    
                    pnl_str = f"${pnl_val:+.2f} ({pnl_pct:+.2f}%)"
                    print(f"• {title}")
                    print(f"  Holding: {size:.2f} shares of [{outcome}]")
                    print(f"  Price: Buy ${avg_price:.3f} | Now ${cur_price:.3f}")
                    print(f"  Value: ${cur_val:.2f} | P&L: {pnl_str}")
                    print("-" * 20)
        except Exception as e:
            print(f"Holdings fetch failed: {e}")

    # 3. Summary
    print(f"\n📈 Portfolio Summary:")
    print(f"   Invested Value:  ${holdings_value:.2f}")
    print(f"   Available Cash:  ${cash:.2f}")
    print(f"   Total Portfolio: ${cash + holdings_value:.2f}")

    # 4. Recent Trades (CLOB)
    try:
        print("\n🔍 Recent Trade Activity (Last 3):")
        trades = client.get_trades()
        if trades:
            for i, t in enumerate(trades[:3]):
                match_time = t.get('match_time', 'N/A')
                print(f"{i+1}. {t.get('side')} {t.get('size')} @ {t.get('price')} (Outcome: {t.get('outcome')})")
        else:
            print("No recent trades.")
    except Exception as e:
        print(f"History fetch failed: {e}")

def lookup(query):
    client, _ = get_client()
    if not client: return
    try:
        print(f"🔍 Searching active markets for '{query}'...")
        encoded_query = urllib.parse.quote(query)
        url = f"https://gamma-api.polymarket.com/markets?search={encoded_query}&active=true&closed=false&limit=5"
        r = requests.get(url, timeout=10)
        markets = r.json()
        
        if not markets:
            print("No matching markets found.")
            return

        for m in markets:
            print(f"\n🎯 {m.get('question')}")
            try:
                tokens = json.loads(m.get('clobTokenIds', '[]'))
                outcomes = json.loads(m.get('outcomes', '["Yes", "No"]'))
                prices = json.loads(m.get('outcomePrices', '["0", "0"]'))
                for i, (token, outcome, price) in enumerate(zip(tokens, outcomes, prices)):
                    print(f"   [{outcome}] ID: {token} (Price: ${float(price):.2f})")
            except:
                print("   (Unable to parse tokens)")
    except Exception as e:
        print(f"Lookup failed: {e}")

def buy(token_id, amount_usdc):
    client, _ = get_client()
    if not client: return
    try:
        print(f"🛒 Preparing to buy ${amount_usdc} USDC of token {token_id}...")
        book = client.get_order_book(token_id)
        if not book.asks:
            print("❌ Error: No liquidity (no sellers).")
            return
        best_ask = float(book.asks[0].price)
        limit_price = min(best_ask + 0.01, 0.99)
        size = amount_usdc / limit_price
        
        resp = client.create_and_post_order(OrderArgs(price=limit_price, size=size, side=BUY, token_id=token_id))
        if resp.get('success'):
            print(f"✅ SUCCESS! Order ID: {resp.get('orderID')}")
        else:
            print(f"❌ FAILED: {resp.get('errorMsg') or resp}")
    except Exception as e:
        print(f"Order failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_portfolio()
    else:
        cmd = sys.argv[1]
        if cmd == "balance" or cmd == "portfolio":
            show_portfolio()
        elif cmd == "lookup" and len(sys.argv) > 2:
            lookup(" ".join(sys.argv[2:]))
        elif cmd == "buy" and len(sys.argv) == 4:
            buy(sys.argv[2], float(sys.argv[3]))
        else:
            print("Usage: python3 trader.py [balance|lookup <query>|buy <token_id> <amount>]")
