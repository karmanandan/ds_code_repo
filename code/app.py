import streamlit as st
import snowflake.connector
import numpy as np
import pandas as pd
import os
from utils import (calculate_numeric_column_attributes,
                   calculate_categorical_column_attributes,
                   calculate_date_description_statistics,
                   dup_data_description)
from snowflake_ui import snowflake_ui_connection
from local_ui import local_ui_connection

conn_type = st.radio(
    "How do you want to connect",
    ["Snowflake", "Local Directory"],
    index=None,
)

if conn_type=='Snowflake':
    snowflake_ui_connection()
else:
    local_ui_connection()
    # vis_conn()