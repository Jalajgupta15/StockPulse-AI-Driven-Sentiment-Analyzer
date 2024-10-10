import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from textblob import TextBlob

# API keys
ALPHA_VANTAGE_API_KEY = '82HV0ISU97VKZEX5'
NEWS_API_KEY = '3340e225471146a4b9c374624bff329c'

# Function to fetch historical stock data
def fetch_historical_stock_data(ticker, days=10):
    stock_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(stock_url)
    data = response.json()

    if "Error Message" in data or "Time Series (Daily)" not in data:
        st.error("Invalid stock ticker or API limit reached.")
        return None

    time_series = data['Time Series (Daily)']
    dates, prices = [], []
    for date in sorted(time_series.keys())[-days:]:
        dates.append(date)
        prices.append(float(time_series[date]['4. close']))

    if not dates or not prices:
        st.error("No historical data found.")
        return None

    # Create DataFrame with 'Date' as a column
    historical_df = pd.DataFrame({'Date': pd.to_datetime(dates), 'Price': prices})

    return historical_df

# Function to fetch stock data
def fetch_stock_data(ticker):
    stock_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(stock_url)
    data = response.json()

    if "Error Message" in data:
        st.error("Invalid stock ticker or API limit reached.")
        return None

    time_series = data.get('Time Series (Daily)', {})
    if not time_series:
        st.error("No data found for this stock.")
        return None

    latest_date = next(iter(time_series))
    latest_data = time_series[latest_date]
    return {
        'date': latest_date,
        'price': float(latest_data['4. close']),
        'open': float(latest_data['1. open']),
        'high': float(latest_data['2. high']),
        'low': float(latest_data['3. low']),
        'volume': int(latest_data['5. volume'])
    }

# Function to fetch news data
def fetch_news_data(ticker):
    news_url = f'https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_API_KEY}'
    response = requests.get(news_url)
    data = response.json()

    if not data.get("articles"):
        st.error("No news found for this stock.")
        return []

    return data['articles'][:5]  # Return top 5 articles

# Function for advanced sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Returns a score between -1 (negative) and 1 (positive)

# Function to calculate percentage change
def calculate_percentage_change(latest_price, previous_price):
    return ((latest_price - previous_price) / previous_price) * 100 if previous_price else 0

# Streamlit app UI
st.title("StockPulse: AI-Driven Market Sentiment")

ticker = st.text_input("Enter Stock Ticker (e.g., TSLA, AAPL)")

# Set default number of historical days to fetch
days = st.number_input("Enter number of historical days to fetch:", min_value=1, max_value=30, value=10)

if ticker:
    # Fetch stock data
    stock_data = fetch_stock_data(ticker)
    if stock_data:
        st.write(f"### Stock Price for {ticker}")
        st.write(f"Date: {stock_data['date']}")
        st.write(f"Current Price: ${stock_data['price']}")
        st.write(f"Open: ${stock_data['open']}, High: ${stock_data['high']}, Low: ${stock_data['low']}, Volume: {stock_data['volume']}")

        # Fetch historical stock data for the specified number of days
        historical_data = fetch_historical_stock_data(ticker, days)
        if historical_data is not None:
            st.write(f"### Stock Data for {ticker} (Last {days} Days)")

            # Set 'Date' as index for plotting
            historical_data.set_index('Date', inplace=True)

            # Plot the historical price data
            st.line_chart(historical_data[['Price']])

            # Calculate moving average and plot it
            historical_data['MA'] = historical_data['Price'].rolling(window=5).mean()
            st.line_chart(historical_data[['Price', 'MA']])

        # Fetch news data
        st.write(f"### Latest News for {ticker}")
        news_articles = fetch_news_data(ticker)

        if news_articles:
            sentiment_scores = []
            headlines = []

            # Display each article with sentiment
            for article in news_articles:
                sentiment_score = analyze_sentiment(article['title'])
                sentiment_scores.append(sentiment_score)
                headlines.append(article['title'])

                st.write(f"**{article['title']}**")
                st.write(f"Published At: {article['publishedAt']}")
                st.write(f"Source: {article['source']['name']}")
                st.write(f"Description: {article.get('description', 'No description available')}")
                sentiment = "Positive" if sentiment_score > 0 else "Negative"
                st.write(f"Sentiment: {sentiment} (Score: {sentiment_score:.2f})")
                st.write(f"[Read More]({article['url']})")
                st.write("---")

            # Overall sentiment
            overall_sentiment = "Positive" if np.mean(sentiment_scores) > 0 else "Negative"
            st.write(f"### Overall Sentiment: {overall_sentiment}")

            # Display overall sentiment and price change percentage
            if len(historical_data) > 1:
                previous_price = historical_data['Price'].iloc[-2]
                price_change_percentage = calculate_percentage_change(stock_data['price'], previous_price)
                st.write(f"### Price Change Percentage: {price_change_percentage:.2f}%")

            # Show sentiment scores graph
            st.write("### Sentiment Scores for Recent News")
            fig, ax = plt.subplots()
            ax.barh(headlines, sentiment_scores, color=['green' if s > 0 else 'red' for s in sentiment_scores])
            ax.set_xlabel('Sentiment Score')
            ax.set_title('Sentiment Analysis of News Headlines')
            st.pyplot(fig)

            # Display overall sentiment analysis result
            if np.mean(sentiment_scores) > 0:
                st.success("The overall sentiment is positive. Possible stock price increase.")
            else:
                st.error("The overall sentiment is negative. Possible stock price decrease.")
                
