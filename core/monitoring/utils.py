import yfinance as yf
from decimal import Decimal

from .models import Asset, PriceHistory

from django.conf import settings
from django.core.mail import send_mail

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
    
def send_alert_email(asset: Asset, price: Decimal, allert_type:str):
    # Emails alerting for buying or selling
    subject = f'[Atenção] Ativo {asset.symbol} - {allert_type.upper()}'
    body = f''''
            O ativo {asset.symbol} ({asset.name}) atingiu o preço de R${price} \nLimite configurado: {asset.inferior_limit} - {asset.superior_limit}\n\n Sugestão: {str.upper(allert_type)}!
            '''
    
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email_list = [settings.EMAIL_HOST_USER]

    send_mail(subject,body,from_email,to_email_list)
    
def check_and_save_price(asset: Asset):
    # Checks and saves assets current price, and sends email in case it crosses limits

    price = fetch_asset_current_price(asset.symbol)
    PriceHistory.objects.create(asset, price)

    # If price cross lower limt, sugest buying
    if price <= asset.inferior_limit:
        send_alert_email(asset, price, 'buy')

    # If price cross upper limit, sugest selling
    elif price >= asset.superior_limit:
        send_alert_email(asset, price, 'sell')