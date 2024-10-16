import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

STOCK_API_KEY = "INR272ORTAAXCHLD"
NEWS_API_KEY = "98a35a9cc2334565811bef0605e6dbe4"

account_sid = 'AC445920c1f46d9ea11bfde27ae263a670'
auth_token = '0b6ccc76d3d7cfc43515ec9587fb705d'


def get_stock_data():
    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": STOCK_API_KEY
    }
    response = requests.get(url="https://www.alphavantage.co/query?", params=parameters)
    response.raise_for_status()
    data = response.json()
    first_date = list(data["Time Series (Daily)"].keys())[0]
    first_close_value = data["Time Series (Daily)"][first_date]["4. close"]
    print(first_date)
    print(first_close_value)
    second_date = list(data["Time Series (Daily)"].keys())[1]
    second_close_value = data["Time Series (Daily)"][second_date]["4. close"]
    print(second_date)
    print(second_close_value)
    close_data = [
        {"date": first_date, "close": float(first_close_value)},
        {"date": second_date, "close": float(second_close_value)}
    ]
    return close_data


def compare_close(data):
    delta = (abs(data[0]['close'] - data[1]['close']) / data[1]['close']) * 100
    return delta


def get_news_data():
    parameters = {
        "q": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url="https://newsapi.org/v2/top-headlines?", params=parameters)
    response.raise_for_status()
    data = response.json()
    print(data)
    print(data['articles'][0])
    news_data = [
        {"Headline": data['articles'][0]['title'], "Brief": data['articles'][0]['description']},
        {"Headline": data['articles'][1]['title'], "Brief": data['articles'][1]['description']},
        {"Headline": data['articles'][2]['title'], "Brief": data['articles'][2]['description']}
    ]
    print(news_data)
    return news_data


def send_message(data, delta):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        to='whatsapp:+4915901637965',
        body=f"{STOCK}: {delta}%\n"
             f"Headline: {data[0]['Headline']}\n"
             f"Brief:  {data[0]['Brief']}"
    )
    print(message.status)


price_close_data = get_stock_data()
delta = compare_close(price_close_data)
if compare_close(price_close_data) > 0.05:
    print("Get News")
    news = get_news_data()
    send_message(news, delta)
news = get_news_data()
send_message(news, delta)
