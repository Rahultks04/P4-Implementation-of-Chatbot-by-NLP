# Library Chatbot using NLP

## Overview

This project implements a **library chatbot** using **Natural Language Processing (NLP)** techniques. The chatbot provides book recommendations based on various genres and leverages machine learning for intent recognition. It uses the `nltk` library for text preprocessing, `scikit-learn` for intent classification, and `streamlit` for an interactive user interface.

---

## Features

- **Genre-Based Recommendations**: Suggests books from genres like Science Fiction, Fantasy, Romance, and more.
- **Intent Recognition**: Understands user input using machine learning and provides appropriate responses.
- **Interactive Web Interface**: Built with `streamlit` for an easy-to-use web application.
- **Customizable Intents**: Supports modification of intents and responses through code adjustments.

---

## Technologies Used

- **Python**: Core programming language.
- **NLTK**: Natural Language Toolkit for text processing.
- **Scikit-learn**: Machine learning library for intent classification.
- **Streamlit**: Web app framework for the chatbot interface.

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```
### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
```
On macOS/Linux:

```bash
source venv/bin/activate
```
On Windows:

```bash
venv\Scripts\activate
```

### 3. Install Required Packages:

```bash
pip install -r requirements.txt
```

### 4. Download NLTK Data

Launch Python and download the required NLTK data

```bash
import nltk nltk.download('punkt')
```

---

## Usage

### Run the chatbot application:

```bash
streamlit run app.py
```

### Interaction:

- Open the chatbot interface in your browser.
- Type a genre (e.g., "Suggest a Sci-fi book") and press Enter.
- The chatbot will recommend a book from the requested genre.

---

## Intents Data

The chatbot's intents are predefined in the `intents` variable in `app.py`. Each intent includes:
- **Tag**: A unique identifier for the intent.
- **Patterns**: User phrases to trigger the intent.
- **Responses**: A list of possible chatbot responses.

You can customize these intents by editing the code to add new genres or modify existing responses.

---

## Acknowledgments

- **NLTK**: For robust natural language processing capabilities.
- **Scikit-learn**: For implementing intent classification.
- **Streamlit**: For a simple and intuitive user interface.

