import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #1. THE QUESTION
    This tool is designed to help a student club at Babson College choose the best day for an outdoor event. It compares the weather forecast for the next seven days, considering temperature, chance of rain, and wind speed. Based on these conditions, the tool recommends the best day to organize the event.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #2. MY PLAN BEFORE AI

    **My plan:**

    1. I will use the Geocoding API to find the latitude and longitude of the town selected by the user.

    2. I will use these coordinates to get the weather forecast for the next seven days from Open-Meteo.

    3. I will organize the information in a table showing the date, highest and lowest temperatures, chance of rain, and wind speed.

    4. I will check which days meet all the conditions for the outdoor event: a maximum temperature between 55°F and 80°F, a chance of rain of 30% or less, and wind speed of 15 mph or less.

    5. I will recommend the best day. If several days meet the conditions, I will choose the one with the lowest chance of rain, and then the lowest wind speed. If no day meets all the conditions, I will choose the day that breaks the fewest rules, using the earliest day if there is a tie.

    **Functions I will need:**

    - `get_coordinates(place, state)`: This function will take the town and state as inputs and return its latitude and longitude. It will make sure the town is in the correct state.
    - `get_weather(latitude, longitude)`: This function will use the coordinates to request the weather forecast and return a list with the weather information for each day.

    **API addresses:**

    - Geocoding API: https://geocoding-api.open-meteo.com/v1/search
    - Forecast API: https://api.open-meteo.com/v1/forecast

    **How I will check the data:**

    I will make sure the forecast includes all 7 days by comparing the number of dates returned by the API with the number of rows in my table. Both numbers should be 7. I will also compare the weather values for one day with the original API response in my browser to check that the information is correct.
    """)
    return


if __name__ == "__main__":
    app.run()
