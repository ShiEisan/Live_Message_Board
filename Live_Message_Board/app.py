from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 資料表
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# 首頁（顯示留言牆）
@app.route('/')
def index():
    return render_template('index.html')

# 取得所有留言
@app.route('/api/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    data = [
        {
            "id": msg.id,
            "name": msg.name,
            "content": msg.content,
            "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for msg in messages
    ]
    return jsonify(data)

# 新增留言
@app.route('/api/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    name = data.get('name', '').strip()
    content = data.get('content', '').strip()

    if not name or not content:
        return jsonify({"error": "Name and content are required"}), 400

    new_msg = Message(name=name, content=content)
    db.session.add(new_msg)
    db.session.commit()
    return jsonify({"message": "Message created"}), 201

if __name__ == '__main__':
    app.run(debug=True)
