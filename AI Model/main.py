import pandas as pd
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from datasets import Dataset
import torch
import time  # Import the time module

# Load the specific CSV file
csv_file_path = 'normalized_allenstreetdb.csv'
df = pd.read_csv(csv_file_path)

# Concatenate all relevant columns into a single text string
df['combined_text'] = df.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# Initialize the tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Set the padding token
tokenizer.pad_token = tokenizer.eos_token

# Convert the DataFrame to a Dataset
dataset = Dataset.from_pandas(df[['combined_text']])

# Define the tokenize function
def tokenize_function(examples):
    encoding = tokenizer(examples['combined_text'], padding="max_length", truncation=True)
    encoding['labels'] = encoding['input_ids'].copy()
    encoding['attention_mask'] = encoding['attention_mask'].copy()
    return encoding

# Apply the tokenize function to the Dataset
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Split the dataset into training and validation sets
train_test_split = tokenized_dataset.train_test_split(test_size=0.2)
train_dataset = train_test_split['train']
val_dataset = train_test_split['test']

# Initialize the model
model = GPT2LMHeadModel.from_pretrained(model_name)

# Save the model and tokenizer
model.save_pretrained("./saved_model_gpt")
tokenizer.save_pretrained("./saved_model_gpt")

# Load the model and tokenizer
model_name_or_path = "./saved_model_gpt"
tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
model = GPT2LMHeadModel.from_pretrained(model_name_or_path)

# Move the model to the GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Function to generate text
def generate_text(prompt, max_length=100):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(device)
    outputs = model.generate(inputs['input_ids'], attention_mask=inputs['attention_mask'], max_length=max_length, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Interactive loop with wait function
while True:
    prompt = input("You: ")
    if prompt.lower() in ["exit", "quit"]:
        break
    print("Thinking...")
    time.sleep(10)  # Wait for 2 seconds to simulate thinking
    response = generate_text(prompt)
    print(f"Model: {response}")