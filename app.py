import os
import random
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import nltk
import ssl
import csv
import datetime


ssl._create_default_https_context = ssl._create_unverified_context
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

# Define intents (sample for the chatbot)
intents =[
    {
        "tag": "Science Fiction",
        "patterns": ["Tell me about sci-fi books", "What are some science fiction books?", "Suggest a sci-fi books", "Sci-fi books","Sci-fi","Science Fiction","sci-fi"],
        "responses": [
            "Dune by Frank Herbert", 
            "The Martian by Andy Weir", 
            "Ender's Game by Orson Scott Card", 
            "Neuromancer by William Gibson", 
            "Snow Crash by Neal Stephenson", 
            "The Left Hand of Darkness by Ursula K. Le Guin"
        ]
    },
    {
        "tag": "Fantasy",
        "patterns": ["Tell me about fantasy books", "What are some fantasy books?", "Suggest fantasy books","fantasy","Fantasy","fantasy books"],
        "responses": [
            "Harry Potter by J.K. Rowling", 
            "The Hobbit by J.R.R. Tolkien", 
            "A Song of Ice and Fire by George R.R. Martin", 
            "The Name of the Wind by Patrick Rothfuss", 
            "Mistborn by Brandon Sanderson", 
            "The Lies of Locke Lamora by Scott Lynch"
        ]
    },
    {
        "tag": "Mystery",
        "patterns": ["Tell me about mystery books", "What are some mystery books?","Mystery", "Suggest a mystery book", "mystery","mystery books","suspense"],
        "responses": [
            "The Girl with the Dragon Tattoo by Stieg Larsson", 
            "Gone Girl by Gillian Flynn", 
            "Sherlock Holmes by Arthur Conan Doyle", 
            "Big Little Lies by Liane Moriarty", 
            "The Woman in White by Wilkie Collins", 
            "In the Woods by Tana French"
        ]
    },
    {
        "tag": "Romance",
        "patterns": ["Tell me about romance books","romance", "What are some romance books?", "Suggest a romance book", "love","Romance books","Romance"],
        "responses": [
            "Pride and Prejudice by Jane Austen", 
            "Me Before You by Jojo Moyes", 
            "The Notebook by Nicholas Sparks", 
            "The Fault in Our Stars by John Green", 
            "Outlander by Diana Gabaldon", 
            "The Rosie Project by Graeme Simsion"
        ]
    },
    {
        "tag": "Horror",
        "patterns": ["Tell me about horror books", "What are some horror books?","Horror", "scary books","fear", "Suggest a horror book"],
        "responses": [
            "It by Stephen King", 
            "The Haunting of Hill House by Shirley Jackson", 
            "Dracula by Bram Stoker", 
            "The Shining by Stephen King", 
            "Bird Box by Josh Malerman", 
            "World War Z by Max Brooks"
        ]
    },
    {
        "tag": "Non-fiction",
        "patterns": ["Tell me about non-fiction books", "What are some non-fiction books?", "Suggest a non-fiction book","Non-fiction books","realistic"],
        "responses": [
            "Sapiens by Yuval Noah Harari", 
            "Educated by Tara Westover", 
            "Becoming by Michelle Obama", 
            "The Immortal Life of Henrietta Lacks by Rebecca Skloot", 
            "Quiet by Susan Cain", 
            "Thinking, Fast and Slow by Daniel Kahneman"
        ]
    },
    {
        "tag": "Biography",
        "patterns": ["Tell me about biography books", "What are some biographies?", "Suggest a biography","autobiography","biography books"],
        "responses": [
            "The Diary of a Young Girl by Anne Frank", 
            "Steve Jobs by Walter Isaacson", 
            "Long Walk to Freedom by Nelson Mandela", 
            "I Am Malala by Malala Yousafzai", 
            "The Glass Castle by Jeannette Walls", 
            "Alexander Hamilton by Ron Chernow"
        ]
    },
    {
        "tag": "Self-Help",
        "patterns": ["Tell me about self-help books", "What are some self-help books?", "Suggest a self-help book","self-care"],
        "responses": [
            "Atomic Habits by James Clear", 
            "The Power of Habit by Charles Duhigg", 
            "The Subtle Art of Not Giving a F*ck by Mark Manson", 
            "How to Win Friends and Influence People by Dale Carnegie", 
            "You Are a Badass by Jen Sincero", 
            "Grit by Angela Duckworth"
        ]
    },
    {
        "tag": "Historical Fiction",
        "patterns": ["Tell me about historical fiction books","history","What are some historical fiction books?", "Suggest a historical fiction book","historical"],
        "responses": [
            "The Nightingale by Kristin Hannah", 
            "All the Light We Cannot See by Anthony Doerr", 
            "The Book Thief by Markus Zusak", 
            "The Tattooist of Auschwitz by Heather Morris", 
            "The Pillars of the Earth by Ken Follett", 
            "The Help by Kathryn Stockett"
        ]
    },
    {
        "tag": "Thriller",
        "patterns": ["Tell me about thriller books", "What are some thriller books?", "Suggest a thriller book","thrillers"],
        "responses": [
            "The Silent Patient by Alex Michaelides", 
            "The Girl on the Train by Paula Hawkins", 
            "Behind Closed Doors by B.A. Paris", 
            "Gone Girl by Gillian Flynn", 
            "The Woman in the Window by A.J. Finn", 
            "Big Little Lies by Liane Moriarty"
        ]
    },
    {
        "tag": "Young Adult",
        "patterns": ["Tell me about young adult books", "What are some young adult books?", "Suggest a young adult book"],
        "responses": [
            "The Hunger Games by Suzanne Collins", 
            "The Fault in Our Stars by John Green", 
            "Divergent by Veronica Roth", 
            "The Perks of Being a Wallflower by Stephen Chbosky", 
            "The Maze Runner by James Dashner", 
            "Eleanor & Park by Rainbow Rowell"
        ]
    },
    {
        "tag": "Classic Literature",
        "patterns": ["Tell me about classic books", "What are some classics?", "Suggest a classic book","literature"],
        "responses": [
            "The Merchant of Venice by William Shakespeare",
            "To Kill a Mockingbird by Harper Lee", 
            "1984 by George Orwell", 
            "Moby Dick by Herman Melville", 
            "Pride and Prejudice by Jane Austen", 
            "The Great Gatsby by F. Scott Fitzgerald", 
            "Frankenstein by Mary Shelley"
        ]
    },
    {
        "tag": "Comedy",
        "patterns": [
            "Tell me about comedy books", 
            "What are some comedy books?", 
            "Suggest a comedy book", 
            "Comedy books", 
            "Funny books", 
            "Books for a laugh"
        ],
        "responses": [
            "The Hitchhiker's Guide to the Galaxy by Douglas Adams", 
            "Good Omens by Neil Gaiman and Terry Pratchett", 
            "Catch-22 by Joseph Heller", 
            "The Rosie Project by Graeme Simsion", 
            "Bossypants by Tina Fey", 
            "Me Talk Pretty One Day by David Sedaris"
        ]
    },
    {
        "tag": "Tragedy",
        "patterns": [
            "Tell me about tragedy books", 
            "What are some tragedy books?", 
            "Suggest a tragedy book", 
            "Tragic books", 
            "Books with tragic endings", 
            "Heartbreaking books"
         ],
        "responses": [
            "Romeo and Juliet by William Shakespeare", 
            "Of Mice and Men by John Steinbeck", 
            "The Fault in Our Stars by John Green", 
            "Atonement by Ian McEwan", 
            "The Book Thief by Markus Zusak", 
            "The Kite Runner by Khaled Hosseini"
        ]
    }
]


# Create the vectorizer and classifier
vectorizer = TfidfVectorizer()
clf = LogisticRegression(random_state=0, max_iter=10000)

# Preprocess the data
tags = []
patterns = []
for intent in intents:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)

# Train the model
x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

# Track the last response for each tag to avoid repetition
last_responses = {}

# Ensure that the chat_log.csv file exists, create it if not
if not os.path.exists('chat_log.csv'):
    with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])

# Chatbot function to generate responses
def chatbot(input_text):
    global last_responses

    # Handle direct "bye" or "goodbye" inputs
    if input_text.lower() in ["bye", "goodbye","thank you","thanks"]:
        return "Thank you for chatting with me. Have a great day!"

    # Transform the user input and predict the tag
    input_text_vectorized = vectorizer.transform([input_text])
    tag = clf.predict(input_text_vectorized)[0]

    # Find the intent corresponding to the tag
    for intent in intents:
        if intent["tag"] == tag:
            responses = intent["responses"]

            # If the tag has been responded to before, remove the last response from the options
            if tag in last_responses and last_responses[tag] in responses:
                responses = [resp for resp in responses if resp != last_responses[tag]]

            # Choose a new response randomly
            response = random.choice(responses)

            # Update the last response for this tag
            last_responses[tag] = response
            return response


# Main Streamlit App
def main():
    st.title("LIBRARY CHATBOT")

    # Create a sidebar for navigation
    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Home Page - User Chat Input
    if choice == "Home":
        st.write("Welcome to the library book recommendation chatbot. Please enter the genre to get a recommendation on the books.")

        user_input = st.text_input("You:")

        if user_input:
            response = chatbot(user_input)

            # Get the current timestamp
            timestamp = datetime.datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")

            # Save the user input and chatbot response to the chat_log.csv file
            with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([user_input, response, timestamp])

            st.text_area("Chatbot:", value=response, height=100, max_chars=None)

            if response.lower() in ['goodbye', 'bye']:
                st.write("Thank you for chatting with me. Have a great day!")
                st.stop()

    # Conversation History Page
    elif choice == "Conversation History":
        st.header("Conversation History")
        st.write("Here is the history of your conversation with the chatbot:")

        # Display conversation history from chat_log.csv
        with open('chat_log.csv', 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                st.text(f"User: {row[0]}")
                st.text(f"Chatbot: {row[1]}")
                st.text(f"Timestamp: {row[2]}")
                st.markdown("---")

    # About Page
    elif choice == "About":
        st.header("Book Recommendation Chatbot using NLP")
        st.write("""
        The goal of this project is to create a book recommendation chatbot that can respond to the user inputs based on book genres. 
        The chatbot is built using Natural Language Processing (NLP) techniques and **Logistic Regression** to extract the intent 
        and provide relevant book recommendations from predefined categories. 
        """)

        st.subheader("Project Overview:")

        st.write("""
        The project consists of two main components:
        
        1. **NLP and Machine Learning Model:**
            - **Text Preprocessing**: The input text is preprocessed using **TF-IDF Vectorization** to convert the raw text into numerical features that the model can understand.
            - **Logistic Regression Model**: The model is trained on labeled intents such as **Science Fiction**, **Fantasy**, and other genres to classify the user's input into relevant categories and provide a corresponding response.
    
        2. **Streamlit Web Application**:
            - The **Streamlit** interface is designed to facilitate real-time user interaction. Users can input their queries, and the chatbot responds with book recommendations based on the identified genre. It also keeps track of the conversation history and displays past exchanges.
        """)
    
        st.subheader("Dataset:")
    
        st.write("""
        The dataset used for training the model is a collection of labeled intents and user patterns. The data is structured as follows:
        
        - **Intents**: The category or genre of the user's request (e.g., **Science Fiction**, **Fantasy**).
        - **Patterns**: The phrases or questions a user might ask related to a specific genre (e.g., "Tell me about sci-fi books", "What are some fantasy books?").
        - **Responses**: Predefined responses (e.g., specific book recommendations like *Dune*, *Harry Potter*).
        
        The data is manually curated to reflect the types of user input and expected responses for different genres.
        """)
    
        st.subheader("Streamlit Chatbot Interface:")
    
        st.write("""
        The chatbot interface is developed using **Streamlit**, providing an interactive platform where users can:
        - **Input Text**: Users type their queries or requests in a text box.
        - **Chatbot Responses**: The chatbot generates responses based on the trained model, displaying relevant book suggestions for the queried genre.
        - **Conversation History**: Users can view past interactions with the chatbot in the conversation history section, ensuring a seamless user experience.
        """)
    
        st.subheader("Conclusion:")

        st.write("""
        In this project, a chatbot is created that effectively understands and responds to user input based on the intent, 
        specifically recommending books from different genres. The chatbot uses **Natural Language Processing** and **Logistic Regression** 
        for intent classification, and **Streamlit** for the user interface. 
        """)
    

if __name__ == '__main__':
    main()
