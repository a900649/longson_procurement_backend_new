import json
import pandas as pd
import variable as v
import pymysql
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl

##############################################################################################################################

# Project Name

def get_project_dict():

    project_name_to_data = {}
    project_id_to_data = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT * FROM `project`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        project_name_to_data[i[1]] = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11]]
        project_id_to_data[i[0]] = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11]]

    return project_name_to_data, project_id_to_data

def get_project_data(project_name):
    project_data_list = []

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT * FROM `project` where `Project Name` = '{}'".format(project_name)
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    if data != ():
        project_data_list = list(data[0])


    return project_data_list

def create_project(name,title,requirements_introduction,common_columns,individual_columns,function,verification_code,internal_mail_receipients,supplier_mail_setting,check,start):

    update_dateime = datetime.now()
    project_id = str(update_dateime.strftime("%Y-%m-%d %H%M%S"))

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "REPLACE INTO project (`Project ID`,`Project Name`,`Title`,`Requirements Introduction`,`Common Columns`," \
          "`Individual Columns`,`Function`,`Verification Code`,`Internal Mail Receipients`,`Supplier Mail Setting`,`Check`,`Start`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    k = cursor.executemany(sql, [[project_id,name,title,requirements_introduction,common_columns,individual_columns,function,verification_code,internal_mail_receipients,supplier_mail_setting,check,start]])
    db.commit()
    db.close()

def edit_project_name(original_project_name,edit_project_name):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update project Set `Project Name` = '{}' Where `Project Name` = '{}'".format(edit_project_name,original_project_name)
    cursor.execute(sql)
    db.commit()
    db.close()

def edit_project_row(name,title,requirements_introduction,common_columns,individual_columns,function,verification_code,internal_mail_receipients,supplier_mail_setting,check,start):
    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update project Set " \
          "`Common Columns` = '{}' , " \
          "`Requirements Introduction` = '{}' , " \
          "`Individual Columns` = '{}' , " \
          "`Function` = '{}' , " \
          "`Verification Code` = '{}' , "\
          "`Internal Mail Receipients` = '{}' , " \
          "`Supplier Mail Setting` = '{}' , " \
          "`Check` = '{}' , " \
          "`Start` = '{}'  Where `Project Name` = '{}'".format(title,requirements_introduction,common_columns,individual_columns,function,verification_code,internal_mail_receipients,supplier_mail_setting,check,start,name)
    cursor.execute(sql)
    db.commit()
    db.close()

##############################################################################################################################

# Title

def get_title_dict():
    title_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT * FROM `title`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        title_dict[i[1]] = [i[2], i[3], i[4], i[5], i[6]]

    return title_dict

def get_title_name_to_id_dict():
    title_name_to_id_dict = {}
    title_id_to_name_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Title ID`,`Title Name` FROM `title`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        title_name_to_id_dict[i[1]] = i[0]
        title_id_to_name_dict[i[0]] = i[1]

    return title_name_to_id_dict,title_id_to_name_dict

def get_title_by_id(title_id):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Title Row 1`,`Title Row 2`,`Title Row 3`,`Title Row 4`,`Title Row 5` FROM `title` where `Title ID` = '{}'".format(title_id)
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchone()

    return list(data)

def create_title(title_name,row_1,row_2,row_3,row_4,row_5):
    update_dateime = datetime.now()
    title_id = str(update_dateime.strftime("%Y-%m-%d %H%M%S"))

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "REPLACE INTO title (`Title ID`,`Title Name`,`Title Row 1`,`Title Row 2`,`Title Row 3`,`Title Row 4`,`Title Row 5`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    k = cursor.executemany(sql, [[title_id,title_name,row_1,row_2,row_3,row_4,row_5]])
    db.commit()
    db.close()

def edit_title_name(original_title_name,edit_title_name):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update title Set `Title Name` = '{}' Where `Title Name` = '{}'".format(edit_title_name,original_title_name)
    cursor.execute(sql)
    db.commit()
    db.close()

def edit_title_row(title_name,row_1,row_2,row_3,row_4,row_5):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update title Set " \
          "`Title Row 1` = '{}' , " \
          "`Title Row 2` = '{}' , " \
          "`Title Row 3` = '{}' , " \
          "`Title Row 4` = '{}' , " \
          "`Title Row 5` = '{}' Where `Title Name` = '{}'".format(row_1,row_2,row_3,row_4,row_5,title_name)
    cursor.execute(sql)
    db.commit()
    db.close()

##############################################################################################################################

# Requirements Introduction

def get_requirements_introduction_dict():
    requirements_introduction_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT * FROM `requirements_introduction`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        requirements_introduction_dict[i[1]] = [i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11]]

    return requirements_introduction_dict

def get_requirements_introduction_name_to_id_dict():
    requirements_introduction_name_to_id_dict = {}
    requirements_introduction_id_to_name_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Requirements Introduction ID`,`Requirements Introduction Name` FROM `requirements_introduction`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        requirements_introduction_name_to_id_dict[i[1]] = i[0]
        requirements_introduction_id_to_name_dict[i[0]] = i[1]

    return requirements_introduction_name_to_id_dict,requirements_introduction_id_to_name_dict

def get_requirements_introduction_by_id(requirements_introduction_id):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Product 1`,`Introduction 1`,`Product 2`,`Introduction 2`,`Product 3`,`Introduction 3`," \
          "`Product 4`,`Introduction 4`,`Product 5`,`Introduction 5` FROM `requirements_introduction` where `Requirements Introduction ID` = '{}'".format(requirements_introduction_id)
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchone()

    return list(data)

def create_requirements_introduction(requirements_introduction_name,product_1,introduction_1,product_2,introduction_2,
                                     product_3,introduction_3,product_4,introduction_4,product_5,introduction_5):
    update_dateime = datetime.now()
    requirements_introduction_id = str(update_dateime.strftime("%Y-%m-%d %H%M%S"))

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "REPLACE INTO requirements_introduction (`Requirements Introduction ID`,`Requirements Introduction Name`,`Product 1`,`Introduction 1`," \
          "`Product 2`,`Introduction 2`," \
          "`Product 3`,`Introduction 3`," \
          "`Product 4`,`Introduction 4`," \
          "`Product 5`,`Introduction 5`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    k = cursor.executemany(sql, [[requirements_introduction_id,requirements_introduction_name,product_1,introduction_1,
                                  product_2,introduction_2,product_3,introduction_3,product_4,introduction_4,product_5,introduction_5]])
    db.commit()
    db.close()

def edit_requirements_introduction_name(original_requirements_introduction_name,edit_requirements_introduction_name):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update requirements_introduction Set `Requirements Introduction Name` = '{}' Where " \
          "`Requirements Introduction Name` = '{}'".format(edit_requirements_introduction_name,original_requirements_introduction_name)
    cursor.execute(sql)
    db.commit()
    db.close()

def edit_requirements_introduction_row(requirements_introduction_name,product_1,introduction_1,product_2,introduction_2,
                                       product_3,introduction_3,product_4,introduction_4,product_5,introduction_5):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update requirements_introduction Set " \
          "`Product 1` = '{}' , " \
          "`Introduction 1` = '{}' , " \
          "`Product 2` = '{}' , " \
          "`Introduction 2` = '{}' , "\
          "`Product 3` = '{}' , " \
          "`Introduction 3` = '{}' , " \
          "`Product 4` = '{}' , " \
          "`Introduction 4` = '{}' , " \
          "`Product 5` = '{}' , " \
          "`Introduction 5` = '{}'  Where `Requirements Introduction Name` = '{}'".format(product_1,introduction_1,product_2,introduction_2,product_3,introduction_3,product_4,introduction_4,product_5,introduction_5,requirements_introduction_name)
    cursor.execute(sql)
    db.commit()
    db.close()

##############################################################################################################################

# Common Columns

def get_common_columns_dict():
    common_columns_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT * FROM `common_columns`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        common_columns_dict[i[1]] = i[2]

    return common_columns_dict

def get_common_columns_name_to_id_dict():
    common_columns_name_to_id_dict = {}
    common_columns_id_to_name_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Common Columns ID`,`Common Columns Name` FROM `common_columns`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        common_columns_name_to_id_dict[i[1]] = i[0]
        common_columns_id_to_name_dict[i[0]] = i[1]

    return common_columns_name_to_id_dict, common_columns_id_to_name_dict

def get_common_columns_by_id(common_columns_id):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Data` FROM `common_columns` where `Common Columns ID` = '{}'".format(common_columns_id)
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchone()

    return data[0]

def create_common_columns(common_columns_name,column_name_list,data_type_list,option_list,instructions_list):
    update_dateime = datetime.now()
    common_columns_id = str(update_dateime.strftime("%Y-%m-%d %H%M%S"))

    data_list = [[column_name_list[i],data_type_list[i],option_list[i],instructions_list[i]] for i in range(0,len(column_name_list))]
    data_df = pd.DataFrame(data_list,columns=["Column Name","Data Type","Option","Instructions"])
    data_df.fillna("",inplace=True)
    data_str = data_df.to_json(orient="split")

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "REPLACE INTO common_columns (`Common Columns ID`,`Common Columns Name`,`Data`) VALUES (%s,%s,%s)"
    k = cursor.executemany(sql, [[common_columns_id,common_columns_name,data_str]])
    db.commit()
    db.close()

def edit_common_columns_name(original_common_columns_name,edit_common_columns_name):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update common_columns Set `Common Columns Name` = '{}' Where " \
          "`Common Columns Name` = '{}'".format(edit_common_columns_name,original_common_columns_name)
    cursor.execute(sql)
    db.commit()
    db.close()

def edit_common_columns_row(common_columns_name, common_columns_data):
    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update common_columns Set `Data` = '{}' Where `Common Columns Name` = '{}'".format(common_columns_data, common_columns_name)
    cursor.execute(sql)
    db.commit()
    db.close()

##############################################################################################################################

# Individual Columns

def get_individual_columns_dict():
    individual_columns_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT * FROM `individual_columns`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        individual_columns_dict[i[1]] = i[2]

    return individual_columns_dict

def get_individual_columns_name_to_id_dict():
    individual_columns_name_to_id_dict = {}
    individual_columns_id_to_name_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Individual Columns ID`,`Individual Columns Name` FROM `individual_columns`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        individual_columns_name_to_id_dict[i[1]] = i[0]
        individual_columns_id_to_name_dict[i[0]] = i[1]

    return individual_columns_name_to_id_dict, individual_columns_id_to_name_dict

def get_individual_columns_by_id(individual_columns_id):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Data` FROM `individual_columns` where `Individual Columns ID` = '{}'".format(individual_columns_id)
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchone()

    return data[0]

def create_individual_columns(individual_columns_name,column_name_list,data_type_list,option_list,instructions_list):
    update_dateime = datetime.now()
    individual_columns_id = str(update_dateime.strftime("%Y-%m-%d %H%M%S"))

    data_list = [[column_name_list[i],data_type_list[i],option_list[i],instructions_list[i]] for i in range(0,len(column_name_list))]
    data_df = pd.DataFrame(data_list,columns=["Column Name","Data Type","Option","Instructions"])
    data_df.fillna("",inplace=True)
    data_str = data_df.to_json(orient="split")

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "REPLACE INTO individual_columns (`Individual Columns ID`,`Individual Columns Name`,`Data`) VALUES (%s,%s,%s)"
    k = cursor.executemany(sql, [[individual_columns_id,individual_columns_name,data_str]])
    db.commit()
    db.close()

def edit_individual_columns_name(original_individual_columns_name,edit_individual_columns_name):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update individual_columns Set `Individual Columns Name` = '{}' Where " \
          "`Individual Columns Name` = '{}'".format(edit_individual_columns_name,original_individual_columns_name)
    cursor.execute(sql)
    db.commit()
    db.close()

def edit_individual_columns_row(individual_columns_name, individual_columns_data):
    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update individual_columns Set `Data` = '{}' Where `Individual Columns Name` = '{}'".format(individual_columns_data, individual_columns_name)
    cursor.execute(sql)
    db.commit()
    db.close()

##############################################################################################################################

# Function

def get_function_dict():
    function_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT * FROM `setting_function`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        function_dict[i[1]] = [i[2], i[3], i[4], i[5]]

    return function_dict

def get_function_data_by_id(function_id):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT * FROM `setting_function` where `Function ID` = '{}'".format(function_id)
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchone()

    return list(data)

def get_function_name_to_id_dict():
    function_name_to_id_dict = {}
    function_id_to_name_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Function ID`,`Function Name` FROM `setting_function`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        function_name_to_id_dict[i[1]] = i[0]
        function_id_to_name_dict[i[0]] = i[1]

    return function_name_to_id_dict, function_id_to_name_dict

def create_function(function_name,attachment,verification_code,send_internal_mail,send_supplier_mail):
    update_dateime = datetime.now()
    function_id = str(update_dateime.strftime("%Y-%m-%d %H%M%S"))

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "REPLACE INTO setting_function (`Function ID`,`Function Name`,`Attachment`,`Verification Code`,`Send Internal Mail`,`Send Supplier Mail`) VALUES (%s,%s,%s,%s,%s,%s)"
    k = cursor.executemany(sql, [[function_id,function_name,attachment,verification_code,send_internal_mail,send_supplier_mail]])
    db.commit()
    db.close()

def edit_function_name(original_function_name,edit_function_name):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update setting_function Set `Function Name` = '{}' Where " \
          "`Function Name` = '{}'".format(edit_function_name,original_function_name)
    cursor.execute(sql)
    db.commit()
    db.close()

def edit_function_row(function_name,attachment,verification_code,send_internal_mail,send_supplier_mail):
    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update setting_function Set `Attachment` = '{}'," \
          " `Verification Code` = '{}', `Send Internal Mail` = '{}'," \
          " `Send Supplier Mail` = '{}' Where `Function Name` = '{}'".format(attachment,verification_code,send_internal_mail,send_supplier_mail,function_name)
    cursor.execute(sql)
    db.commit()
    db.close()

##############################################################################################################################

# Verification Code

def get_verification_code_dict():
    verification_code_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT * FROM `verification_code`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        verification_code_dict[i[1]] = i[2]

    return verification_code_dict

def get_verification_code_name_to_id_dict():
    verification_code_name_to_id_dict = {}
    verification_code_id_to_name_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Verification Code ID`,`Verification Code Name` FROM `verification_code`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        verification_code_name_to_id_dict[i[1]] = i[0]
        verification_code_id_to_name_dict[i[0]] = i[1]

    return verification_code_name_to_id_dict, verification_code_id_to_name_dict

def get_verification_code_by_id(verification_code_id):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Data` FROM `verification_code` where `Verification Code ID` = '{}'".format(verification_code_id)
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchone()

    return data[0]

def create_verification_code(verification_code_name,name_list,code_list):
    update_dateime = datetime.now()
    verification_code_id = str(update_dateime.strftime("%Y-%m-%d %H%M%S"))

    data_list = [[name_list[i],code_list[i]] for i in range(0,len(name_list))]
    data_df = pd.DataFrame(data_list,columns=["Name","Code"])
    data_df.fillna("",inplace=True)
    data_str = data_df.to_json(orient="split")

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "REPLACE INTO verification_code (`Verification Code ID`,`Verification Code Name`,`Data`) VALUES (%s,%s,%s)"
    k = cursor.executemany(sql, [[verification_code_id,verification_code_name,data_str]])
    db.commit()
    db.close()

def edit_verification_code_name(original_verification_code_name,edit_verification_codename):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update verification_code Set `Verification Code Name` = '{}' Where " \
          "`Verification Code Name` = '{}'".format(edit_verification_codename,original_verification_code_name)
    cursor.execute(sql)
    db.commit()
    db.close()

def edit_verification_code_row(verification_code_name, verification_code_data):
    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update verification_code Set `Data` = '{}' Where `Verification Code Name` = '{}'".format(verification_code_data, verification_code_name)
    cursor.execute(sql)
    db.commit()
    db.close()

##############################################################################################################################

# Internal Mail Receipients

def get_internal_mail_receipients_dict():
    internal_mail_receipients_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT * FROM `internal_mail_receipients`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        internal_mail_receipients_dict[i[1]] = i[2]

    return internal_mail_receipients_dict

def get_internal_mail_receipients_name_to_id_dict():
    internal_mail_receipients_name_to_id_dict = {}
    internal_mail_receipients_id_to_name_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Internal Mail Receipients ID`,`Internal Mail Receipients Name` FROM `internal_mail_receipients`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        internal_mail_receipients_name_to_id_dict[i[1]] = i[0]
        internal_mail_receipients_id_to_name_dict[i[0]] = i[1]

    return internal_mail_receipients_name_to_id_dict, internal_mail_receipients_id_to_name_dict

def get_internal_mail_receipients_by_id(internal_mail_receipients_id):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Data` FROM `internal_mail_receipients` where `Internal Mail Receipients ID` = '{}'".format(internal_mail_receipients_id)
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchone()

    return data[0]

def create_internal_mail_receipients(internal_mail_receipients_name,mail_list,subject_list):
    update_dateime = datetime.now()
    internal_mail_receipients_id = str(update_dateime.strftime("%Y-%m-%d %H%M%S"))

    data_list = [[mail_list[i],subject_list[i]] for i in range(0,len(mail_list))]
    data_df = pd.DataFrame(data_list,columns=["Mail","Subject"])
    data_df.fillna("",inplace=True)
    data_str = data_df.to_json(orient="split")

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "REPLACE INTO internal_mail_receipients (`Internal Mail Receipients ID`,`Internal Mail Receipients Name`,`Data`) VALUES (%s,%s,%s)"
    k = cursor.executemany(sql, [[internal_mail_receipients_id,internal_mail_receipients_name,data_str]])
    db.commit()
    db.close()

def edit_internal_mail_receipients_name(original_internal_mail_receipients_name,edit_internal_mail_receipients_name):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update internal_mail_receipients Set `Internal Mail Receipients Name` = '{}' Where " \
          "`Internal Mail Receipients Name` = '{}'".format(edit_internal_mail_receipients_name,original_internal_mail_receipients_name)
    cursor.execute(sql)
    db.commit()
    db.close()

def edit_internal_mail_receipients_row(internal_mail_receipients_name, internal_mail_receipients_data):
    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update internal_mail_receipients Set `Data` = '{}' Where `Internal Mail Receipients Name` = '{}'".format(internal_mail_receipients_data, internal_mail_receipients_name)
    cursor.execute(sql)
    db.commit()
    db.close()

##############################################################################################################################

# Supplier Mail Setting

def get_supplier_mail_setting_dict():
    supplier_mail_setting_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT * FROM `supplier_mail_setting`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        supplier_mail_setting_dict[i[1]] = [i[2], i[3]]

    return supplier_mail_setting_dict

def get_supplier_mail_setting_name_to_id_dict():
    supplier_mail_setting_name_to_id_dict = {}
    supplier_mail_setting_id_to_name_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Supplier Mail Setting ID`,`Supplier Mail Setting Name` FROM `supplier_mail_setting`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        supplier_mail_setting_name_to_id_dict[i[1]] = i[0]
        supplier_mail_setting_id_to_name_dict[i[0]] = i[1]

    return supplier_mail_setting_name_to_id_dict, supplier_mail_setting_id_to_name_dict

def get_supplier_mail_setting_by_id(supplier_mail_setting_id):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Subject`,`Content` FROM `supplier_mail_setting` where `Supplier Mail Setting ID` = '{}'".format(supplier_mail_setting_id)
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchone()

    return list(data)

def create_supplier_mail_setting(supplier_mail_setting_name,subject,content):
    update_dateime = datetime.now()
    supplier_mail_settingid = str(update_dateime.strftime("%Y-%m-%d %H%M%S"))

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "REPLACE INTO supplier_mail_setting (`Supplier Mail Setting ID`,`Supplier Mail Setting Name`,`Subject`,`Content`) VALUES (%s,%s,%s,%s)"
    k = cursor.executemany(sql, [[supplier_mail_settingid,supplier_mail_setting_name,subject,content]])
    db.commit()
    db.close()

def edit_supplier_mail_setting_name(original_supplier_mail_setting_name,edit_supplier_mail_setting_name):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update supplier_mail_setting Set `Supplier Mail Setting Name` = '{}' Where " \
          "`Supplier Mail Setting Name` = '{}'".format(edit_supplier_mail_setting_name,original_supplier_mail_setting_name)
    cursor.execute(sql)
    db.commit()
    db.close()

def edit_supplier_mail_setting_row(supplier_mail_setting_name,subject,content):
    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update supplier_mail_setting Set `Subject` = '{}'," \
          " `Content` = '{}', Where `Supplier Mail Setting Name` = '{}'".format(subject,content,supplier_mail_setting_name)
    cursor.execute(sql)
    db.commit()
    db.close()

##############################################################################################################################

# Check

def get_check_dict():
    check_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT * FROM `setting_check`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        check_dict[i[1]] = i[2]

    return check_dict

def get_check_name_to_id_dict():
    check_name_to_id_dict = {}
    check_id_to_name_dict = {}

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Check ID`,`Check Name` FROM `setting_check`"
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        check_name_to_id_dict[i[1]] = i[0]
        check_id_to_name_dict[i[0]] = i[1]

    return check_name_to_id_dict, check_id_to_name_dict

def get_check_by_id(check_id):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Data` FROM `setting_check` where `Check ID` = '{}'".format(check_id)
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchone()

    return data[0]

def create_check(check_name,check_column_list,formula_list,equal_column_list):
    update_dateime = datetime.now()
    check_id = str(update_dateime.strftime("%Y-%m-%d %H%M%S"))

    data_list = [[check_column_list[i],formula_list[i],equal_column_list[i]] for i in range(0,len(check_column_list))]
    data_df = pd.DataFrame(data_list,columns=["Check Column","Formula","Equal Column"])
    data_df.fillna("",inplace=True)
    data_str = data_df.to_json(orient="split")

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "REPLACE INTO setting_check (`Check ID`,`Check Name`,`Data`) VALUES (%s,%s,%s)"
    k = cursor.executemany(sql, [[check_id,check_name,data_str]])
    db.commit()
    db.close()

def edit_check_name(original_check_name,edit_check_name):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update setting_check Set `Check Name` = '{}' Where " \
          "`Check Name` = '{}'".format(edit_check_name,original_check_name)
    cursor.execute(sql)
    db.commit()
    db.close()

def edit_check_row(check_name, check_data):
    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "Update setting_check Set `Data` = '{}' Where `Check Name` = '{}'".format(check_data, check_name)
    cursor.execute(sql)
    db.commit()
    db.close()

##############################################################################################################################

# Save
def upload_temp_row(project_id,name,verification_code,data):
    update_dateime = datetime.now()
    temp_id = str(update_dateime.strftime("%Y-%m-%d %H%M%S"))

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "REPLACE INTO procurement_temp (`Temp ID`,`Project ID`,`Name`,`Verification Code`,`Data`,`Update DateTime`) VALUES (%s,%s,%s,%s,%s,%s)"
    k = cursor.executemany(sql, [[temp_id, project_id, name, verification_code,data,update_dateime]])
    db.commit()
    db.close()

def upload_results_table(project_id,name,verification_code,data):
    update_dateime = datetime.now()
    results_id = str(update_dateime.strftime("%Y-%m-%d %H%M%S"))

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    cursor = db.cursor()
    sql = "REPLACE INTO procurement_results (`Results ID`,`Project ID`,`Name`,`Verification Code`,`Data`,`Update DateTime`) VALUES (%s,%s,%s,%s,%s,%s)"
    k = cursor.executemany(sql, [[results_id, project_id, name, verification_code, data, update_dateime]])
    db.commit()
    db.close()

##############################################################################################################################

# Load

def get_temp_row(project_id,name,verification_code):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Data` from `procurement_temp` where `Project ID` = '{}' and `Name` = '{}' and `Verification Code` = '{}' order by `Update DateTime` Desc".format(project_id,name,verification_code)
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchone()

    if data == None:
        return ""
    else:
        return data[0]

def get_results_row(project_id,name,verification_code):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Data` from `procurement_results` where `Project ID` = '{}' and `Name` = '{}' and `Verification Code` = '{}' order by `Update DateTime` Desc".format(project_id,name,verification_code)
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchone()

    if data == ():
        return ""
    else:
        return data[0]

def get_results_by_project(project_id):

    db = pymysql.connect(host=v.mysql_host, port=v.mysql_port, user=v.mysql_user, password=v.mysql_password, database=v.db_name)
    sql = "SELECT `Name`,`Verification Code`,`Data`,`Update DateTime` from `procurement_results` where `Project ID` = '{}' order by `Update DateTime` Desc".format(project_id)
    cursor = db.cursor()
    k = cursor.execute(sql)
    data = cursor.fetchall()

    data_df = pd.DataFrame(data,columns=["Name","Verification Code","Data","Update DateTime"])

    return data_df
##############################################################################################################################

# Send Mail

def send_internal_mail(df,internal_mail_receipients_df):


    for i in range(0,len(internal_mail_receipients_df)):

        server = smtplib.SMTP(v.smtp_server, v.port)

        try:
            # 建立連線
            context = ssl.create_default_context()

            receivers = internal_mail_receipients_df.loc[i,"Mail"]
            subject = internal_mail_receipients_df.loc[i,"Subject"]


            # 調整Subject
            for col in df.columns:
                if "[["+col+"]]" in subject:
                    subject = subject.replace("[["+col+"]]",df[col].values[0])

            # 建立內文，夾帶附件用MIMEMultipart()
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['FROM'] = v.sender
            msg['To'] = receivers

            # 建立內文文字
            att2 = MIMEText(subject)
            msg.attach(att2)

            server.starttls(context=context)
            server.login(v.mail_user, v.mail_password)
            server.sendmail(v.sender, receivers, msg.as_string())

        except Exception as e:
            print(e)
            print("Mail Error Internal")
        finally:
            server.quit()

def send_supplyer_mail(df,subject,content):

    supplier_mail_list = [df[col].values[0] for col in df.columns if "mail" in str(col.lower())]

    server = smtplib.SMTP(v.smtp_server, v.port)

    try:
        # 建立連線
        context = ssl.create_default_context()

        receivers = supplier_mail_list[0]

        # 調整Subject
        for col in df.columns:
            if "[[" + col + "]]" in subject:
                subject = subject.replace("[[" + col + "]]", df[col].values[0])

        # 建立內文，夾帶附件用MIMEMultipart()
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['FROM'] = v.sender
        msg['To'] = receivers

        # 建立內文文字
        att2 = MIMEText(content)
        msg.attach(att2)

        server = smtplib.SMTP(v.smtp_server, v.port)
        server.starttls(context=context)
        server.login(v.mail_user, v.mail_password)
        server.sendmail(v.sender, receivers, msg.as_string())

    except Exception as e:
        print(e)
        print("Mail Error Supplyer")
    finally:
        server.quit()