import csv
import logging
from collections import deque
import asyncio
import openai
import tracemalloc  # Use the standard tracemalloc module
import sqlite3

# Initialize Tracemalloc
tracemalloc.start()

# Set your OpenAI API key directly in the code
openai.api_key = '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'

def load_csv_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = [row for row in reader]
        return data
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        logging.error(f"Failed to load CSV file at path '{file_path}': {str(e)}")
        raise  # Re-raise the exception to propagate it up

def create_in_memory_db(data):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE data (
        source_document TEXT,
        southern_cross_street_of_block TEXT,
        northern_cross_street_of_block TEXT,
        house_number TEXT,
        family_number TEXT,
        relationship_to_head_of_household TEXT,
        surname TEXT,
        given_name TEXT,
        birthplace TEXT,
        sex TEXT,
        year_born INTEGER,
        age INTEGER,
        year_arrived INTEGER,
        years_in_usa INTEGER,
        citizen_alien TEXT,
        occupation TEXT,
        business TEXT,
        further_comments TEXT
    )
    ''')
    for row in data[1:]:  # Skip header row
        cursor.execute('''
        INSERT INTO data (source_document, southern_cross_street_of_block, northern_cross_street_of_block, house_number, family_number, relationship_to_head_of_household, surname, given_name, birthplace, sex, year_born, age, year_arrived, years_in_usa, citizen_alien, occupation, business, further_comments)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [None if field == '' else field for field in row])
    conn.commit()
    return conn

def count_tokens(messages):
    """Estimate the number of tokens in a list of messages."""
    return sum(len(message['content'].split()) for message in messages)

class ChatBot:
    def __init__(self, db_conn):
        self.message_queue = deque()
        self.response_queue = deque()
        self.client = openai
        self.db_conn = db_conn

    async def assistant(self, user_message):
        """Retrieve and execute the GPT model."""
        # Truncate the message queue to fit within the token limit
        max_tokens = 16385
        truncated_message_queue = list(self.message_queue)
        while count_tokens(truncated_message_queue) > max_tokens:
            truncated_message_queue.pop(0)
        response = await self.client.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=truncated_message_queue
        )
        return response

    async def chatbot_response(self, user_message):
        """
        Process a user message within the context of the conversation.
        Returns the bot's response after processing the message.
        """
        try:
            # Ensure messages are properly formatted
            if isinstance(user_message, str):
                self.message_queue.append({
                    "role": "user",
                    "content": user_message
                })
                logging.info(f"Processing user message: {user_message}")

                # Get completion from OpenAI and await the response
                completion = await self.assistant(user_message)
                response = completion.choices[0].message['content']

                # Add to message history
                self.message_queue.append({
                    "role": "assistant",
                    "content": response
                })

                logging.info(f"Bot response generated: {response}")

                # Get current memory usage
                current, peak = tracemalloc.get_traced_memory()
                memory_usage_info = f"Current memory usage: {current / 1024 / 1024:.2f} MB; Peak: {peak / 1024 / 1024:.2f} MB"

                # Include memory usage information in the response
                response_with_memory = f"{response}\n\n{memory_usage_info}"

                return response_with_memory
            else:
                raise TypeError("User message must be a string.")

        except Exception as e:
            print(f"Error processing message: {str(e)}")
            raise

    async def send_message_to_queue(self, user_message):
        """
        Send a message into the conversation queue.
        Returns True if successful, False otherwise.
        """
        try:
            # Simulate sending the message to the database
            self.message_queue.append({
                "role": "user",
                "content": user_message
            })
            
            logging.info(f"Message sent by user: {user_message}")
            
            return True
        except Exception as e:
            print(f"Failed to send message: {str(e)}")
            logging.error(f"Error sending message: {e}")
            raise

    async def get_conversation_history(self):
        """
        Retrieve the conversation history from the database.
        Returns a list of messages in chronological order.
        """
        try:
            pass  # Implement actual database retrieval logic here
            
            logging.info("Successfully retrieved conversation history")
            
            return self.message_queue

        except Exception as e:
            print(f"Error fetching conversation history: {str(e)}")
            raise

    async def respond_to_conversation(self, user_message):
        """
        Retrieve the conversation history and generate a response.
        Returns the full conversation including user messages and bot responses.
        """
        try:
            # Simulate retrieving data from the database
            conversation_history = await self.get_conversation_history()
            
            logging.info("Generated conversation history")
            
            return conversation_history

        except Exception as e:
            print(f"Error responding to conversation: {str(e)}")
            raise

    async def execute_sql_query(self, query):
        """
        Execute an SQL query on the database.
        Returns the query result.
        """
        try:
            result = self.sql_chain.run(query)
            return result
        except Exception as e:
            print(f"Error executing SQL query: {str(e)}")
            raise

async def main():
    normalized_data = load_csv_data("normalized_allenstreetdb.csv")
    db_conn = create_in_memory_db(normalized_data)
    # Initialize chatbot
    chatbot = ChatBot(db_conn)
    # Set initial context from CSV data
    context = " ".join([" ".join(row) for row in normalized_data[1:]])  # Combine all rows into a single string, skip header

    # Truncate context to fit within the token limit
    max_tokens = 16385
    context_tokens = context.split()
    if len(context_tokens) > max_tokens:
        context = " ".join(context_tokens[-max_tokens:])

    # Add a system message to describe the data
    description = "This data is about Allen Street in 1905, including information from the NYC census and Trow's directory."
    chatbot.message_queue.append({"role": "system", "content": description})
    chatbot.message_queue.append({"role": "system", "content": context})

    print("ChatBot is ready. Type 'exit' to quit.")
    while True:
        user_message = input("You: ")
        if user_message.lower() == 'exit':
            break
        if user_message.lower().startswith("sql:"):
            query = user_message[4:].strip()
            result = await chatbot.execute_sql_query(query)
            print(f"SQL Result: {result}")
        else:
            bot_response = await chatbot.chatbot_response(user_message)
            print(f"Bot: {bot_response}")

if __name__ == "__main__":
    asyncio.run(main())

# Stop Tracemalloc and display memory usage
tracemalloc.stop()
print(tracemalloc.get_traced_memory())