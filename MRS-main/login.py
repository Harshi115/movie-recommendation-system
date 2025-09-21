import streamlit as st
import mysql.connector
from st_pages import hide_pages
from time import sleep



def create_connection():
    """Create a connection to the MySQL database."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="system",
        database="register")
    return db

def fetch_user_record(db, user_id,password):
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE register")
    # Fetch the user by ID
    select_user_query = "SELECT password FROM reg_tb WHERE user_id = %s"
    adr = (user_id,)

    cursor.execute(select_user_query, adr)

    user_detail = cursor.fetchall()
    for i in user_detail:
        print(i[0])
        if (i[0] == password):
            return True
        else:
            return False

    #cursor.execute(select_user_query, (user_id,))
    #user_detail = cursor.fetchone()
    #return user_detail

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


def login_form():
    st.title("LOGIN")
    st.subheader("enter your details below")
    with st.form("login",clear_on_submit=True):
        user_id = st.text_input("USER ID")
        pass_word = st.text_input("PASSWORD",type="password")
        validation_result = validate_user_id(user_id)
        submit = st.form_submit_button("LOGIN")

        if submit:
            if not (user_id and pass_word):
                st.error("All fields are required.")
            elif validation_result is not None:
                st.error(validation_result)

            else:
                db = create_connection()
                if fetch_user_record(db, user_id,pass_word):
                    st.session_state['loggedIn'] = True
                    st.success("login successful!")
                else:
                    st.error("Invalid user")
                    st.session_state['loggedIn'] = False;
        return st.session_state['loggedIn']




if __name__ == "__main__":
    login_form()