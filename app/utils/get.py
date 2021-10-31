def get_currency_op(currency: str):
    index_dict = {
        "rmb": "￥",
        "jpn": "￥",
        "eur": "€",
        "usd": "$"
    }

    return index_dict.get(currency.lower(), "￥")
