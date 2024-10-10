StockPulse: AI-Driven Sentiment Analyzer
Overview
StockPulse is an AI-driven sentiment analysis application that helps users analyze stock market trends by combining historical stock data and sentiment analysis of relevant news articles. By using advanced techniques to analyze the latest news related to any stock ticker, this tool offers an insightful look into how current events might affect stock prices. The application is hosted on Streamlit for easy access.

Hosted Application
Access the live application here: StockPulse on Streamlit

Features
Real-Time Stock Data: Fetches real-time stock price, including open, high, low, and volume information for any given stock ticker.
Historical Data: Visualizes historical stock price data for up to 30 days, including moving average calculations.
Sentiment Analysis: Analyzes sentiment of the latest news articles related to the stock using TextBlob and displays the sentiment score.
Price Change Prediction: Provides potential stock price movements based on both sentiment analysis and recent price changes.
Visualization: Offers a clean, interactive chart of stock prices, moving averages, and sentiment scores of news headlines.
How It Works
Enter Stock Ticker: Input a valid stock ticker symbol (e.g., TSLA, AAPL).
Historical Data: The app fetches the last 10 days of historical data by default (modifiable).
News Analysis: It retrieves the latest news articles about the stock and performs sentiment analysis to determine the overall market sentiment.
Display Results: The app displays stock price details, historical data plots, and sentiment analysis of the news articles along with visual sentiment score representation.
Prediction: Based on the overall sentiment and price change percentage, the app suggests a potential stock price trend.
API Integration
The app integrates with the following APIs:

Alpha Vantage API: Fetches real-time and historical stock market data.
NewsAPI: Provides the latest news articles related to the stock for sentiment analysis.
Setup & Installation
To run this application locally, follow these steps:

Clone the repository:
bash
Copy code
git clone https://github.com/your-username/StockPulse-AI-Driven-Sentiment-Analyzer.git
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Create a .env file and add your API keys:
arduino
Copy code
ALPHA_VANTAGE_API_KEY='your_alpha_vantage_key'
NEWS_API_KEY='your_news_api_key'
Run the Streamlit app:
bash
Copy code
streamlit run streamlit_app.py
Requirements
Python 3.8+
Streamlit
Requests
Pandas
Matplotlib
NumPy
TextBlob
License
This project is licensed under the MIT License - see the LICENSE file for details.

Credits
Created by Jalaj.
