import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import matplotlib.pyplot as plt
import pdfkit


def create_visualizations_and_report(dataframe, output_pdf_filename="report.pdf"):
    # Separate numerical and categorical columns
    numerical_cols = dataframe.select_dtypes(include=['number']).columns
    categorical_cols = dataframe.select_dtypes(include=['object', 'category']).columns

    # Create visualizations for numerical data
    numerical_figures = []
    for col in numerical_cols:
        fig, ax = plt.subplots()
        dataframe[col].plot(kind='hist', ax=ax)
        ax.set_title(f'Numerical - {col}')
        numerical_figures.append(fig)

    # Create visualizations for categorical data
    categorical_figures = []
    for col in categorical_cols:
        fig, ax = plt.subplots()
        dataframe[col].value_counts().plot(kind='bar', ax=ax)
        ax.set_title(f'Categorical - {col}')
        categorical_figures.append(fig)

    # Generate PDF report
    pdfkit_options = {
        'quiet': ''
    }
    pdfkit.from_file(
        ['temp_numerical.html', 'temp_categorical.html'],
        output_pdf_filename,
        options=pdfkit_options
    )

    # Display success message
    print(f'PDF report generated as {output_pdf_filename}')

    # Close all Matplotlib figures
    plt.close('all')



# def vis_conn():

    # # Create a Plotly bar chart
    # fig = px.bar(data, x='Category', y='Value', title='Sample Plotly Visualization')

    # # Streamlit app
    # st.title('Streamlit Plotly Report')

    # # Display the Plotly chart
    # st.plotly_chart(fig)
    # if st.button('Generate PDF Report'):
    #     # Create a PDF report
    #     pdf = FPDF()
    #     pdf.add_page()
    #     pdf.set_font("Arial", size=12)
    #     pdf.cell(200, 10, txt="Streamlit Plotly Report", ln=True, align='C')

    #     # Save Plotly figure as an image
    #     fig.write_image("plotly_image.png")

    #     # Add the Plotly image to the PDF report
    #     pdf.image("plotly_image.png", x=10, w=190)
        
    #     # Save the PDF report
    #     pdf_file_name = "streamlit_plotly_report.pdf"
    #     pdf.output(pdf_file_name)

    #     # Display a link to download the PDF report
    #     st.success(f"PDF report generated! [Download PDF report]({pdf_file_name})")



def generate_vislizations(dataframe):
    # Separate numerical and categorical columns
    numerical_cols = dataframe.select_dtypes(include=['number','int64']).columns
    categorical_cols = dataframe.select_dtypes(include=['object', 'category']).columns

    # Create visualizations for numerical data
    numerical_figures = []
    for col in numerical_cols:
        fig, ax = plt.subplots()
        dataframe[col].plot(kind='hist', ax=ax)
        ax.set_title(f'Numerical - {col}')
        numerical_figures.append(fig)

    # Create visualizations for categorical data
    categorical_figures = []
    for col in categorical_cols:
        fig, ax = plt.subplots()
        dataframe[col].value_counts().plot(kind='bar', ax=ax)
        ax.set_title(f'Categorical - {col}')
        categorical_figures.append(fig)

    [st.plotly_chart(num_fig) for num_fig in numerical_figures]
    [st.plotly_chart(cat_fig) for cat_fig in categorical_figures]

