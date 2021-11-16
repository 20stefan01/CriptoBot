import requests
import json
from Config import keys


class ConvertionException(Exception):
    pass


class CryptoConvertor:
    def convert(base: str, quote: str, amount: str):
        if base == quote:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
            if amount < 0:
                raise ConvertionException(f'Не удалось обработать количество {amount}')
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total = round(json.loads(r.content)[keys[quote]]*amount, 2)
        return total
