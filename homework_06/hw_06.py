CURRENCY_RATES = {
    "USD": {"UAH": 38.17, "CHF": 0.89},
    "UAH": {"USD": 0.026, "CHF": 0.023},
    "CHF": {"USD": 1.13, "UAH": 43.12, "CHF": 1},
}


def convert(value: float, from_currency: str, to_currency: str) -> float:
    return value * CURRENCY_RATES[from_currency][to_currency]


class Price:
    def __init__(self, value: float, currency: str) -> None:
        self.value = value
        self.currency = currency

    def __add__(self, other: "Price") -> "Price":
        if self.currency == other.currency:
            return Price(
                value=self.value + other.value, currency=self.currency
            )

        left_value: float = convert(
            value=self.value,
            from_currency=self.currency,
            to_currency="CHF",
        )

        right_value: float = convert(
            value=other.value,
            from_currency=other.currency,
            to_currency="CHF",
        )

        total_in_pounds = left_value + right_value

        total_in_left: float = convert(
            value=total_in_pounds,
            from_currency="CHF",
            to_currency=self.currency,
        )

        return Price(value=total_in_left, currency=self.currency)

    def __sub__(self, other: "Price") -> "Price":
        if self.currency == other.currency:
            return Price(
                value=self.value - other.value, currency=self.currency
            )

        left_value: float = convert(
            value=self.value,
            from_currency=self.currency,
            to_currency="CHF",
        )

        right_value: float = convert(
            value=other.value,
            from_currency=other.currency,
            to_currency="CHF",
        )

        total_in_pounds = left_value - right_value

        total_in_left: float = convert(
            value=total_in_pounds,
            from_currency="CHF",
            to_currency=self.currency,
        )
        return Price(value=total_in_left, currency=self.currency)

    def __repr__(self) -> str:
        return f"Price: {self.value} '{self.currency}'"


price1 = Price(1000, "USD")
price2 = Price(500, "USD")
price3 = Price(8000, "UAH")

print("Operations with same currency:")
print(price1 + price2)
print(price1 - price2)

print("Operations with different currencies:")
print(price1 + price3)
print(price1 - price3)
