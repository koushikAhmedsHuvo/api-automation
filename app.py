import requests
import csv
import time

# Step 1: Fetch data from the GraphQL API
def fetch_countries():
    url = "https://countries.trevorblades.com/"
    query = """
    query {
      countries {
        name
        capital
        currency
      }
    }
    """
    try:
        response = requests.post(url, json={'query': query})
        response.raise_for_status()
        data = response.json()
        countries = data.get("data", {}).get("countries", [])
        return countries
    except requests.exceptions.RequestException as e:
        print(f"Error fetching countries: {e}")
        return []

# Step 2: Post details of one country to the REST API
def post_country_details(country):
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "title": f"Country: {country['name']}",
        "body": f"Capital: {country['capital']}, Currency: {country['currency']}",
        "userId": 1
    }
    
    retries = 3
    backoff = 1  # Initial backoff in seconds

    for attempt in range(retries):
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 403:
                print("403 Forbidden: Skipping the request.")
                return None
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 500:
                print("500 Internal Server Error: Retrying...")
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff
            else:
                print(f"HTTP Error: {e}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            break
    return None

# Step 5: Save all fetched countries to a CSV file
def save_countries_to_csv(countries):
    file_name = "countries.csv"
    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Country Name", "Capital", "Currency"])
            for country in countries:
                writer.writerow([country.get("name", "N/A"), country.get("capital", "N/A"), country.get("currency", "N/A")])
        print(f"Countries saved to {file_name}.")
    except Exception as e:
        print(f"Error saving countries to CSV: {e}")

# Step 4: Automate the workflow
def main():
    print("Fetching countries from GraphQL API...")
    countries = fetch_countries()

    if not countries:
        print("No countries data fetched. Exiting.")
        return

    print("Fetched countries successfully.")

    # Select one country (e.g., the first one)
    country = countries[0]
    print(f"Posting details for country: {country['name']}...")
    response = post_country_details(country)

    if response:
        print(f"Country details posted successfully. Response: {response}")
    else:
        print("Failed to post country details.")

    # Save all countries to CSV
    print("Saving all countries to CSV...")
    save_countries_to_csv(countries)

if __name__ == "__main__":
    main()
