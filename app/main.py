import json
from flask import Flask, request, jsonify, render_template
from transformers import GPT2TokenizerFast, GPT2LMHeadModel
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Flask app setup
app = Flask(__name__, template_folder='templates', static_folder='static')

# Load doctor schedules data
try:
    with open('data/schedules.json') as f:
        schedules = json.load(f)
except FileNotFoundError:
    logging.error("File schedules.json tidak ditemukan!")
    schedules = []

bookings = []  # List untuk menyimpan data booking

# Hugging Face GPT Model Setup
model_name = "w11wo/indo-gpt2-small" #Ganti model ini dengan fine-tuning hasil trainer.py
tokenizer = GPT2TokenizerFast.from_pretrained(model_name)
tokenizer.model_max_length = 1024
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

def ask_indogpt(question):
    """Generate response using GPT model."""
    if tokenizer is None or model is None:
        return "Model tidak tersedia saat ini."
    try:
        inputs = tokenizer(question, return_tensors="pt", padding=True, truncation=True, max_length=512)
        outputs = model.generate(inputs['input_ids'], attention_mask=inputs['attention_mask'], 
        #pad_token_id=50256,
                                do_sample=True, 
                                max_length=100, 
                                min_length=50,
                                top_k=50,
                                pad_token_id=tokenizer.eos_token_id,
                                num_return_sequences=1)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        logging.error(f"Error saat menghasilkan respons chatbot: {e}")
        return "Maaf, terjadi kesalahan pada chatbot."

# Load RAG system
try:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    retriever = FAISS.load_local("data/faiss_index", embeddings, allow_dangerous_deserialization=True)
except Exception as e:
    logging.error(f"Error saat memuat FAISS index: {e}")
    retriever = None

@app.route('/')
def home():
    """Render the home page."""
    return render_template("index.html")

@app.route('/search_schedule', methods=['GET'])
def search_schedule():
    try:
        doctor = request.args.get('doctor')
        specialty = request.args.get('specialty')

        results = []
        for schedule in schedules:
            if doctor and schedule['doctor'].lower() == doctor.lower():
                results.append(schedule)
            elif specialty and schedule['specialty'].lower() == specialty.lower():
                results.append(schedule)

        return jsonify(results)
    except Exception as e:
        logging.error(f"Error saat mencari jadwal: {e}")
        return jsonify({"error": "Terjadi kesalahan saat mencari jadwal."}), 500

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    """Book an appointment with a doctor."""
    try:
        data = request.json
        booking = {
            "doctor": data['doctor'],
            "date": data['date'],
            "time": data['time'],
            "patient_name": data['patient_name']
        }

        # Check for conflicts with existing bookings
        for b in bookings:
            if b['doctor'] == booking['doctor'] and b['date'] == booking['date'] and b['time'] == booking['time']:
                return jsonify({"message": "Time slot already booked!"}), 409

        bookings.append(booking)
        return jsonify({"message": "Booking successful!", "booking": booking})
    except Exception as e:
        logging.error(f"Error saat melakukan booking: {e}")
        return jsonify({"error": "Terjadi kesalahan saat melakukan booking."}), 500

@app.route('/booking_history', methods=['GET'])
def booking_history():
    """View booking history."""
    try:
        return jsonify({"bookings": bookings})
    except Exception as e:
        logging.error(f"Error saat mengambil riwayat booking: {e}")
        return jsonify({"error": "Terjadi kesalahan saat mengambil riwayat booking."}), 500

@app.route('/ask_bot', methods=['POST'])
def ask_bot():
    """Handle chatbot questions."""
    try:
        data = request.json
        question = data['question']
        response = ask_indogpt(question)
        return jsonify({"response": response})
    except Exception as e:
        logging.error(f"Error saat menggunakan chatbot: {e}")
        return jsonify({"error": "Terjadi kesalahan pada chatbot."}), 500

@app.route('/get_health_tips', methods=['GET'])
def get_health_tips():
    """Retrieve health tips using RAG."""
    try:
        query = request.args.get('query')
        if retriever is None:
            return jsonify({"error": "RAG system tidak tersedia saat ini."}), 500
        response = retriever.similarity_search(query, k=1)  # Mengambil 3 dokumen paling relevan
        tips = [doc.page_content for doc in response]
        return jsonify({"tips": tips})
    except Exception as e:
        logging.error(f"Error saat mencari tips kesehatan: {e}")
        return jsonify({"error": "Terjadi kesalahan saat mencari tips kesehatan."}), 500

if __name__ == '__main__':
    app.run(debug=True)


