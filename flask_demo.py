from flask import Flask

app = Flask(__name__)



@app.route('/')
def index(): #for root page
    return 'yaaaaaay!!!'

@app.route('/arsenal')
def arsenal():
    return '<h2>Arsenal is pretty shit right now</h2>'


if __name__ == "__main__":
    app.run(debug=True)
