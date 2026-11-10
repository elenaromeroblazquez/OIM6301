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
    import polars as pl
    from datetime import date

    database = mo.notebook_dir() / "database.duckdb"
    as_of = date(2026, 11, 3)

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return pl.DataFrame(_con.sql(sql))

    return as_of, ask, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **PART B** (Database Project)
    ###**B. Babson Investment Club**

    In this notebook, I will use SQL to answer questions about the club's portfolios, trades, assets, and investment activity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 💡 Reading It Back ...
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 3 - Current Portfolio Holdings

    I expect the joins between trades, portfolios, and assets to return 324 rows before grouping.
    This is because the database contains 324 trades, and each trade belongs to one portfolio and one asset. Joining these three tables should keep the same number of rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ❓ QUESTIONS
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Question 1️⃣
    ##Trading Activity in the Last 30 Days

    How many trades did each portfolio make in the last 30 days, and how much money did it spend and receive?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT
            p.portfolio_id,
            p.portfolio_name,
            COALESCE(SUM(v.total_trades), 0) AS total_trades,
            ROUND(COALESCE(SUM(v.money_spent), 0), 2) AS money_spent,
            ROUND(COALESCE(SUM(v.money_received), 0), 2) AS money_received
        FROM portfolios p
        LEFT JOIN portfolio_daily_activity v
            ON p.portfolio_id = v.portfolio_id
            AND v.trade_date BETWEEN
                DATE '{as_of.isoformat()}' - INTERVAL 29 DAYS
                AND DATE '{as_of.isoformat()}'
        GROUP BY p.portfolio_id, p.portfolio_name
        ORDER BY total_trades DESC, p.portfolio_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Portfolio 8 had the most trading activity in the last 30 days, with 6 trades. It spent $3,534.81 on purchases and received $3,238.40 from sales. Portfolios 7, 13, and 15 had no trades during this period.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Question 2️⃣
    ##Members and Their Portfolios

    How many portfolios does each member own, and how much money have they spent buying assets?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            m.member_id,
            m.first_name,
            m.last_name,
            COUNT(DISTINCT p.portfolio_id) AS total_portfolios,
            ROUND(COALESCE(SUM(
                CASE
                    WHEN t.trade_type = 'buy'
                    THEN t.quantity * t.price_per_unit
                    ELSE 0
                END
            ), 0), 2) AS total_bought
        FROM members m
        LEFT JOIN portfolios p
            ON m.member_id = p.member_id
        LEFT JOIN trades t
            ON p.portfolio_id = t.portfolio_id
        GROUP BY m.member_id, m.first_name, m.last_name
        ORDER BY total_bought DESC, m.member_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Liam Miller has the highest total value of purchases, with $1,059,885.81 across 2 portfolios. Lucas Anderson comes second with $969,066.98. Three members (Charlotte, Henry, and Amelia) have no portfolios and have not made any purchases.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Question 3️⃣
    ##Current Portfolio Holdings

    What assets does each portfolio hold as of November 3, 2026, and how many units does it own?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT
            p.portfolio_id,
            p.portfolio_name,
            a.asset_name,
            ROUND(SUM(
                CASE
                    WHEN t.trade_type = 'buy' THEN t.quantity
                    WHEN t.trade_type = 'sell' THEN -t.quantity
                END
            ), 4) AS units_held
        FROM trades t
        JOIN portfolios p
            ON t.portfolio_id = p.portfolio_id
        JOIN assets a
            ON t.asset_id = a.asset_id
        WHERE t.trade_date <= DATE '{as_of.isoformat()}'
        GROUP BY p.portfolio_id, p.portfolio_name, a.asset_name
        HAVING SUM(
            CASE
                WHEN t.trade_type = 'buy' THEN t.quantity
                WHEN t.trade_type = 'sell' THEN -t.quantity
            END
        ) > 0
        ORDER BY p.portfolio_id, a.asset_name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As of November 3, 2026, the 18 portfolios hold 138 positive asset positions across 10 different assets. For example, Portfolio 1 holds 22 units of Apple, 23 of Meta, and 17 of Amazon. These holdings were calculated by subtracting units sold from units purchased.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Question 4️⃣
    ## Trade Prices vs. Closing Prices

    How did the prices of trades made in the last 90 days compare to the assets' closing prices on those days?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT
            t.trade_id,
            p.portfolio_name,
            a.asset_name,
            t.trade_date,
            ROUND(t.price_per_unit, 2) AS trade_price,
            ROUND(cp.closing_price, 2) AS closing_price,
            ROUND(
                100.0 * (t.price_per_unit - cp.closing_price)
                / NULLIF(cp.closing_price, 0), 2
            ) AS price_difference_pct
        FROM trades t
        JOIN portfolios p
            ON t.portfolio_id = p.portfolio_id
        JOIN assets a
            ON t.asset_id = a.asset_id
        LEFT JOIN closing_prices cp
            ON t.asset_id = cp.asset_id
            AND t.trade_date = cp.price_date
        WHERE t.trade_date BETWEEN
            DATE '{as_of.isoformat()}' - INTERVAL 89 DAYS
            AND DATE '{as_of.isoformat()}'
        ORDER BY t.trade_date DESC, t.trade_id
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT
            COUNT(*) AS total_trades,
            COUNT(*) FILTER (
                WHERE cp.closing_price IS NULL
            ) AS trades_without_closing_price,
            ROUND(AVG(ABS(
                100.0 * (t.price_per_unit - cp.closing_price)
                / NULLIF(cp.closing_price, 0)
            )), 2) AS average_price_difference_pct
        FROM trades t
        LEFT JOIN closing_prices cp
            ON t.asset_id = cp.asset_id
            AND t.trade_date = cp.price_date
        WHERE t.trade_date BETWEEN
            DATE '{as_of.isoformat()}' - INTERVAL 89 DAYS
            AND DATE '{as_of.isoformat()}'
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the last 90 days, the club made 82 trades. Of these, 2 trades had no matching closing price, as expected from the data we generated. For the other 80 trades, the average absolute price difference was 0.24%.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Question 5️⃣
    ## Assests Never Traded
    Which assets does the investment club follow but have never been traded by any portfolio?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            a.asset_id,
            a.asset_name,
            a.asset_type
        FROM assets a
        LEFT JOIN trades t
            ON a.asset_id = t.asset_id
        WHERE t.trade_id IS NULL
        ORDER BY a.asset_name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The investment club follows 12 assets, but 2 of them have never been traded: Ethereum (crypto) and Tesla (stock). The other 10 assets have been traded at least once.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Question 6️⃣
    ## Asset Ticker Changes

    Which asset changed its ticker during the year, and what was its total traded value under both tickers?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            a.asset_name,
            tk.ticker,
            tk.start_date,
            tk.end_date
        FROM asset_tickers tk
        JOIN assets a
            ON tk.asset_id = a.asset_id
        WHERE tk.asset_id IN (
            SELECT asset_id
            FROM asset_tickers
            GROUP BY asset_id
            HAVING COUNT(DISTINCT ticker) > 1
        )
        ORDER BY a.asset_name, tk.start_date
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT
            tk.ticker,
            COUNT(*) AS total_trades,
            ROUND(SUM(t.quantity * t.price_per_unit), 2) AS traded_value,
            ROUND(
                SUM(SUM(t.quantity * t.price_per_unit)) OVER (), 2
            ) AS total_both_tickers
        FROM trades t
        JOIN assets a
            ON t.asset_id = a.asset_id
        JOIN asset_tickers tk
            ON t.asset_id = tk.asset_id
            AND t.trade_date >= tk.start_date
            AND (tk.end_date IS NULL OR t.trade_date <= tk.end_date)
        WHERE a.asset_name = 'Nova Analytics'
            AND t.trade_date <= DATE '{as_of.isoformat()}'
        GROUP BY tk.ticker
        ORDER BY tk.ticker
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Nova Analytics changed its ticker from NOVA to NVAL on May 7, 2026. Before the change, 12 trades had a total value of $4,519.53. After the change, 14 trades had a total value of $7,682.74. Together, the 26 trades represented $12,202.27 in traded value.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Question 7️⃣
    ##Trades Without Closing Prices

    Which trades happened on a day when their asset had no closing price?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            t.trade_id,
            p.portfolio_name,
            a.asset_name,
            t.trade_date,
            t.trade_type
        FROM trades t
        JOIN portfolios p
            ON t.portfolio_id = p.portfolio_id
        JOIN assets a
            ON t.asset_id = a.asset_id
        LEFT JOIN closing_prices cp
            ON t.asset_id = cp.asset_id
            AND t.trade_date = cp.price_date
        WHERE cp.asset_id IS NULL
        ORDER BY t.trade_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The database found 2 trades that happened on days without a closing price: trade 321 (Apple, Portfolio 1) and trade 322 (Microsoft, Portfolio 2). These are the two intentional rule violations included in our generated data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Question 8️⃣
    ##Selling More Units Than Owned

    Which trades sold more units of an asset than the portfolio owned at that time?
    """)
    return


@app.cell
def _(ask):
    ask("""
        WITH trade_history AS (
            SELECT
                t.*,
                COALESCE(
                    SUM(
                        CASE
                            WHEN t.trade_type = 'buy' THEN t.quantity
                            ELSE -t.quantity
                        END
                    ) OVER (
                        PARTITION BY t.portfolio_id, t.asset_id
                        ORDER BY t.trade_date, t.trade_id
                        ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
                    ), 0
                ) AS units_before_trade
            FROM trades t
        )
        SELECT
            t.trade_id,
            p.portfolio_name,
            a.asset_name,
            t.trade_date,
            t.quantity AS units_sold,
            t.units_before_trade,
            t.quantity - t.units_before_trade AS excess_units
        FROM trade_history t
        JOIN portfolios p
            ON t.portfolio_id = p.portfolio_id
        JOIN assets a
            ON t.asset_id = a.asset_id
        WHERE t.trade_type = 'sell'
            AND t.quantity > t.units_before_trade
        ORDER BY t.trade_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The database found 2 trades that violated the selling rule. Trade 323 sold 5 Apple shares when Portfolio 17 had none available. Trade 324 sold 12 Microsoft shares when Portfolio 18 only had 7. Both trades exceeded the available holdings by 5 units.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Question 9️⃣
    ##Current Portfolio Values

    What is the total market value of each portfolio as of November 3, 2026?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        WITH holdings AS (
            SELECT
                portfolio_id,
                asset_id,
                SUM(
                    CASE
                        WHEN trade_type = 'buy' THEN quantity
                        ELSE -quantity
                    END
                ) AS units_held
            FROM trades
            WHERE trade_date <= DATE '{as_of.isoformat()}'
            GROUP BY portfolio_id, asset_id
            HAVING SUM(
                CASE
                    WHEN trade_type = 'buy' THEN quantity
                    ELSE -quantity
                END
            ) > 0
        )
        SELECT
            p.portfolio_id,
            p.portfolio_name,
            COUNT(h.asset_id) AS asset_positions,
            ROUND(
                COALESCE(SUM(h.units_held * cp.closing_price), 0),
                2
            ) AS portfolio_value,
            COUNT(h.asset_id) FILTER (
                WHERE cp.closing_price IS NULL
            ) AS positions_missing_price
        FROM portfolios p
        LEFT JOIN holdings h
            ON p.portfolio_id = h.portfolio_id
        LEFT JOIN closing_prices cp
            ON h.asset_id = cp.asset_id
            AND cp.price_date = DATE '{as_of.isoformat()}'
        GROUP BY p.portfolio_id, p.portfolio_name
        ORDER BY portfolio_value DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As of November 3, 2026, Portfolio 14 has the highest market value at $448,280.08, followed by Portfolio 6 with $407,124.97 and Portfolio 8 with $331,079.99. All 18 portfolios have closing prices available for their positive holdings.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Question 1️⃣0️⃣
    ##Trading Fees by Asset Type

    Which asset type generates the highest trading fees, and how much does the club spend on these fees?
    """)
    return


@app.cell
def _(as_of, ask):
    fee_summary = ask(f"""
        SELECT
            a.asset_type,
            COUNT(*) AS total_trades,
            ROUND(SUM(t.fee), 2) AS total_fees,
            ROUND(SUM(t.quantity * t.price_per_unit), 2) AS traded_value,
            ROUND(
                100.0 * SUM(t.fee)
                / NULLIF(SUM(t.quantity * t.price_per_unit), 0),
                4
            ) AS fee_percentage
        FROM trades t
        JOIN assets a
            ON t.asset_id = a.asset_id
        WHERE t.trade_date <= DATE '{as_of.isoformat()}'
        GROUP BY a.asset_type
        ORDER BY total_fees DESC
    """)
    fee_summary
    return (fee_summary,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Stocks generated the highest trading fees, with $80.50 across 215 trades. ETFs generated $32.00 across 77 trades, and cryptocurrencies generated $15.50 across 32 trades. In total, the club paid $128.00 in fees across 324 trades.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🙃 HOW I KNOW THESE NUMBERS ARE RIGHT
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##✅ Check 1: Total Trading Fees
    I will compare the total number of trades and fees from Question 1️⃣0️⃣ with the totals calculated directly from the trades table.
    """)
    return


@app.cell
def _(ask, fee_summary):
    direct_totals = ask("""
        SELECT
            COUNT(*) AS total_trades,
          ROUND(SUM(fee), 2) AS total_fees
        FROM trades
    """)

    trades_by_type = fee_summary["total_trades"].sum()
    fees_by_type = fee_summary["total_fees"].sum()

    trades_direct = direct_totals["total_trades"][0]
    fees_direct = direct_totals["total_fees"][0]

    print("Trades by asset type:", trades_by_type)
    print("Trades directly:", trades_direct)
    print("Fees by asset type:", fees_by_type)
    print("Fees directly:", fees_direct)

    assert trades_by_type == trades_direct
    assert abs(fees_by_type - fees_direct) < 0.01

    print("Check passed: Both methods agree.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##✅ Check 2: Assest Never Traded
    I will check Question 5 using a different SQL method to see if it returns the same two assets.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            a.asset_name,
            a.asset_type
        FROM assets a
        WHERE NOT EXISTS (
            SELECT 1
            FROM trades t
            WHERE t.asset_id = a.asset_id
        )
        ORDER BY a.asset_name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Both methods returned the same two assets: Ethereum and Tesla. This confirms that these are the only assets that have never been traded.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🤖 WORKING WITH THE AGENT
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In Question 6, the Agent suggested using `at` as an alias for the asset_tickers table, but the query gave me an error.

    I changed the alias to `tk` and ran the query again. This time it worked and returned the two tickers for Nova Analytics (NOVA and NVAL).

    I verified the result by checking that the ticker dates matched the data we generated in Part A.

    The corrected code is in the first SQL query of Question 6.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 💡 Reading It Back ...
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before running the queries, I predicted that joining the trades, portfolios, and assets tables would return 324 rows before grouping. I saved this prediction in the ***db: prediction*** commit.

    I expected 324 rows because the database contains 324 trades, and each trade belongs to one portfolio and one asset.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            COUNT(*) AS joined_rows,
            COUNT(DISTINCT t.trade_id) AS unique_trades
        FROM trades t
        JOIN portfolios p
            ON t.portfolio_id = p.portfolio_id
        JOIN assets a
            ON t.asset_id = a.asset_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The results confirmed my prediction. Joining the three tables returned 324 rows and 324 unique trades, so no trades were duplicated or lost.

    Before grouping, each row represents one trade, including its portfolio and asset information.

    After grouping the data by portfolio and asset in Question 3, the result contained 138 positive holdings. Each row then represented one asset held in one portfolio, rather than an individual trade.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🧠 GOING FURTHER
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I wanted to add a bar chart to make the results from Question 10 easier to understand. It compares the total trading fees paid for stocks, ETFs, and cryptocurrencies.
    """)
    return


@app.cell
def _(fee_summary):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    ax.bar(
        fee_summary["asset_type"].to_list(),
        fee_summary["total_fees"].to_list()
    )

    ax.set_title("Trading Fees by Asset Type")
    ax.set_xlabel("Asset Type")
    ax.set_ylabel("Total Trading Fees ($)")

    fig

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The chart shows that stocks generated the highest trading fees ($80.50), followed by ETF ($32.00) and cryptocurrencies ($15.50).

    This visualization makes it easier to compare trading costs across asset types and helps the investment club understand where most of its fees come from.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ⏰ TIME SPENT:
    Aprox. 2 hours working on part B of this project
    """)
    return


if __name__ == "__main__":
    app.run()
