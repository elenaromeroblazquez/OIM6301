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

    return (mo,)


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
    ## Reading It Back

    ### Question 3 - Current Portfolio Holdings

    I expect the joins between trades, portfolios, and assets to return 324 rows before grouping.
    This is because the database contains 324 trades, and each trade belongs to one portfolio and one asset. Joining these three tables should keep the same number of rows.
    """)
    return


if __name__ == "__main__":
    app.run()
