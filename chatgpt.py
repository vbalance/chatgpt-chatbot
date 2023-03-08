import openai
import requests
import os

# Define a function to open a file and return its contents as a string
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Define a function to save content to a file
def save_file(filepath, content):
    with open(filepath, 'a', encoding='utf-8') as outfile:
        outfile.write(content)

# Set the OpenAI API key by reading it from a file
openai.api_key = open_file('openaiapikey.txt')

# Initialize an empty list to store the conversation
conversation = []

# Read the content of a file containing the chatbot's prompt
chatbot = open_file('chatbot.txt')

# Define a function to make an API call to the OpenAI ChatCompletion endpoint
def chatgpt(user_input, temperature=1, frequency_penalty=0.2, presence_penalty=0):
    global conversation # When a variable is declared as global within a function, it means that any changes made to the variable inside the function will also affect the value of the variable outside the function.

    # Update conversation by appending the user's input
    conversation.append({"role": "user", "content": user_input})

    # Insert prompt/s into message history - By inserting the chatbot's prompt message into the conversation history before making an API call to the OpenAI ChatCompletion endpoint, the function ensures that the chatbot's response will be generated in the correct context and take into account any previous messages in the conversation history. This can improve the quality and relevance of the chatbot's responses.
    messages_input = conversation.copy()
    prompt = [{"role": "system", "content": chatbot}]
    prompt_item_index = 0
    for prompt_item in prompt:
        messages_input.insert(prompt_item_index, prompt_item)
        prompt_item_index += 1

    # Make an API call to the ChatCompletion endpoint with the updated messages
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messages_input)

    # Extract the chatbot's response from the API response
    chat_response = completion['choices'][0]['message']['content']

    # Update conversation by appending the chatbot's response
    conversation.append({"role": "assistant", "content": chat_response})

    # Return the chatbot's response
    return chat_response

# Enter an infinite loop to prompt the user for input and get the chatbot's response - This loop will continue running until it is manually interrupted or terminated by the user, allowing the user to have a conversation with the chatbot by entering messages as input and receiving the chatbot's responses in return.
while True:
    user_message = input("> ") # Prompt the user for input
    response = ("\n\n") + chatgpt(user_message) + ("\n\n") # Call the chatgpt function with user input
    print(response) # Print the chatbot's response
    save_file("Chatlog.txt", user_message + ('\n\n') + response + ('\n\n'))