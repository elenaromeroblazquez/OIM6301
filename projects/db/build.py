import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo
    import duckdb

    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        import polars as pl
        with duckdb.connect(database, read_only=True) as _con:
            return pl.DataFrame(_con.sql(sql))



    return ask, database, duckdb, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **PART A** (Database Project)
    ###**BabsonAI Labs**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📊 The Tables

    The database contains 6 tables to store information about club members, portfolios, assets, ticker history, trades, and closing prices.
    """)
    return


@app.cell
def _():
    members_sql = """
    CREATE TABLE members (
        member_id INTEGER PRIMARY KEY,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        school_email VARCHAR NOT NULL UNIQUE,
        class_year INTEGER NOT NULL,
        join_date DATE NOT NULL
    );
    """

    return (members_sql,)


@app.cell
def _():
    portfolios_sql = """
    CREATE TABLE portfolios (
        portfolio_id INTEGER PRIMARY KEY,
        member_id INTEGER NOT NULL,
        portfolio_name VARCHAR NOT NULL,
        created_date DATE NOT NULL,
        strategy_label VARCHAR,
        FOREIGN KEY (member_id) REFERENCES members(member_id)
    );
    """

    return (portfolios_sql,)


@app.cell
def _():
    assets_sql = """
    CREATE TABLE assets (
        asset_id INTEGER PRIMARY KEY,
        asset_name VARCHAR NOT NULL,
        asset_type VARCHAR NOT NULL
            CHECK (asset_type IN ('stock', 'ETF', 'crypto')),
        sector VARCHAR
    );
    """

    return (assets_sql,)


@app.cell
def _():
    asset_tickers_sql = """
    CREATE TABLE asset_tickers (
        ticker_history_id INTEGER PRIMARY KEY,
        asset_id INTEGER NOT NULL,
        ticker VARCHAR NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE,
        FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
        CHECK (end_date IS NULL OR end_date >= start_date)
    );
    """

    return (asset_tickers_sql,)


@app.cell
def _():
    trades_sql = """
    CREATE TABLE trades (
        trade_id INTEGER PRIMARY KEY,
        portfolio_id INTEGER NOT NULL,
        asset_id INTEGER NOT NULL,
        trade_date DATE NOT NULL,
        trade_type VARCHAR NOT NULL
            CHECK (trade_type IN ('buy', 'sell')),
        quantity DOUBLE NOT NULL CHECK (quantity > 0),
        price_per_unit DOUBLE NOT NULL CHECK (price_per_unit > 0),
        fee DOUBLE NOT NULL DEFAULT 0 CHECK (fee >= 0),
        FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id),
        FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
        UNIQUE (portfolio_id, asset_id, trade_date)
    );
    """

    return (trades_sql,)


@app.cell
def _():
    closing_prices_sql = """
    CREATE TABLE closing_prices (
        asset_id INTEGER NOT NULL,
        price_date DATE NOT NULL,
        closing_price DOUBLE NOT NULL CHECK (closing_price > 0),
        PRIMARY KEY (asset_id, price_date),
        FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
    );
    """

    return (closing_prices_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🧾 The Data

    I used `make_data.py` to generate six CSV files with a fixed random seed (6301), so the data is the same every time.

    The data covers November 4, 2025, to November 3, 2026.

    I generated 15 members, 18 portfolios, 12 assets, 13 ticker records, 3,340 closing prices, and 324 trades.

    **Intentional rule violations:**

    - Trades 321 and 322: These trades happen on days when the assets have no closing prices.
    - Trades 323 and 324: These trades sell more units than the portfolios own.

    I also included members without portfolios and assets without trades, so the database can answer questions about them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🛠️ Building the Database

    This section creates the database and its 6 tables.
    """)
    return


@app.cell
def _(
    asset_tickers_sql,
    assets_sql,
    closing_prices_sql,
    database,
    duckdb,
    members_sql,
    mo,
    portfolios_sql,
    trades_sql,
):
    # Remove the old database if it exists
    if database.exists():
        database.unlink()

    # Create the database, tables, and load CSV files
    with duckdb.connect(database) as _con:

        # Create all six tables
        for statement in [
            members_sql,
            portfolios_sql,
            assets_sql,
            asset_tickers_sql,
            trades_sql,
            closing_prices_sql,
        ]:
            _con.execute(statement)

        # Load data from CSV files
        tables = [
            "members",
            "portfolios",
            "assets",
            "asset_tickers",
            "closing_prices",
            "trades",
        ]

        for table in tables:
            csv_path = (mo.notebook_dir() / "data" / f"{table}.csv").as_posix()
            csv_path = csv_path.replace("'", "''")

            _con.execute(
                f"COPY {table} FROM '{csv_path}' (HEADER TRUE, DELIMITER ',')"
            )

        # Create a view for portfolio trading activity
        _con.execute("""
            CREATE VIEW portfolio_daily_activity AS
            SELECT
                p.portfolio_id,
                p.portfolio_name,
                t.trade_date,
                COUNT(*) AS total_trades,
                ROUND(SUM(CASE
                    WHEN t.trade_type = 'buy'
                    THEN t.quantity * t.price_per_unit + t.fee
                    ELSE 0
                END), 2) AS money_spent,
                ROUND(SUM(CASE
                    WHEN t.trade_type = 'sell'
                    THEN t.quantity * t.price_per_unit - t.fee
                    ELSE 0
                END), 2) AS money_received
            FROM portfolios p
            JOIN trades t
                ON p.portfolio_id = t.portfolio_id
            GROUP BY p.portfolio_id, p.portfolio_name, t.trade_date
        """)


    print("Database created and all CSV files loaded!")


    return


@app.cell
def _(ask):
    ask("SELECT * FROM portfolio_daily_activity LIMIT 10")
    return


@app.cell
def _(ask):
    ask("SHOW TABLES")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🔎  A Look at the Data

    This chart shows how Apple's simulated closing price changes over time.
    """)
    return


@app.cell
def _(mo):
    import polars as pl
    import matplotlib.pyplot as plt

    # Read the CSV file
    prices_df = pl.read_csv(
        mo.notebook_dir() / "data" / "closing_prices.csv",
        try_parse_dates=True
    )

    # Select Apple (asset_id = 1)
    apple_prices = prices_df.filter(
        pl.col("asset_id") == 1
    ).sort("price_date")

    # Create the chart
    fig, ax = plt.subplots(figsize=(9, 4))

    ax.plot(
        apple_prices["price_date"].to_list(),
        apple_prices["closing_price"].to_list()
    )

    ax.set_title("Apple - Simulated Closing Prices")
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price ($)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    fig

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The prices look reasonably realistic because they show daily fluctuations, with some larger increases and decreases over time. Since the data is simulated, it does not represent Apple's actual stock prices. I did not need to make any changes to the data generation script.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🔢 Row Counts

    This section shows the number of rows in each table.
    """)
    return


@app.cell
def _(ask):
    ask("""
    SELECT 'members' AS table_name, COUNT(*) AS total_rows FROM members
    UNION ALL
    SELECT 'portfolios', COUNT(*) FROM portfolios
    UNION ALL
    SELECT 'assets', COUNT(*) FROM assets
    UNION ALL
    SELECT 'asset_tickers', COUNT(*) FROM asset_tickers
    UNION ALL
    SELECT 'closing_prices', COUNT(*) FROM closing_prices
    UNION ALL
    SELECT 'trades', COUNT(*) FROM trades
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🚩 A Row It Refuses

    This section tests whether the database rejects a row that violates one of its constraints.
    """)
    return


@app.cell
def _(database, duckdb):
    # Try to insert an invalid asset type
    try:
        with duckdb.connect(database) as _con:
            _con.execute("""
                INSERT INTO assets
                (asset_id, asset_name, asset_type, sector)
                VALUES (999, 'Test Asset', 'bond', 'Finance')
            """)
        print("Unexpected: the row was accepted.")

    except Exception as e:
        print("The database rejected the row.")
        print("Error:", e)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🧠  Answers Already Known

    Before running the queries, I expected these results:

    1. **Total members:** 15, because we generated 15 students.
    2. **Members without portfolios:** 3, because only 12 of the 15 members have portfolios.
    3. **Tickers for Nova Analytics:** 2, because the company changes its ticker from NOVA to NVAL.
    """)
    return


@app.cell
def _(ask):
    ask("""
    SELECT COUNT(*) AS total_members
    FROM members
    """)

    return


@app.cell
def _(ask):
    ask("""
    SELECT COUNT(*) AS members_without_portfolios
    FROM members m
    LEFT JOIN portfolios p
        ON m.member_id = p.member_id
    WHERE p.portfolio_id IS NULL
    """)

    return


@app.cell
def _(ask):
    ask("""
    SELECT COUNT(*) AS nova_tickers
    FROM asset_tickers
    WHERE asset_id = 8
    """)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 👁️  A View

    The investment club can use this view every week to check the trading activity of its portfolios, including the number of trades and the money spent or received.
    """)
    return


@app.cell
def _(ask):
    ask("SELECT * FROM portfolio_daily_activity LIMIT 10")
    return


if __name__ == "__main__":
    app.run()
