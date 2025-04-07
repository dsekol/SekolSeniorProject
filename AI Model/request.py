from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import pandas as pd

model_name_or_path = "./saved_model_gpt"
tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
model = GPT2LMHeadModel.from_pretrained(model_name_or_path)

# Move the model to the GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

while True:
    prompt = input("You: ")
    if prompt.lower() in ["exit", "quit"]:
        break
    response = generate_text(prompt)
    print(f"Model: {response}")