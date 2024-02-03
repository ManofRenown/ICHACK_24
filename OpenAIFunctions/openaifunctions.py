import os
import json
import time

def get_last_assistant_message(client, thread_id):
    messages_response = client.beta.threads.messages.list(thread_id=thread_id)
    messages = messages_response.data
    #print("message responses: ", messages_response ,"\n")
    # Iterate through messages in reverse chronological order to find the last assistant message
    for message in messages:
        if message.role == 'assistant':
            # Get the content of the last assistant message
            assistant_message_content = " ".join(
                content.text.value for content in message.content if hasattr(content, 'text')
            )
            return assistant_message_content.strip()
  
    return ""  # Return an empty string if there is no assistant message


def create_ytlink_assistant(client):
  assistant_file_path = 'ytlink_assistant.json' #this file simply contains id of assistant

  # If there is an assistant.json file already, then load that assistant
  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    # If no assistant.json is present, create a new assistant using the below specifications

    assistant = client.beta.assistants.create(
        # Getting assistant prompt from "prompts.py" file, edit on left panel if you want to change the prompt
        name="obsidian_analyser",
        instructions="""
        You are an assistant that analyses notes and generate youtube requests to find relevant youtube videos. 
        Do add any other text to your response, only include the requests themselves.
        """,
        model="gpt-3.5-turbo-1106"
        #no need for tools here, no retrieval or code interpreter used
        )

    # Create a new assistant.json file to load on future runs
    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id #return the id of the assistant



def create_insight_assistant(client):
  assistant_file_path = 'insight_assistant.json' #this file simply contains id of assistant

  # If there is an assistant.json file already, then load that assistant
  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    # If no assistant.json is present, create a new assistant using the below specifications

    assistant = client.beta.assistants.create(
        # Getting assistant prompt from "prompts.py" file, edit on left panel if you want to change the prompt
        name="obsidian_analyser",
        instructions="""
        You are an assistant that analyses notes and generate interesting self contained insights. 
        I don't need any other references or context to understand each insight 
        Format the responses nicely using markdown syntax
        """,
        model="gpt-3.5-turbo-1106"
        #no need for tools here, no retrieval or code interpreter used
        )

    # Create a new assistant.json file to load on future runs
    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id #return the id of the assistant

def send_message(client, assistant_id, thread_id, message):

  # Send the message and wait for a response
  user_message = client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message
  )

  # Run the assistant and wait until it's done
  run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
  )

  iterations = 0 #just a counter to keep track of number of iterations
  while True:
    run_status = client.beta.threads.runs.retrieve(
                  thread_id=thread_id,
                  run_id=run.id
                )
    if run_status.status == 'completed':
      print("the run status after completion: ", run_status.status ,"\n")
      break
    if run_status.status == 'failed':
      print("the run has failed: ", run_status.last_error,"\n")
    time.sleep(1)  # sleep to avoid hitting the API too frequently
    iterations+=1
    print("current run status: ", run_status.status, " iteration: ", iterations)
    
  # Get all messages from the assistant since the last 'user' message
  response_content = get_last_assistant_message(client, thread_id)
  return response_content
