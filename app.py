import pyrebase, json, datetime, os, random
from time import sleep
from requests.exceptions import HTTPError
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

firebaseConfig = {
  'apiKey': "AIzaSyDFWPmnk4vcSPUO9X3wT62zWljIRWzhsSE",
  'authDomain': "side-project-404814.firebaseapp.com",
  'projectId': "side-project-404814",
  'storageBucket': "side-project-404814.appspot.com",
  'messagingSenderId': "131412246169",
  'appId': "1:131412246169:web:944456b0eb31fd5c864208",
  'measurementId': "G-SZ1NVJC5FP",
  'databaseURL': 'https://side-project-404814-default-rtdb.firebaseio.com',
};

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
storage = firebase.storage()
db = firebase.database()

def generatePrivateUniqueId(adder):
    characters = 'qwertyuiopasdfghjklzxcvbnm' + '1234567890'
    unique_id = ''.join(random.choices(characters, k=10))
    return "bogareksa"+adder+"-"+unique_id.lower()

def registerMethod(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        registerDetail = auth.get_account_info(user['idToken'])['users'][0]
        userData = {
            'email': registerDetail['email'],
            'role': int(request.form['role']),
            'username': request.form['username'],
            'registeredAt': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return {'message':'CREATED', 'desc':'Successfully registered!', 'registerDetail': db.child('users').child(registerDetail['localId']).set(userData)}
    except HTTPError as e:
        errMsg = json.loads(e.strerror)['error']['message']
        if errMsg == 'EMAIL_EXISTS':
            return {'message':errMsg, 'desc':'Email is already existed!'}
        else:
            return {'message':errMsg}
        
def loginMethod(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        loginDetail = auth.get_account_info(user['idToken'])
        session['loggedIn'] = True
        session['userId'] = loginDetail['users'][0]['localId']
        return {'message':'OK', 'desc':'Successfully signed in!', 'loginDetail':loginDetail['users'][0]}
    except HTTPError as e:
        errMsg = json.loads(e.strerror)['error']['message']
        if errMsg == 'INVALID_LOGIN_CREDENTIALS':
            return {'message':errMsg, 'desc':'Password is incorrect!'}
        else:
            return {'message':errMsg}


def imageMethod(fileName): # UPLOAD
    cloudStorageFormat = f"images/{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}{os.path.splitext(fileName)[1].lower()}"
    storage.child(cloudStorageFormat).put(fileName)
    imageData = {
        'imageId': generatePrivateUniqueId('ImageId'),
        'filePath':cloudStorageFormat
    }
    return imageData


app = Flask(__name__)
app.secret_key = 'askeragob'

@app.route('/')
def host():
    return jsonify(
        {
            'status': {
                'code': 200,
                'message': 'Flask REST API is working!'
            }
        }
    ), 200

@app.route('/home')
def home():
    return render_template('index.html', title="Bogareksa Home")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method in ['GET', 'POST']:
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            return loginMethod(email, password), 200
    else:
        return jsonify({
            'status': {
                'code': 400,
                'message': 'Nah, your request aren\'t processed!'
            },
            'data': 1,
        }), 400

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method in ['GET', 'POST']:
        if request.method == 'GET':
            return render_template('register.html')
        elif request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            return registerMethod(email, password), 201
    else:
        return jsonify({
            'status': {
                'code': 400,
                'message': 'Nah, your request aren\'t processed!'
            },
            'data': 1,
        }), 400

@app.route('/logout')
def logout():
   session.pop('loggedIn', None)
   session.pop('id', None)
   return redirect(url_for('login'))

@app.route('/auth_status')
def auth_status():
    if 'loggedIn' in session:
        return jsonify(
            {
                'status': {
                    'code': 200,
                    'message': 'Authenticated'
                },
                'userId': session['userId']
            }
        ), 200
    else:
        return jsonify(
            {
                'status': {
                    'code': 401,
                    'message': 'Unauthenticated'
                }
            }
        ), 401

# @app.route('/user')
# def user():
#     users = db.child("users").get()
#     for user in users.each():
#         return jsonify(user.val())

# @app.route('/products', methods=['GET', 'POST'])
# def image():
#     if request.method == 'GET':
#         imageId = request.args.get('id')
#         if imageId is None:
#             return "Nothing to find", 404
#         else:
#             return f"Image ID: {imageId}", 200
#     elif request.method == 'POST':
#         fileName = "G:\Sticker\E4-Ox_VVUAYW6HT.jpg"
#         imageId = imageMethod(fileName)['imageId']
#         filePath = imageMethod(fileName)['filePath']
#         return db.child('images').child(imageId).child("filePath").set(filePath)
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)