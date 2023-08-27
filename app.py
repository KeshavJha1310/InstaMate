from flask import Flask , render_template,  request , redirect , url_for , jsonify 
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect 
from win10toast import ToastNotifier
from instabot import Bot 
import os , time
import glob
import json
import queue
import threading
#import cherrypy

app = Flask(__name__ , template_folder="templates")

q = queue.Queue()
bot = Bot()
toaster = ToastNotifier()
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
        
            
            is_login = False 

            is_login = bot.login(username=Username1 , password=Password1, is_threaded=True)
            toaster.show_toast("Please Wait", "This might take a minute", duration=10)
            if is_login == True:
                toaster.show_toast("Successfully ", "Loged in", duration=10) 
                
                return render_template("operations.html" ,Username1=Username1 )
            else :
                toaster.show_toast("Failed to login", "Please try again later", duration=10)



         return render_template("login.html")


@app.route("/operations" )
def operations():



    return render_template("operations.html")

@app.route("/follow"  , methods = ['GET','POST'])
def follow():
    if request.method == 'POST':
        success = False
        print("hello bhai")
        number = request.form.get('number') 
        print(number)
        user1 = request.form.get('User1')
        print(user1)
        user2 = request.form.get('User2')
        print(user2)
        user3 = request.form.get('User3')
        print(user3)
        user4 = request.form.get('User4')
        print(user4)
        if number== '1':
            print("ander aa rha h bhai")
             
            success = bot.follow(user1)
            if success == True:
                
                toaster.show_toast("Successfully", "You are following...", duration=10)    
            else :
                toaster.show_toast("Unsuccess", "Failure in following..." , duration=10)

        elif number == '2':
           
            success =bot.follow([user1,user2])
            if success == True:
                
                toaster.show_toast("Successfully", "You are following...", duration=10)
            else :
                toaster.show_toast("Unsuccess", "Failure in following..." , duration=10)
        elif number == '3':
            
            success =bot.follow([user1,user2,user3])
            if success == True:
                
                toaster.show_toast("Successfully", "You are following...", duration=10)
            else :
                toaster.show_toast("Unsuccess", "Failure in following..." , duration=10)
        elif number == '4' :
          
            success =bot.follow([user1,user2,user3,user4])
            if success == True:
                
                toaster.show_toast("Successfully", "You are following...", duration=10)
            else :
                toaster.show_toast("Unsuccess", "Failure in following..." , duration=10)



    return render_template("follow.html")

@app.route("/unfollow" , methods = ['GET','POST'])
def unfollow():
    if request.method == 'POST':
        success = False
        conformation = request.form.get('conformation')
        if conformation == "CONFIRM":
            success = bot.unfollow_non_followers()
            if success == True:
                toaster.show_toast("Successfully", "Unfollowed all the non followers" , duration=10)
            else :
                 toaster.show_toast("Unsuccess", "Failure in Unfollowing..." , duration=10)
    return render_template("unfollow.html")

@app.route("/message", methods = ['GET', 'POST'])
def message():
    if request.method == 'POST':
        success = False
        number = request.form.get('number') 
        user1 = request.form.get('User1')
        user2 = request.form.get('User2')
        user3 = request.form.get('User3')
        user4 = request.form.get('User4')
        message = request.form.get('message')
        if number== '1':
            success = bot.send_message(message,user1)
            if success == True:
                
                toaster.show_toast("Successfully", "Message Send", duration=10)    
            else :
                toaster.show_toast("Unsuccess", "Message cannot Send" , duration=10)

        elif number == '2':
          
            success =bot.send_message(message,[user1,user2])
            if success == True:
                
                toaster.show_toast("Successfully", "Message Send", duration=10)
            else :
                toaster.show_toast("Unsuccess", "Message cannot Send" , duration=10)
        elif number == '3':
           
            success =bot.send_message(message,[user1,user2,user3])
            if success == True:
                
                toaster.show_toast("Successfully", "Message Send", duration=10)
            else :
                toaster.show_toast("Unsuccess", "Message cannot Send" , duration=10)
        elif number == '4' :
      
            success =bot.send_message(message,[user1,user2,user3,user4])
            if success == True:
                
                toaster.show_toast("Successfully", "Message Send", duration=10)
            else :
                toaster.show_toast("Unsuccess", "Message cannot Send" , duration=10)


    return render_template("message.html")

@app.route("/like_comment", methods = ['GET', 'POST'])
def like_comment():
    if request.method == 'POST':
        like_user = request.form.get('User4')
        amount = request.form.get('number')
        comment = request.form.get('message')
        success = False
        try:
            success = bot.like_user(like_user , amount=int(amount), filtration=False )
            user_id = bot.get_user_id_from_username(like_user)
            media_id = bot.get_last_user_medias(user_id)
            success = bot.comment(media_id, comment)
            if success == True:
                
                toaster.show_toast("Successfully", "Liked the Posts", duration=10)
            else :
                toaster.show_toast("Unsuccess", "Failed..." , duration=10)

        except Exception as e:
            print(str(e))


            

    return render_template("like_comment.html")

@app.route("/view", methods = ['GET', 'POST'])
def view():
    if request.method == 'POST':
        id = request.form.get('id')
        listers_name = []
        listing_name = [] 
        true = True
        followers_list = bot.get_user_followers(id)
        following_list = bot.get_user_following(id)
        for each_follower in followers_list: 
            listers_name.append(bot.get_username_from_user_id(each_follower))
        for each_following in following_list:
            listing_name.append(bot.get_username_from_user_id(each_following))   
        if true == True:
            print(listers_name)
            print(listing_name) 
            return render_template("list.html" , listers_name=listers_name , listing_name=listing_name)
    return render_template("view.html")

@app.route("/post", methods = ['GET', 'POST'])
def post():
    if request.method == 'POST':
        post = request.files['file'].filename
        caption = request.form.get('caption')
        full_path = os.path.join('static\images', post)
        
        request.files['file'].save(full_path)
        time.sleep(5)
        success = False
        success = bot.upload_photo(full_path,caption=caption)
       
        if success == True:
            toaster.show_toast("Successfully", "Posted the Image", duration=10)
        else:
            toaster.show_toast("Successfully", "Posted the Image", duration=10)

        if os.path.exists(full_path):
            os.remove(full_path)
            print(f"{full_path} deleted successfully")
        else:
            print(f"{full_path} does not exist")


        

    return render_template("post.html")

if __name__ == "__main__": 
    app.run(debug = True , port=5000, use_reloader =False)
   

cookie_del = glob.glob("config/*cookie.json")
os.remove(cookie_del[0])


   