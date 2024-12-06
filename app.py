from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'Home page'

@app.route('/form')
def form():
    return render_template('formulario.html')

@app.route('/cube')
def cubeR():
    return render_template('cube.html')

if __name__ == '__main__':
    app.run(debug=True)