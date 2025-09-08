from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
candidate_labels = ["requer ação", "não requer ação", "comunicado"]

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
    
    predicted_label = classification_result['labels'][0]
    
     # Se a predição principal for "requer ação", é produtivo.
    if predicted_label == "requer ação":
        category = "PRODUTIVO"
        suggested_response = RESPONSES["PRODUTIVO"]
    # Caso contrário, consideramos improdutivo, mesmo que seja "comunicado"
    else:
        category = "IMPRODUTIVO"
        suggested_response = RESPONSES["IMPRODUTIVO"]

    response = {
        "category": category,
        "suggested_response": suggested_response
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)