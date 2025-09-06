from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

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

    classification_result = classifier(email_content)[0]
    label = classification_result['label'].upper()

    if label == 'POSITIVE':
        category = "PRODUTIVO"
        
        # suggested_response = RESPONSES["PRODUTIVO"]
        
        # Gerar uma resposta mais inteligente
        prompt = f"Responda ao seguinte e-mail de forma profissional: '{email_content}'"
        generated_response = generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']
        suggested_response = generated_response.strip()

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