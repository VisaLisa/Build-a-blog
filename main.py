#!/usr/bin/env python

__author__ = "student"
__version__ = "1.0"
# June 26, 2017
# Flask Blog App re: LaunchCode lc101
# Rubric: http://education.launchcode.org/web-fundamentals/assignments/build-a-blog/


from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:enterbab@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(1500))
    date = db.Column(db.DateTime)

    def __init__(self, title, content, date=None):
        self.title = title
        self.content = content
        if date is None:
            date = datetime.utcnow()
        self.date = date


# landing page redirected to blog
@app.route('/')
def index():
    return redirect('/blog')


# redirected from / showing all blogs
@app.route('/blog', methods=['GET'])
def blog():
    # TODO: with the date timestamp added to blog entries, you can add a query parameter to sort by date descending
    blogs = Blog.query.all()
    return render_template('blog.html', title='Your Blog', blogs=blogs)


# query all blogs and return/gets the selected blog
@app.route('/selected_blog', methods=['GET'])
def selected_blog():
    blog_id = request.args.get('id')
    blog_post = Blog.query.filter_by(id=blog_id).first()
    return render_template('selected_blog.html', selected_blog=blog_post)


# new post and check for errors
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    # currently no errors
    title_error = ''
    content_error = ''
    error_check = False

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']

        # no title error send to newpost
        if not blog_title:
            title_error = 'Eh...Try Again'
            error_check = True

            # no content error send to newpost
        if not blog_content:
            content_error = 'Write something!'
            error_check = True

            # redirect to blog
        if error_check:
            return render_template('newpost.html', title_error=title_error, content_error=content_error)

        new_blog = Blog(blog_title, blog_content)
        db.session.add(new_blog)
        db.session.commit()
        blog_id = str(new_blog.id)
        return redirect("/blog?id=" + blog_id)
    return render_template('newpost.html')


if __name__ == '__main__':
    app.run()
