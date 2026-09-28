from decimal import Decimal


class CurrencyService:

    RATES_FROM_PKR = {
        "PKR": Decimal("1"),
        "USD": Decimal("278"),
        "GBP": Decimal("375"),
    }

    @classmethod
    def convert_from_pkr(
        cls,
        amount,
        currency,
    ):
        if currency not in cls.RATES_FROM_PKR:
            raise ValueError(
                "Unsupported currency."
            )

        rate = cls.RATES_FROM_PKR[currency]

        return (
            Decimal(amount) / rate
        ).quantize(
            Decimal("0.01")
        )

    @classmethod
    def get_rate(cls, currency):
        if currency not in cls.RATES_FROM_PKR:
            raise ValueError(
                "Unsupported currency."
            )

        return cls.RATES_FROM_PKR[currency]