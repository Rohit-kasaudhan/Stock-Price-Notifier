import streamlit as st
from notifier import send_email
import yfinance as yf
import re

# Function to fetch current stock price
def get_current_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    if data.empty:
        return None
    return data['Close'].iloc[-1]

# Email validation
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# Predefined stock options
popular_tickers = {
    "Apple (AAPL)": "AAPL",
    "Tesla (TSLA)": "TSLA",
    "Amazon (AMZN)": "AMZN",
    "Microsoft (MSFT)": "MSFT",
    "Google (GOOGL)": "GOOGL",
    "NVIDIA (NVDA)": "NVDA",
    "Meta (META)": "META",
    "Netflix (NFLX)": "NFLX"
}

# Streamlit App UI
st.set_page_config(page_title="📈 Stock Price Notifier")
st.title("📈 Stock Price Notifier App\n- Prepared By: Rohit Kasaudhan")
st.write("Set alerts for your favorite stocks and get notified by email!")

# Dropdown for stock selection
selected_stock_name = st.selectbox("Select a Stock:", list(popular_tickers.keys()))
ticker = popular_tickers[selected_stock_name]

# Show last 5-day stock price trend
hist = yf.Ticker(ticker).history(period="5d")
st.subheader(f"📊 Last 5 Days Closing Prices for {ticker}")
st.line_chart(hist['Close'])

# User input
target_price = st.number_input("Target Price ($):", min_value=0.0)
alert_direction = st.radio("Alert me when the price is:", ["Falls below", "Rises above"])
user_email = st.text_input("Enter Your Email Where You Want To Get Notified:").strip()

# Alert button logic
if st.button("🔔 Set Alert"):
    if not ticker or not target_price or not user_email:
        st.error("Please fill all the fields.")
    elif not is_valid_email(user_email):
        st.error("❌ Invalid email address.")
    else:
        current_price = get_current_price(ticker)
        if current_price is None:
            st.error("❌ Could not fetch stock price. Try again later.")
        else:
            st.info(f"Current Price of {ticker}: ${current_price:.2f}")
            
            alert_triggered = (
                alert_direction == "Falls below" and current_price <= target_price
            ) or (
                alert_direction == "Rises above" and current_price >= target_price
            )

            if alert_triggered:
                condition_text = "dropped below" if alert_direction == "Falls below" else "risen above"
                subject = f"🔔 {ticker} has {condition_text} ${target_price}!"
                body = (
                    f"{ticker} is currently at ${current_price:.2f}, "
                    f"which has {condition_text} your alert price of ${target_price}.\n\n"
                    "Check the market now! 📈📉"
                )
                send_email(subject, body, user_email)
                st.success("🚀 Email alert sent!")
            else:
                st.warning("ℹ️ Alert condition not met. No email sent.")
