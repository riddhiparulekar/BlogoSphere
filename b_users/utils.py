import requests

def fetch_all_countries():
    api_url = "http://scalable-env.eba-qim7vucr.us-east-1.elasticbeanstalk.com/api/v1/countries"
    all_countries = []
    next_url = api_url  # Start with the initial URL

    try:
        while next_url:
            response = requests.get(next_url)
            if response.status_code != 200:
                print("Failed to fetch data:", response.status_code)
                break

            data = response.json()
            print(next_url)
            all_countries.extend(data['data'])  # Add the countries from the current page

            # Update the next_url with the URL of the next page, or None if there is no next page
            next_url = data['links']['next']
    except Exception as e:
        print(e)
    return [(country['iso2'], country['name']) for country in all_countries]