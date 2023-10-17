import os
import streamlit as st
import snowflake.connector
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from gen_visulizations import create_visualizations_and_report,generate_vislizations

from utils import (calculate_numeric_column_attributes,
                   calculate_categorical_column_attributes,
                   calculate_date_description_statistics,
                   dup_data_description)

def local_ui_connection():
    st.title("Database Connector")
    local_dir = st.text_input("Enter your local directory path")
    if local_dir:
        li_files = os.listdir(local_dir)
        filename = local_dir.split('\\')[-1]
        excel_file_path = f"{filename}.xlsx"
        if st.button("Download Statistical Report"):
            with pd.ExcelWriter(excel_file_path) as writer:
                tab_names = []
                tab_obs = []
                for table_name in li_files:
                    path_ = os.path.join(local_dir, table_name)
                    df = pd.read_csv(path_)
                    st.write(df.head())
                    generate_vislizations(df)
                    tab_names.append(table_name)
                    tab_obs.append(dup_data_description(df, table_name)[0])
                    ####
                    for k,_ in dup_data_description(df, table_name)[1].items():
                        res_df = pd.DataFrame(dup_data_description(df, table_name)[1][k])
                        ###
                        if not (res_df.empty):
                            res_df.to_excel(writer, sheet_name=(os.path.splitext(table_name)[0]+'_'+k)[:30], index=False)

                desc_df = pd.DataFrame(dict(zip(tab_names,tab_obs))).T
                desc_df
                desc_df.to_excel(writer, sheet_name='Table desc')
                if excel_file_path:
                    st.success(f"Data downloaded as -> {excel_file_path}")
                    # st.markdown(f"Download [here]({excel_file_path})")
            # except Exception as e:
            #         st.error(f"Connection failed: {str(e)}")
        # if st.button("Download Visual Report"):
        #     st.success("Coming soon!!")
        # elif st.button("Download Visual Report"):
        #     for table_name in li_files:
        #         path_ = os.path.join(local_dir, table_name)
        #         df = pd.read_csv(path_)
        #         create_visualizations_and_report(df, filename)

    ##############
    # **************
    ##############
    # # # Set up tkinter
    # root = tk.Tk()
    # root.withdraw()

    # # Make folder picker dialog appear on top of other windows
    # root.wm_attributes('-topmost', 1)

    # st.write('Please select a folder:')
    # clicked = st.button('Choose Folder')
    # if clicked:
    #     local_dir = filedialog.askdirectory(master=root)
    #     print("local_dir",local_dir)
    #     if local_dir:
    #         li_files = os.listdir(local_dir)
    #         st.write(li_files)
    #         # filename = local_dir.split('\\')[-1]
    #         filename = 'check'
    #         st.write(filename)
    #         excel_file_path = f"{filename}.xlsx"
    #         if st.button("Download Report"):
    #             st.write("a")
    #             with pd.ExcelWriter(excel_file_path) as writer:
    #                 tab_names = []
    #                 tab_obs = []
    #                 for table_name in li_files:
    #                     print("txzhf",table_name)
    #                     path_ = os.path.join(local_dir, table_name)
    #                     df = pd.read_csv(path_)
    #                     st.write(df)
    #                     tab_names.append(table_name)
    #                     tab_obs.append(dup_data_description(df, table_name)[0])
    #                     ####
    #                     for k,_ in dup_data_description(df, table_name)[1].items():
    #                         res_df = pd.DataFrame(dup_data_description(df, table_name)[1][k])
    #                         ###
    #                         if not (res_df.empty):
    #                             res_df.to_excel(writer, sheet_name=(os.path.splitext(table_name)[0]+'_'+k)[:30], index=False)

    #                 desc_df = pd.DataFrame(dict(zip(tab_names,tab_obs))).T
    #                 desc_df
    #                 desc_df.to_excel(writer, sheet_name='Table desc')
    #                 if excel_file_path:
    #                     st.success(f"Data downloaded as -> {excel_file_path}")
    #         else:
    #             st.write("wrong")

# def vis_conn():
#     import streamlit as st
#     import pandas as pd
#     import plotly.express as px
#     from fpdf import FPDF
#     import pdfkit

#     # Sample DataFrame
#     data = pd.DataFrame({
#         'Category': ['A', 'B', 'C', 'D'],
#         'Value': [10, 20, 15, 25]
#     })

#     # Create a Plotly bar chart
#     fig = px.bar(data, x='Category', y='Value', title='Sample Plotly Visualization')

#     # Streamlit app
#     st.title('Streamlit Plotly Report')

#     # Display the Plotly chart
#     st.plotly_chart(fig)
#     if st.button('Generate PDF Report'):
#         # # Create a PDF report
#         # pdf = FPDF()
#         # pdf.add_page()
#         # pdf.set_font("Arial", size=12)
#         # pdf.cell(200, 10, txt="Streamlit Plotly Report", ln=True, align='C')

#         # # Save Plotly figure as an image
#         # fig.write_image("plotly_image.png")

#         # # Add the Plotly image to the PDF report
#         # pdf.image("plotly_image.png", x=10, w=190)
        
#         # # Save the PDF report
#         # pdf_file_name = "streamlit_plotly_report.pdf"
#         # pdf.output(pdf_file_name)

#         # # Display a link to download the PDF report
#         # st.success(f"PDF report generated! [Download PDF report]({pdf_file_name})")

#         # Create HTML for the report
#         report_html = f"""
#         <html>
#         <head></head>
#         <body>
#             <h1>Report</h1>
#             <h2>Data</h2>
#             {data.to_html()}
#             <h2>Bar Chart</h2>
#             {fig.to_html()}
#             <h2>Pie Chart</h2>
#             {fig.to_html()}
#         </body>
#         </html>
#         """
#         # Save the HTML content to a file
#         with open('report_new.html', 'w',encoding="utf-8") as f:
#             f.write(report_html)

#         # Generate PDF from HTML using pdfkit (you need to install wkhtmltopdf separately)
#         pdfkit.from_file('report_new.html', 'report_new.pdf')

#         # Provide a download link for the PDF
#         st.success('PDF Report generated successfully!')
#         st.markdown('[Download PDF Report](report_new.pdf)')






