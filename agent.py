from agents.realtime import RealtimeAgent

from dotenv import load_dotenv
load_dotenv("API_key.env")
from typing import Literal
from agents import Agent, function_tool
from agents import function_tool

import psycopg
# psycopg3 uses context managers
conn = psycopg.connect(
    "dbname=ai_project user=postgres password=1234 host=localhost port=5432"
)


@function_tool
def check_client_id(fname:str, lname :str) -> str:
    cursor = conn.cursor()
    command = f"SELECT client_id FROM clients where first_name = %s and last_name = %s"
    cursor.execute(command,(fname,lname))
    result = cursor.fetchall()
    cursor.close()
    return result if result else "Not found"

@function_tool
def check_client_id_full(fname:str | None, lname :str | None, address :str | None, telephone :str | None, email :str | None ) -> str:
    cursor = conn.cursor()
    command = f"SELECT client_id FROM clients where 1=1 "
    if fname != None:
        command += f"and first_name = %s ",(fname)
    if lname != None:
        command += f"and last_name = %s ",(lname)
    if address != None:
        command += f"and address = %s ",(address)
    if telephone != None:
        command += f"and telephone = %s ",(telephone)
    if email != None:
        command += f"and email = %s ",(email)
    cursor.execute(command)
    result = cursor.fetchall()
    cursor.close()
    return result if result else "Not found"

@function_tool
def check_receivable_id(fname:str, lname :str) -> str:
    cursor = conn.cursor()
    command = f"SELECT client_id FROM clients where first_name = %s and last_name = %s"
    cursor.execute(command,(fname,lname))
    result = cursor.fetchall()
    cursor.close()
    return result if result else "Not found"

@function_tool
def read_data_from_clients(key: Literal["first_name", "last_name", "address", "telephone", "email"],id: str) -> str:
    cursor = conn.cursor()
    command = f"SELECT {key} FROM clients where client_id = {id}"
    cursor.execute(command)
    result = cursor.fetchall()
    cursor.close()
    return result if result else "Not found"

@function_tool
def read_data_from_events(key: Literal["event_id", "receivable_id", "members", "history_date", "action", "result"], id: str) -> str:
    cursor = conn.cursor()
    cursor.execute(f"SELECT {key} FROM events where receivabke_id = {id}")
    result = cursor.fetchall()
    cursor.close()
    return result if result else "Not found"


#QEE CHECKING RECEUVABLE
@function_tool
def read_data_from_receivable(key: Literal["receivable_id", "client_id", "document_id", "amount", "revenue"], id: str) -> str:
    cursor = conn.cursor()
    cursor.execute(f"SELECT {key} FROM receivable WHERE client_id = {id}")
    result = cursor.fetchall()
    cursor.close()
    return result if result else "Not found"


db_agent = Agent(
name="DB agent",
instructions="""Browse the database with tools.
Your tools only search the database they do not allow for any other action.
You have following tools at your disposal
check_client_id to check what client id is with first name and last name at your disposal
check_client_id_full to check what client id is with other information
read_data_from_clients to find information from specific column name of clients table
read_data_from_receivable to find information from specific column name of receivable table with client id as identifier
When using read_data_from_ family of tools remember to always use check_client_id tool to retrieve client_id, do not tell user what client id you retrieved
show all tools used and results
""",#check what outputs if blank and if two records are same
tools=[check_client_id,check_client_id_full, read_data_from_clients,read_data_from_receivable],
)

negotiation_agent = Agent(
    name="Negotiation_agent",
    instructions="You are a negotiation agent for debt collection. Your job is to negotiate deal with user to pay off debt in installments"
)

agent = RealtimeAgent(
    name="Twilio Assistant",
    instructions="""You are a helpful assistant that starts every conversation with a creative greeting.
     Keep responses concise and friendly since this is a phone conversation.
     You manage work of other agents and are responsible for communication with the user.
    Decide which specialist agent should handle the request:
    - Use db_Agent to query database
    - Use negotiation_agent to negotiate when user requests to pay off debt the user has. If user did not ask for debt use db_agent to query database
    Remember that database is in english so when you are asked in other language and have no results ask user to spell out names they provided.
     """,
    tools = [
        db_agent.as_tool("db_agent", "queriers database"),
        negotiation_agent.as_tool("negotiation_agent","negotiates when user requests to pay off debt the user has. If user did not ask for debt use db_agent to query database")
    ],
)