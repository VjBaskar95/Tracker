import streamlit as st
import requests
import pandas as pd
import schedule
import time


st.write("Get")

def get():
    headers = {
    'X-ApiKey': '7J3M742r9A8f5v6s69k8H6i4d5k6j3E7',
}
    response = requests.get('https://dev.mwomen.srv1.mtlstaging.com/api/product/product/', headers=headers)
    data=response.json()
    results=data['results']
    df=pd.DataFrame(results)
    df.to_csv('C:\\API\\api_out.csv')
    st.write('thank')

schedule.every(1).minutes.do(get)
