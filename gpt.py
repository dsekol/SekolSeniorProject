import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from config import Config

# Load the tokenizer and model from the specified directory.
tokenizer = GPT2Tokenizer.from_pretrained(Config.MODEL_PATH, local_files_only=True)
model = GPT2LMHeadModel.from_pretrained(Config.MODEL_PATH, local_files_only=True)

# Move model to GPU if available.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def generate_text(prompt, max_length=100):
    # Dynamically adjust response length based on input
    max_length = min(len(prompt.split()) * 3, 150)  # Scale response length

    # Tokenize the prompt and move input tensors to the appropriate device
    inputs = tokenizer(
        prompt, return_tensors="pt", padding=True, truncation=True
    ).to(device)
    
    # Generate model output using sampling parameters that promote diversity
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=max_length,
        num_return_sequences=1,
        do_sample=True,
        temperature=1,  # Increase creativity
        top_k=50,         # Diverse word selection
        top_p=0.8,       # Controls probability mass
        repetition_penalty=1.5,  # Avoid repeated phrases
        early_stopping=True  # Prevent unnatural outputs
    )
    
    # Decode the generated tokens into a string and remove special tokens
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
