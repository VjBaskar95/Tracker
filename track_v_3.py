import streamlit as st
import pandas as pd

#button reuse
def stateful_button(*args, key=None, **kwargs):
    if key is None:
        raise ValueError("Must pass key")

    if key not in st.session_state:
        st.session_state[key] = False

    if st.button(*args, **kwargs):
        st.session_state[key] = not st.session_state[key]


    return st.session_state[key]
#single file upload
def file_upload():
    st.header('Single File Upload ')
    global uploaded_file
    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
    file_check()
#checking the file

def file_check():
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        st.write("File has uploaded successfully")
        #st.write(dataframe)
        global new_input
        new_input =dataframe[['C.NOTE NUMBER','CUSTOMER REFERENCE NUMBER','CONSIGNMENT DESCRIPTION']]

        if stateful_button('Process', key="Process"):
            process()


#convert input into tracking
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
    global final_tracking_csv
    global final_tracking
    final_tracking=tracking.reset_index()
    final_tracking=final_tracking[['order_id','tracking_provider','tracking_number','date_shipped','status_shipped','sku','qty']]
    final_tracking_csv= final_tracking.to_csv(index=False).encode("utf-8")
    st.write("Process Completed")

    button()

#button for Process
def button():
    #col1,col2= st.columns([1,1])
    #with col2:

    #with col1:
    st.download_button(
    label="Download data as CSV",
    data=final_tracking_csv,
    file_name='Tracking_{}.csv'.format(pd.Timestamp("today").strftime("%d/%m/%Y")),
    mime='text/csv',
    key='process_download',)

    if stateful_button('Merge', key="Merge"):
        join_process()


#importing multifile and joining
def join():
    st.header('Multi File Upload ')
    data = st.file_uploader("Upload Tracking CSV:",type = 'csv',
    accept_multiple_files=True)
    table=pd.DataFrame(columns=['order_id','tracking_provider','tracking_number','date_shipped','status_shipped','sku','qty'])
    for file in data:
        df=pd.read_csv(file)
        #table=table.append(df,ignore_index=True)
        table=pd.concat([table,df])
    #st.write(table)
    table_csv= table.to_csv(index=False).encode("utf-8")
    if stateful_button('Combine', key="Merge_1"):
        st.write("Merged all imported file")
        st.download_button(
    label="Download data as CSV",
    data=table_csv,
    file_name='Merge_Tracking_{}.csv'.format(pd.Timestamp("today").strftime("%d/%m/%Y")),
    mime='text/csv',
    )

def join_process():
    st.header('Multi File Upload ')
    data = st.file_uploader("Upload Tracking CSV:",type = 'csv',
    accept_multiple_files=True)
    table=final_tracking
    for file in data:
        df=pd.read_csv(file)
        #table=table.append(df,ignore_index=True)
        table=pd.concat(table,df)
    st.write(table)
    table_csv= table.to_csv(index=False).encode("utf-8")
    if stateful_button('Combine', key="Merge_2"):
        st.write("Merged all imported file")
        st.download_button(
    label="Download data as CSV",
    data=table_csv,
    file_name='Merge_Tracking_{}.csv'.format(pd.Timestamp("today").strftime("%d/%m/%Y")),
    mime='text/csv',
    )

add_selectbox = st.sidebar.selectbox(
    "What you like do ",
    ("Convert", "Combine", "next option")
)

if add_selectbox == "Convert":
    file_upload()

if add_selectbox == "Combine":
    join()

#if st.sidebar.button('New_Process',key="new_process"):
#    file_upload()
