from flask import Flask, request, render_template, jsonify
import pickle
import chromadb
import json
import logging
from groq import Groq
from sentence_transformers import SentenceTransformer
import mysql.connector
from mysql.connector import Error
import requests


app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

client = chromadb.Client()
collection = client.create_collection("my_chatbot_data")
groq_api = Groq(api_key="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")
embeddings = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def generate_embeddings(final_corpus):
    return embeddings.encode(final_corpus)

def prepare_embeddings(final_corpus):
    return generate_embeddings(final_corpus).tolist()

def query_chroma(query):
    query_embedding = prepare_embeddings([query])
    logging.debug(f"Query embedding: {query_embedding}")
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3,
    )
    
    if results and "metadatas" in results and results["metadatas"]:
        results = [data['Answer : '] for data in results["metadatas"][0]]
        logging.debug(f"ChromaDB query results: {results}")
        return results
    else:
        logging.debug("No results found in ChromaDB.")
        return ["No relevant context found."]

def llm_response(question):
    context = '-----'.join(query_chroma(question))
    logging.debug(f"Context for LLM: {context}")
    
    chat_completion = groq_api.chat.completions.create(
        messages=[
            {
            "role": "system",
            "content": "You are an AI assistant designed to assist users with questions related to the Indian Aviation Academy. When asked about job or internship opportunities, ask for specific details such as the type of role, desired position, and area of interest before providing relevant and concise information. Ensure that all answers are directly aligned with the user’s request and focus on addressing their needs with accuracy and clarity."
            },

            {
                "role": "user",
                "content": f"This is the question asked by user {question} and the context given is {context}. Answer this question based on the context provided",
            }
        ],
        model="llama-3.1-70b-versatile",
    )
    logging.debug(f"LLM response: {chat_completion.choices[0].message.content}")
    return chat_completion.choices[0].message.content

def prepare_docs(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    final_corpus = [line.strip() for line in lines if line.strip()]
    metadata = [{'Answer : ': line.strip()} for line in lines if line.strip()]
    
    return final_corpus, metadata

# MySQL database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # or your DB host
            database='chatbot_db',
            user='root',
            password='MySQL'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    

# Route to receive and store feedback
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    user_feedback = data['feedback']
    
    # Save the feedback to the MySQL database
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        insert_query = """INSERT INTO feedback (user_feedback) VALUES (%s)"""
        cursor.execute(insert_query, (user_feedback,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Feedback submitted successfully!"})
    else:
        return jsonify({"message": "Failed to submit feedback"}), 500

@app.route('/')
def index():
    return render_template('aai.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    user_input = data['message']  # Updated key to match the HTML
    logging.debug(f"User input: {user_input}")
    
    prediction = llm_response(user_input)
    logging.debug(f"Prediction: {prediction}")
    
    return jsonify({'reply': prediction})  # Updated key to 'reply'

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/get_internships', methods=['GET'])
def get_internships():
    lng = request.args.get('lng')
    lat = request.args.get('lat')
    
    # Reverse geocode to get the city name using Mapbox API
    mapbox_token = "pk.eyJ1IjoiYXRoYXJ2dmlpdCIsImEiOiJjbHlxYWkwZGYweWJ2MmxvaXFnenBrY2l2In0.xi6flE6wLdkrAb25XTskhA"
    geocode_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{lng},{lat}.json?access_token={mapbox_token}&types=place&limit=1"
    geocode_response = requests.get(geocode_url)
    geocode_data = geocode_response.json()
    
    if geocode_data["features"]:
        city_name = geocode_data["features"][0]["text"]

        # Query your database or collection for internships in the city
        internships = find_internships_by_city(city_name)
        return jsonify({"city": city_name, "internships": internships})
    else:
        return jsonify({"message": "City not found"}), 404

# Example function to find internships in a specific city
def find_internships_by_city(city_name):
    # Replace this with an actual database query or logic to retrieve internships
    internships = ["Internship 1", "Internship 2", "Internship 3"]  # Example data
    return internships

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

# edit file
@app.route('/edit_sample', methods=['GET'])
def edit_sample():
    try:
        # Load the contents of the sample.txt file
        with open(r"E:\download folder\IAA (3)\IAA\IAA\wbot\New folder (2)\samp.txt") as file:
            file_content = file.read()
        return file_content  # Return raw file content
    except Exception as e:
        logging.error(f"Error loading samp.txt: {e}")
        return "Error loading file", 500


@app.route('/save_sample', methods=['POST'])
def save_sample():
    try:
        # Get the edited content from the form
        new_content = request.form['file_content']
        logging.debug(f"New content to be saved: {new_content}")
        
        # Save the new content back to sample.txt
        with open(r"E:\download folder\IAA (3)\IAA\IAA\wbot\New folder (2)\samp.txt","w") as file:
            file.write(new_content)
        logging.debug("New content saved to sample.txt.")
        return jsonify({'message': 'File saved successfully!'}), 200
    except Exception as e:
        logging.error(f"Error saving sample.txt: {e}")
        return jsonify({'message': 'Failed to save file'}), 500
# edit file end


# @app.route('/feedback', methods=['POST'])
# def feedback():
#     data = request.get_json()
#     user_feedback = data.get('feedback')
#     logging.debug(f"User feedback: {user_feedback}")
    
#     # Store feedback in a file or database (here we simply log it)
#     with open("feedback.txt", "a") as f:
#         f.write(user_feedback + "\n")
    
#     return jsonify({'message': 'Thank you for your feedback!'})


if __name__ == "__main__":
    final_corpus, metadata = prepare_docs(r"D:\4th year project\IAA (3)\IAA\IAA\wbot\New folder (2)\samp.txt")
    embedded_vectors = prepare_embeddings(final_corpus)
    ids = [f"doc_{i}" for i in range(len(embedded_vectors))]
    
    collection.add(ids=ids, embeddings=embedded_vectors, metadatas=metadata)
    app.run(debug=True)
