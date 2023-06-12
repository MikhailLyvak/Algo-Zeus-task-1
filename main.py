import requests
import csv
from pprint import pprint
from dataclasses import dataclass
import json
from datetime import datetime
from art import tprint


def get_symbol_data():
    symbol_choice = {1: "ETHUSDT", 2: "BTCUSDT", 3: "ETHBTC", 4: "XRPUSDT", 5: "LTCBTC"}

    intervals = {1: "1h", 2: "4h", 3: "1d"}

    for key, value in symbol_choice.items():
        print(f"{key} -> {value}")

    choosen_symbol = int(
        input(" [+] Choose coin u interested in and push its number here --> ")
    )

    for key, value in intervals.items():
        print(f"{key} -> {value}")

    choosen_interval = int(
        input(
            " [+] Choose date interval u interested in and print its number here --> "
        )
    )

    symbol = symbol_choice.get(choosen_symbol)
    interval = intervals.get(choosen_interval)
    start_date = str(
        input(" [+] Print start date in format yyyy.m.d examle > 2023.6.12 < here --> ")
    )
    end_date = str(
        input(" [+] Print end date in format yyyy.m.d examle > 2023.6.13 < here --> ")
    )

    start = start_date.split(".")
    s_year, s_month, s_day = start[0], start[1], start[2]

    end = end_date.split(".")
    e_year, e_month, e_day = end[0], end[1], end[2]
    URL = "https://api.binance.com/api/v3/klines"

    startTime = str(
        int(datetime(int(s_year), int(s_month), int(s_day)).timestamp() * 1000)
    )
    endTime = str(
        int(datetime(int(e_year), int(e_month), int(e_day)).timestamp() * 1000)
    )
    limit = 1000

    request_params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": startTime,
        "endTime": endTime,
        "limit": limit,
    }

    response = json.loads(requests.get(URL, params=request_params).text)

    @dataclass
    class Coin:
        name: str
        interval: str
        time: str
        open_price: float
        close_price: float
        high_price: float
        low_price: float
        volume: float

    result_date = []

    for coin in response:
        result_date.append(
            Coin(
                name=symbol,
                interval=interval,
                time=datetime.fromtimestamp((coin[0] / 1000)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                open_price=float(coin[1]),
                close_price=float(coin[4]),
                high_price=float(coin[2]),
                low_price=float(coin[3]),
                volume=float(coin[5]),
            )
        )

    output_file = (
        f"{symbol}_from_{start_date}_to_{end_date}_with_interval_{interval}.csv"
    )

    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Symbol",
                "Interval",
                "Time",
                "Open Price",
                "Close Price",
                "High Price",
                "Low Price",
                "Volume",
            ]
        )

        for item in result_date:
            writer.writerow(
                [
                    item.name,
                    item.interval,
                    item.time,
                    item.open_price,
                    item.close_price,
                    item.high_price,
                    item.low_price,
                    item.volume,
                ]
            )

    print(f"Data saved to {output_file}.")


def main():
    tprint("Welcome   to   ALGO-ZEUS")
    get_symbol_data()


if __name__ == "__main__":
    main()
