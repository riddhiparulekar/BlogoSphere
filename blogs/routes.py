from blogs import blogs_bp
from flask import render_template, url_for, redirect, request, flash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from base64 import b64encode
from extension import database
import requests
import json
from decimal import Decimal, ROUND_HALF_UP
from .models import Blogs, Comments, Category
from .forms import BlogForm


@blogs_bp.route("/")
@login_required
def blogs():
    blogs_data = Blogs.query.all()
    for b in blogs_data:
        b.blog_image = b64encode(b.blog_image).decode('utf-8')
    return render_template('blogs.html', blogs_data=blogs_data)


@blogs_bp.route("/my_blogs")
@login_required
def my_blogs():
    blogs_data = Blogs.query.filter_by(author_id=current_user.id)
    for b in blogs_data:
        b.blog_image = b64encode(b.blog_image).decode('utf-8')
    return render_template('my_blogs.html', blogs_data=blogs_data)


@blogs_bp.route("/view_blog/<int:id>")
@login_required
def view_blog(id):
    blog_data = Blogs.query.get(id)
    blog_data.no_of_views += 1
    database.session.commit()
    comments = Comments.query.filter_by(blog_id=id)

    blog_data = Blogs.query.get(id)
    blog_data.blog_image = b64encode(blog_data.blog_image).decode('utf-8')
    return render_template('view_blog.html', blog_data=blog_data, comments=comments)


@blogs_bp.route("/blogs_form", methods=['GET', 'POST'])
@blogs_bp.route("/blogs_form/<int:id>", methods=['GET', 'POST'])
@login_required
def blogs_form(id=None):
    blog = Blogs.query.get(id) if id else Blogs()
    form = BlogForm(obj=blog)
    if id:
        base64_data = b64encode(blog.blog_image).decode('utf-8')
        mime_type = blog.blog_image_mimetype
        image_src = f"data:{mime_type};base64,{base64_data}"
    else:
        image_src = None

    if form.validate_on_submit():
        if not id:
            img = request.files['img']
            blog_image = img.read()
            blog_image_name = secure_filename(img.filename)
            blog_image_mimetype = img.mimetype

            if blog_image_name == '':
                flash('Please select a file.', 'danger')
                return render_template('blogs_form.html', form=form, image_src=image_src)

            title = form.title.data
            blog_content = form.blog_content.data 
            category = form.category.data

            blog_record = Blogs(title=title, category=category, blog_content=blog_content, author_id=current_user.id, blog_image=blog_image, blog_image_name=blog_image_name, blog_image_mimetype=blog_image_mimetype)
            database.session.add(blog_record)
        else:
            blog.title = form.title.data
            blog.blog_content = form.blog_content.data 
            blog.category = form.category.data
            img = request.files['img']

            if request.files['img'].filename != '':
                blog.blog_image = img.read()
                blog.blog_image_name = secure_filename(img.filename)
                blog.blog_image_mimetype = img.mimetype
        
        database.session.commit()

        return redirect(url_for('blogs.my_blogs'))
    if id:
        form.category.data = blog.category.name   
    return render_template('blogs_form.html', form=form, image_src=image_src)


@blogs_bp.route("/delete_blog/<int:id>")
@login_required
def delete_blog(id):
    blog = Blogs.query.get(id)
    database.session.delete(blog)
    database.session.commit()
    return redirect(url_for('blogs.my_blogs'))


@blogs_bp.route("/comments/<int:blog_id>", methods=['GET', 'POST'])
@login_required
def add_comment(blog_id):
    comment = request.form['comment']

    url = "https://ap8i28dv72.execute-api.us-east-1.amazonaws.com/BlogoSphere/sentiment_analysis"
    body = {
                'text': comment,
            }
    response = requests.post(url, json=body)
    sentiments = json.loads(response.json()['body'])

    neg_sentiment_score = Decimal(sentiments['neg']).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    neu_sentiment_score = Decimal(sentiments['neu']).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    pos_sentiment_score = Decimal(sentiments['pos']).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    compound_sentiment_score = Decimal(sentiments['compound']).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)


    comment = Comments(comment=comment, blog_id=blog_id, author_id=current_user.id, neg_sentiment_score=neg_sentiment_score, neu_sentiment_score=neu_sentiment_score, pos_sentiment_score=pos_sentiment_score, compound_sentiment_score=compound_sentiment_score)
    database.session.add(comment)
    database.session.commit()

    return redirect(url_for('blogs.view_blog', id=blog_id))


@blogs_bp.route("/delete_comment/<int:id>/<int:blog_id>", methods=['GET', 'POST'])
@login_required
def delete_comment(id, blog_id):
    comment = Comments.query.get(id)
    database.session.delete(comment)
    database.session.commit()

    return redirect(url_for('blogs.view_blog', id=blog_id))


@blogs_bp.route("/news_articles", methods=['GET', 'POST'])
@login_required
def news_articles():

    if request.method == "POST":
        category = request.form['category']
    else:
        category = "entertainment"

    news_api = "https://ap8i28dv72.execute-api.us-east-1.amazonaws.com/BlogoSphere/news_articles"

    data = {
        "category" : category
    }
    print(data)
    response = requests.post(url=news_api, json=data)
    data = json.loads(response.json()['body']) 
    articles = data['articles']  
    # print(articles)
    return render_template('news_articles.html', articles=articles)

@blogs_bp.route("/blog_videos", methods=['GET', 'POST'])
@login_required
def blog_videos():
    if request.method == "POST":
        keyword = request.form('keyword')
    else:
        keyword = "Blogging"

    api = "https://afyvb7t8u0.execute-api.us-east-1.amazonaws.com/prod/search_engine"
    data = {
        "query" : keyword
    }
    response = requests.post(url=api, json=data)
    videos = json.loads(response.json()['body'])
    # print(videos)
    return render_template('blog_videos.html', videos=videos)
   

