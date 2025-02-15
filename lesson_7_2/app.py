import random
import string
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Flask アプリケーションのセットアップ
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sample_user:sample_pass@localhost:5432/sample_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemyのセットアップ
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# モデル定義
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True)
    posts = db.relationship('Post', back_populates='user')  # 1対多のリレーション

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 外部キー
    user = db.relationship('User', back_populates='posts')  # Userとのリレーション

# ランダムな文字列を作成
def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# メインのエントリーポイント
if __name__ == "__main__":
    with app.app_context():
        # データベースを作成
        db.create_all()

        # 元の名前とメール
        name = "Bob"
        email = "bob@example.com"

        # ユーザーがすでに存在するか確認
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            # 重複した場合はランダムなユーザー名とメールを生成
            name = f"{name}_{generate_random_string(4)}"
            email = f"user_{generate_random_string(8)}@example.com"
            print(f"Duplicate found. Generated new user: {name}, {email}")
        else:
            print(f"No duplicate found. Using original user: {name}, {email}")

        # 新しいユーザーを作成
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()

        # 投稿の追加
        post1 = Post(title="First Post", content="This is my first post.", user=user)
        post2 = Post(title="Second Post", content="This is my second post.", user=user)
        db.session.add_all([post1, post2])
        db.session.commit()

        # データの取得
        user_from_db = User.query.filter_by(email=email).first()
        print(f"{user_from_db.name}'s posts:")
        for post in user_from_db.posts:
            print(f"- {post.title}: {post.content}")

    # Flaskアプリケーションの起動
    app.run(debug=True, port=5001)
