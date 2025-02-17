import streamlit as st

st.title("Hello Streamlit!")
st.write("This is a basic test of our setup.")

# Optional: confirm yfinance is installed
import yfinance as yf
st.write("yfinance is installed! Current version:")
import pkg_resources
st.write(pkg_resources.get_distribution("yfinance").version)
import streamlit as st
import math

st.title("Options Swing Risk/Reward Calculator")

st.write(" ")

profit_goal = st.number_input("Profit Goal Per Trade ($)", value=400, step=50)
st.write(" ")

# 1. Underlying Stock Inputs
ticker_symbol = st.text_input("**STOCK SELECTION**", value="AAPL")


# Try to fetch the current price from yfinance
if ticker_symbol:
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="1d")
        if not hist.empty:
            fetched_price = hist['Close'].iloc[-1]
            st.write(f"**<span style='color:blue'>${fetched_price:.2f}**</span>", unsafe_allow_html=True)
        else:
            fetched_price = None
            st.warning("No price data available from yfinance.")
    except Exception as e:
        st.error(f"Error fetching price: {e}")
        fetched_price = None
else:
    fetched_price = None

# Allow the user to manually enter/override the current price
if fetched_price:
    current_price = st.number_input("Current Stock Price (override if needed)", value=fetched_price, step=0.01)
else:
    current_price = st.number_input("Enter Current Stock Price", value=0.0, step=0.01)

st.write(" ")
st.write("**PROFIT / RISK TARGETS**")
target_move = st.number_input("Expected Upward Move in Underlying ($)", value=3.0, step=0.5)
stop_move = st.number_input("Downward Move to Stop ($)", value=0.43, step=0.1)
st.write(" ")
# 2. Option Trade Inputs
st.write("**OPTIONS DETAILS**")
option_premium = st.number_input("Option Premium ($)", value=2.75, step=0.25)
delta = st.number_input("Delta", value=0.46, step=0.01)
gamma = st.number_input("Gamma", value=0.0465, step=0.001)


# 3. Calculations (using a simple delta+gamma approximation)
d_option_up = delta * target_move + 0.5 * gamma * (target_move ** 2)
new_option_price_up = option_premium + d_option_up
profit_per_contract = d_option_up * 100  # one contract represents 100 shares

if profit_per_contract > 0:
    contracts_needed = math.ceil(profit_goal / profit_per_contract)
else:
    contracts_needed = 0

d_option_down = delta * (-stop_move) + 0.5 * gamma * (stop_move ** 2)
new_option_price_down = option_premium + d_option_down
loss_per_contract = abs(d_option_down * 100)

total_profit = profit_per_contract * contracts_needed
total_loss = loss_per_contract * contracts_needed

# 4. Display the Results
st.subheader("Calculation Results")
st.write(f"Current underlying price: ${current_price:.2f}")
st.markdown(f"<p style='font-size:16px;'>Profit per contract (if underlying moves up by <b>${target_move:.2f}</b>): <span style='color:green'>${profit_per_contract:,.2f}</span></p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:16px;'>Loss per contract (if underlying stops by $<b>{stop_move:.2f}</b>): <span style='color:red'>-${loss_per_contract:,.2f}</span></p>", unsafe_allow_html=True)
st.write("")
st.write("<b>SUMMARY</b>", unsafe_allow_html=True)
st.write(f"Contracts needed to reach a ${profit_goal} profit goal: <b>{contracts_needed}</b>", unsafe_allow_html=True)
st.write(f"Total potential profit: <span style='color:green'>${total_profit:,.2f}</span>", unsafe_allow_html=True)
st.write(f"Total potential loss: <span style='color:red'>-${total_loss:,.2f}</span>", unsafe_allow_html=True)
if total_loss > 0:
    rr_ratio = round(total_profit / total_loss, 2)
    st.write(f"Risk:Reward Ratio = 1 : {rr_ratio}")
else:
    st.write("Risk:Reward Ratio cannot be computed (loss = 0).")

st.caption("This is a simplified calculation using a delta+gamma approximation and does not factor in time decay or IV changes.")
