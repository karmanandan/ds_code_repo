import os
import streamlit as st
import snowflake.connector
import numpy as np
import pandas as pd
from utils import (calculate_numeric_column_attributes,
                   calculate_categorical_column_attributes,
                   calculate_date_description_statistics,
                   dup_data_description)
from gen_visulizations import create_visualizations_and_report,generate_vislizations
from recommendations import data_quality_recommendations

def snowflake_ui_connection():
    st.title("Snowflake Database Connector")
    st.write("Enter your Snowflake database credentials to connect.")

    with st.container():
        # User Input Form
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        account = st.text_input("Account")
        warehouse = st.text_input("Warehouse")
        database = st.text_input("Database")
        schema = st.text_input("Schema")
        role = st.text_input("Role")
        filename = st.text_input("File Name")

    def connect_to_snowflake(username, password, account, warehouse, database, schema,role):
        conn = snowflake.connector.connect(
            user=username,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema,
            role=role
        )
        return conn

    if st.button("Download Statistical Report"):
        path_ = os.getcwd()
        try:
            conn = connect_to_snowflake(username, password, account, warehouse, database, schema, role)
            st.success("Connected to Snowflake Database!")
            # Create a cursor object
            cur = conn.cursor()
            # Execute a SQL query to retrieve table names
            query = "SHOW TABLES"
            cur.execute(query)
            # Fetch all the table names
            table_names = [row[1] for row in cur.fetchall()]
            st.write(table_names)
            excel_file_path = f"{filename}.xlsx"
            with pd.ExcelWriter(excel_file_path) as writer:
                tab_names = []
                tab_obs = []
                for table_name in table_names:
                    try:
                        st.write(table_name)
                        query = f"SELECT TOP 100 * FROM {table_name}"
                        conn = connect_to_snowflake(username, password, account, warehouse, database, schema,role)
                        # df = pd.read_sql(query, conn)
                        cur = conn.cursor()
                        cur.execute(query)
                        df = pd.read_sql(query, conn)
                        st.write(df.head())
                        # generate_vislizations(df)
                        data_quality_recommendations(df)
                        tab_names.append(table_name)
                        tab_obs.append(dup_data_description(df, table_name)[0])
                        for k,_ in dup_data_description(df, table_name)[1].items():
                            res_df = pd.DataFrame(dup_data_description(df, table_name)[1][k])
                            if not (res_df.empty):
                                res_df.to_excel(writer, sheet_name=(os.path.splitext(table_name)[0]+'_'+k)[:30], index=False)
                    except Exception as e:
                        st.error(f"Connection failed: {str(e)}")   
                desc_df = pd.DataFrame(dict(zip(tab_names,tab_obs))).T
                desc_df.to_excel(writer, sheet_name='Table desc')
                conn.close()
            if excel_file_path:
                st.success(f"Data downloaded as -> {excel_file_path}")
                # ppath = f"{path_}\{excel_file_path}"
                # st.write(ppath)
                # st.download_button(label='📥 Download Current Result',
                #                     data=desc_df ,
                #                     file_name= excel_file_path)
                st.markdown(f"Download [here]({path_}\{excel_file_path})")
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")

    if st.button("Download Visual Report"):
        st.success("Coming soon!!")