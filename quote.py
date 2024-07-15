from datetime import datetime,timezone,timedelta
import pandas as pd
import streamlit as st
import numpy as np
import warnings
import json
from datetime import datetime
from io import BytesIO
import openpyxl as op
from openpyxl.styles import Font,NamedStyle,Alignment
import warnings
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from azure.storage.blob import BlobServiceClient,ContainerClient
import os
import math
import variable as v
import my_function as my

# http://localhost:8501/?page=quote&project=Test%20Project%201

warnings.filterwarnings("ignore")
st.set_page_config(page_title=v.page_title, page_icon=v.icon_path, layout='wide')

st.markdown("""
            <style>
            .big-font {
                font-size:40px;
                line-height: 0.7;
                font-weight:bold;
                text-align: center;
            }
            </style>
            """, unsafe_allow_html=True)

st.markdown('''
   <style>
       .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
       font-size:27px;
       font-weight:bold;
       }
   </style>
   ''', unsafe_allow_html=True)

st.markdown("""
            <style>
            .medium-font {
                font-size:25px;
                line-height: 0.7;
                font-weight:bold;
            }
            </style>
            """, unsafe_allow_html=True)

st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] 
    {
    gap: 40px;
    }
    .stTabs [data-baseweb="tab"] {
    height: 80px;
    white-space: pre-wrap;
    background-color: #FFFFFF;
    border-radius: 4px 4px 0px 0px;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
    }

    .stTabs [aria-selected="true"] {
    background-color: #D9D9D9;
    }

</style>""", unsafe_allow_html=True)

def home():

    params_dict = st.query_params

    if params_dict.get("page") == "quote":
        project_name = params_dict.get("project")
        project_data_list = my.get_project_data(project_name)
        if len(project_data_list) == 0:
            st.write("Nothing")
        elif len(project_data_list) != 0 and project_data_list[-1] == "False":
            st.write("Not Started")
        else:
            # 獲取設定的ID
            title_id = project_data_list[2]
            requirements_introduction_id = project_data_list[3]
            common_columns_id = project_data_list[4]
            individual_columns_id = project_data_list[5]
            function_id = project_data_list[6]
            verification_code_id = project_data_list[7]
            internal_mail_receipients_id = project_data_list[8]
            supplier_mail_setting_id = project_data_list[9]
            setting_check_id = project_data_list[10]


            # 獲取Function資料
            function_data = my.get_function_data_by_id(function_id)
            use_attachment = function_data[2]
            use_verification_code = function_data[3]
            use_internal_mail = function_data[4]
            use_supplyer_mail = function_data[5]

            now_datetime = (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%Y-%m-%d %H%M%S")

            if use_verification_code.lower() == "false":
                st.session_state.verification = True
                st.session_state.name = now_datetime
                st.session_state.verification_code = now_datetime

            if st.session_state.get("verification") == False or st.session_state.get("verification") == None:
                keyin_verification_code = st.text_input(label="Please Enter Verification Code")

                if st.button('Check Verification Code', key="Check Verification Code"):

                    # 讀取驗證碼
                    verification_code_str = my.get_verification_code_by_id(verification_code_id)
                    verification_code_df = pd.DataFrame(json.loads(verification_code_str)["data"], columns=json.loads(verification_code_str)["columns"], index=json.loads(verification_code_str)["index"])
                    verification_code_df = verification_code_df[verification_code_df["Code"] != ""]
                    st.session_state.verification_code_df = verification_code_df
                    verification_code_list = list(verification_code_df["Code"])

                    if keyin_verification_code not in verification_code_list:
                        st.session_state.verification = False
                        st.session_state.name = now_datetime
                        st.error("Verification Code Error")
                    else:
                        name = verification_code_df.loc[verification_code_list.index(keyin_verification_code), "Name"]
                        st.session_state.verification = True
                        st.session_state.name = name
                        st.session_state.verification_code = keyin_verification_code
                        st.success("Verification Code OK")
                        st.rerun()

            elif st.session_state.get("verification") == True:

                form(now_datetime, st.session_state.name,project_data_list,use_attachment,use_internal_mail,use_supplyer_mail)

                a1, a2 = st.columns([10, 1])
                with a2:
                    st.write(v.version)

def form(now_datetime,name,project_data_list,use_attachment,use_internal_mail,use_supplyer_mail):

    # 獲取設定的ID
    project_id = project_data_list[0]
    project_name = project_data_list[1]
    title_id = project_data_list[2]
    requirements_introduction_id = project_data_list[3]
    common_columns_id = project_data_list[4]
    individual_columns_id = project_data_list[5]
    function_id = project_data_list[6]
    verification_code_id = project_data_list[7]
    internal_mail_receipients_id = project_data_list[8]
    supplier_mail_setting_id = project_data_list[9]
    setting_check_id = project_data_list[10]

    # 讀取Requirements Introduction
    requirements_introduction_data = my.get_requirements_introduction_by_id(requirements_introduction_id)
    product_list = [requirements_introduction_data[0], requirements_introduction_data[2], requirements_introduction_data[4],
                    requirements_introduction_data[6], requirements_introduction_data[8]]
    product_list = [i for i in product_list if i != ""]
    product_num = len(product_list)
    introduction_list = [requirements_introduction_data[requirements_introduction_data.index(i) + 1] for i in product_list]

    # 讀取Common Columns
    common_col_str = my.get_common_columns_by_id(common_columns_id)
    common_col_df = pd.DataFrame(json.loads(common_col_str)["data"], columns=json.loads(common_col_str)["columns"], index=json.loads(common_col_str)["index"])
    common_col_df = common_col_df[common_col_df["Column Name"] != ""]
    common_col_df.reset_index(inplace=True,drop=True)

    # 讀取Individual Columns
    individual_col_str = my.get_individual_columns_by_id(individual_columns_id)
    individual_col_df = pd.DataFrame(json.loads(individual_col_str)["data"], columns=json.loads(individual_col_str)["columns"], index=json.loads(individual_col_str)["index"])
    individual_col_df = individual_col_df[individual_col_df["Column Name"] != ""]
    individual_col_df.reset_index(inplace=True, drop=True)

    # 讀取Title
    title_list = my.get_title_by_id(title_id)
    title_list = [i for i in title_list if i != ""]

    # 前圖
    front_image1, front_image2, front_image3, front_image4, front_image5 = st.columns([1, 1, 1, 1, 1])
    with front_image3:
        st.image(v.logo_path)

    # Title
    title1, title2, title3 = st.columns([1, 1, 1])
    with title2:
        for text in title_list:
            st.markdown('<p class="big-font">{}<p>'.format(str(text)), unsafe_allow_html=True)

    df_col_name_list = ["Product"] + list(common_col_df["Column Name"]) + list(individual_col_df["Column Name"])
    save_col_name_list = [i[0] for i in v.first_col] + list(common_col_df["Column Name"]) + list(individual_col_df["Column Name"]) + [i[0] for i in v.last_col]

    # Content
    common_col_list = [[common_col_df.loc[i, "Column Name"],
                        common_col_df.loc[i, "Data Type"],
                        common_col_df.loc[i, "Option"],
                        common_col_df.loc[i, "Instructions"]] for i in range(0, len(common_col_df))]
    individual_col_list = [[individual_col_df.loc[i, "Column Name"],
                            individual_col_df.loc[i, "Data Type"],
                            individual_col_df.loc[i, "Option"],
                            individual_col_df.loc[i, "Instructions"]] for i in range(0, len(individual_col_df))]

    a1, a2, a3 = st.columns([1, 10, 1])
    with a2:
        st.markdown('---')
        create_df(project_id,name,st.session_state.verification_code, product_list, df_col_name_list)
        st.markdown('---')

        common_results_dict = {}

        for i in range(0, len(common_col_list),1):
            common_results_dict = create_data_input(common_col_list[i], common_results_dict, "Common")

        st.write("")  # 做個間隔
        st.write("")  # 做個間隔

        # Tab
        if product_num == 1:
            pass
        elif product_num == 2:
            tab1, tab2 = st.tabs(product_list)
        elif product_num == 3:
            tab1, tab2, tab3 = st.tabs(product_list)
        elif product_num == 4:
            tab1, tab2, tab3, tab4 = st.tabs(product_list)
        elif product_num == 5:
            tab1, tab2, tab3, tab4, tab5 = st.tabs(product_list)

        for ind in range(0, product_num):
            if ind == 0:
                if product_num == 1 :
                    st.write("")  # 做個間隔
                    st.markdown('<p class="medium-font">{}<p>'.format("Requirements introduction."), unsafe_allow_html=True)
                    st.write("")  # 做個間隔
                    st.text(introduction_list[ind])
                    st.write("")  # 做個間隔

                    tab1_individual_results_dict = {}
                    for i in range(0, len(individual_col_list)):
                        tab1_individual_results_dict = create_data_input(individual_col_list[i], tab1_individual_results_dict, "Tab1")

                    if str(use_attachment).lower() == "true":
                        tab1_uploaded_file_list = st.file_uploader(label="Upload Attachment",
                                                                   type=["xlsx", "xls", "jpg", "doc", "docx", "pdf", "ppt", "pptx"],
                                                                   accept_multiple_files=True,
                                                                   key="Attachment Tab1")
                else:
                    with tab1:
                        st.write("")  # 做個間隔
                        st.markdown('<p class="medium-font">{}<p>'.format("Requirements introduction."), unsafe_allow_html=True)
                        st.write("")  # 做個間隔
                        st.text(introduction_list[ind])
                        st.write("")  # 做個間隔

                        tab1_individual_results_dict = {}
                        for i in range(0, len(individual_col_list)):
                            tab1_individual_results_dict = create_data_input(individual_col_list[i], tab1_individual_results_dict, "Tab1")

                        if str(use_attachment).lower() == "true":
                            tab1_uploaded_file_list = st.file_uploader(label="Upload Attachment",
                                                                       type=["xlsx", "xls", "jpg", "doc", "docx", "pdf", "ppt", "pptx"],
                                                                       accept_multiple_files=True,
                                                                       key="Attachment Tab1")
            elif ind == 1:
                with tab2:
                    st.write("")  # 做個間隔
                    st.markdown('<p class="medium-font">{}<p>'.format("Requirements introduction."), unsafe_allow_html=True)
                    st.write("")  # 做個間隔
                    st.text(introduction_list[ind])
                    st.write("")  # 做個間隔

                    tab2_individual_results_dict = {}

                    for i in range(0, len(individual_col_list)):
                        tab2_individual_results_dict = create_data_input(individual_col_list[i], tab2_individual_results_dict, "Tab2")

                    if str(use_attachment).lower() == "true":
                        tab2_uploaded_file_list = st.file_uploader(label="Upload Attachment",
                                                                   type=["xlsx", "xls", "jpg", "doc", "docx", "pdf", "ppt", "pptx"],
                                                                   accept_multiple_files=True,
                                                                   key="Attachment Tab2")
            elif ind == 2:
                with tab3:
                    st.write("")  # 做個間隔
                    st.markdown('<p class="medium-font">{}<p>'.format("Requirements introduction."), unsafe_allow_html=True)
                    st.write("")  # 做個間隔
                    st.text(introduction_list[ind])
                    st.write("")  # 做個間隔

                    tab3_individual_results_dict = {}

                    for i in range(0, len(individual_col_list)):
                        tab3_individual_results_dict = create_data_input(individual_col_list[i], tab3_individual_results_dict, "Tab3")

                    if str(use_attachment).lower() == "true":
                        tab3_uploaded_file_list = st.file_uploader(label="Upload Attachment",
                                                                   type=["xlsx", "xls", "jpg", "doc", "docx", "pdf", "ppt", "pptx"],
                                                                   accept_multiple_files=True,
                                                                   key="Attachment Tab3")
            elif ind == 3:
                with tab4:
                    st.write("")  # 做個間隔
                    st.markdown('<p class="medium-font">{}<p>'.format("Requirements introduction."), unsafe_allow_html=True)
                    st.write("")  # 做個間隔
                    st.text(introduction_list[ind])
                    st.write("")  # 做個間隔

                    tab4_individual_results_dict = {}

                    for i in range(0, len(individual_col_list)):
                        tab4_individual_results_dict = create_data_input(individual_col_list[i], tab4_individual_results_dict, "Tab4")

                    if str(use_attachment).lower() == "true":
                        tab4_uploaded_file_list = st.file_uploader(label="Upload Attachment",
                                                                   type=["xlsx", "xls", "jpg", "doc", "docx", "pdf", "ppt", "pptx"],
                                                                   accept_multiple_files=True,
                                                                   key="Attachment Tab4")
            elif ind == 4:
                with tab5:
                    st.write("")  # 做個間隔
                    st.markdown('<p class="medium-font">{}<p>'.format("Requirements introduction."), unsafe_allow_html=True)
                    st.write("")  # 做個間隔
                    st.text(introduction_list[ind])
                    st.write("")  # 做個間隔

                    tab5_individual_results_dict = {}

                    for i in range(0, len(individual_col_list)):
                        tab5_individual_results_dict = create_data_input(individual_col_list[i], tab5_individual_results_dict, "Tab5")

                    if str(use_attachment).lower() == "true":
                        tab5_uploaded_file_list = st.file_uploader(label="Upload Attachment",
                                                                   type=["xlsx", "xls", "jpg", "doc", "docx", "pdf", "ppt", "pptx"],
                                                                   accept_multiple_files=True,
                                                                   key="Attachment Tab5")

        st.button("Confirm modification", key='alter_df')

    if st.session_state["alter_df"] == True:
        for ind in range(0, product_num):
            for key in common_results_dict.keys():
                value = common_results_dict[key]
                st.session_state["df"].loc[ind, key] = value

        for ind in range(0, product_num):
            if ind == 0:
                for key in tab1_individual_results_dict.keys():
                    value = tab1_individual_results_dict[key]
                    st.session_state["df"].loc[ind, key] = value
            elif ind == 1:
                for key in tab2_individual_results_dict.keys():
                    value = tab2_individual_results_dict[key]
                    st.session_state["df"].loc[ind, key] = value
            elif ind == 2:
                for key in tab3_individual_results_dict.keys():
                    value = tab3_individual_results_dict[key]
                    st.session_state["df"].loc[ind, key] = value
            elif ind == 3:
                for key in tab4_individual_results_dict.keys():
                    value = tab4_individual_results_dict[key]
                    st.session_state["df"].loc[ind, key] = value
            elif ind == 4:
                for key in tab5_individual_results_dict.keys():
                    value = tab5_individual_results_dict[key]
                    st.session_state["df"].loc[ind, key] = value

        st.rerun()

    if st.session_state['submit'] == True:
        df = st.session_state["df"]

        # 判斷Verification Code
        v_code = st.session_state.verification_code
        if st.session_state.verification_code != now_datetime:
            verification_code_df = st.session_state.verification_code_df
            v_name = verification_code_df[verification_code_df["Code"] == st.session_state.verification_code]["Name"].values[0]
        else:
            v_name = None


        # 存暫存檔
        for col_list in common_col_list+individual_col_list:
            if col_list[1] == "Date":
                df[col_list[0]] = df[col_list[0]].apply(lambda x:str(x))
        my.upload_temp_row(project_id,name,st.session_state.verification_code, df.to_json())


        # 寫入附件
        attachment_filename_list = []
        if str(use_attachment).lower() == "true":

            blob_service_client = BlobServiceClient.from_connection_string(v.blob_connection_string)
            container_client = blob_service_client.get_container_client(v.blob_container)
            for ind in range(0, len(product_list)):
                product = product_list[ind]
                attachment_data_path = v.attachment_path.format(project_name,product,name + " " + now_datetime)
                if ind == 0:
                    attachment_filename = ",".join([uploaded_file.name for uploaded_file in tab1_uploaded_file_list])
                    for uploaded_file in tab1_uploaded_file_list:
                        blob_client = container_client.get_blob_client(attachment_data_path + "\\" + uploaded_file.name)
                        blob_client.upload_blob(uploaded_file.getbuffer(), overwrite=True)
                elif ind == 1:
                    attachment_filename = ",".join([uploaded_file.name for uploaded_file in tab2_uploaded_file_list])
                    for uploaded_file in tab2_uploaded_file_list:
                        blob_client = container_client.get_blob_client(attachment_data_path + "\\" + uploaded_file.name)
                        blob_client.upload_blob(uploaded_file.getbuffer(), overwrite=True)
                elif ind == 2:
                    attachment_filename = ",".join([uploaded_file.name for uploaded_file in tab3_uploaded_file_list])
                    for uploaded_file in tab3_uploaded_file_list:
                        blob_client = container_client.get_blob_client(attachment_data_path + "\\" + uploaded_file.name)
                        blob_client.upload_blob(uploaded_file.getbuffer(), overwrite=True)
                elif ind == 3:
                    attachment_filename = ",".join([uploaded_file.name for uploaded_file in tab4_uploaded_file_list])
                    for uploaded_file in tab4_uploaded_file_list:
                        blob_client = container_client.get_blob_client(attachment_data_path + "\\" + uploaded_file.name)
                        blob_client.upload_blob(uploaded_file.getbuffer(), overwrite=True)
                elif ind == 4:
                    attachment_filename = ",".join([uploaded_file.name for uploaded_file in tab5_uploaded_file_list])
                    for uploaded_file in tab5_uploaded_file_list:
                        blob_client = container_client.get_blob_client(attachment_data_path + "\\" + uploaded_file.name)
                        blob_client.upload_blob(uploaded_file.getbuffer(), overwrite=True)

                attachment_filename_list.append(attachment_filename)
        else:
            attachment_filename_list = [None] * len(product_list)

        # 存正式資料
        df["RowID"] = str(now_datetime)
        df['Verification Code'] = st.session_state.verification_code
        df["Verification Code Name"] = st.session_state.name
        my.upload_results_table(project_id,name,st.session_state.verification_code,df.to_json())

        # Send Mail
        if str(use_internal_mail).lower() == "true":
            # 讀取Internal Mail Receipients
            internal_mail_receipients_str = my.get_internal_mail_receipients_by_id(internal_mail_receipients_id)
            internal_mail_receipients_df = pd.DataFrame(json.loads(internal_mail_receipients_str)["data"], columns=json.loads(internal_mail_receipients_str)["columns"], index=json.loads(internal_mail_receipients_str)["index"])
            internal_mail_receipients_df = internal_mail_receipients_df[internal_mail_receipients_df["Mail"] != ""]
            internal_mail_receipients_df.reset_index(inplace=True, drop=True)

            my.send_internal_mail(st.session_state['df'],internal_mail_receipients_df)

        # Send Supplyer Mail
        if str(use_supplyer_mail).lower() == "true":
            # 讀取Supplier Mail Setting
            supplier_mail_setting_list = my.get_supplier_mail_setting_by_id(supplier_mail_setting_id)
            subject = supplier_mail_setting_list[0]
            content = supplier_mail_setting_list[1]

            my.send_supplyer_mail(st.session_state['df'], subject, content)

        st.session_state["submit_status"] = True
        st.rerun()

def create_data_input(col_info_list,results_dict,area):

    col = col_info_list[0]
    col_type = col_info_list[1]
    col_option = col_info_list[2]
    col_instructions = col_info_list[3]
    if col_instructions == "" or str(col_instructions) == "nan":
        show_col = col
    else:
        show_col = col + "(" + str(col_instructions) + ")"
    if area == "Common":
        ind = 0
    else:
        ind = int(area[-1]) - 1

    default_value = st.session_state['df'].loc[ind,col]

    if col_type.lower() == "text":
        results_dict[col] = st.text_input(show_col, key=col + " " + area, value=default_value)
    elif col_type.lower() == "date":
        if default_value == None or default_value == "" or str(default_value) == "nan":
            results_dict[col] = st.date_input(show_col, key=col + " " + area)
        else:
            results_dict[col] = st.date_input(show_col, key=col + " " + area, value=datetime.strptime(str(default_value), "%Y-%m-%d").date())
    elif col_type.lower() == "decimal":
        col_option = round(float(col_option))
        if default_value == None or default_value == "" or str(default_value) == "nan":
            default_value = None
        results_dict[col] = st.number_input(show_col, key=col + " " + area, step=10 ** -col_option, format="%.{}f".format(col_option), value=default_value)
    elif col_type.lower() == "integer":
        if default_value == None or default_value == "" or str(default_value) == "nan":
            default_value = None
        else:
            default_value = int(default_value)
        results_dict[col] = st.number_input(show_col, key=col + " " + area, step=1, value=default_value)
    elif col_type.lower() == "radio":
        col_option_list = col_option.replace("\n", "").split(";")
        if col_option_list[-1] == "":
            del col_option_list[-1]
        if default_value == None or default_value == "" or str(default_value) == "nan":
            results_dict[col] = st.radio(show_col, key=col + " " + area, options=col_option_list, index=0)
        else:
            results_dict[col] = st.radio(show_col, key=col + " " + area, options=col_option_list, index=col_option_list.index(default_value))
    elif col_type.lower() == "multiselect":
        col_option_list = col_option.replace("\n", "").split(";")
        if col_option_list[-1] == "":
            del col_option_list[-1]
        if default_value == None or default_value == "" or str(default_value) == "nan":
            selected_list = st.multiselect(show_col, key=col + " " + area, options=col_option_list)
            results_dict[col] = ",".join(selected_list)
        else:
            selected_list = default_value.split(",")
            results_dict[col] = st.multiselect(show_col, key=col + " " + area, options=col_option_list, default=selected_list)
    else:
        results_dict[col] = st.text_input(show_col, key=col + " " + area, value=default_value)
    return results_dict

def create_df(project_id,name,verification_code, product_list, col_name_list):

    if "df" not in st.session_state:

        record_dict_str = my.get_temp_row(project_id,name,verification_code)

        if record_dict_str == "":
            df = pd.DataFrame([[product] + [""] * (len(col_name_list) - 1) for product in product_list], columns=col_name_list)
        else:
            record_dict = json.loads(record_dict_str)
            df = pd.DataFrame(record_dict)

        # index改成數字
        df.index = [i for i in range(0,len(df))]
        st.session_state["df"] = df

    st.dataframe(st.session_state["df"].set_index("Product"))

    st.button("Submit Quote", key='submit')

    if "submit_status" in st.session_state:
        if st.session_state["submit_status"]:
            st.success("Submit Succeeded")



home()