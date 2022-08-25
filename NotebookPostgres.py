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
conn.autocommit = True





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
cur.execute("INSERT INTO notebook (notetype, date, notetitle, note) VALUES (%s, %s, %s, %s);", (NoteType, Date, NoteTitle, Note))
#conn.commit()

#cur.execute('INSERT INTO Notes (Date , NoteType, NoteTitle, Note) VALUES (?, ?, ?, ?)',
#(Date, NoteType, NoteTitle, Note))


#publish database
#cur = conn.cursor()
#cur.execute('SELECT Date, NoteType, NoteTitle, Note FROM Notebook ORDER BY id DESC LIMIT 100')
df = pd.read_sql('''SELECT Date, NoteType, NoteTitle, Note FROM Notebook WHERE note <> 'Note' ORDER BY id DESC LIMIT 100''', conn)
st.table(df)

#@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     download = pd.read_sql('''SELECT Date, NoteType, NoteTitle, Note FROM Notebook WHERE note <> 'Note' ORDER BY id DESC''', conn)
     return download.to_csv().encode('utf-8')

csv = convert_df(df)

st.download_button(
    label="Download Notebook as CSV",
    data=csv,
    file_name='Notebook.csv',
    mime='text/csv',
)
