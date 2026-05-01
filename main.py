from flask import Flask, request, render_template
import firebase_admin
from firebase_admin import credentials,firestore
import bcrypt

app = Flask(__name__)

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred)

db=firestore.client()
@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        password_bytes = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        user_data = {
            "username": username,
            "password": hashed_password.decode('utf-8')
        }

        db.collection("users").document(username).set(user_data)

        return render_template('register.html', message=" Registered Successfully!")

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_doc = db.collection("users").document(username).get()

        if not user_doc.exists:
            return " User not found"

        stored_data = user_doc.to_dict()
        stored_hash = stored_data["password"].encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return " Login Successful"
        else:
            return render_template("login.html", message="Invalid Password")

    return render_template("login.html", message="Login Successful")

@app.route('/')
def home():
    return '''
    <h2>Welcome</h2>
    <a href="/register">Register</a><br>
    <a href="/login">Login</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)
