from flask import Flask, url_for

app = Flask(__name__)

@app.route('/welcome')
def welcome():
    return 'Welcome to ABC Corporation'

#@app.route('/')
#def index():
    company_name = 'ABC Corporation'
    location = 'India'
    contact_detail = '999-999-9999'
    return (f'Company Name: {company_name}<br>Location: {location}<br>Contact Detail: {contact_detail}')

@app.route('/hello_world')
def hello_world():
    return 'Hello World!!'


@app.route('/hello/<name>')
def hello(name):
    return 'Hello, {}!'.format(name)

@app.route('/')
def index():
    # Build a URL for the hello function, with the name argument set to 'John'
    url = url_for('hello', name='John')
    # Return a link to the hello function with the name 'John'
    return '<a href="{}">Say hi to John</a>'.format(url)


if __name__ == '__main__':
    app.run()
