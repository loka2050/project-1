import pandas as pd
import streamlit as st
# db
import sqlite3
# EDA Pkgs
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False


conn = sqlite3.connect('data.db')
c = conn.cursor()


# function

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate DATE)')


def add_data(author, title, article, postdate):
    c.execute('INSERT INTO blogatable(author,title,article,postdate) VALUES (?,?,?,?)', (author, title, article, postdate))
    conn.commit()


def view_all_notes():
    c.execute('SELECT * FROM blogatable')
    data = c.fetchall()
    return data


def view_all_titles():
    c.execute('SELECT DISTINCT title FROM bloga table')
    data = c.fetchall()
    return data


def view_all_title():
    c.execute('SELECT DISTINCT title FROM blogatable')
    data= c.fetchall()
    return data


def get_blog_by_title(title):
    c.execute('SELECT * FROM blogatable WHERE title="{}"'.format(title))
    data = c.fetchall()
    return data


def get_blog_by_author(author):
    c.execute('SELECT * FROM blogatable WHERE author="{}"'.format(author))
    data = c.fetchall()
    return data


def delete_data(title):
	c.execute('DELETE FROM blogatable WHERE title="{}"'.format(title))
	conn.commit()
# Login/Signup








def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



#layout tamplates
title_temp ="""
	<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
	<h6>Author:{}</h6>
	<br/>
	<br/>	
	<p style="text-align:justify">{}</p>
	</div>
	"""
article_temp ="""
	<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<h6>Author:{}</h6> 
	<h6>Post Date: {}</h6>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
	<br/>
	<br/>
	<p style="text-align:justify">{}</p>
	</div>
	"""
head_message_temp ="""
	<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;">
	<h6>Author:{}</h6> 		
	<h6>Post Date: {}</h6>		
	</div>
	"""
full_message_temp ="""
	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<p style="text-align:justify;color:black;padding:10px">{}</p>
	</div>
	"""
def main():
    """ A simple CRUD blog """
    st.title('simple blog')
    menu = ("home", "view post", "login", "signUp","search")
    choice = st.sidebar.selectbox("menu", menu)
    if choice == "home":
        st.subheader("home")
        result = view_all_notes()

        for i in result:
            b_author=i[0]
            b_title=i[1]
            b_article = i[2]
            b_post_date = i[3]
            st.markdown(title_temp.format(b_title,b_author,b_article,b_post_date),unsafe_allow_html=True)


    elif choice == "view post":
        st.subheader("view post")
        all_titles = [i[0]for i in view_all_title()]
        postlist = st.sidebar.selectbox("view post",all_titles)
        post_result = get_blog_by_title(postlist)
        for i in post_result:
            b_author = i[0]
            b_title = i[1]
            b_article = str(i[2])[0:30]
            b_post_date = i[3]
            st.markdown(head_message_temp.format(b_title, b_author, b_post_date), unsafe_allow_html=True)
            st.markdown(full_message_temp.format(b_article), unsafe_allow_html=True)



    elif choice == "login":
        st.subheader("Logged In")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                st.success("Logged In As: {}".format(username))

                task = st.selectbox("Task", ["add post", "manage", "Users Profile"])
                if task == "add post":
                    st.subheader("add post")
                    create_table()

                    blog_author = st.text_input("enter Auther Name", max_chars=50)
                    blog_title = st.text_input("enter title")
                    blog_article = st.text_area("enter Article here ", height=200)
                    blog_post_date = st.date_input("date")
                    if st.button("Add"):
                        add_data(blog_author, blog_title, blog_article, blog_post_date)
                        st.success("Post:{} saved".format(blog_title))



                elif task == "manage":
                    st.subheader("manage")
                    result = view_all_notes()
                    clean_db = pd.DataFrame(result, columns=["author", "title", "article", "post date"])
                    st.dataframe(clean_db)

                    unique_title = [i[0] for i in view_all_title()]
                    delete_blog_by_title = st.selectbox("unique title", unique_title)
                    if st.button("delete"):
                        delete_data(delete_blog_by_title)
                        st.warning("deleted:'{}'".format(delete_blog_by_title))
                    if st.checkbox("metrics"):
                        new_df = clean_db
                        new_df['length'] = new_df['article'].str.len()
                        st.dataframe(new_df)
                        st.subheader("author stats")
                        new_df["author"].value_counts().plot(kind='bar')
                        st.pyplot()
                        st.set_option('deprecation.showPyplotGlobalUse', False)
                        st.subheader("author stats")
                        new_df["author"].value_counts().plot.pie(autopct="%1.1f%%")
                        st.pyplot()
                        st.set_option('deprecation.showPyplotGlobalUse', False)
                    if st.checkbox("word cloud"):
                        st.subheader("Generate word cloud ")
                        text = new_df['article'].iloc[0]
                        wordcloud = WordCloud().generate(text)
                        plt.imshow(wordcloud, interpolation='bilinear')
                        plt.axis('off')
                        st.pyplot()
                    if st.checkbox("barH Plot"):
                        st.subheader("length of articles")
                        new_df = clean_db
                        new_df['length'] = new_df['article'].str.len()
                        barh_plot = new_df.plot.barh(x='author', y='length', figsize=(20, 10))
                        st.pyplot()

                elif task == "Users Profile":
                    st.subheader("Users Profile")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result, columns=['User', 'Password'])
                    st.dataframe(clean_db)





    elif choice == "search":
        st.subheader("Search Articles")
        search_term = st.text_input('Enter Search Term')
        search_choice = st.radio("Field to Search By", ("title", "author"))

        if st.button("Search"):

            if search_choice == "title":
                article_result = get_blog_by_title(search_term)
            elif search_choice == "author":
                article_result = get_blog_by_author(search_term)

            for i in article_result:
                b_author = i[0]
                b_title = i[1]
                b_article = i[2]
                b_post_date = i[3]
                st.markdown(head_message_temp.format(b_title, b_author, b_post_date), unsafe_allow_html=True)
                st.markdown(full_message_temp.format(b_article), unsafe_allow_html=True)
    elif choice == "signUp":
        st.subheader("Create A New Account")
        new_user = st.text_input("User name")
        new_password = st.text_input("Password", type='password')
        if st.button("SignUp"):
            create_usertable()

            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully create an Account")


if __name__ == '__main__':
    main()
