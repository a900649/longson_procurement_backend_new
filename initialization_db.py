import pymysql
import variable as v
from datetime import datetime

def create_db():
    # 建立DB
    db = pymysql.connect(host=v.mysql_host,port=v.mysql_port,user=v.mysql_user,password=v.mysql_password)
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(v.db_name))
    db.close()

def create_project_table():

    db = pymysql.connect(host=v.mysql_host,port=v.mysql_port,user=v.mysql_user,password=v.mysql_password,database=v.db_name)
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS project (
    `Project ID` VARCHAR(200), 
    `Project Name` VARCHAR(500), 
    `Title` VARCHAR(300), 
    `Requirements Introduction` VARCHAR(300), 
    `Common Columns` VARCHAR(300), 
    `Individual Columns` VARCHAR(300), 
    `Function` VARCHAR(300), 
    `Verification Code` VARCHAR(300), 
    `Internal Mail Receipients` VARCHAR(300), 
    `Supplier Mail Setting` VARCHAR(300), 
    `Check` VARCHAR(300), 
    `Start` VARCHAR(100), 
    PRIMARY KEY (`Project ID`,`Project Name`))"""
    cursor.execute(sql)
    db.close()

def create_title_table():

    db = pymysql.connect(host=v.mysql_host,port=v.mysql_port,user=v.mysql_user,password=v.mysql_password,database=v.db_name)
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS title (
    `Title ID` VARCHAR(200), 
    `Title Name` VARCHAR(500), 
    `Title Row 1` VARCHAR(500), 
    `Title Row 2` VARCHAR(500), 
    `Title Row 3` VARCHAR(500), 
    `Title Row 4` VARCHAR(500), 
    `Title Row 5` VARCHAR(500), 
    PRIMARY KEY (`Title ID`,`Title Name`))"""
    cursor.execute(sql)
    db.close()

def create_requirements_introduction_table():

    db = pymysql.connect(host=v.mysql_host,port=v.mysql_port,user=v.mysql_user,password=v.mysql_password,database=v.db_name)
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS requirements_introduction (
    `Requirements Introduction ID` VARCHAR(200), 
    `Requirements Introduction Name` VARCHAR(500),
    `Product 1` VARCHAR(500), 
    `Introduction 1` LONGTEXT, 
    `Product 2` VARCHAR(500), 
    `Introduction 2` LONGTEXT, 
    `Product 3` VARCHAR(500), 
    `Introduction 3` LONGTEXT, 
    `Product 4` VARCHAR(500), 
    `Introduction 4` LONGTEXT, 
    `Product 5` VARCHAR(500), 
    `Introduction 5` LONGTEXT, 
    PRIMARY KEY (`Requirements Introduction ID`,`Requirements Introduction Name`))"""
    cursor.execute(sql)
    db.close()

def create_common_columns_table():

    db = pymysql.connect(host=v.mysql_host,port=v.mysql_port,user=v.mysql_user,password=v.mysql_password,database=v.db_name)
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS common_columns (
    `Common Columns ID` VARCHAR(200), 
    `Common Columns Name` VARCHAR(500),
    `Data` LONGTEXT, 
    PRIMARY KEY (`Common Columns ID`,`Common Columns Name`))"""
    cursor.execute(sql)
    db.close()

def create_individual_columns_table():

    db = pymysql.connect(host=v.mysql_host,port=v.mysql_port,user=v.mysql_user,password=v.mysql_password,database=v.db_name)
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS individual_columns (
    `Individual Columns ID` VARCHAR(200), 
    `Individual Columns Name` VARCHAR(500),
    `Data` LONGTEXT, 
    PRIMARY KEY (`Individual Columns ID`,`Individual Columns Name`))"""
    cursor.execute(sql)
    db.close()

def create_function_table():

    db = pymysql.connect(host=v.mysql_host,port=v.mysql_port,user=v.mysql_user,password=v.mysql_password,database=v.db_name)
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS setting_function (
    `Function ID` VARCHAR(200), 
    `Function Name` VARCHAR(500),
    `Attachment` VARCHAR(100),
    `Verification Code` VARCHAR(100),
    `Send Internal Mail` VARCHAR(100),
    `Send Supplier Mail` VARCHAR(100),
    PRIMARY KEY (`Function ID`,`Function Name`))"""
    cursor.execute(sql)
    db.close()

def create_verification_code_table():

    db = pymysql.connect(host=v.mysql_host,port=v.mysql_port,user=v.mysql_user,password=v.mysql_password,database=v.db_name)
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS verification_code (
    `Verification Code ID` VARCHAR(200), 
    `Verification Code Name` VARCHAR(500),
    `Data` LONGTEXT, 
    PRIMARY KEY (`Verification Code ID`,`Verification Code Name`))"""
    cursor.execute(sql)
    db.close()

def create_internal_mail_receipients_table():

    db = pymysql.connect(host=v.mysql_host,port=v.mysql_port,user=v.mysql_user,password=v.mysql_password,database=v.db_name)
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS internal_mail_receipients (
    `Internal Mail Receipients ID` VARCHAR(200), 
    `Internal Mail Receipients Name` VARCHAR(500),
    `Data` LONGTEXT, 
    PRIMARY KEY (`Internal Mail Receipients ID`,`Internal Mail Receipients Name`))"""
    cursor.execute(sql)
    db.close()

def create_supplier_mail_setting_table():

    db = pymysql.connect(host=v.mysql_host,port=v.mysql_port,user=v.mysql_user,password=v.mysql_password,database=v.db_name)
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS supplier_mail_setting (
    `Supplier Mail Setting ID` VARCHAR(200), 
    `Supplier Mail Setting Name` VARCHAR(500),
    `Subject` VARCHAR(500),
    `Content` LONGTEXT,
    PRIMARY KEY (`Supplier Mail Setting ID`,`Supplier Mail Setting Name`))"""
    cursor.execute(sql)
    db.close()

def create_check_table():

    db = pymysql.connect(host=v.mysql_host,port=v.mysql_port,user=v.mysql_user,password=v.mysql_password,database=v.db_name)
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS setting_check (
    `Check ID` VARCHAR(200), 
    `Check Name` VARCHAR(500),
    `Data` LONGTEXT, 
    PRIMARY KEY (`Check ID`,`Check Name`))"""
    cursor.execute(sql)
    db.close()

def create_results_table():

    db = pymysql.connect(host=v.mysql_host,port=v.mysql_port,user=v.mysql_user,password=v.mysql_password,database=v.db_name)
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS procurement_results (
    `Results ID` VARCHAR(200), 
    `Project ID` VARCHAR(200), 
    `Name` VARCHAR(500), 
    `Verification Code` VARCHAR(500), 
    `Data` LONGTEXT, 
    `Update DateTime` DateTime,
    PRIMARY KEY (`Results ID`))"""
    cursor.execute(sql)
    db.close()

def create_temp_table():

    db = pymysql.connect(host=v.mysql_host,port=v.mysql_port,user=v.mysql_user,password=v.mysql_password,database=v.db_name)
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS procurement_temp (
    `Temp ID` VARCHAR(200), 
    `Project ID` VARCHAR(200), 
    `Name` VARCHAR(500), 
    `Verification Code` VARCHAR(500), 
    `Data` LONGTEXT, 
    `Update DateTime` DateTime,
    PRIMARY KEY (`Temp ID`))"""
    cursor.execute(sql)
    db.close()