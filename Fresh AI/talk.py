import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the T5 model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('t5-base')
tokenizer = T5Tokenizer.from_pretrained('t5-base')

def generate_response(user_input):
    # Tokenize the user input
    input_ids = tokenizer.encode("generate response: " + user_input, return_tensors='pt')

    # Generate a response using the T5 model
    outputs = model.generate(input_ids, max_length=100)

    # Convert the response to a string
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response

# Test the chatbot
while True:
    user_input = input("User: ")
    response = generate_response(user_input)
    print("Chatbot:", response)