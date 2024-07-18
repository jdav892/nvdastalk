import requests
from twilio.rest import Client


STOCK_NAME = "NVDA"
COMPANY_NAME = "NVIDIA Corp"


STOCK_API_KEY = "get your own "
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "get your own"
TWILIO_SID = "make your own "
TWILIO_AUTH_TOKEN = "make your own "

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "outputsize": "compact",
    "datatype": "json",
    "apikey": STOCK_API_KEY
    
}


response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]
prior_day_data = stock_data_list[0]
prior_day_close = prior_day_data["4. close"]
print(prior_day_close)


day_before_prior_data = stock_data_list[1]
day_before_prior_close = day_before_prior_data["4. close"]
print(day_before_prior_close)

difference_of_days = (abs(float(prior_day_close) - float(day_before_prior_close)))

pos_neg = None
if difference_of_days > 0:
    pos_neg = "📈"
else:
    pos_neg = "📉"

percent_change = round((difference_of_days / float(day_before_prior_close)) * 100)

if abs(percent_change) > 1:
    news_params = {
        "apiKey" : NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }

    news = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)
    headline_list = [f"{STOCK_NAME}: {pos_neg}{percent_change}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in headline_list:
        message = client.messages.create(
            body=article,
            from_="make your own",
            to="use yours"
        )
