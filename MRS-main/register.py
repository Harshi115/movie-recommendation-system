import streamlit as st
import pandas as pd
import mysql.connector
import re

#mycursor.execute("CREATE TABLE reg_tb (name VARCHAR(255),user_id VARCHAR(255)  PRIMARY KEY,age int(50),email VARCHAR(50),password VARCHAR(50))");
def create_connection():
    """Create a connection to the MySQL database."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="system",
        database="register")
    return db
def insert_user_record(db,name,user_id, age, email, password):
    """Insert a new patient record into the 'patients' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE register")

    insert_user_query = """
    INSERT INTO reg_tb (name,user_id, age, email, password)
    VALUES (%s, %s, %s, %s, %s)
    """

    user_data = (name,user_id, age, email, password)

    cursor.execute(insert_user_query, user_data)
    db.commit()
    st.write("user record inserted successfully.")



def validate_email(email):
    # Regular expression pattern for validating email
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False


def validate_user_id(user_id):
    # Check if user ID is not empty and meets certain conditions
    if user_id.strip() == "":
        return "User ID cannot be empty."
    elif len(user_id) < 6:
        return "User ID must be at least 6 characters long."
    elif not user_id.isalnum():
        return "User ID must contain only alphanumeric characters."
    else:
        return None  # Return None if validation passes

def validate_pass(pass_word):
    # Check if user ID is not empty and meets certain conditions
    if pass_word.strip() == "":
        return "password cannot be empty."
    elif len(pass_word) < 8:
        return "password must be at least 8 characters long."
    elif not pass_word.isalnum():
        return "password must contain only alphanumeric characters."
    else:
        return None  # Return None if validation passes


def register_form():
    st.title("REGISTER YOURSELF")
    st.subheader("enter your details below")
    with st.form("register",clear_on_submit=True):
        name = st.text_input("enter your name",placeholder="enter your name")
        user_id = st.text_input("enter your user_id",placeholder="eg:-abmca123(must be 6 characters long)")
        validation_result = validate_user_id(user_id)
        age = st.number_input("enter your age",min_value=18,max_value=80)
        email = st.text_input("enter your email",placeholder="eg:- sam123@gmail.com")
        pass_word = st.text_input("enter your password",type="password",placeholder="length must greater than 8")
        vpass = validate_pass(pass_word)
        submit = st.form_submit_button("Register")


        if submit:
            if not (name and user_id and age and email and pass_word):
                st.error("All fields are required.")
            elif not validate_email(email):
                st.error("Please enter a valid email address.")
            elif validation_result is not None:
                st.error(validation_result)
            elif vpass is not None:
                st.error(vpass)
            else:
                db = create_connection()
                insert_user_record(db, name, user_id, age, email, pass_word)
                st.success("Registration successful!")
                st.session_state['loggedIn'] = True

if __name__ == "__main__":
    register_form()
