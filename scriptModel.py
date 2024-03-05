import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import os
import google.generativeai as genai
import textwrap
from IPython.display import display
from IPython.display import Markdown
import re
from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error
import datetime
import yaml

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

def load_models():
    load_dotenv()

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model2 = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    nlp = pipeline("ner", model=model2, tokenizer=tokenizer,grouped_entities=True)

    return model, nlp

def enter_company(model, nlp,company_name):
    # company_name = input("Please enter the name of the company who you want to compare with its competitors: ")
    print(company_name)
    response = model.generate_content("List competitors of "+company_name)
    print(response.text)

    competitors=[]

    for i in nlp(response.text):
        competitors.append(i["word"])
    for i in competitors:
        if(i[0]=='#'):
            i = re.sub('^#+', '', i)
            temp=competitors[-1]
            del competitors[-1]
            temp+=i
            if temp not in competitors:
                competitors.append(temp)
            continue
            
        if i not in competitors:
            competitors.append(i)

    print(competitors)

    return competitors

def connect_to_postgres():
    with open('database.yaml', 'r') as yaml_file:
        db_config = yaml.safe_load(yaml_file)
    try:
        connection = psycopg2.connect(
            user=db_config['database']['user'],
            password=db_config['database']['password'],
            host=db_config['database']['host'],
            port=db_config['database']['port'],
            database=db_config['database']['name']
        )
        print("Connection to PostgreSQL database successful")
        return connection
    except Error as e:
        print(f"Error while connecting to PostgreSQL: {e}")

def insert_response(connection, current_datetime, company_name, competitor_name, response_text):
    try:
        cursor = connection.cursor()
        # Define your SQL query to insert response into the database
        postgres_insert_query = "INSERT INTO PromptData (date_and_time, company_name, competitor_name, comparison_result) VALUES (%s, %s, %s, %s);"

        # Execute the SQL query
        cursor.execute(postgres_insert_query, (current_datetime, company_name, competitor_name, response_text))
        connection.commit()
        print("Response inserted successfully into the table")
    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to insert response into the table", error)

def choose_competitor(model, company_name, selected_competitor):
    print(selected_competitor)
    response = model.generate_content("Give insights and compare " + company_name + " and " + selected_competitor)
    
    response_text = response.text
    
    query="comparison between " + company_name + " and " + selected_competitor
    current_datetime = datetime.datetime.now()

    connection=connect_to_postgres()
    insert_response(connection, current_datetime, company_name, selected_competitor, response_text)
    
    print(response_text)
    return response_text
