import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Load the model and tokenizer
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained("./saved_model")

# Create a pipeline for text classification
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

# Define responses based on labels
responses = {
    "LABEL_0": "It seems like you're talking about occupation.",
    "LABEL_1": "This looks like a discussion about citizenship status.",
    # Add more responses based on your labels
}

def chat_with_model():
    print("Chatbot is ready! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = classifier(user_input)
        label = response[0]['label']
        print(f"Model: {responses.get(label, 'I am not sure about that.')}")
        
if __name__ == "__main__":
    chat_with_model()