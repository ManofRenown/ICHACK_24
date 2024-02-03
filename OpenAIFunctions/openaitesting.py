from openai import OpenAI
import os
import json
import openaifunctions
import time

api_key = os.environ.get('OPENAI_API_KEY') #the env variable
client = OpenAI()
client.api_key = api_key

assistant_id = openaifunctions.create_ytlink_assistant(client)
thread_id = client.beta.threads.create().id; #create thread

  
# Print out each of the assistant's messages
#print(openaifunctions.send_message(client,assistant_id,thread_id,"how to get a six pack")+"\n")