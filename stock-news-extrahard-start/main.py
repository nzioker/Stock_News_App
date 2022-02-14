import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
INTERVAL = "60min"
API_KEY = "ZSF00190CAT37ZZX"
NEWS_API_KEY = "1a88a94681d84eea89f0b3fbfdbd7e6e"
COMPANY = "tesla"
twilio_number = "+18593747438"
my_number = "+254707378757"
account_sid = "AC410ca3e03cd4dfa047ae1782fc5d1562"
auth_token = "5fc0834c136c8dcca5794567b6bf034a"

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={STOCK}&interval={INTERVAL}&apikey={API_KEY}"
data_request = requests.get(url)
data_request.raise_for_status()
data = data_request.json()
stock_symbol = data["Meta Data"]["2. Symbol"]

closing_price = data["Time Series (60min)"]["2022-02-03 20:00:00"]["4. close"]
opening_price = data["Time Series (60min)"]["2022-02-04 05:00:00"]["1. open"]
change = (float(opening_price) - float(closing_price))/float(opening_price) * 100


# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
if change >= 5:
    news_url = f"https://newsapi.org/v2/everything?q={COMPANY}&apiKey={NEWS_API_KEY}"
    news_data = requests.get(news_url)
    news_data.raise_for_status()
    cleaned_news_data = news_data.json()
    print(cleaned_news_data)
    for i in range(3):
        article_title = cleaned_news_data["articles"][i]["title"]
        article_description = cleaned_news_data["articles"][i]["description"]

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
        client = Client(account_sid, auth_token)
        message_info = f"{stock_symbol}\nHeadline: {article_title}\nBrief: {article_description}"
        print(message_info)
        message = client.messages.create(body=message_info, from_=twilio_number, to=my_number)

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

