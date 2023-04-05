from flask import Flask, render_template, request, redirect, url_for, session
#from mysql.connector import MySQLConnection, Error
import MySQLdb
import sys
import base64
#import six
import io
import pymysql
import os
from werkzeug.utils import secure_filename
from datetime import datetime


app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = MySQLdb.connect(host="localhost", user="root", password="123456789", db="bookit_db")



@app.route("/")
def index():
    return render_template("index.html", title="SignUP")


############################Promise Vai####################################################

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

        return redirect(url_for("dashboard"))
    else:

        return redirect(url_for("loginerror"))


@app.route("/checkuser", methods=["POST"])
def checkuser():
    user_email = str(request.form["email"])
    password = str(request.form["password"])

    cursor = conn.cursor()
    cursor.execute("SELECT password FROM user WHERE email LIKE %s", (user_email,))
    user_password = cursor.fetchone()

    if user_password is None:
        flash("This gmail is not Found!")
        return redirect(url_for("index"))

    print(user_password[0])
    x = user_password[0]



    if (password == x):

        session['user_email'] = user_email

        return redirect(url_for("user_posts"))
    else:

        return redirect(url_for("loginerror"))


@app.route("/approve/<string:name>/")
def approve(name=None):
    cursor = conn.cursor()
    name = str(name)
    cursor.execute("UPDATE post SET APPROVED =1 WHERE book_name = \"" + name + "\"")
    books = cursor.fetchall()

    cursor.close()
    conn.commit()

    return str(books)


@app.route("/user_posts")
def user_posts():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post,user WHERE post.user_email = user.email")
    books = cursor.fetchall()

    print (books)

    cursor.close()
    conn.commit()

    return render_template("user_posts.html", books = books)


@app.route("/post_entry", methods=["GET","POST"])
def post_entry():
    if request.method == 'POST':
        # data = request.form.to_dict()
        ################

        user_email = session['user_email']

        book_name = str(request.form["bookname"])
        writer_name = str(request.form["author"])
        category = str(request.form["category"])
        book_photo = request.files["book_image"]
        for_sell_rent = str(request.form["for_sell_rent"])
        price = str(request.form["book_price"])

        for_what = ""

        if for_sell_rent == "Add book for give rent":
            for_what = "For Rent"

        else:
            for_what = "For Sell"

        #price = request.form["price"]

        if book_photo:

            book_photo.filename = user_email + book_name + writer_name + ".png"  # some custom file name that you want

            ################

            UPLOAD_FOLDER = 'static/book_images'
            ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            photo_name = book_photo.filename
            book_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_name))

            book_image_path = "/static/book_images/" + photo_name
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO post (user_email,book_name,writer_name,category,book_image_path,rent_or_sell,price)VALUES(%s,%s,%s,%s,%s,%s,%s)",
            (user_email, book_name, writer_name, category, book_image_path,for_what,price))

        ###################
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
        conn.commit()

        return redirect(url_for("user_posts"))


@app.route("/posts", methods=['GET','POST'])
def posts():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post")
    books = cursor.fetchall()

    cursor.close()
    conn.commit()

    if(request.method=="POST"):
        return redirect(url_for("user_posts"))

    return render_template("posts.html", **locals())


@app.route("/loginerror")
def loginerror():
    return render_template("loginerror.html")


@app.route("/logout")
def logout():
    session.pop('user_email', None)
    return render_template("logout.html")


@app.route("/dashboard",methods=['GET','POST'])
def dashboard():

    if request.method == 'POST':
        bookname = str(request.form["book_name"])
        author = str(request.form["writer_name"])

        if author is None:
            author = "Not given"

        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(APP_ROOT, 'static/pdf_books/')
        print(target)
        print(request.files.getlist("file"))
        for upload in request.files.getlist("file"):
            print(upload)
            print("{} is the file name".format(upload.filename))
            filename = upload.filename
            destination = "/".join([target, filename])

            upload.save(destination)
            pdf_path = "static/pdf_books/" + filename

            print (pdf_path)

            cursor = conn.cursor()

            cursor.execute("INSERT INTO book_db (name,link,author)VALUES(%s,%s,%s)",
                       (bookname,pdf_path,author))
            conn.commit()

    cursor = conn.cursor()
    cursor.execute("SELECT name, author FROM notification_table NATURAL JOIN book_db WHERE book_db.ID = notification_table.request_id")
    books = cursor.fetchall()

    cursor.close()
    conn.commit()

    return render_template("dashboard.html", **locals())

###############################################################################################




##################################### Marzan #########################################################################


@app.route("/read_pdf")
def read_pdf():
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM book_db")
    bookList=cursor.fetchall()
    return  render_template("bookit_read_pdf.html",bookList=bookList)

@app.route("/all_books",methods=['GET','POST'])
def book():
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM book_db")
    bookList=cursor.fetchall()
    return  render_template("all_books.html",bookList=bookList)

@app.route("/bookit_category_template",methods=['GET','POST'])
def bookit_category_template():

    category = request.args.get('cat')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM book_db WHERE category=%s",(category,))
    bookList=cursor.fetchall()
    return  render_template("bookit_category_template.html",bookList=bookList)

@app.route("/bookit_writer_template",methods=['GET','POST'])
def bookit_writer_template():

    writer = request.args.get('writer')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM book_db WHERE author=%s",(writer,))
    bookList=cursor.fetchall()
    return  render_template("bookit_writer_template.html",bookList=bookList)



@app.route("/buy_book",methods=['GET','POST'])
def buy_book():
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM book_db")
    bookList=cursor.fetchall()
    return  render_template("buy_book.html",bookList=bookList)

@app.route("/buy_category_template",methods=['GET','POST'])
def buy_category_template():

    category = request.args.get('cat')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM book_db WHERE category=%s",(category,))
    bookList=cursor.fetchall()
    return  render_template("buy_category_template.html",bookList=bookList)

@app.route("/buy_writer_template",methods=['GET','POST'])
def buy_writer_template():

    writer = request.args.get('writer')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM book_db WHERE author=%s",(writer,))
    bookList=cursor.fetchall()
    return  render_template("buy_writer_template.html",bookList=bookList)


@app.route("/bookit_subpage",methods=['GET', 'POST'])
def bookit_subpage():

    bookID= request.args.get('id')
    user_email = session['user_email']

    cursor=conn.cursor()
    cursor.execute("SELECT * FROM book_db WHERE ID=%s",(bookID,))
    bookList=cursor.fetchall()

    #book_name = bookList[0][1]
    #print (book_name)
    date = datetime.now()


    if request.method == "POST":
        q= request.form['quantity']
        print(q)


        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notification_table (bookID,user_email,quantity,date)VALUES (%s,%s,%s,%s)",
            (bookID, user_email,q,date))

        conn.commit()
        return redirect(url_for("buy_book"))



    return  render_template("bookit_subpage.html",bookList=bookList)

#########################################################################################################################



########################################################Neetu#################################################################



@app.route("/user_profile",methods=["POST","GET"])



def user_profile():

        myname = session['user_email']

        cursor = conn.cursor()
        cursor.execute("SELECT username,location,user_image,email FROM user WHERE email LIKE %s",(myname,))
        info = cursor.fetchone()
        username = info[0]
        location = info[1]
        user_image = info[2]

        #print (info[2])

        if request.method == "POST":


            user_email = session['user_email']

            book_name = str(request.form["book_name"])
            writer_name = str(request.form["writer_name"])
            category = str(request.form["category"])
            book_photo = request.files["book_image"]
            for_sell_rent = str(request.form["for_sell_rent"])
            price= str(request.form["book_price"])

            book_photo.filename = user_email+book_name+writer_name+".png"  # some custom file name that you want


            if for_sell_rent=="Add book for give rent" :

                for_what = "For sell"

                UPLOAD_FOLDER = 'static/rent_book_photo'
                ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                photo_name = secure_filename(book_photo.filename)
                book_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_name))

                book_image_path = "/static/rent_book_photo/"+photo_name


                cursor.execute("INSERT INTO rent_book (user_email,book_name,writer_name,category,book_image_path,rent_price)VALUES(%s,%s,%s,%s,%s,%s)",
                                         (user_email, book_name, writer_name, category,book_image_path,price))

                cursor.execute(
                    "INSERT INTO post (user_email,book_name,writer_name,category,book_image_path,rent_or_sell,price)VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (user_email, book_name, writer_name, category, book_image_path, for_what,price))

            if for_sell_rent=="Add book for sell" :
                for_what = "For rent"

                UPLOAD_FOLDER = 'static/sell_book_photo'
                ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                photo_name = secure_filename(book_photo.filename)
                book_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_name))

                book_image_path = "/static/sell_book_photo/"+photo_name


                cursor.execute("INSERT INTO sell_book (user_email,book_name,writer_name,category,book_image_path,sell_price)VALUES(%s,%s,%s,%s,%s,%s)",
                                         (user_email, book_name, writer_name, category,book_image_path,price))

                cursor.execute(
                    "INSERT INTO post (user_email,book_name,writer_name,category,book_image_path,rent_or_sell,price)VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (user_email, book_name, writer_name, category, book_image_path, for_what, price))

        cursor.close()
        conn.commit()

        return render_template('user_profile.html', info = info)


@app.route("/edit_profile", methods=["GET","POST"])
def edit_profile():

    if request.method == "POST" :
        user_email = session['user_email']
        change_username = str(request.form["change_username"])
        change_password = str(request.form["change_password"])
        change_location = str(request.form["change_location"])

        cursor1 = conn.cursor()

        if change_username :
            cursor1.execute("""
               UPDATE user
               SET username=%s
               WHERE email=%s
            """, (change_username, user_email))

        if change_password :
            cursor1.execute("""
               UPDATE user
               SET password=%s
               WHERE email=%s
            """, (change_password, user_email))


        if change_location :
            cursor1.execute("""
               UPDATE user
               SET location=%s
               WHERE email=%s
            """, (change_location, user_email))

        print(change_username)

        return redirect(url_for("user_profile"))

        conn.commit()
        conn.close()

        #cursor1.execute(" UPDATE user SET username=%s WHERE email='%s' " % (change_username,user_email))


        #return redirect(url_for())



    return render_template("edit_profile.html")

@app.route("/change_pro_pic", methods=["GET","POST"])

def change_pro_pic():

    if request.method == "POST":

        user_email = session['user_email']

        dp = request.files["pro_image"]

        cursor = conn.cursor()
        cursor.execute("SELECT user_image FROM user WHERE email LIKE %s", (user_email,))
        user_image = cursor.fetchone()

        dp.filename = user_email + ".png"  # some custom file name that you want

        dpname = dp.filename

        UPLOAD_FOLDER = 'static/user_images'
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        #print (dpname)

        if user_image[0] is not None:

            path = "static/user_images/" + dpname
            os.remove(path)

        dp.save(os.path.join(app.config['UPLOAD_FOLDER'], dpname))

        dp_image_path = "/static/user_images/" + dpname

        cursor.execute("""
                       UPDATE user
                       SET user_image=%s
                       WHERE email=%s
                    """, (dp_image_path, user_email))

        #else :



        return redirect(url_for("user_profile"))


    return render_template("edit_profile.html")







#def user(username):

@app.route("/view_books", methods=["GET","POST"])

def view_books():

    myname = session['user_email']



    cursor = conn.cursor()
    cursor.execute("SELECT book_name,writer_name,book_image_path,sell_price,category FROM sell_book WHERE user_email LIKE %s", (myname,))
    sell_info = cursor.fetchall()

    cursor.execute("SELECT book_name,writer_name,book_image_path,rent_price ,category FROM rent_book WHERE user_email LIKE %s", (myname,))
    rent_info = cursor.fetchall()


    return render_template("view_books.html",rent_info=rent_info, sell_info = sell_info)



@app.route("/rent_book", methods=["GET","POST"])

def rent_book():
    cursor = conn.cursor()

    category = ""

    cursor.execute("SELECT book_name,writer_name,book_image_path,category FROM rent_book")

    rent_book_info= cursor.fetchall()

    if request.method == "POST":

        #category = str(request.form["category"])
        book_name = str(request.form["search_book"])
        writer_name = str(request.form["search_writer"])
        print(book_name)

        if book_name:

            cursor.execute("SELECT book_name,writer_name,book_image_path,category FROM rent_book WHERE book_name LIKE %s", (book_name,))
            rent_book_info = cursor.fetchall()

        if writer_name:
            cursor.execute(
                "SELECT book_name,writer_name,book_image_path,category FROM rent_book WHERE writer_name LIKE %s",
                (writer_name,))
            rent_book_info = cursor.fetchall()

    return render_template("rent_book.html", rent_book_info=rent_book_info)

    conn.commit()
    conn.close()

    #return render_template("rent_book.html")



@app.route("/rent_book_category", methods=["GET","POST"])
def rent_book_category():

    #url_ = request.url()

    category = request.args.get('cat')
    book_name = request.args.get('name')
    print(category)

    cursor = conn.cursor()

    cursor.execute("SELECT book_name,writer_name,book_image_path,category FROM rent_book WHERE category LIKE %s",
                   (category,))
    rent_book_info = cursor.fetchall()

    if request.method == "POST":

        #category = str(request.form["category"])
        book_name = str(request.form["search_book"])
        writer_name = str(request.form["search_writer"])
        print(book_name)

        if book_name:

            cursor.execute("SELECT book_name,writer_name,book_image_path,category FROM rent_book WHERE book_name LIKE %s", (book_name,))
            rent_book_info = cursor.fetchall()

        if writer_name:
            cursor.execute(
                "SELECT book_name,writer_name,book_image_path,category FROM rent_book WHERE writer_name LIKE %s",
                (writer_name,))
            rent_book_info = cursor.fetchall()





    return render_template("rent_book_category.html", rent_book_info = rent_book_info)





@app.route("/rent_book_owners", methods=["GET","POST"])
def rent_book_owners():

    book = request.args.get('book')





    cursor = conn.cursor()
    cursor.execute("SELECT user_image,username,location,email,rent_price,book_image_path From user,rent_book WHERE email= user_email AND rent_book.book_name= %s",(book,))
    owners = cursor.fetchall()

    cursor.execute("SELECT  * FROM rent_book WHERE book_name LIKE %s",
                   (book,))
    book_info = cursor.fetchone()
    #owners = owner[0][0]
    #print(owners)
    #print (book_info)

    return render_template("rent_book_owners.html",book_info= book_info,owners=owners)





@app.route("/buy_from_user", methods=["GET","POST"])

def buy_from_user():
    cursor = conn.cursor()

    category = ""

    cursor.execute("SELECT book_name,writer_name,book_image_path,category,sell_price FROM sell_book")

    sell_book_info= cursor.fetchall()

    if request.method == "POST":

        #category = str(request.form["category"])
        book_name = str(request.form["search_book"])
        writer_name = str(request.form["search_writer"])
        print(book_name)

        if book_name:

            cursor.execute("SELECT book_name,writer_name,book_image_path,category FROM sell_book WHERE book_name LIKE %s", (book_name,))
            sell_book_info = cursor.fetchall()

        if writer_name:
            cursor.execute(
                "SELECT book_name,writer_name,book_image_path,category FROM sell_book WHERE writer_name LIKE %s",
                (writer_name,))
            sell_book_info = cursor.fetchall()


    return render_template("buy_from_user.html", sell_book_info=sell_book_info)

    conn.commit()
    conn.close()





@app.route("/buy_book_category", methods=["GET","POST"])
def buy_book_category():

    #url_ = request.url()

    category = request.args.get('cat')
    book_name = request.args.get('name')
    print(category)

    cursor = conn.cursor()

    cursor.execute("SELECT book_name,writer_name,book_image_path,category FROM sell_book WHERE category LIKE %s",
                   (category,))
    sell_book_info = cursor.fetchall()


    if request.method == "POST":

        #category = str(request.form["category"])
        book_name = str(request.form["search_book"])
        writer_name = str(request.form["search_writer"])
        print(book_name)

        if book_name:

            cursor.execute("SELECT book_name,writer_name,book_image_path,category FROM sell_book WHERE book_name LIKE %s", (book_name,))
            sell_book_info = cursor.fetchall()

        if writer_name:
            cursor.execute(
                "SELECT book_name,writer_name,book_image_path,category FROM sell_book WHERE writer_name LIKE %s",
                (writer_name,))
            sell_book_info = cursor.fetchall()


    return render_template("buy_book_category.html", sell_book_info=sell_book_info)



@app.route("/buy_book_owners", methods=["GET","POST"])
def buy_book_owners():

    book = request.args.get('book')



    cursor = conn.cursor()
    cursor.execute("SELECT user_image,username,location,email,sell_price,book_image_path From user,sell_book WHERE email= user_email AND sell_book.book_name= %s",(book,))
    owner = cursor.fetchall()

    cursor.execute("SELECT  * FROM sell_book WHERE book_name LIKE %s",
                   (book,))
    book_info = cursor.fetchone()

    #cursor.execute()
    #owners = owner[0][0]
    print(owner)

    return render_template("buy_book_owner.html",book_info=book_info,owners=owner)



if __name__ == "__main__":
    app.run(debug=True)

###################################################################################################################
