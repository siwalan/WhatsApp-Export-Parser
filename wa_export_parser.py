import os
import re
import pandas as pd

for file in os.listdir():
    if file.endswith(".txt"):
        text_file = file
        
chat_with = text_file.partition("WhatsApp Chat with ")[2].partition(".txt")[0]
text_file_open= open(text_file,'r')
data=text_file_open.read().replace("\n", " ")
data = re.sub(r'(([0-9]|[0-9]{2})\/([0-9]|[0-9]{2})\/([0-9]{2}|[0-9]{4}), [0-9]{2}:[0-9]{2})', r'\n\g<1>' , data)
line_by_line = [x.strip() for x in data.split('\n')]

column_names = ["Date", "Hour", "User","Message", "File"]
message_df = pd.DataFrame(columns = column_names)

for x in line_by_line[2:]:
    pattern = r'(((([0-9]|[0-9]{2})\/([0-9]|[0-9]{2})\/([0-9]{2}|[0-9]{4})), ([0-9]{2}:[0-9]{2}) (-) )(.*?):(.*?)$)'
    message = x
    regex_list = re.findall(pattern,x)
    message_Date = regex_list[0][2]
    message_Time = regex_list[0][6]
    message_User_Name = regex_list[0][8]
    message_Content = regex_list[0][9]
    pattern_file = r"(.*?)(\(file attached\))"
    isFile = False
    if (re.findall(pattern_file,message_Content)) != []:
        # Is not chat, but rather a message
        message_Content = re.findall(pattern_file,message_Content)[0][0]
        isFile=True
        
    message_df = message_df.append({'Date': message_Date, 'Hour': message_Time, 'User': message_User_Name, 'Message':message_Content, "File": isFile}, ignore_index=True)

image_fn = lambda x: "<img src='{}'; style='max-width:30%; max-height:30%;''>".format(x) if (x.endswith((".jpg",".png"))) else x
pdf_fn = lambda x: "<a href='{}'>".format(x)+x+"</a>" if (x.endswith('.pdf')) else x

message_df.Message = message_df.Message.str.strip()

message_df['Message'] = message_df['Message'].apply(image_fn).apply(pdf_fn)

user_number = len(message_df['User'].unique())
user_conversation_list = ""
first = True
for user in message_df['User'].unique():
    if (user_number > 1) and (first == False) :
        user_conversation_list = user_conversation_list + " , " + user 
    elif (user_number > 1):
        user_conversation_list = user_conversation_list + user
        first = False
    else:
        user_conversation_list = user_conversation_list + " & " + user
    user_number = user_number - 1

html_header= """ 
<!DOCTYPE html>
<html>

<head>
    <title>Message WhatsApp {}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">


    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>


    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.css">
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.js"></script>
</head>

<body>
<div class ="container">
<div class="row">
<div class="col">

<h1> WhatsApp Conversation "{}""</h1>

""".format(user_conversation_list, user_conversation_list)

html_footer= """
</div>
</div>
</div>
</body>
<script>
$(document).ready( function () {
    $('#data_table').DataTable();
} );
</script>
</html>
"""

html = html_header +message_df.drop('File', axis=1).to_html(classes='cell-border compact stripe " id="data_table" style="overflow-x:auto;', escape=False) + html_footer

Html_file= open("chat_wa_index.html","w")
Html_file.write(html)
Html_file.close()
