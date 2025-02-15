from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Flaskアプリケーションの初期化
app = Flask(__name__)

# Configクラスの定義(dockerで起動しているPostgreの接続)
class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://sample_user:sample_pass@localhost:5432/sample_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configクラスを直接使用して設定
app.config.from_object(Config)

# SQLAlchemyの初期化
db = SQLAlchemy(app)

# Userモデルの定義
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

# CRUDエンドポイントの定義

# Create: ユーザーを追加
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": f"User {name} added successfully"}), 201

# Read: 全てのユーザーを取得
@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    return jsonify(result), 200

# Update: ユーザー情報を更新
@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)

    db.session.commit()
    return jsonify({"message": f"User {user.id} updated successfully"}), 200

# Delete: ユーザーを削除
@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {user.id} deleted successfully"}), 200

# アプリケーションの起動
@app.route('/')
def index():
    return "Flask CRUD with PostgreSQL is running!"

if __name__ == "__main__":
    app.run(debug=True ,port=5001)
