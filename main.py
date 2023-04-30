from flask import Flask, render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Article: {self.id}, {self.username}, {self.title}, {self.text}!!!"

    def show_type(self):
        return 'Our type Article'


with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        username = request.form['username']
        title = request.form['title']
        text = request.form['text']

        article = Article(username=username, title=title, text=text)
        # print(article.show_type())
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return render_template("500.html")

    else:
        return render_template("create-article.html")


@app.route('/posts')
def posts():
    article = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=article)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    print(article)
    return render_template('posts_detail.html', article=article)

@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return f"User page {name} - id {id}"


if __name__ == '__main__':
    app.run(debug=True)