from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# Загружаем данные об экспонатах
def load_exhibits():
    with open('exhibits.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['exhibits']

# Главная страница - список всех экспонатов
@app.route('/')
def index():
    exhibits = load_exhibits()
    return render_template('index.html', exhibits=exhibits)

# Страница отдельного экспоната
@app.route('/exhibit/<int:exhibit_id>')
def exhibit(exhibit_id):
    exhibits = load_exhibits()
    # Находим нужный экспонат
    exhibit_data = None
    for ex in exhibits:
        if ex['id'] == exhibit_id:
            exhibit_data = ex
            break
    
    if exhibit_data:
        return render_template('exhibit.html', exhibit=exhibit_data)
    else:
        return "Экспонат не найден", 404

# Простой API для получения списка экспонатов (можно использовать для мобильного приложения)
@app.route('/api/exhibits')
def api_exhibits():
    exhibits = load_exhibits()
    return jsonify(exhibits)

# API для поиска экспонатов
@app.route('/api/search')
def search():
    query = request.args.get('q', '').lower()
    exhibits = load_exhibits()
    
    results = []
    for ex in exhibits:
        if (query in ex['title'].lower() or 
            query in ex['description'].lower() or
            query in ex['location'].lower()):
            results.append(ex)
    
    return jsonify(results)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
