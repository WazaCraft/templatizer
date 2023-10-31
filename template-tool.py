import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import base64

def generate_slot_html(data_row, left_image=True):
    alignment = "left" if left_image else "right"
    return f"""
    <!--Begin Product {alignment.capitalize()}-Image-->
    <tr>
    <td align="center" style="width: 600px; padding-top: 20px; padding-bottom: 35px;">
    <div style="width: {290 if left_image else 280}px; padding-left: 10px; float: {alignment};">
    <p align="top" style="margin: 0px; padding: 0px 20px 8px 0px; text-align: left; color: #aa00aa; font-size: 30px; font-weight: bold; font-family: Helvetica, Tahoma, Roboto, Arial, sans serif; font-stretch: condensed; line-height: 30px;"><a href="{data_row['URL']}" style="text-decoration: none; color: #000000; font-size: 30px;">{data_row['Title']}</a></p>
    <p align="top" style="margin: 0px; padding: 0px 20px 20px 0px; text-align: left; color: #aa00aa; font-size: 19px; font-weight: normal; font-family: Futura, Roboto, sans serif; line-height: 20px;"><a href="{data_row['URL']}" style="text-decoration: none; color: #aa00aa; font-size: 19px; font-weight: normal;">{data_row['Subheader']}</a></p>
    <p align="top" style="margin: 0px; padding: 0px 20px 30px 0px; text-align: left; font-size: 18px; font-family: Helvetica, Tahoma, Roboto, Arial, sans serif; font-stretch: ultra-condensed; font-weight: 400; line-height: 21px;">{data_row['Description']}</p>
    <p align="top" style="margin: 0px; background: #aa00aa; color: #ffffff; font-weight: bold; border-radius: 20px; padding: 10px 20px; text-align: center; display: inline-block; width: max-content; height: max-content; font-family: Futura, Roboto, sans serif; float: left;"><a href="{data_row['URL']}" style="color: #ffffff; text-decoration: none; font-weight: normal;">{data_row['CTA']}</a></p>
    </div>
    <div style="width: 300px; float: {alignment};"><a href="{data_row['URL']}"><img alt="{data_row['Title']}" src="" style="display: block; border-radius: 30px; margin-bottom: 0px; margin-left: auto; margin-right: auto; float: left;" width="300"></a></div>
    </td>
    </tr>
    <!--End Product {alignment.capitalize()}-Image-->
    """

def update_template(template, data):
    soup = BeautifulSoup(template, 'html.parser')
    parent = soup.find('tr').parent

    for tag in parent.find_all('tr'):
        tag.decompose()

    updated_slots = [generate_slot_html(data.iloc[i], left_image=(i % 2 == 0)) for i in range(len(data))]
    new_content = BeautifulSoup(''.join(updated_slots), 'html.parser')
    parent.append(new_content)

    return str(soup)
def get_table_download_link(csv):
    csv = csv.encode('utf-8')
    b64 = base64.b64encode(csv).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="updated_template.html">Download updated template code</a>'

st.title("HTML Email Template Updater")

uploaded_file = st.file_uploader("Upload CSV File", type=['csv'])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(data.head())
    
    template_file = st.text_area("Paste your HTML template here:", height=200, value='''
    <!--Paste the provided default template here if needed-->
    ''')
    
    if st.button("Update Template"):
        updated_template = update_template(template_file, data)
        
        tab1, tab2, tab3 = st.tabs(["Original Template", "Updated Template Code", "Updated Template Preview"])
        
        with tab1:
            st.markdown(template_file, unsafe_allow_html=True)
            
        with tab2:
            st.code(updated_template, language='html')
            st.markdown(get_table_download_link(updated_template), unsafe_allow_html=True)
            
        with tab3:
            st.markdown(updated_template, unsafe_allow_html=True)
