from flask_script import Manager
from flask import Flask, render_template, request, session, redirect
import json

# default values
POSTS_PER_PAGE = 6

app = Flask(__name__)
manager = Manager(app)

def readPosts():
    with open('static/posts.json', 'r') as f:
        posts = json.load(f)
    return posts

@app.route('/')
def default():
    return render_template('twitter.html')

@app.route('/wall/<int:page>')
def posts(page):

    # build posts paramter
    posts = readPosts()

    # count page numbers
    numPages = len(posts) // POSTS_PER_PAGE + (0 if len(posts) % POSTS_PER_PAGE == 0 else 1)

    # 404 page if page number not in range
    if page < 0 or page > numPages:
        return render_template('klaus.html', notfoundpage='notfound.html'), 404

    # bulid pages parameter
    pages = []
    for i in range(1, numPages+1):
        pages.append(str(i))
    
    # test helper
    # print('\n```\n')
    # print('{} post(s) loaded'.format(len(posts)))
    # print('{} page(s) in {}'.format(numPages, pages))
    # print('\n```\n')

    return render_template('nontwitter.html', prepage=str(page-1), nextpage=str(page+1 if page < numPages else 0), thispage=str(page), posts=posts[POSTS_PER_PAGE*(page-1) : POSTS_PER_PAGE*page], pages=pages)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('klaus.html', notfoundpage='nofound.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manager.run()