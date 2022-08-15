# streamlit_app.py

import streamlit as st
import psycopg2
import pandas as pd


# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

'''# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from notebook;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")'''



#Record=()

#Title
st.title("Note Book")
st.header("Jot your thoughts, notes, to do and other people's actions")

#def Record():

#user input
NoteType=st.radio("What are you noting?",["Note", "To Do", "Action"])
Date=st.date_input("What Date (default today)?")
NoteTitle=st.text_input("What's the title?", "Title")
#Note=st.text_input("What's your note?", "Note", on_change=Record)
Note=st.text_input("What's your note?", "Note")

#Record data into database
cur = conn.cursor()
cur.execute("INSERT INTO Notebook (Date , NoteType, NoteTitle, Note) VALUES (%s, %s, %s, %s);", (Date, NoteType, NoteTitle, Note))
#cur.execute('INSERT INTO Notes (Date , NoteType, NoteTitle, Note) VALUES (?, ?, ?, ?)',
#(Date, NoteType, NoteTitle, Note))
conn.commit()

#publish database
#cur = conn.cursor()
#cur.execute('SELECT Date, NoteType, NoteTitle, Note FROM Notes ORDER BY id DESC LIMIT 100')
df = pd.read_sql('SELECT Date, NoteType, NoteTitle, Note FROM Notes ORDER BY id DESC LIMIT 100', conn)
st.dataframe(df)

#@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     download = pd.read_sql('SELECT Date, NoteType, NoteTitle, Note FROM Notes ORDER BY id DESC', conn)
     return download.to_csv().encode('utf-8')

csv = convert_df(df)

st.download_button(
    label="Download Notebook as CSV",
    data=csv,
    file_name='Notebook.csv',
    mime='text/csv',
)
