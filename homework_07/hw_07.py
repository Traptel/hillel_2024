import json
from dataclasses import dataclass
from datetime import datetime
import requests

ALPHAVANTAGE_API_KEY = "WC91R1D8QFCGIZN9"
MIDDLE_CURRENCY = "CHF"


@dataclass
class Price:
    value: float
    currency: str

    def __add__(self, other: "Price") -> "Price":
        if self.currency == other.currency:
            return Price(
                value=(self.value + other.value), currency=self.currency
            )

        left_in_middle: float = convert(
            value=self.value,
            currency_from=self.currency,
            currency_to=MIDDLE_CURRENCY,
        )
        right_in_middle: float = convert(
            value=other.value,
            currency_from=other.currency,
            currency_to=MIDDLE_CURRENCY,
        )

        total_in_middle: float = left_in_middle + right_in_middle
        total_in_left_currency: float = convert(
            value=total_in_middle,
            currency_from=MIDDLE_CURRENCY,
            currency_to=self.currency,
        )

        return Price(value=total_in_left_currency, currency=self.currency)


def convert(value: float, currency_from: str, currency_to: str) -> float:
    response = requests.get(
        f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency="
        f"{currency_from}&to_currency={currency_to}&apikey={ALPHAVANTAGE_API_KEY}"
    )
    result = response.json()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_info = {
        "currency_from": currency_from,
        "currency_to": currency_to,
        "rate": result["Realtime Currency Exchange Rate"]["5. Exchange Rate"],
        "timestamp": timestamp,
    }
    with open("logs.json", "r+") as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            data = {"results": []}
        data["results"].append(log_info)
        file.seek(0)
        json.dump(data, file, indent=4)
    coefficient = float(
        result["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    )
    return value * coefficient


flight = Price(value=200, currency="USD")
hotel = Price(value=1000, currency="UAH")

total = flight + hotel
print(total)
