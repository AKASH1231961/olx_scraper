import requests

url = "https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=20)
    print("Status Code:", response.status_code)
    print(response.text[:500])  # Print the first 500 characters of the response HTML
except Exception as e:
    print("Error:", e)




