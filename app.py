import streamlit as st
import pandas as pd
from io import BytesIO
import time
import base64

# Enable Wide Mode
st.set_page_config(layout="wide")

# App Title
st.title("CleanConvert Pro")
st.write("Welcome to CleanConvert Pro, your all-in-one data management solution. Effortlessly convert your CSV and Excel files while cleaning your data by removing duplicates, handling missing values, and customizing your file columns for easy analysis!")

# File uploader
files = st.file_uploader('Upload your CSV or Excel file:', type=['csv', 'xlsx'], accept_multiple_files=True)

if files:
    for idx, file in enumerate(files):
        ext = file.name.split('.')[-1]

        try:
            df = pd.read_csv(file) if ext == 'csv' else pd.read_excel(file)
            st.subheader(f'{file.name} - Preview')
            st.dataframe(df.head())

            with st.expander(f'Process {file.name}'):
                if st.checkbox(f'Remove Duplicates - {file.name}', key=f'duplicates_{idx}_{file.name}'):
                    df.drop_duplicates(inplace=True)
                    st.success('Duplicates removed successfully!')
                    st.dataframe(df.head())

                if st.checkbox(f'Remove Missing Values - {file.name}', key=f'missing_values_{idx}_{file.name}'):
                    df.fillna(df.select_dtypes(include=['number']).mean(), inplace=True)
                    st.success('Missing values filled successfully!')
                    st.dataframe(df.head())

                selected_columns = st.multiselect(f'Select columns to display - {file.name}', df.columns, default=df.columns)
                df = df[selected_columns]
                st.dataframe(df.head())

                if st.checkbox(f'Show Chart - {file.name}') and not df.select_dtypes(include=['number']).empty:
                    st.write("Bar Chart based on numerical data:")
                    st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

            format_choice = st.radio(f'Convert {file.name} to', ['CSV', 'Excel'], key=f'convert_{file.name}')

            st.subheader("Processing your file...")
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.05)
                progress_bar.progress(i + 1)

            st.subheader(f"Download {file.name} as {format_choice}")

            if format_choice == 'CSV':
                output = BytesIO()
                df.to_csv(output, index=False)
                mime = 'text/csv'
                new_name = file.name.replace(ext, 'csv')
            else:
                output = BytesIO()
                df.to_excel(output, index=False, engine='openpyxl')
                mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                new_name = file.name.replace(ext, 'xlsx')

            output.seek(0)
            encoded_file = base64.b64encode(output.read()).decode()

            st.markdown(f'''
                <a href="data:{mime};base64,{encoded_file}" class="download-btn" download="{new_name}">
                    Download File
                </a>
            ''', unsafe_allow_html=True)

            st.success('File processing completed!')

        except Exception as e:
            st.error(f"Error processing the file: {e}")
else:
    st.warning("Please upload a CSV or Excel file to begin.")
