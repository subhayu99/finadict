# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date
import yfinance as yf
import numpy as np
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from fbprophet.diagnostics import cross_validation
from plotly import graph_objs as go
import pycountry
import re

@st.cache
def load_data(ticker, period, interval, date_index):
    comp = yf.Ticker(ticker)
    data = comp.history(period=period, interval=interval)
    data.reset_index(inplace=True)
    data[date_index] = data[date_index].astype(str)
    if(date_index == 'Datetime'):
        data[date_index] = data[date_index].str[:-6]
    if(len(data)>10):
        return data.bfill().ffill()

def download_csv(df, selected_stock, filename):
    today = date.today().strftime("%b-%d-%Y")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Press to Download",
        data=csv,
        file_name=f'{selected_stock} {filename} {today}.csv',
        mime='text/csv',
    )

# Plot raw data
def plot_raw_data(data, date_index):
    st.subheader('Raw data plots')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data[date_index], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data[date_index], y=data['Close'], name="stock_close"))
    fig.layout.update(title_text='Time Series data in Line chart', xaxis_rangeslider_visible=True)

    csfig = go.Figure(data=[go.Candlestick(
        x=data[date_index],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'])]
    )
    csfig.layout.update(title_text='Time Series data in Candle-sticks chart', xaxis_rangeslider_visible=True)

    with st.expander("Tap to expand/collapse", expanded=False):
        st.plotly_chart(fig, use_container_width=True)
        st.plotly_chart(csfig, use_container_width=True)

def build_model(comp_country_code):
    # Define forecasting model.
    m = Prophet(
            interval_width=0.95, 
            daily_seasonality=True,
            # weekly_seasonality=True, 
            changepoint_prior_scale=1 
            )
    if(comp_country_code):
        m.add_country_holidays(country_name=comp_country_code)
    return m

def show_forecast(m, forecast, data, p, df_train, currency, c2):
    # Show and plot forecast
    st.subheader('Forecast data')

    original = df_train['y']
    prediction = forecast['yhat'][:-p]

    # st.write(original)
    # st.write(prediction)

    only_forecast = forecast # [len(data)-1:len(forecast)]
    only_forecast['Confidence (%)'] = (prediction / original) * 100
    only_forecast['Actual Price'] = df_train['y']
    only_forecast['Date'] = only_forecast['ds'].astype(str)
    only_forecast['Predicted Price'] = only_forecast['yhat']
    only_forecast['Predicted Price (Lower)'] = only_forecast['yhat_lower']
    only_forecast['Predicted Price (Upper)'] = only_forecast['yhat_upper']

    rmpse = (np.sqrt(np.nanmean(np.square(((original - prediction) / original))))*100)**2
    accuracy = round(only_forecast['Confidence (%)'].mean()-rmpse, 2)
   
    with st.expander("Tap to expand/collapse", expanded=False):
        st.write(only_forecast[["Date","Actual Price","Predicted Price","Confidence (%)","Predicted Price (Lower)","Predicted Price (Upper)"]].iloc[::-1])
        download_csv(only_forecast[["Date","Actual Price","Predicted Price","Confidence (%)","Predicted Price (Lower)","Predicted Price (Upper)"]], "prediction_data")
        st.write('Mean Confidence Percentage =', accuracy, '%')
        st.write('Root Mean Percentage Squared Error =', round(rmpse, 4), '%')

    # Tomorrow's Price metric
    label = "Tomorrow\'s Closing Price (confidence: " + str(accuracy) + '%)'
    prd_price = round(only_forecast['Predicted Price'].iloc[-1], 4)
    if(prd_price > 99):
        prd_price = round(prd_price, 2)
    act_price = only_forecast['Actual Price'].iloc[-2]
    value=str(prd_price) + ' ' + currency
    delta = str(round(((prd_price - act_price) / act_price) * 100, 2))+'% since today'
    with st.spinner('Predicting price...'):
        c2.metric(label=label, value=value, delta=delta)

    st.subheader('Forecast plot')
    fig1 = plot_plotly(m, forecast)
    with st.expander("Tap to expand/collapse", expanded=False):
        st.plotly_chart(fig1, use_container_width=True)
    
    st.subheader("Forecast components")
    fig2 = m.plot_components(forecast)
    with st.expander("Tap to expand/collapse", expanded=False):
        st.write(fig2)


def main():
    st.set_page_config(
            page_title="FINAnce preDICT",
            page_icon="•",
            layout="centered",
            initial_sidebar_state="expanded",
            )

    # st.sidebar.image('FINADICT.png', width=2)

    menu = ['Stocks', 'Forex', 'Crypto']
    choice = st.sidebar.selectbox('Select your market choice', menu)

    if(choice==menu[0]):
        st.title('Stock Prediction')

        selected_stock = st.text_input("Type in a ticker symbol", value='TCS.NS', help="'[TICKER]' for Nasdaq and '[TICKER].NS' for NSE registered stocks")
        st.write("*<p style='text-decoration:none; font-size:13px'>Find the ticker symbol <strong>[here](https://finance.yahoo.com/lookup)</strong>.</p>*", unsafe_allow_html=True)
        st.write(' ')
        if not selected_stock:
            selected_stock = 'TCS.NS'
        comp = yf.Ticker(selected_stock)
        comp_info = comp.info
        comp_country_code = pycountry.countries.search_fuzzy(comp_info.get('country'))[0].alpha_2
        currency = comp_info.get('financialCurrency')

        # st.write('Showing results for **[', comp_info.get('longName'),'](',comp_info.get('website'),')**')
        st.write(f"<p style='text-decoration:none; font-size:20px'>Showing results for <strong><a style='text-decoration:none;'>{comp_info.get('longName')}</a></strong></p>", unsafe_allow_html=True)
        # comp_col1, comp_col2 = st.columns([1, 2])
        # with comp_col1.expander("Company logo", expanded=False):
            # if(len(comp_info.get('logo_url'))>1):
                # st.image(comp_info.get('logo_url'))
        # st.write('Financial Currency :**', comp_info.get('financialCurrency'),'**\n')
        # st.write('\nyFinance\'s Recommendation :**', comp_info.get('recommendationKey'),'**\n')
        # with comp_col2.expander("Company information in JSON format", expanded=False):
            # comp_info.pop("longBusinessSummary")
            # st.json(comp_info)
        
    elif(choice==menu[1]):
        st.title('Forex Prediction')

        col1, col2 = st.columns(2)
        x = col1.text_input("From", value='USD')
        y = col2.text_input("To", value='INR')
        st.write("*<p style='text-decoration:none; font-size:13px'>Find the currency symbol <strong>[here](https://finance.yahoo.com/currencies)</strong>.</p>*", unsafe_allow_html=True)
        if not x:
            x = 'USD'
        if not y:
            y = 'INR'
        
        selected_stock = x+y+'=X'
        comp = yf.Ticker(selected_stock)
        currency = y.upper()
        comp_country_code = False

        st.write(f"<p style='text-decoration:none; font-size:20px'>Showing results for <strong>{x.upper()}</strong> to <strong>{y.upper()}</strong> conversion rate.</p>", unsafe_allow_html=True)

    elif(choice==menu[2]):
        st.title('Crypto Prediction')

        selected_stock = st.text_input("Type in a conversion string", value='BTC-INR', help="'[CURRENCY 1]-[CURRENCY 2]' to get [CURRENCY 1] to [CURRENCY 2] conversion rate.")
        st.write("*<p style='text-decoration:none; font-size:13px'>Find the currency symbol <strong>[here](https://finance.yahoo.com/cryptocurrencies)</strong>.</p>*", unsafe_allow_html=True) 
        if not selected_stock:
            selected_stock = 'BTC-INR'
        comp = yf.Ticker(selected_stock)
        comp_country_code = False
        x = re.search("^[a-zA-Z]*", selected_stock)
        y = re.search("[a-zA-Z]*$", selected_stock)
        currency = y.group().upper()

        st.write(f"<p style='text-decoration:none; font-size:20px'>Showing results for <strong>{x.group().upper()}</strong> to <strong>{y.group().upper()}</strong> conversion rate.</p>", unsafe_allow_html=True)

    form = st.sidebar.form("take parameters")

    interval_aliases = ('5 mins', '15 mins', '30 mins', '1 hour', '1 day', '1 week', '1 month')
    interval_choices = ('5m', '15m', '30m', '60m', '1d', '1wk', '1mo')
    interval_alias = form.radio('Select interval', interval_aliases, index=4, help="Prediction only supported for '1 day' interval.") 
    interval = interval_choices[interval_aliases.index(interval_alias)]

    if(interval=='5m'):
        l = 60
        t = 'd'
        date_index = 'Datetime'
        # p = 10
        # f = '5min'
    elif(interval=='15m'):
        l = 60
        t = 'd'
        date_index = 'Datetime'
        # p = 10
        # f = 'h'
    elif(interval=='30m'):
        l = 60 
        t = 'd'
        date_index = 'Datetime'
        # p = 10
        # f = '30min'
    elif(interval=='60m'):
        l = 60 
        t = 'd'
        date_index = 'Datetime'
        # p = st.sidebar.slider('No. of hour\'s prediction:', 1, 60)
        # f = 'h'
    elif(interval=='1d'):
        y = form.slider('No. of months\' data to fetch:', 2, 12, value=4, help="Default value is '4' because it gives best results in most cases.")
        y *= 30
        t = 'd'
        period = str(y)+t
        date_index = 'Date'
        p = 1  # st.sidebar.slider('No. of day\'s prediction:', 1, 10)
        f = 'd'
    elif(interval=='1wk'):
        l = 20 
        t = 'y'
        date_index = 'Date'
        # f = 'W'
    elif(interval=='1mo'):
        l = 20
        t = 'y'
        date_index = 'Date'
        # f = 'm'

    if(interval in interval_choices[:4]):
        y = form.slider('No. of days\' data to fetch:', 2, l, value=15)
        period = str(y)+t
    elif(interval in interval_choices[5:]):
        y = form.slider('No. of years\' data to fetch:', 2, l, value=15)
        period = str(y)+t

    form.form_submit_button("Submit")

    data = load_data(selected_stock, period, interval, date_index)

    c1, c2 = st.columns(2)

    # Latest actual Price metric
    if(interval in interval_choices[4:5]):
        label = "Todays\'s Closing Price"
        today_price = round(data['Close'].iloc[-1], 4)
        if(today_price > 99):
            today_price = round(today_price, 2)
        yest_price = data['Close'].iloc[-2]
        value = str(today_price) + ' ' + currency
        delta = str(round(((today_price - yest_price) / yest_price) * 100, 2))+'% since yesterday'
    else:
        label = "Latest Closing Price"
        today_price = round(data['Close'].iloc[-1], 4)
        if(today_price > 99):
            today_price = round(today_price, 2)
        yest_price = data['Close'].iloc[-2]
        value = str(today_price) + ' ' + currency
        delta = str(round(((today_price - yest_price) / yest_price) * 100, 2))+'% since last time'

    c1.metric(label=label, value=value, delta=delta)

    st.subheader('Raw data')
    with st.expander("Tap to expand/collapse", expanded=False):
        st.dataframe(data.iloc[::-1])
        download_csv(data, selected_stock, "raw_data")
    plot_raw_data(data, date_index)

    df_train = data[[date_index,'Close']]
    df_train = df_train.rename(columns={date_index: "ds", "Close": "y"})
    # st.write(df_train)

    if (interval in interval_choices[4:5]):
        with st.spinner('Predicting prices...'):
            m = build_model(comp_country_code)
            m.fit(df_train)
            # Predict forecast.
            future = m.make_future_dataframe(periods=p)
            forecast = m.predict(future)

            show_forecast(m, forecast, data, p, df_train, currency, c2)


if __name__ == '__main__':
    try:
        main()
    except AttributeError:
        st.error("Found nothing with the inputs :'(")
    except KeyError:
        st.error("Input is not valid :-!")
    except ValueError and TypeError:
        st.error("Didn't get enough value :(")
    #except:
    #    st.error("Oops! Something went wrong :(")

