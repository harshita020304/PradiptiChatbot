from flask import Flask, request, render_template
import pickle
import chromadb
import json
from groq import Groq
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# Load the notebook content from the .pkl file (if applicable)
# with open('notebook_content.pkl', 'rb') as f:
#     notebook_content = pickle.load(f)

# Initialize ChromaDB and other components
client = chromadb.Client()
collection = client.create_collection("my_chatbot_data")
groq_api = Groq(api_key="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")
embeddings = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Function to generate embeddings
def generate_embeddings(final_corpus):
    return embeddings.encode(final_corpus)

# Function to prepare embeddings for a query
def prepare_embeddings(final_corpus):
    return generate_embeddings(final_corpus).tolist()

# Function to query ChromaDB
def query_chroma(query):
    query_embedding = prepare_embeddings([query])  # Ensure query is a list
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3,
    )
    results = [data['Answer : '] for data in results["metadatas"][0]]
    return results

# Function to get the response from the LLM
def llm_response(question):
    context = '-----'.join(query_chroma(question))
    chat_completion = groq_api.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"This is the question asked by user {question} and the context given is {context}. Answer this question based on the context provided",
            }
        ],
        model="llama-3.1-70b-versatile",
    )
    return chat_completion.choices[0].message.content

# Function to process input using the notebook content (LLM)
def process_input_with_notebook(input_query):
    return llm_response(input_query)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get user input from the form
    user_input = request.form['query']

    # Process the input query using the notebook content
    prediction = process_input_with_notebook(user_input)

    # Display the prediction on the result page
    return render_template('recommendation.html', prediction=prediction)

if __name__ == "__main__":
    # Prepare and add data to ChromaDB
    final_corpus, metadata = prepare_docs("D:\New folder (2)p\sample.txt")  # Adjust path as needed
    embedded_vectors = prepare_embeddings(final_corpus)

    # Generate unique IDs for each document
    ids = [f"doc_{i}" for i in range(len(embedded_vectors))]

    # Add data to the ChromaDB collection with IDs
    collection.add(ids=ids, embeddings=embedded_vectors, metadatas=metadata)
    
    app.run(debug=True)
