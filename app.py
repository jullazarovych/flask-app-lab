from flask import Flask
app=Flask(__name__)

@app.route('/')
def main():
    return '<h1>Hello, world</h1>', 200

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    
    return f"This is your homepage :) "
if __name__=='__main__':
    app.run(debug=True)