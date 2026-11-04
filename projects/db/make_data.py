
import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Use a fixed seed to generate the same data every time
random.seed(6301)

# Dates covered by the database
as_of = date(2026, 11, 3)
start_date = as_of - timedelta(days=364)

# Folder where the CSV files will be saved
data_dir = Path(__file__).parent / "data"
data_dir.mkdir(exist_ok=True)

# Generate 15 club members
members = []

first_names = [
    "Emma", "James", "Olivia", "Noah", "Sophia",
    "Liam", "Ava", "Lucas", "Mia", "Ethan",
    "Isabella", "Daniel", "Charlotte", "Henry", "Amelia"
]

last_names = [
    "Smith", "Johnson", "Brown", "Davis", "Wilson",
    "Miller", "Taylor", "Anderson", "Thomas", "Jackson",
    "White", "Harris", "Martin", "Clark", "Lewis"
]

for i in range(15):
    join_date = start_date + timedelta(
        days=random.randint(0, 90)
    )

    members.append({
        "member_id": i + 1,
        "first_name": first_names[i],
        "last_name": last_names[i],
        "school_email": f"{first_names[i].lower()}.{last_names[i].lower()}@babson.edu",
        "class_year": random.randint(2026, 2029),
        "join_date": join_date.isoformat()
    })

with open(data_dir / "members.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=members[0].keys())
    writer.writeheader()
    writer.writerows(members)

print(f"Generated {len(members)} members")


# Generate 18 investment portfolios
portfolios = []

strategies = [
    "Growth",
    "Value",
    "Technology",
    "Diversified",
    "Long-term",
    None
]

for i in range(18):
    member_id = (i % 12) + 1

    member_join_date = date.fromisoformat(
        members[member_id - 1]["join_date"]
    )

    created_date = member_join_date + timedelta(
        days=random.randint(0, 14)
    )

    portfolios.append({
        "portfolio_id": i + 1,
        "member_id": member_id,
        "portfolio_name": f"Portfolio {i + 1}",
        "created_date": created_date.isoformat(),
        "strategy_label": random.choice(strategies)
    })

with open(data_dir / "portfolios.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=portfolios[0].keys())
    writer.writeheader()
    writer.writerows(portfolios)

print(f"Generated {len(portfolios)} portfolios")


# Generate 12 financial assets
assets = [
    {"asset_id": 1, "asset_name": "Apple", "asset_type": "stock", "sector": "Technology"},
    {"asset_id": 2, "asset_name": "Microsoft", "asset_type": "stock", "sector": "Technology"},
    {"asset_id": 3, "asset_name": "NVIDIA", "asset_type": "stock", "sector": "Technology"},
    {"asset_id": 4, "asset_name": "Amazon", "asset_type": "stock", "sector": "Consumer Discretionary"},
    {"asset_id": 5, "asset_name": "Alphabet", "asset_type": "stock", "sector": "Communication Services"},
    {"asset_id": 6, "asset_name": "Tesla", "asset_type": "stock", "sector": "Consumer Discretionary"},
    {"asset_id": 7, "asset_name": "Meta", "asset_type": "stock", "sector": "Communication Services"},
    {"asset_id": 8, "asset_name": "Nova Analytics", "asset_type": "stock", "sector": "Technology"},
    {"asset_id": 9, "asset_name": "S&P 500 ETF", "asset_type": "ETF", "sector": "Diversified"},
    {"asset_id": 10, "asset_name": "Nasdaq 100 ETF", "asset_type": "ETF", "sector": "Technology"},
    {"asset_id": 11, "asset_name": "Bitcoin", "asset_type": "crypto", "sector": None},
    {"asset_id": 12, "asset_name": "Ethereum", "asset_type": "crypto", "sector": None}
]

with open(data_dir / "assets.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=assets[0].keys())
    writer.writeheader()
    writer.writerows(assets)

print(f"Generated {len(assets)} assets")


# Generate ticker history for each asset
asset_tickers = []

tickers = [
    "AAPL", "MSFT", "NVDA", "AMZN",
    "GOOGL", "TSLA", "META", "NOVA",
    "SPY", "QQQ", "BTC", "ETH"
]

for i, ticker in enumerate(tickers):
    asset_tickers.append({
        "ticker_history_id": i + 1,
        "asset_id": i + 1,
        "ticker": ticker,
        "start_date": start_date.isoformat(),
        "end_date": None
    })

# Nova Analytics changes its ticker during the year
change_date = as_of - timedelta(days=180)

asset_tickers[7]["end_date"] = (
    change_date - timedelta(days=1)
).isoformat()

asset_tickers.append({
    "ticker_history_id": 13,
    "asset_id": 8,
    "ticker": "NVAL",
    "start_date": change_date.isoformat(),
    "end_date": None
})

with open(data_dir / "asset_tickers.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=asset_tickers[0].keys())
    writer.writeheader()
    writer.writerows(asset_tickers)

print(f"Generated {len(asset_tickers)} ticker records")


# Generate daily closing prices
closing_prices = []

# Starting prices for each asset
initial_prices = {
    1: 190.0,     # Apple
    2: 430.0,     # Microsoft
    3: 130.0,     # NVIDIA
    4: 205.0,     # Amazon
    5: 175.0,     # Alphabet
    6: 260.0,     # Tesla
    7: 590.0,     # Meta
    8: 60.0,      # Nova Analytics
    9: 610.0,     # S&P 500 ETF
    10: 520.0,    # Nasdaq 100 ETF
    11: 89000.0,  # Bitcoin
    12: 3000.0    # Ethereum
}

for asset in assets:
    asset_id = asset["asset_id"]
    asset_type = asset["asset_type"]
    price = initial_prices[asset_id]

    current_date = start_date

    while current_date <= as_of:

        # Stocks and ETFs trade Monday to Friday
        # Cryptocurrencies trade every day
        if current_date.weekday() < 5 or asset_type == "crypto":

            if asset_type == "crypto":
                volatility = 0.035
            elif asset_type == "ETF":
                volatility = 0.008
            else:
                volatility = 0.018

            daily_change = random.gauss(0, volatility)
            price = max(0.01, price * (1 + daily_change))

            closing_prices.append({
                "asset_id": asset_id,
                "price_date": current_date.isoformat(),
                "closing_price": round(price, 2)
            })

        current_date += timedelta(days=1)

with open(data_dir / "closing_prices.csv", "w",
          newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file, fieldnames=closing_prices[0].keys()
    )
    writer.writeheader()
    writer.writerows(closing_prices)

print(f"Generated {len(closing_prices)} closing prices")


# Generate 320 valid trades
trades = []
holdings = {}

# Leave Tesla and Ethereum without trades
traded_asset_ids = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]

# Look up closing prices by asset and date
price_lookup = {
    (row["asset_id"], row["price_date"]): row["closing_price"]
    for row in closing_prices
}

# Keep available trading dates for each asset
cutoff = (as_of - timedelta(days=4)).isoformat()

available_dates = {
    asset_id: [
        row["price_date"]
        for row in closing_prices
        if row["asset_id"] == asset_id
        and row["price_date"] <= cutoff
    ]
    for asset_id in traded_asset_ids
}

# Plan 320 trades on valid dates
planned_trades = []
used_combinations = set()

while len(planned_trades) < 320:
    portfolio = random.choice(portfolios)
    portfolio_id = portfolio["portfolio_id"]
    asset_id = random.choice(traded_asset_ids)

    valid_dates = [
        day for day in available_dates[asset_id]
        if day >= portfolio["created_date"]
    ]

    trade_date = random.choice(valid_dates)
    combination = (portfolio_id, asset_id, trade_date)

    if combination in used_combinations:
        continue

    used_combinations.add(combination)
    planned_trades.append(combination)

# Process trades in chronological order
planned_trades.sort(key=lambda x: (x[2], x[0], x[1]))

for portfolio_id, asset_id, trade_date in planned_trades:
    key = (portfolio_id, asset_id)
    owned = holdings.get(key, 0)

    if owned > 0 and random.random() < 0.4:
        trade_type = "sell"
        quantity = random.randint(1, owned)
        holdings[key] -= quantity
    else:
        trade_type = "buy"
        quantity = random.randint(1, 8)
        holdings[key] = owned + quantity

    closing_price = price_lookup[(asset_id, trade_date)]
    trade_price = round(
        closing_price * random.uniform(0.995, 1.005), 2
    )

    trades.append({
        "trade_id": len(trades) + 1,
        "portfolio_id": portfolio_id,
        "asset_id": asset_id,
        "trade_date": trade_date,
        "trade_type": trade_type,
        "quantity": quantity,
        "price_per_unit": trade_price,
        "fee": random.choice([0, 0, 0.5, 1.0])
    })

# Two intentional violations:
# Trades on days without closing prices
for portfolio_id, asset_id, trade_date in [
    (1, 1, "2026-10-31"),
    (2, 2, "2026-11-01")
]:
    trades.append({
        "trade_id": len(trades) + 1,
        "portfolio_id": portfolio_id,
        "asset_id": asset_id,
        "trade_date": trade_date,
        "trade_type": "buy",
        "quantity": 2,
        "price_per_unit": price_lookup[
            (asset_id, "2026-10-30")
        ],
        "fee": 0
    })

# Two intentional violations:
# Selling more units than the portfolio owns
for portfolio_id, asset_id in [(17, 1), (18, 2)]:
    owned = holdings.get((portfolio_id, asset_id), 0)

    trades.append({
        "trade_id": len(trades) + 1,
        "portfolio_id": portfolio_id,
        "asset_id": asset_id,
        "trade_date": as_of.isoformat(),
        "trade_type": "sell",
        "quantity": owned + 5,
        "price_per_unit": price_lookup[
            (asset_id, as_of.isoformat())
        ],
        "fee": 0
    })

# Save trades to CSV
with open(
    data_dir / "trades.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:
    writer = csv.DictWriter(
        file, fieldnames=trades[0].keys()
    )
    writer.writeheader()
    writer.writerows(trades)

print(f"Generated {len(trades)} trades")
print("Missing closing prices: trades 321 and 322")
print("Overselling: trades 323 and 324")
