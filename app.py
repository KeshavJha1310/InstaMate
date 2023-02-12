from flask import Flask , render_template,  request , redirect , url_for , jsonify 
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect 
from instabot import Bot 
import os
import glob
import json
import queue
import threading


app = Flask(__name__ , template_folder="templates")

q = queue.Queue()

def worker():
    while True:
        task = q.get()
        task()
        q.task_done()
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()



app.secret_key = os.urandom(24)
app.config['WTF_CSRF_SECRET_KEY'] = 'secret-key'
# app.config['WTF_CSRF_ENABLED'] = True
csrf = CSRFProtect(app)
# bot = Bot()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login" , methods = ['GET','POST'])
# @csrf.protect
def login():
        #  csrf_token = csrf.generate_csrf()
        # error = None
         if request.method == 'POST':
            Username1 = request.form.get('Username')
            Password1 = request.form.get('Password')
        # session['user'] = request.form['Username'] 
        # is_login = False
        # print(is_login)
            bot = Bot()
            is_login = False 

            is_login = bot.login(username=Username1 , password=Password1)
            
            try:
                response_json = json.loads(is_login)
            except json.JSONDecodeError as e:
                 return jsonify({"error": "Failed to decode the response from the server. Please try again later."})
            q.put(login)   
            return jsonify(response_json) 
        
            
               
        #session.pop('user',None)
        # print(is_login)
            # if is_login == True:
            #  return redirect(url_for("operations" ,u = Username1, p = Password1))

            #  return "logged in"
        #    return render_template('operations.html',u = Username1, p = Password1) message = "Wrong credentials...Try Again!"
        #  return render_template("login.html")
         return render_template("login.html")
    # else:
    #     return render_template("login.html")
    #       if 'user' in session:
    #           return redirect(url_for('operations'))

    #       return render_template('login.html')

@app.route("/operations")
def operations():
    return render_template("operations.html")
    #  if 'user' in session:
    #     user = session['user']
    #     return f"<h1>{{user}}</h1>"
    #  else:
    #      redirect(url_for('login'))
    #  if g.user:
    #   return render_template('operations.html', user=session['user'])
    #  return redirect(url_for('login.html'))   

# @app.before_request
# def before_request():
#      g.user = None

#      if 'user' in session:
#          g.user = session['user']
#          return f"<h1>{{user}}</h1>"
#      else:
#          return redirect(url_for('login.html'))

# @app.route('/dropsession')
# def dropsession():
#     session.pop('user',None)
#     return(url_for('login.html'))


if __name__ == "__main__": 
   app.run(debug = True , port=5000, use_reloader =False)
   
cookie_del = glob.glob("config/*cookie.json")
os.remove(cookie_del[0])


   