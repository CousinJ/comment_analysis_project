from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)
#PRACTICE WITH FLASK
# @app.route('/')
# def title():
#     return ' <h1> TITLE PAGE<h1>   '

# @app.route('/<name>')
# def page(name):
#     return f"this is the {name} page. hiya."

# @app.route('/admin')
# def admin():
#     return redirect(url_for('title'))

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()



