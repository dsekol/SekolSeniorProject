import pandas as pd
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset
import torch

# Load the CSV file
df = pd.read_csv('normalized_allenstreetdb.csv')

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
    return encoding

# Apply the tokenize function to the Dataset
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Split the dataset into training and validation sets
train_test_split = tokenized_dataset.train_test_split(test_size=0.2)
train_dataset = train_test_split['train']
val_dataset = train_test_split['test']

# Set up training arguments
training_args = TrainingArguments(
    output_dir="./results_gpt",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Initialize the model
model = GPT2LMHeadModel.from_pretrained(model_name)

# Move the model to the GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# Start training
trainer.train()

# Evaluate the model
eval_results = trainer.evaluate()
trainer.save_model("./saved_model_gpt")

print(eval_results)