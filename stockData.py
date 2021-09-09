# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date
import yfinance as yf
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.set_page_config(
        page_title="Stock Prection", 
        page_icon="•",
        layout="centered", 
        initial_sidebar_state="auto",
        )

st.title('Stock Price Prediction WebApp')

# stocks = ('GOOG', 'AAPL', 'MSFT', 'GME')
# selected_stock = st.selectbox('Select dataset for prediction', stocks)
st.text_input("Type in a ticker symbol (For eg. 'AAPL' for Apple Inc.)", key="selected_stock", value='AAPL')
st.write('*Forgotten the ticker symbol?* Find it [here](https://finance.yahoo.com/lookup)')
comp = yf.Ticker(st.session_state.selected_stock)
comp_info = comp.info
if(comp_info.get('shortName')!=None):
    st.write('> Showing results for**', comp_info.get('shortName'),'**')
else:
    st.write('> No value passed!\nShowing results for **Apple Inc.**')

# n_years = st.slider('Years of prediction:', 1, 4)

interval_aliases = ('5 mins', '15 mins', '30 mins', '1 hour', '1 day', '1 week', '1 month')
interval_choices = ('5m', '15m', '30m', '60m', '1d', '1wk', '1mo')
interval_alias = st.radio('Select interval:', interval_aliases) 
interval = interval_choices[interval_aliases.index(interval_alias)]

if(interval=='5m'):
    period = '60d'
    date_index = 'Datetime'
    # p = 10
    # f = '5min'
elif(interval=='15m'):
    period = '60d'
    date_index = 'Datetime'
    # p = 10
    # f = '15min'
elif(interval=='30m'):
    period = '60d'
    date_index = 'Datetime'
    # p = 10
    # f = '30min'
elif(interval=='60m'):
    period = '146d'
    date_index = 'Datetime'
    p = 168
    f = 'h'
elif(interval=='1d'):
    period = '10y'
    date_index = 'Date'
    p = 60
    f = 'd'
elif(interval=='1wk'):
    period = '10y'
    date_index = 'Date'
    p = 10
    f = 'W'
elif(interval=='1mo'):
    period = '10y'
    date_index = 'Date'
    p = 2
    f = 'm'

@st.cache
def load_data(ticker):
    if not ticker:
        ticker='AAPL'
    comp = yf.Ticker(ticker)
    # data = comp.history(start=START, end=TODAY, interval=interval)
    data = comp.history(period=period, interval=interval)
    data.reset_index(inplace=True)
    data[date_index] = data[date_index].astype(str)
    if(date_index == 'Datetime'):
        data[date_index] = data[date_index].str[:-6]
    return data

	
# data_load_state = st.text('Fetching data...')
data = load_data(st.session_state.selected_stock)
# data_load_state.text('Fetching data... done!')

percentage = round(len(data)/100*90)
data_split = data.iloc[percentage:len(data),:]
st.subheader('Raw data')
st.dataframe(data)

# Plot raw data
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_split[date_index], y=data_split['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data_split[date_index], y=data_split['Close'], name="stock_close"))
    fig.layout.update(title_text='Time Series data in Line-chart', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)

    csfig = go.Figure(data=[go.Candlestick(x=data_split[date_index],
        open=data_split['Open'],
        high=data_split['High'],
        low=data_split['Low'],
        close=data_split['Close'])])
    csfig.layout.update(title_text='Time Series data in Candle-chart', xaxis_rangeslider_visible=True)
    st.plotly_chart(csfig, use_container_width=True)

plot_raw_data()

if not (interval in interval_choices[:3]):
    data_load_state = st.text('Predicting stocks\' value...')
    # Predict forecast with Prophet.
    df_train = data[[date_index,'Close']]
    df_train = df_train.rename(columns={date_index: "ds", "Close": "y"})
    
    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=p, freq=f)
    forecast = m.predict(future)
    
    # Show and plot forecast
    st.subheader('Forecast data')
    st.write(forecast[len(data)-1:len(forecast)])
    st.write('No of values: ',len(forecast[len(data):len(forecast)]))
    
    st.write(f'Forecast plot ')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1, use_container_width=True)
    
    st.write("Forecast components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)
    data_load_state.text('Prediction done.')

