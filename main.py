from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    posts = db.session.query(BlogPost).all()
    for blog_post in posts:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route('/edit-post/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    blog_post = db.session.query(BlogPost).get(post_id)
    is_edit = True
    form = CreatePostForm(
        title=blog_post.title,
        subtitle=blog_post.subtitle,
        author=blog_post.author,
        img_url=blog_post.img_url,
        body=blog_post.body,
    )
    if form.validate_on_submit():
        blog_post.title = request.form['title']
        blog_post.subtitle = request.form['subtitle']
        blog_post.author = request.form['author']
        blog_post.img_url = request.form['img_url']
        blog_post.body = request.form['body']
        db.session.commit()
        return redirect('/')

    return render_template('make-post.html', form=form, is_edit=is_edit)


@app.route('/new-post', methods=['GET', 'POST'])
def make_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        title = request.form['title']
        subtitle = request.form['subtitle']
        author = request.form['author']
        img_url = request.form['img_url']
        body = request.form['body']
        date = datetime.datetime.now().strftime("%B %d,%Y")
        blog_post = BlogPost(
            title=title,
            author=author,
            subtitle=subtitle,
            img_url=img_url,
            body=body,
            date=date,
        )
        db.session.add(blog_post)
        db.session.commit()
        return redirect('/')

    return render_template('make-post.html', form=form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/delete/<int:post_id>", methods=['POST', 'GET'])
def delete(post_id):
    blog_post = db.session.query(BlogPost).get(post_id)
    db.session.delete(blog_post)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
