from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
candidate_labels = ["produtivo", "improdutivo"]

generator = pipeline("text-generation", model="gpt2")

RESPONSES = {
    "PRODUTIVO": "Prezado, sua solicitação foi recebida e está em andamento. Em breve, enviaremos uma atualização.",
    "IMPRODUTIVO": "Obrigado pela sua mensagem! Tenha um ótimo dia."
}

@app.route('/classify_email', methods=['POST'])
def classify_email():
    if not request.json or 'email_content' not in request.json:
        return jsonify({'error': 'Nenhum conteúdo de e-mail fornecido'}), 400

    email_content = request.json['email_content']
    classification_result = classifier(email_content, candidate_labels)
    category = classification_result['labels'][0].upper()
    suggested_response = ""

    if category == 'PRODUTIVO':
        prompt = f"Responda ao seguinte e-mail de forma profissional: '{email_content}'"
        generated_response = generator(prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
        prompt_end_index = generated_response.find(email_content) + len(email_content)
        suggested_response = generated_response[prompt_end_index:].strip()        
        if len(suggested_response) < 20 or suggested_response.lower().startswith("Olá,"):
            suggested_response = RESPONSES["PRODUTIVO"]
    else:
        suggested_response = RESPONSES["IMPRODUTIVO"]

    response = {
        "category": category,
        "suggested_response": suggested_response
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)