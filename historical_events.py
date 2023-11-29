import requests
import json
import random
from datetime import date
from config import YOUR_API_KEY


def get_facts_data():
    """
    Returns list of historical events that happened today.
    Returns error message if request did not work.
    """
    # Get today's month and day
    today = str(date.today())
    year, month, day = today.split("-")

    # Obtain list of facts
    api_url = f"https://api.api-ninjas.com/v1/historicalevents?month={month}&day={day}"
    response = requests.get(api_url, headers={"X-Api-Key": f"{YOUR_API_KEY}"})
    if response.status_code == requests.codes.ok:
        fact_data = json.loads(response.text)  # convert from str to list
        return fact_data
    else:
        return "Error:", response.status_code, response.text

    # references:
    # https://www.geeksforgeeks.org/get-current-date-using-python/
    # https://api-ninjas.com/api/historicalevents


def get_fact():
    """
    Returns random event from list of historical events and the year it happened.
    """
    fact_list = get_facts_data()

    random_index = random.randint(0, len(fact_list) - 1)
    return fact_list[random_index]["year"], fact_list[random_index]["event"]

    # references:
    # https://www.geeksforgeeks.org/random-numbers-in-python/


def main():
    year, fact = get_fact()
    print(year)
    print(fact)


if __name__ == "__main__":
    main()
