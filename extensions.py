import json
import requests
from token_value import keys

class ExchangeException(Exception):
    pass

class Exchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ExchangeException(f'Одинаковая валюта исправьте {base}.')

        try:
            quote_key = keys[quote]
        except KeyError:
            raise ExchangeException(f'Не известная валюта {quote}')

        try:
            base_key = keys[base]
        except KeyError:
            raise ExchangeException(f'Не известная валюта {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ExchangeException(f'введите количество корректно {amount}')


        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_key}&tsyms={base_key}')

        total_base = json.loads(r.content)[keys[base]]
        total_base = total_base * amount
        return total_base
