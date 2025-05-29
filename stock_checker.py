import yfinance as yf
from notifier import send_email
import time

def get_current_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    if data.empty:
        print(f"No data for {ticker}")
        return None
    return data['Close'].iloc[-1]

def check_and_notify(ticker, target_price, user_email):
    current_price = get_current_price(ticker)
    if current_price is None:
        return

    print(f"{ticker} current price: ${current_price:.2f}")
    if current_price <= target_price:
        subject = f"🔔 {ticker} dropped to ${current_price:.2f}!"
        body = f"Hey bhai,\n\n{ticker} ka price ab ${current_price:.2f} hai, jo target ${target_price} se kam ya barabar hai.\nAb dekh le market ka scene! 🚀📉"
        send_email(subject, body, user_email)
        print("🚨 Alert sent!")
    else:
        print("No alert sent. Price above target.")

if __name__ == "__main__":
    # Example values
    ticker = "TSLA"
    target_price = 700.00
    user_email = "ksdrohit28@gmail.com"

    # Optional: Check every 5 mins
    while True:
        check_and_notify(ticker, target_price, user_email)
        print("🔁 Waiting 5 mins for next check...\n")
        time.sleep(300)  # 5 minutes