# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This tool helps financial advisors manage their clients' portfolios. It shows how many shares they should buy or sell to reach their target percentages and how much cash they will have left.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, I will calculate the value of each stock by multiplying the number of shares by its price.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Second, I will add all the stock values and the cash to find the total portfolio value.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Third, I will calculate how much money should be invested in each stock and how many shares I need to buy or sell to get closer to the target.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finally, I will calculate the remaining cash and check how close each stock is to its target percentage.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Q1: The loop will go through each stock and add its value to a running total until I get the total portfolio value.


    Q2: I will compare the total portfolio value before and after rebalancing. Both numbers should be the same as buying and selling shares don't change the value of the portfolio.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    holdings = [
        ("AAPL", 100, 173.93),
        ("MSFT", 50, 319.53),
        ("GOOG", 80, 131.36),
        ("AMZN", 200, 129.33),
        ("NVDA", 20, 410.17),
        ("TSLA", 150, 255.70),
    ]
    cash = 5000.00
    target_weights = {"AAPL": 0.20, "MSFT": 0.20, "GOOG": 0.15,
                      "AMZN": 0.15, "NVDA": 0.15, "TSLA": 0.15}
    return cash, holdings, target_weights


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(cash, holdings):
    total_value = cash

    for stock in holdings:
        shares = stock[1]
        price = stock[2]
        stock_value = shares * price
        total_value += stock_value

    print(f"Total portfolio value: ${total_value:,.2f}")
    return (total_value,)


@app.cell
def _(holdings, target_weights, total_value):
    for company in holdings:
        ticker = company[0]
        weight = target_weights[ticker]
        target_amount = total_value * weight

        print(f"{ticker}: ${target_amount:,.2f}")
    return


@app.cell
def _(holdings, target_weights, total_value):
    for item in holdings:
        stock_name = item[0]
        current_shares = item[1]
        stock_price = item[2]

        desired_value = total_value * target_weights[stock_name]
        desired_shares = int(desired_value // stock_price)

        shares_difference = desired_shares - current_shares

        print(f"{stock_name}: {desired_shares} shares, difference: {shares_difference}")
    return


@app.cell
def _(holdings, target_weights, total_value):
    for holding in holdings:
        name = holding[0]
        price_per_share = holding[2]

        target_number = int(
            (total_value * target_weights[name]) // price_per_share
        )

        final_value = target_number * price_per_share
        final_weight = (final_value / total_value) * 100

        print(f"{name}: ${final_value:,.2f} ({final_weight:.2f}%)")
    return


@app.cell
def _(cash, holdings, target_weights, total_value):
    remaining_cash = cash

    for position in holdings:
        company_name = position[0]
        shares_now = position[1]
        share_price = position[2]

        target_money = total_value * target_weights[company_name]
        shares_target = int(target_money // share_price)

        shares_to_trade = shares_target - shares_now
        trade_value = shares_to_trade * share_price

        remaining_cash -= trade_value

    print(f"Remaining cash: ${remaining_cash:,.2f}")
    return (remaining_cash,)


@app.cell
def _(holdings, remaining_cash, target_weights, total_value):
    total_after = remaining_cash

    for asset in holdings:
        asset_name = asset[0]
        asset_price = asset[2]

        new_shares = int(
            (total_value * target_weights[asset_name]) // asset_price
        )

        total_after += new_shares * asset_price

    print(f"Before rebalancing: ${total_value:,.2f}")
    print(f"After rebalancing: ${total_after:,.2f}")
    return (total_after,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(holdings, target_weights, total_value):
    print(f"{'Stock':<8}{'Now':>8}{'Target':>10}{'Trade':>10}{'Value After':>16}{'Weight':>10}{'Gap (pp)':>12}")

    for row in holdings:
        ticker_final = row[0]
        shares_current = row[1]
        price_final = row[2]

        shares_goal = int(
            (total_value * target_weights[ticker_final]) // price_final
        )

        trade_final = shares_goal - shares_current
        value_after = shares_goal * price_final
        weight_after = value_after / total_value * 100
        weight_gap = abs(weight_after - target_weights[ticker_final] * 100)
    
        print(f"{ticker_final:<8}{shares_current:>8}{shares_goal:>10}{trade_final:>10}{value_after:>16,.2f}{weight_after:>9.2f}%{weight_gap:>12.2f}")
    return


@app.cell
def _(remaining_cash):
    print(f"\nRemaining cash: ${remaining_cash:,.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The tool shows how many shares we need to buy or sell to get closer to our target percentages, leaving $725.62 in cash.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The final percentages are very close to the targets. There are small differences because we can only buy or sell whole shares, but I think the portfolio is well balanced.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(cash, holdings, total_after):
    check_value = cash

    for check_stock in holdings:
        check_shares = check_stock[1]
        check_price = check_stock[2]

        check_value += check_shares * check_price

    print(f"Original portfolio value: ${check_value:,.2f}")
    print(f"Rebalanced portfolio value: ${total_after:,.2f}")
    print(f"Difference: ${abs(check_value - total_after):,.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I checked the portfolio value in 2 different ways.

    1- I calculated the original value using the shares, prices, and cash.

    2- I compared it with the value after rebalancing.

    Both results were $121,302.70, with no difference between them. This shows that the total portfolio value stayed the same after buying and selling shares.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When I calculated the total portfolio value, the AI told me that total should be $121,706.10, but my code showed $121,302.70.

    Instead of changing my code, I checked the original data and the calculations. I found that my result was correct and the AI had made a mistake.

    This showed me why it is important to check AI answers instead of just trusting them. You can see this calculation in Section 4.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _(holdings, target_weights, total_value):
    for extra_stock in holdings:
        extra_name = extra_stock[0]
        extra_shares = extra_stock[1]
        extra_price = extra_stock[2]

        extra_target = int(
            (total_value * target_weights[extra_name]) // extra_price
        )

        extra_difference = extra_target - extra_shares

        if extra_difference > 0:
            print(f"{extra_name}: Buy {extra_difference} shares")
        elif extra_difference < 0:
            print(f"{extra_name}: Sell {abs(extra_difference)} shares")
        else:
            print(f"{extra_name}: No trade needed")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I added an extra step that shows whether we need to buy, sell, or keep each stock. I used if, elif, and else to do this.
    The results show that we need to buy shares of AAPL, MSFT, GOOG, and NVDA, and sell shares of AMZN and TSLA.
    This makes the results easier to read because the user does not have to interpret positive and negative numbers. I just wanted to make the tool easier to understand and use the if/elif/else commands from previous sessions.
    """)
    return


if __name__ == "__main__":
    app.run()
