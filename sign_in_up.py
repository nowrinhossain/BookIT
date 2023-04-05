from flask import Flask, render_template, request, redirect, url_for
import MySQLdb
import os

app = Flask(__name__)

conn = MySQLdb.connect(host="localhost", user= "root", password= "promise12", db = "bookit_db")

@app.route("/")
def index():
    return render_template("index.html", title="SignUP")


@app.route("/signUp", methods=["POST"])
def signUp():
    username = str(request.form["user"])
    password = str(request.form["password"])
    email = str(request.form["email"])
    nid = str(request.form["nid"])
    location = str(request.form["location"])

    cursor = conn.cursor()

    cursor.execute("INSERT INTO user (username,password,email,nid_number,location)VALUES(%s,%s,%s,%s,%s)",
                   (username, password, email,nid,location))
    conn.commit()
    return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("home_login.html")

@app.route("/checker", methods=["POST"])
def checker():
        admin_email = str(request.form["email"])
        admin_password = str(request.form["password"])

        cursor = conn.cursor()
        cursor.execute("SELECT password FROM admin_login WHERE email LIKE %s", (admin_email,))
        fetch_password = cursor.fetchone()
        print(fetch_password[0])

        y = fetch_password[0]
        print(y)

        if (admin_password == y):

            return redirect(url_for("posts"))
        else:

            return redirect(url_for("loginerror"))

@app.route("/checkuser", methods=["POST"])
def checkuser():
    user_email = str(request.form["email"])
    password = str(request.form["password"])

    cursor = conn.cursor()
    cursor.execute("SELECT password FROM user WHERE email LIKE %s", (user_email,))
    user_password = cursor.fetchone()
    print(user_password[0])
    x = user_password[0]


    if (password == x) :

         return redirect(url_for("user_posts"))
    else :

        return redirect(url_for("loginerror"))

@app.route("/approve/<string:name>/")
def approve(name=None):
    cursor = conn.cursor()
    name=str(name)
    cursor.execute("UPDATE post SET APPROVED =1 WHERE book_name = \""+name+"\"")
    books = cursor.fetchall()


    cursor.close()
    conn.commit()

    return str(books)



@app.route("/user_posts")
def user_posts():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post")
    books = cursor.fetchall()


    cursor.close()
    conn.commit()



    return render_template("user_posts.html",**locals())



    

@app.route("/post-entry/",methods=["POST"])
def post_entry():
    if request.method=='POST':
        #data = request.form.to_dict()
        ################

        user_email = "Promise@gmail.com"
        book_name = str(request.form["bookname"])
        writer_name = str(request.form["author"])
        category = str(request.form["category"])
        book_photo = request.files["book_image"]
        for_sell_rent = str(request.form["for_sell_rent"])
        price = request.form["price"]
        book_photo.filename = user_email + book_name + writer_name + ".png"  # some custom file name that you want

        ################

        UPLOAD_FOLDER = 'static/book_images'
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        photo_name = book_photo.filename
        book_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_name))

        book_image_path = "/static/book_images/" + photo_name
        cursor = conn.cursor()

        cursor.execute("INSERT INTO post (user_email,book_name,writer_name,category,book_image_path)VALUES(%s,%s,%s,%s,%s)",
                (user_email, book_name, writer_name,category, book_image_path))

        ###################


        #print(data['bookname'])
        #print(data['author'])

        #UPLOAD_FOLDER = 'static/book_images'
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
        #app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        #photo_name = (data['book_image'].filename)
        #data['book_image'].save(os.path.join(app.config['UPLOAD_FOLDER'], photo_name))

        #book_image_path = "/static/book_images/" + photo_name

        #cursor = conn.cursor()

        #cursor.execute("INSERT INTO post (book_name,writer_name,rent_or_sell,book_image_path,price)VALUES(%s,%s)",
                       #(data['bookname'],data['author'],data['for_sell_rent'],book_image_path,data['price']))
        conn.commit()

        return redirect(url_for("posts"))


@app.route("/posts")
def posts():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post")
    books = cursor.fetchall()


    cursor.close()
    conn.commit()



    return render_template("posts.html",**locals())

@app.route("/loginerror")
def loginerror():
        return render_template("loginerror.html")

@app.route("/logout")
def logout():
    return render_template("logout.html")


@app.route("/dashboard",methods=['GET','POST'])
def dashboard():

    if request.method == 'POST':
        bookname = str(request.form["book_name"])

        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(APP_ROOT, 'static/book_pdf/')
        print(target)
        print(request.files.getlist("file"))
        for upload in request.files.getlist("file"):
            print(upload)
            print("{} is the file name".format(upload.filename))
            filename = upload.filename
            destination = "/".join([target, filename])

            upload.save(destination)
            pdf_path = "/static/book_pdf/" + filename

            cursor = conn.cursor()

            cursor.execute("INSERT INTO book_db (name,link)VALUES(%s,%s)",
                       (bookname,pdf_path))
            conn.commit()


    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
