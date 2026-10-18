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
    #1. ❓ THE QUESTION
    This tool is designed to help a student club at Babson College choose the best day for an outdoor event. It compares the weather forecast for the next seven days, considering temperature, chance of rain, and wind speed. Based on these conditions, the tool recommends the best day to organize the event.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #2. 💡 MY PLAN BEFORE AI

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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. 🌡️☔🌤️ INPUTS
    """)
    return


@app.cell
def _():
    place = "Wellesley"
    state = "Massachusetts"

    lowest_high_f = 55
    highest_high_f = 80

    max_rain_chance = 5
    max_wind_mph = 15

    return (
        highest_high_f,
        lowest_high_f,
        max_rain_chance,
        max_wind_mph,
        place,
        state,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #4. 💻 THE WORK
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Function get_coordinates():** function that uses the Geocoding API to find the latitude and longitude of Wellesley, MA, so we can get its weather forecast.
    """)
    return


@app.cell
def _():
    import requests

    def get_coordinates(place, state):
        url = "https://geocoding-api.open-meteo.com/v1/search"

        params = {
            "name": place,
            "count": 100,
            "language": "en",
            "format": "json"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        for _location in data.get("results", []):
            if _location["admin1"] == state and _location["country_code"] == "US":
                return _location["latitude"], _location["longitude"]

        raise ValueError("Town not found in the selected state")


    return get_coordinates, requests


@app.cell
def _(get_coordinates, place, state):
    latitude, longitude = get_coordinates(place, state)

    print(latitude, longitude)

    return latitude, longitude


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It correctly returns the latitude (42.29649) and longitude (-71.29256) of Wellesley, MA.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Function get_weather():** I want get_weather() to use these coordinates to request the weather forecast for the next 7 days from the Forecast API.
    """)
    return


@app.cell
def _(requests):
    def get_weather(latitude, longitude):
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "timezone": "America/New_York",
            "forecast_days": 7
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        daily = response.json()["daily"]

        weather = []

        for _i in range(len(daily["time"])):
            weather.append({
                "date": daily["time"][_i],
                "high_f": daily["temperature_2m_max"][_i],
                "low_f": daily["temperature_2m_min"][_i],
                "rain_chance": daily["precipitation_probability_max"][_i],
                "wind_mph": daily["wind_speed_10m_max"][_i]
            })

        return weather


    return (get_weather,)


@app.cell
def _(get_weather, latitude, longitude):
    weather = get_weather(latitude, longitude)

    for _day in weather:
        print(_day)

    return (weather,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This function uses Wellesley's coordinates to get the weather forecast for the next 7 days and organizes the data into a list of daily records.
    """)
    return


@app.cell
def _(weather):
    import json
    from pathlib import Path

    _data_folder = Path("projects/mp2/data")
    _data_folder.mkdir(parents=True, exist_ok=True)

    _data_file = _data_folder / "weather_data.json"

    with open(_data_file, "w", encoding="utf-8") as _file:
        json.dump(weather, _file, indent=2)

    print(f"Saved {len(weather)} days of weather data.")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *I saved the weather data from the API in a JSON file, so I have a copy of the information.*
    """)
    return


@app.cell
def _(highest_high_f, lowest_high_f, max_rain_chance, max_wind_mph, weather):
    for _day in weather:
        _good_temp = lowest_high_f <= _day["high_f"] <= highest_high_f
        _good_rain = _day["rain_chance"] <= max_rain_chance
        _good_wind = _day["wind_mph"] <= max_wind_mph

        if _good_temp and _good_rain and _good_wind:
            _day["passes"] = "Yes"
        else:
            _day["passes"] = "No"

        print(_day["date"], _day["passes"])

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I checked the weather conditions for each of the 7 days. The program found that 5 days meet all the requirements for the outdoor event, while 2 days do not.
    """)
    return


@app.cell
def _(highest_high_f, lowest_high_f, max_rain_chance, max_wind_mph, weather):
    best_day = None

    for _day in weather:
        if _day["passes"] == "Yes":
            if best_day is None:
                best_day = _day
            elif _day["rain_chance"] < best_day["rain_chance"]:
                best_day = _day
            elif _day["rain_chance"] == best_day["rain_chance"] and _day["wind_mph"] < best_day["wind_mph"]:
                best_day = _day

    if best_day is not None:
        print(f"The best day is {best_day['date']}, with {best_day['rain_chance']}% chance of rain and {best_day['wind_mph']} mph wind.")
    else:
        _backup_day = None
        _fewest_broken = 4

        for _day in weather:
            _broken_rules = 0

            if not (lowest_high_f <= _day["high_f"] <= highest_high_f):
                _broken_rules += 1

            if _day["rain_chance"] > max_rain_chance:
                _broken_rules += 1

            if _day["wind_mph"] > max_wind_mph:
                _broken_rules += 1

            if _broken_rules < _fewest_broken:
                _fewest_broken = _broken_rules
                _backup_day = _day

        best_day = _backup_day

        print(f"No day meets all conditions. The best alternative is {_backup_day['date']}, which breaks {_fewest_broken} rules.")


    return (best_day,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The program recommends October 19. I also added an alternative in case no day meets all the conditions, choosing the day that breaks the fewest rules.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #5. ✏️ THE ANSWER
    """)
    return


@app.cell
def _(weather):
    print(f"{'Date':<12} {'High (F)':>9} {'Low (F)':>9} {'Rain (%)':>9} {'Wind (mph)':>11} {'Passes':>8}")
    print("-" * 65)

    for _day in weather:
        print(f"{_day['date']:<12} {_day['high_f']:>9.1f} {_day['low_f']:>9.1f} {_day['rain_chance']:>9} {_day['wind_mph']:>11.1f} {_day['passes']:>8}")

    return


@app.cell
def _(best_day, place):
    if best_day["passes"] == "Yes":
        print(f"The best day for an outdoor event in {place} is {best_day['date']}, with a high of {best_day['high_f']}°F, {best_day['rain_chance']}% chance of rain, and {best_day['wind_mph']} mph wind.")
    else:
        print(f"No day meets all the conditions in {place}. The best alternative is {best_day['date']}, with a high of {best_day['high_f']}°F, {best_day['rain_chance']}% chance of rain, and {best_day['wind_mph']} mph wind.")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #6. 🔢 HOW I KNOW THESE NUMBERS ARE RIGHT
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **I will check the results in 2 ways:**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ####First one
    """)
    return


@app.cell
def _(latitude, longitude, requests, weather):
    check_url = "https://api.open-meteo.com/v1/forecast"

    check_params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max",
        "timezone": "America/New_York",
        "forecast_days": 7
    }

    check_response = requests.get(check_url, params=check_params)
    check_response.raise_for_status()

    api_days = len(check_response.json()["daily"]["time"])
    table_days = len(weather)

    print(f"Days returned by the API: {api_days}")
    print(f"Days in our table: {table_days}")
    print(f"Do they match? {api_days == table_days}")

    return (check_url,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I compared the number of days returned by the API with the number of days in our table. Both have 7 days, so no records are missing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ####Second one:
    """)
    return


@app.cell
def _(check_url, latitude, longitude, requests, weather):
    value_check_params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max",
        "temperature_unit": "fahrenheit",
        "timezone": "America/New_York",
        "forecast_days": 7
    }

    value_check_response = requests.get(check_url, params=value_check_params)
    value_check_response.raise_for_status()

    api_temperature = value_check_response.json()["daily"]["temperature_2m_max"][0]
    our_temperature = weather[0]["high_f"]

    print(f"Temperature from API: {api_temperature}")
    print(f"Temperature in our table: {our_temperature}")
    print(f"Do they match? {api_temperature == our_temperature}")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I compared the first day's temperature in our table with the value from the API. Both values match, confirming that the temperature was recorded correctly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #7. 🤖 WORKING WITH THE AGENT
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I used Marimo Agent to help me write and understand the code throughout the project.

    One thing I improved was how the program handles days that do not meet the weather conditions.
    At first, the code only said that no day met the requirements. I changed it so that the program also recommends the day that breaks the fewest rules.

    I made this change because the assignment requires the tool to recommend an alternative day.

    This improvement can be seen in Section 4.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #8. ⏪ READING IT BACK
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Function 1: get_coordinates()**

    This function takes the town and state as inputs and uses the Geocoding API to find its location. It returns the latitude and longitude.

    One line I needed to understand was data.get("results", []). I learned that it gets the list of locations from the API and returns an empty list if no results are found.

    **Function 2: get_weather()**

    This function takes the latitude and longitude and uses the Forecast API to get the weather for the next seven days. It returns a list of dictionaries with the date, temperatures, chance of rain, and wind speed.

    One line I needed to understand was for _i in range(len(daily["time"])). I learned that it loops through the days so we can organize the weather information for each day into one dictionary.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##**🧠 MY PREDICTION**

    I will change the maximum rain chance from 30% to 5%. I expect fewer days to meet the conditions because the rain limit will be stricter. I also expect October 19 to remain the best day if the forecast stays the same, since it has only a 1% chance of rain.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ###**What happened**

    After changing the maximum rain chance from 30% to 5%, the number of suitable days decreased from 5 to 2.

    October 19 remained the best day because it had the lowest chance of rain.

    This matched my prediction and showed that the tool responds correctly when the inputs change.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #9. 🏅 GOING FURTHER
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I wanted to add a weather score from 0 to 10 for each day. The score will be based on temperature, rain probability, and wind speed. This will make it easier to compare the weather conditions, even when some days do not meet all the requirements.
    """)
    return


@app.cell
def _(highest_high_f, lowest_high_f, max_rain_chance, max_wind_mph, weather):
    weather_scores = []

    for _day in weather:
        _score = 0

        if lowest_high_f <= _day["high_f"] <= highest_high_f:
            _score += 4

        if _day["rain_chance"] <= max_rain_chance:
            _score += 3

        if _day["wind_mph"] <= max_wind_mph:
            _score += 3

        weather_scores.append({
            "date": _day["date"],
            "score": _score
        })

    print(f"{'Date':<12} {'Score (/10)':>12}")
    print("-" * 25)

    for _day in weather_scores:
        print(f"{_day['date']:<12} {_day['score']:>12}")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I added a scoring system from 0 to 10 based on temperature, rain, and wind conditions. Then, it is easy to compare the weather across the seven 7, even when some days do not meet all the requirements.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ###**🔎 What I Found**

    October 19 and 20 received the highest score of 10/10 because they meet all the weather conditions. However, October 19 is still the best option because it has a lower chance of rain (1% compared to 2%).

    This scoring system makes it easier to compare all 7 days.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #10. ⏰ TIME SPENT
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    About 3 hours.
    """)
    return


if __name__ == "__main__":
    app.run()
