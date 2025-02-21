import time
import streamlit as st
import spacy
spacy.load('en_core_web_sm')

import pandas as pd
import time, datetime
from pyresparser import ResumeParser
# from resume_parser import resumeparse
from streamlit_tags import st_tags
from PIL import Image
# import pymysql
import mysql.connector
import plotly.express as px
from plotly import optional_imports
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(to_email, subject, message):
    try:
        # Define the sender's email and password
        sender_email = "smarthiringsystem2024@gmail.com"    # "20hritikdey@gmail.com"
        sender_password = "ngpx aerc otlw vxxj"  # Store this securely in practice "ewfb zfri yufy mzfv"
        
        # Setup the MIME
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add body to email
        msg.attach(MIMEText(message, 'plain'))

        # Create server object with Gmail's SMTP server details
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security
        server.login(sender_email, sender_password)

        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)

        # Close the server connection
        server.quit()

    except Exception as e:
        print(f'Error sending email: {e}')



page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://i.imghippo.com/files/5UcL11724915435.png");

background-position: center center;

/* Make image fixed */
background-attachment: fixed;

/* Not repeat images */
background-repeat: no-repeat;

/* Set background size auto */
background-size: 100%;
}}



[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


# connection = pymysql.connect(host='localhost', user='root', password='')
connection = mysql.connector.connect(host='sql12.freesqldatabase.com', user='sql12763883', password='UbNkeHVXWh',database='sql12763883')
cursor = connection.cursor()

def insert_data(name, email, timestamp, exp, skills,count,Resume):
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (name, email, timestamp, str(exp), skills,count,Resume)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

# def insert_com_data(cid,name,password):
#     DB_table_name = 'com_data'
#     insert_sql = "insert into " + DB_table_name + """
#     values (%s,%s,%s)"""
#     rec_values = (cid,name,password)
#     cursor.execute(insert_sql, rec_values)
#     connection.commit()

def insert_com_data(name, password):
    DB_table_name = 'com_data'
    insert_sql = "insert into " + DB_table_name + """
    (Name, password) values (%s,%s)"""
    rec_values = (name, password)
    cursor.execute(insert_sql, rec_values)
    connection.commit()
    return cursor.lastrowid  # Return the auto-generated cid


def insert_recruit_data(cid,domain,reco_skill,timestamp,experience):
    DB_table_name = 'recruit_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s)"""
    rec_values = (cid,domain,reco_skill,timestamp,experience)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

def fetch_previous_recruitments(cid):
    query = "SELECT * FROM recruit_data WHERE cid = %s"
    cursor.execute(query, (cid,))
    return cursor.fetchall()

# def delete_data(email):
#     DB_table_name = 'user_data12'
#     delete_sql = f"DELETE FROM {DB_table_name} WHERE email_id = %s"
#     cursor.execute(delete_sql, (email,))
#     connection.commit()
def update_data(email, a,b,c,d):
    DB_table_name = 'user_data'
    update_sql = f"UPDATE {DB_table_name} SET timestamp = %s, experience = %s, actual_skills = %s, resume = %s WHERE email_id = %s"
    cursor.execute(update_sql, (a,b,c,d, email))
    connection.commit()

# def fetch_resume(email):
#     query = "SELECT Resume FROM user_data12 WHERE Email_ID = %s"
#     cursor.execute(query, (email,))
#     return cursor.fetchone()

def run():

    original_title ='''<p style="font-size: 50px; font-weight: bold;color: #333; 
    text-shadow: 
        1px 1px 0px #eab,  /* Top-left shadow (light) */
        2px 2px 0px #ccc,  /* Middle-left shadow */
        3px 3px 0px #999;  /* Bottom-left shadow (dark) */
    font-family: Times new roman;"><b>SMART HIRING SYSTEM</b></p>'''
    st.markdown(original_title, unsafe_allow_html=True)

    # st.title(":green[Smart Resume Screening]")
    st.sidebar.markdown("### **Choose User**")
    activities = ["User 🧑🏻‍💻", "Admin 👤","Company 🏢"]
    choice = st.sidebar.selectbox("**Choose among the given options:**", activities)

    # Create the DB
    # db_sql = """CREATE DATABASE IF NOT EXISTS SRA3;"""
    # cursor.execute(db_sql)
    # connection.select_db("sra4")

    # Create table
    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(100) NOT NULL,
                     Email_ID VARCHAR(50) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Experience VARCHAR(10) NOT NULL,
                     Actual_skills VARCHAR(700) NOT NULL,
                     Count INT(5) NOT NULL,
                     Resume LONGBLOB NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)

    if choice == 'User 🧑🏻‍💻':

        
            original_title1 ='''<p style="font-size: 18px; border: 1px double #ed3939;border-radius: 10px; padding: 10px; display: inline-block; background-color: #fdcab82f;
            box-shadow: 
        5px 5px 0px #eab, /* Shadow to simulate depth */
        8px 8px 15px #999;"><i><b>Welcome to User Side<i></b></p>'''
            st.markdown(original_title1, unsafe_allow_html=True)
            

            try:
                pdf_file = st.file_uploader("**Choose your Resume**", type=["pdf"])
                if st.button("Submit Resume", type="primary"):
                    if pdf_file is not None:
                        # save_image_path = './Uploaded_Resumes/' + pdf_file.name
                        # with open(save_image_path, "wb") as f:
                        #     f.write(pdf_file.getbuffer())
                        resume_binary = pdf_file.read()  # Read the PDF file content
                        resume_data = ResumeParser(pdf_file).get_extracted_data()
                        # data2 = resumeparse.read_file(save_image_path)
                        # text = extract_text(save_image_path)
                        # st.text(text)
                        if resume_data:
                            with st.spinner('Wait for it...'):
                                time.sleep(2)
                            try:
                                st.subheader("**Resume Analysis:**")
                                st.success("**_Congratulations " + resume_data['name'] + ' 🎉. Your Resume has been Submitted._**')
                                
                                st.subheader("**Candidates Basic Information:**")
                                st.text('Name: ' + resume_data['name'])
                                st.text('Email: ' + resume_data['email'])
                                # st.text('Resume pages: ' + str(resume_data['no_of_pages']))
                                st.text('Experience: ' + str(resume_data['total_experience']))
                                # raise ValueError("There is an error parsing the resume")
                            except ValueError:
                                st.error("**⚠ An unexpected ERROR occurred during resume processing.**")
                            # except Exception as e:
                            #     st.error("An unexpected error occurred during resume processing.")

                            ts = time.time()
                            cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                            cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            timestamp = str(cur_date + '_' + cur_time)

                            st.balloons()

                            # delete_data(resume_data['email'])

                            sql = "SELECT email_id FROM user_data"
                            cursor.execute(sql)
                            result = cursor.fetchall()
                            # print(result)
                            email_list = [email[0] for email in result]
                            a=resume_data['email']
                            if a in email_list:
                                update_data(resume_data['email'], timestamp,
                                str(resume_data['total_experience']), str(resume_data['skills']),resume_binary)
                            # delete_data(resume_data['email'])
                            else:
                                insert_data(resume_data['name'], resume_data['email'], timestamp,
                                    str(resume_data['total_experience']), str(resume_data['skills']),0,resume_binary)

                            connection.commit()

                        else:
                            st.error("**:red[⚠ sometimes went wrong.....]**")
                    else:
                        st.warning('**:red[⚠ Warning message]**')
                        st.error("**_:red[Please Upload Your Resume]_**")
            except Exception:
                st.error("**⚠ An unexpected ERROR occurred during resume processing.**")


    elif choice=='Admin 👤':
        try:
            original_title1 ='''<p style="font-size: 18px; border: 1px double #ed3939;border-radius: 10px; padding: 10px; display: inline-block; background-color: #fdcab82f;
            box-shadow: 
        5px 5px 0px #eab, /* Shadow to simulate depth */
        8px 8px 15px #999;"><i><b>Welcome to Admin Side<i></b></p>'''
            st.markdown(original_title1, unsafe_allow_html=True)

            # st.header(":blue[Welcome to Admin Side]")
            admin_user=st.text_input("**:orange[Username]**")
            admin_password=st.text_input("**:orange[Password]**",type='password')
            loadnow11=st.button("login",type="primary")
            #initialize session state
            if "loadnow11_state" not in st.session_state:
                st.session_state.loadnow11_state= False
            if loadnow11 or st.session_state.loadnow11_state:
                st.session_state.loadnow11_state=True
                with st.spinner(':blue[Wait for it...]'):
                    time.sleep(2)
                if admin_user=='admin' and admin_password=='admin123':
                    st.success("##### **_:blue[Welcome Admin]_**")

                    cursor.execute('''SELECT ID,Name,Email_ID,Timestamp,Experience,Actual_skills FROM user_data''')
                    data = cursor.fetchall()
                    st.header("**User's Data**")
                    df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Timestamp', 'Experience', 'Actual Skills'])
                    # df_filtered = df.drop(columns=['Count'])
                    st.dataframe(df)

                    cursor.execute('''SELECT*FROM com_data''')
                    data1 = cursor.fetchall()
                    st.header("**Company's Data**")
                    df = pd.DataFrame(data1, columns=['CID', 'CName', 'Password'])
                    st.dataframe(df)

                    c_id=st.text_input("**Enter Company ID for Show company's Previous Posts:**")
                    loadnow1=st.button("Show Previous Posts",type="primary")
                    #initialize session state
                    if "loadnow1_state" not in st.session_state:
                        st.session_state.loadnow1_state= False
                    if loadnow1 or st.session_state.loadnow1_state:
                        st.session_state.loadnow1_state=True
                        if c_id.isdigit():
                            c_id=int(c_id)
                            cursor.execute(f"SELECT * FROM com_data WHERE cid = %s", (c_id,))
                            company_exists1 = cursor.fetchone()
                            if company_exists1:
                                st.subheader(f"Previous recruitments for {c_id}:")
                                recruitments = fetch_previous_recruitments(c_id)
                                if recruitments:
                                    # st.success(f"Previous recruitments for {c_id}:")
                                    recruit_df = pd.DataFrame(recruitments, columns=['RID', 'CID', 'Domain', 'Reco_Skills', 'Timestamp', 'Experience'])
                                    st.dataframe(recruit_df)
                                else:
                                    
                                    st.info(f"**No previous recruitment posts for {c_id}.**")
                            else:
                                st.error("There is no such ID exists.")

                else:
                    st.error("**_:red[Wrong ID or Password is Provided]_**")

        except Exception as main_error:
            st.error(f"**⚠ An unexpected error occurred: {main_error}**")

    else:
        try:
            original_title1 ='''<p style="font-size: 18px; border: 1px double #ed3939;border-radius: 10px; padding: 10px; display: inline-block; background-color: #fdcab82f;
            box-shadow: 
        5px 5px 0px #eab, /* Shadow to simulate depth */
        8px 8px 15px #999;"><i><b>Welcome to Company Side<i></b></p>'''
            st.markdown(original_title1, unsafe_allow_html=True)

            activities1 = ["Sign in", "Sign up"]
            choice1 = st.selectbox("**Choose among the given options:**", activities1)
            DB_table_name1 = 'com_data'
            table_sql1 = "CREATE TABLE IF NOT EXISTS " + DB_table_name1 + """
                        (cid INT NOT NULL AUTO_INCREMENT,
                        Name varchar(100) NOT NULL UNIQUE,
                        password VARCHAR(50) NOT NULL,
                        PRIMARY KEY (cid)) AUTO_INCREMENT=101;
                        """
            cursor.execute(table_sql1)

            if choice1=='Sign up':
                name=st.text_input("**Company_name**")
                password=st.text_input("**Company_password**")

                if st.button("Create Profile", type="primary"):
                    # # insert_com_data(cid,name,password)
                    # new_cid = insert_com_data(name, password)
                    # st.success(f":blue[Your profile is created. Your company ID is {new_cid}]")
                    # # connection.commit()
                    # # st.success(":blue[your profile is created]")
                    # st.balloons()
                    
                    cursor.execute(f"SELECT * FROM {DB_table_name1} WHERE Name = %s", (name,))
                    company_exists = cursor.fetchone()

                    if company_exists:
                        st.error(f"**_A company with the name '{name}' already exists. Please use a different name or log in._**")
                    else:
                        try:
                            new_cid = insert_com_data(name, password)
                            st.success(f"**_:blue[Your profile is created. Your company ID is {new_cid}]_**")
                            st.balloons()
                        except Exception as e:
                            st.error(f"**_An unexpected error occurred: {e}_**")

            else:       

                DB_table_name2 = 'recruit_data'
                table_sql2 = "CREATE TABLE IF NOT EXISTS " + DB_table_name2 + """
                        (rid INT NOT NULL AUTO_INCREMENT,
                        cid INT NOT NULL,
                        domain varchar(100) NOT NULL,
                        reco_skill varchar(100) NOT NULL,
                        timestamp varchar(100) NOT NULL,
                        experience varchar(100) NOT NULL,
                        PRIMARY KEY (rid),
                        FOREIGN KEY(cid) REFERENCES com_data(cid) ON DELETE CASCADE);
                        """
                cursor.execute(table_sql2)  
                connection.commit()
                

                # st.header(":blue[Welcome to Company Side]")
                company_user=st.text_input("**:orange[User ID]**")
                company_password=st.text_input("**:orange[Password]**",type='password')

                load=st.button('Sign in',type="primary")
                #initialize session state
                if "load_state" not in st.session_state:
                    st.session_state.load_state= False
                if load or st.session_state.load_state:
                    st.session_state.load_state=True

                    if company_user.isdigit():  # Only proceed if the input is numeric (since cid is INT)
                        company_user = int(company_user)

                        cursor.execute(f"SELECT * FROM {DB_table_name1} WHERE cid = %s AND password = %s", (company_user, company_password))
                        result100 = cursor.fetchone()
                        # cursor.execute(f"SELECT * FROM {DB_table_name1} WHERE password= %s", (company_password,))
                        # result101 = cursor.fetchall()
                    
                    # load=st.button('login')
                    #     #initialize session state
                    # if "load_state" not in st.session_state:
                    #     st.session_state.load_state= False
                    # if load or st.session_state.load_state:
                    #     st.session_state.load_state=True
                        # if company_user=='company' and company_password=='company123':
                        
                        if result100:
                            # db_user=result100[0]
                            # db_password=result100[2]
        
                    
                            # if company_user==db_user and company_password==db_password:

                                st.success("##### **_:blue[Welcome Company]_**")
                                # st.success("welcome")
                                        
                                activities = ["Web Development", "Python Development", "Java Development", "Data Scientist", "Full Stack Development","Android Development"]     
                                choice1 = st.selectbox("**Choose Required Domain:**", activities)
                                # st.write("You Selected:", choice1)
                                st.subheader("You Selected: " + choice1)
                                cursor.execute('''SELECT Actual_skills FROM user_data''')
                                data = cursor.fetchall()
                                cursor.execute('''SELECT Email_ID FROM user_data''')
                                data2 = cursor.fetchall()
                                if choice1=="Web Development":
                                    options = st.multiselect(
                                        "Choose the required fields",
                                        ["JavaScript", "HTML", "CSS","React","PHP","Node.js","Next.js","Express.js"],
                                        ["HTML"],
                                    )
                                    li=options
                                    l=[]
                                    for x in data:
                                        # print(x)
                                        for y in x:
                                            converted_list = eval(y)
                                            c=0
                                            lowercase_list = [item.lower() for item in converted_list]
                                            # print("list: ",lowercase_list)
                                            for i in range(len(li)):
                                                # print(li[i].lower())
                                                if li[i].lower() in lowercase_list:
                                                    c=c+1
                                            
                                            l.append(c)
                                    emails_list = [email[0] for email in data2]
                                    result = dict(zip(emails_list, l))
                                    for email, value in result.items():
                                        # cursor.execute("UPDATE user_data11 SET Count = %s WHERE Email_ID = ?", (value, email))
                                        delete_sql = f"UPDATE {DB_table_name} SET Count = %s WHERE Email_ID = %s"
                                        cursor.execute(delete_sql, (value,email,))
                                        connection.commit()
                                    # print("You selected:", options)
                    
                                elif choice1=="Python Development":
                                    options = st.multiselect(
                                        "Choose the required fields",
                                        ["Python", "Django", "Flask","Tkinter","CherryPy","WEB2PY","FastAPI","TensorFlow"],
                                        ["Python"],
                                    )
                                    li=options
                                    l=[]
                                    for x in data:
                                        # print(x)
                                        for y in x:
                                            converted_list = eval(y)
                                            c=0
                                            lowercase_list = [item.lower() for item in converted_list]
                                            # print("list: ",lowercase_list)
                                            for i in range(len(li)):
                                                # print(li[i].lower())
                                                if li[i].lower() in lowercase_list:
                                                    c=c+1
                                            l.append(c)
                                    emails_list = [email[0] for email in data2]
                                    result = dict(zip(emails_list, l))
                                    for email, value in result.items():
                                        # cursor.execute("UPDATE user_data11 SET Count = ? WHERE Email_ID = ?", (value, email))
                                        delete_sql = f"UPDATE {DB_table_name} SET Count = %s WHERE Email_ID = %s"
                                        cursor.execute(delete_sql, (value,email,))
                                        connection.commit()
                                    # st.write("You selected:", options)
                    
                                elif choice1=="Java Development":
                                    options = st.multiselect(
                                        "Choose the required fields",
                                        ["java", "JSP", "Servlet","Spring boot","JavaScript","angular"],
                                        ["java"],
                                    )
                                    li=options
                                    l=[]
                                    for x in data:
                                        # print(x)
                                        for y in x:
                                            converted_list = eval(y)
                                            c=0
                                            lowercase_list = [item.lower() for item in converted_list]
                                            # print("list: ",lowercase_list)
                                            for i in range(len(li)):
                                                # print(li[i].lower())
                                                if li[i].lower() in lowercase_list:
                                                    c=c+1
                                            l.append(c)
                                    emails_list = [email[0] for email in data2]
                                    result = dict(zip(emails_list, l))
                                    for email, value in result.items():
                                        # cursor.execute("UPDATE user_data11 SET Count = ? WHERE Email_ID = ?", (value, email))
                                        delete_sql = f"UPDATE {DB_table_name} SET Count = %s WHERE Email_ID = %s"
                                        cursor.execute(delete_sql, (value,email,))
                                        connection.commit()
                                    # st.write("You selected:", options)
                                
                                elif choice1=="Data Scientist":
                                    options = st.multiselect(
                                        "Choose the required fields",
                                        ["Mechine Learning", "Python", "AI","NLP","Deep Learning","Pandas","TensorFlow","Power BI","Pytorch","Excel"],
                                        ["AI"],
                                    )
                                    li=options
                                    l=[]
                                    for x in data:
                                        # print(x)
                                        for y in x:
                                            converted_list = eval(y)
                                            c=0
                                            lowercase_list = [item.lower() for item in converted_list]
                                            # print("list: ",lowercase_list)
                                            for i in range(len(li)):
                                                # print(li[i].lower())
                                                if li[i].lower() in lowercase_list:
                                                    c=c+1
                                            l.append(c)

                                    emails_list = [email[0] for email in data2]
                                    result = dict(zip(emails_list, l))
                                    for email, value in result.items():
                                        # cursor.execute("UPDATE user_data11 SET Count = ? WHERE Email_ID = ?", (value, email))
                                        delete_sql = f"UPDATE {DB_table_name} SET Count = %s WHERE Email_ID = %s"
                                        cursor.execute(delete_sql, (value,email,))
                                        connection.commit()
                                    # st.write("You selected:", options)

                                elif choice1=="Full Stack Development":
                                    options = st.multiselect(
                                        "Choose the required fields",
                                        ["Python", "Java", "R", "Ruby", "Node.js", "PHP", "React", "Angular", "Express.js","C++","MongoDB","MySQL","PostgreSQL"],
                                        ["PHP"],
                                    )
                                    li=options
                                    l=[]
                                    for x in data:
                                        # print(x)
                                        for y in x:
                                            converted_list = eval(y)
                                            c=0
                                            lowercase_list = [item.lower() for item in converted_list]
                                            # print("list: ",lowercase_list)
                                            for i in range(len(li)):
                                                # print(li[i].lower())
                                                if li[i].lower() in lowercase_list:
                                                    c=c+1
                                            l.append(c)
                                    emails_list = [email[0] for email in data2]
                                    result = dict(zip(emails_list, l))
                                    for email, value in result.items():
                                        # cursor.execute("UPDATE user_data11 SET Count = ? WHERE Email_ID = ?", (value, email))
                                        delete_sql = f"UPDATE {DB_table_name} SET Count = %s WHERE Email_ID = %s"
                                        cursor.execute(delete_sql, (value,email,))
                                        connection.commit()

                                elif choice1=="Android Development":
                                    options = st.multiselect(
                                        "Choose the required fields",
                                        ["Java","Kotlin","Android UI","C++","Python"],
                                        ["Java"],
                                    )
                                    li=options
                                    l=[]
                                    for x in data:
                                        # print(x)
                                        for y in x:
                                            converted_list = eval(y)
                                            c=0
                                            lowercase_list = [item.lower() for item in converted_list]
                                            # print("list: ",lowercase_list)
                                            for i in range(len(li)):
                                                # print(li[i].lower())
                                                if li[i].lower() in lowercase_list:
                                                    c=c+1
                                            l.append(c)

                                    emails_list = [email[0] for email in data2]
                                    result = dict(zip(emails_list, l))
                                    for email, value in result.items():
                                        # cursor.execute("UPDATE user_data11 SET Count = ? WHERE Email_ID = ?", (value, email))
                                        delete_sql = f"UPDATE {DB_table_name} SET Count = %s WHERE Email_ID = %s"
                                        cursor.execute(delete_sql, (value,email,))
                                        connection.commit()

                                # ts = time.time()
                                # cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                                # cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                                # timestamp = str(cur_date + '_' + cur_time)
                            
                            # st.balloons()
                                age = st.slider("**select required experience year?**", 0, 40, 5)
                                st.subheader("**Experience level set to: **"+ str(age) + "** years**")

                                # d = st.date_input("Select the deadline of posts", value=None)
                                # st.write("Recruitment deadline is:", d)

                                load1=st.button('Submit new recruitment posts')
                                #initialize session state
                                if "load1_state" not in st.session_state:
                                    st.session_state.load1_state= False
                                if load1 or st.session_state.load1_state:
                                    st.session_state.load1_state=True
                                # if st.button("Submit new recruitment posts", type="primary"):
                                    ts = time.time()
                                    cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                                    cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                                    timestamp = str(cur_date + '_' + cur_time)
                                    insert_recruit_data(company_user, choice1, ', '.join(options), timestamp, age)
                                    # cursor.execute(f"SELECT*FROM {DB_table_name} WHERE Experience>=%s ORDER BY Count DESC", (str(exp),))
                                    # cursor.execute(f"SELECT * FROM {DB_table_name} WHERE Count>=1 and Experience >= %s ORDER BY Count DESC", (age,))

                                    cursor.execute(f"SELECT ID,Name,Email_ID,Experience,Actual_skills,Count FROM {DB_table_name} WHERE Count>=1 and Experience >= %s ORDER BY Count DESC", (age,))
                                    data10 = cursor.fetchall()

                                    st.header("**User's Basic Data**")
                                    df1 = pd.DataFrame(data10, columns=['ID', 'Name', 'Email', 'Experience', 'Actual Skills','Matching skills'])        
                                    st.dataframe(df1)
                                    # st.balloons()



                                    cursor.execute(f"SELECT ID,Name,Email_ID FROM {DB_table_name} WHERE Count>=1 and Experience >= %s ORDER BY Count DESC", (age,))
                                    data = cursor.fetchall()
                        
                                    # connection.commit()
                                    
                                    columns = [description[0] for description in cursor.description]
                                    # Convert to pandas DataFrame
                                    df = pd.DataFrame(data, columns=columns)

                                    st.write("## Candidate's List")

                                    # Iterate over each row in the DataFrame and display in Streamlit columns
                                    for index, row in df.iterrows():
                                        cols = st.columns([1, 2, 2, 2])  # Adjust column width ratio as needed
                                        cols[0].write(row["ID"])
                                        cols[1].write(row["Name"])
                                        # cols[2].write(row["Email_ID"])
                                        

                                        

                                        # Add a direct download button for each file
                                        # Fetch resume data directly when the button is clicked

                                        cursor.execute("SELECT Resume FROM user_data WHERE Email_ID = %s", (row["Email_ID"],))
                                        resume_data = cursor.fetchone()

                                        if resume_data and resume_data[0]:  # Check if data exists
                                            cols[2].download_button(
                                                label="Download Resume",
                                                data=resume_data[0],  # Resume binary data
                                                file_name=f"{row['Name']}_resume.pdf",
                                                mime="application/pdf"
                                            )
                                        
                                        with cols[3]:
                                            if st.button(f"Accept {row['Name']}",type="primary"):
                                                cursor.execute(f"SELECT Name FROM {DB_table_name1} WHERE cid = %s", (company_user,))
                                                r = cursor.fetchone()
                                
                                                subject = f"Congratulations! Your Application Has Been Shortlisted"
                                                message = f"Dear {row['Name']},\n\nWe are pleased to inform you that your resume has been shortlisted for the position of {choice1} at {r[0].upper()}.\n\nYour skills and qualifications align well with the company requirements. The further process will be managed directly by {r[0].upper()}. They will reach out to you soon regarding the next steps in the selection process.\n\nWishing you the best of luck!\n\nBest regards,\nSmart Hiring System\nsmarthiringsystem2024@gmail.com."
                                                send_email(row["Email_ID"], subject, message)
                                                st.success(f"**Acceptance email sent to {row['Name']}**")


                                if st.button("View Previous Recruitment Posts"):
                                    previous_posts = fetch_previous_recruitments(company_user)
                                
                                    if previous_posts:
                                        # delete_expired_posts()
                                        st.header("**Previous Recruitment Posts**")
                                        df = pd.DataFrame(previous_posts, columns=['RID', 'CID', 'Domain', 'Recommended Skills', 'Timestamp', 'Experience'])
                                        st.dataframe(df)
                                    else:
                                        st.info("No previous recruitment posts found.")

                        else:
                            st.error("**_:red[Wrong ID & Password Provided]_**")

        except Exception as main_error:
            st.error(f"**⚠ An unexpected error occurred: {main_error}**")

run()

