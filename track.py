import streamlit as st
import pandas as pd

st.header('Single File Upload ')
uploaded_file = st.file_uploader("Choose a CSV file", type='csv')

def process():

        df = pd.DataFrame(new_input['CONSIGNMENT DESCRIPTION'].str.split(',').tolist(), index=new_input[['C.NOTE NUMBER','CUSTOMER REFERENCE NUMBER']]).stack()
        df=df.reset_index()
        df['C.NOTE NUMBER'], df['CUSTOMER REFERENCE NUMBER'] = zip(*df.level_0)
        final=df[['C.NOTE NUMBER','CUSTOMER REFERENCE NUMBER']]
        final['sku']=df[0]
        final = final.assign(tracking_provider='DTDC')
        final = final.assign(status_shipped=1)
        final = final.assign(qty=1)
        final['date']=pd.Timestamp("today").strftime("%d/%m/%Y")
        tracking=final[['CUSTOMER REFERENCE NUMBER','tracking_provider','C.NOTE NUMBER','date','status_shipped','sku','qty']]
        tracking.rename(columns = {'CUSTOMER REFERENCE NUMBER':'order_id', 'C.NOTE NUMBER':'tracking_number','date':'date_shipped'}, inplace = True)
        tracking =tracking.groupby(['order_id','tracking_number','date_shipped','sku','status_shipped','tracking_provider'])['qty'].sum()
        final_tracking=tracking.reset_index()
        #st.download_button('Download file', final_tracking)
        st.write(final_tracking)
        final_tracking= final_tracking.to_csv(index=False).encode("utf-8")
        st.download_button(

        label="Download data as CSV",

        data=final_tracking,

        file_name='Tracking.csv',

        mime='text/csv',)




if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.write("File has uploaded successfully")
    #st.write(dataframe)
    new_input =dataframe[['C.NOTE NUMBER','CUSTOMER REFERENCE NUMBER','CONSIGNMENT DESCRIPTION']]
    if st.button('PROCESS'):
        process()
