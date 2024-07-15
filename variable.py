

# 圖片
logo_path = 'System Photo/Longson.jpg'
icon_path = 'System Photo/Smile.webp'
form_tail_path = 'System Photo/Thanks.jpg'

# DB 資訊
mysql_host = "longson.mysql.database.azure.com"
mysql_user='paul'
mysql_password='Yunxuan123'
mysql_port = 3306
db_name = "longson_procurement"

# BLOB
blob_connection_string = "DefaultEndpointsProtocol=https;AccountName=kenso;AccountKey=Wto5Ig361Z/aVQuxEfvM7b9MnKi3IctRB70fq5X53CCLlQ84BpFaS9T5HWVLcFwOVSEcljz0Aa40+AStQgHifw==;EndpointSuffix=core.windows.net"
blob_container = "longson"

# Aaron給的Mail
smtp_server = "smtp.office365.com"
port = 587
sender = "longsonprocure@outlook.com"
mail_user = "longsonprocure@outlook.com"
mail_password = "Yunxuan123"

version = "Version 2.00000"

# 網頁Title
page_title = "Longson Procurement System"

# Results Other Columns
first_col = [["RowID","Text"],["Product","Text"]]
last_col = [["Attachment","Text"],["Update DateTime","DateTime"],["Verification Code","Text"],["Verification Code Name","Text"]]

# 附件存放路徑
attachment_path = "Attachment" + "/{}" + "/{}" + "/{}"