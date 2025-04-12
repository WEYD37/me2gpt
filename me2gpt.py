import openai
import json
import os

# Set your API key
openai.api_key = ""

def read_system_prompt():
    try:
        with open('system_prompt.txt', 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "You are a helpful AI assistant. Respond accurately to user queries."

def save_conversation(history):
    with open('history.json', 'w', encoding='utf-8') as file:
        json.dump(history, file, indent=2)

def load_conversation():
    try:
        with open('history.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

history = load_conversation()

if not history:
    system_prompt = read_system_prompt()
    history.append({"role": "system", "content": system_prompt})

print("Ready to chat! Type your messages below (type 'exit' to quit).")

# Start a conversation loop
while True:
    user_input = input("\nYou: ")
    
    if user_input.lower() == "exit":
        print("Goodbye!")
        save_conversation(history)
        break

    history.append({"role": "user", "content": user_input})
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=history
    )
    
    bot_response = response['choices'][0]['message']['content']
    
    history.append({"role": "assistant", "content": bot_response})
    
    save_conversation(history)
    
    print(f"AI: {bot_response}")