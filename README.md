# Med_Bud

A chatbot designed to provide information about various medicines, including their descriptions, side effects, and more. Built using Streamlit and the Sentence Transformers library for natural language understanding, this chatbot is capable of answering specific queries and providing random medicine facts.

## Features

- **Query Handling:** Responds to user queries about specific tablets, including their uses, side effects, and interactions.
- **Random Facts:** Provides random facts about various tablets.
- **Jokes:** Includes fun medicine-related jokes for user engagement.
- **Chat History:** Saves chat history locally for future reference.
- **Embeddings Storage:** Utilizes local embeddings for efficient query processing.

## Technologies Used

- **Python:** The primary programming language.
- **Streamlit:** For building the web application interface.
- **Sentence Transformers:** For generating sentence embeddings to understand user queries.
- **Model Used:** paraphrase-albert-small-v2
- **Pandas:** For data manipulation and handling CSV data.
- **NumPy:** For numerical operations and embedding management.
- **Scikit-Learn:** For calculating cosine similarity.
- **FuzzyWuzzy:** For fuzzy string matching.

## Installation

1. **Clone the repository:**

   ```bash
   git clone <https://github.com/AbhinayaVeerapannei/Med_Bud.git>
   cd Med_Bud
   ```

2. **Install the required packages:**

   You can install the necessary Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Download the Sentence Transformer model:**

   ```bash
   python -m sentence_transformers download paraphrase-albert-small-v2
   ```

4. **Prepare the embeddings and CSV data:**

   Ensure that the embeddings and `medicine_data.csv` file are stored in the appropriate directories as specified in the code.

## Usage

1. **Run the Streamlit application:**

   ```bash
   streamlit run app.py
   ```

2. **Interact with the chatbot:**
   - Choose to ask about a specific tablet, get random tablet facts, or hear a medicine joke.
   - Enter your queries in the provided text input.

## Code Overview

### Main Components

- **`MedicineChatbot` class:**
  - Handles loading embeddings, processing queries, and generating responses based on user input.
  
- **Methods:**
  - `load_embeddings()`: Loads pre-computed embeddings from local storage.
  - `load_csv_data()`: Loads medicine data from a CSV file.
  - `get_query_embedding(query)`: Generates an embedding for the user's query.
  - `generate_response(query)`: Processes the query and generates a response based on intent detection and similarity matching.
  - `get_random_tablet_info()`: Provides random tablet information.

### Streamlit Application
- The application interface is built using Streamlit, allowing users to interact with the chatbot seamlessly.

## Chat History

The chatbot saves the chat history in a JSON file located on the user's desktop. This allows users to revisit their previous interactions.
