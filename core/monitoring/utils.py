import yfinance as yf
from decimal import Decimal

from models import Asset, PriceHistory

def fetch_asset_current_price(symbol: str) -> Decimal:
    # Getting asset's current price using yahoo finance's API
    try:
        # getting data througn the symbole and it's current price
        asset = yf.Ticker(symbol)
        price = asset.info.get('regularMarketPrice')

        if not price:
            raise ValueError(f"Can't obtain {symbol}'s price. Check if the symbol is correct")

        return Decimal(price)
    
    except Exception as e:
        print(f"Something went wrong searching the asset {symbol}: {e}")
        return Decimal("0.0")
    
def send_alert_email(asset, price, type):
    pass
    
def check_and_save_price(asset: Asset):
    # Checks and saves assets current price, and sends email in case it crosses limits

    price = fetch_asset_current_price(asset.symbol)
    PriceHistory.objects.create(asset, price)

    # If price cross lower limt, sugest buying
    if price <= asset.inferior_limit:
        send_alert_email(asset, price, type='buy')

    # If price cross upper limit, sugest selling
    elif price >= asset.superior_limit:
        send_alert_email(asset, price, type='sell')