import os
import re

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

for x in result[2:]:
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
