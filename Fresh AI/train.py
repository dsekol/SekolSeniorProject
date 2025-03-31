import pandas as pd
import torch
from transformers import BertTokenizer, BertForMaskedLM
import sympy
import os

# Load your CSV file
df = pd.read_csv('normalized_allenstreetdb.csv')

# Create a new column that combines the text columns
text_columns = ['surname', 'given name', 'birthplace (if resident)', 'occupation']

# Check if all columns exist in the DataFrame
for col in text_columns:
    if col not in df.columns:
        print(f"Column '{col}' does not exist in the DataFrame.")
        # You can either remove the column from text_columns or handle the missing column in some other way

# Create a new column that combines the text columns
df['text'] = df.apply(lambda row:''.join([str(row[col]) if col in row else '' for col in text_columns]), axis=1)

# Create a custom dataset class
class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, df, tokenizer):
        self.df = df
        self.tokenizer = tokenizer

    def __getitem__(self, idx):
        text = self.df.iloc[idx]['text']
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=512,
            return_attention_mask=True,
            return_tensors='pt',
            truncation=True,
            padding='max_length'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': encoding['input_ids'].flatten()  # Use the input IDs as labels for masked language modeling
        }

    def __len__(self):
        return len(self.df)

# Create a data loader
batch_size = 32
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
dataset = CustomDataset(df, tokenizer)
data_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Train your BERT model
model = BertForMaskedLM.from_pretrained('bert-base-uncased')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

# Create a directory to save the model
save_dir ='saved_model'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

for epoch in range(5):
    model.train()
    total_loss = 0
    for batch in data_loader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)  # Use the input IDs as labels for masked language modeling

        optimizer.zero_grad()

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss

        loss.backward()
        optimizer.step()

        total_loss += loss.item()
    print(f'Epoch {epoch+1}, Loss: {total_loss / len(data_loader)}')

    # Save the model after each epoch
    torch.save(model.state_dict(), os.path.join(save_dir, f'model_epoch_{epoch+1}.pth'))
    print(f'Model saved to {save_dir} after epoch {epoch+1}')

# Save the final model
torch.save(model.state_dict(), os.path.join(save_dir, 'final_model.pth'))
print(f'Final model saved to {save_dir}')