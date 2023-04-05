from flask import Flask, render_template,request,redirect,url_for
import MySQLdb

app = Flask(__name__)
conn= MySQLdb.connect(host="localhost",user="root",password="marzan12345.",db="book_store")

@app.route("/")
def index():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book_db")
    bookList = cursor.fetchall()
    return render_template("bookit_read_pdf.html", bookList=bookList)


@app.route("/all_books", methods=['GET', 'POST'])
def book():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book_db")
    bookList = cursor.fetchall()
    return render_template("all_books.html", bookList=bookList)


@app.route("/bookit_category_template", methods=['GET', 'POST'])
def bookit_category_template():
    category = request.args.get('cat')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book_db WHERE category=%s", (category,))
    bookList = cursor.fetchall()
    return render_template("bookit_category_template.html", bookList=bookList)


@app.route("/bookit_writer_template", methods=['GET', 'POST'])
def bookit_writer_template():
    writer = request.args.get('writer')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book_db WHERE author=%s", (writer,))
    bookList = cursor.fetchall()
    return render_template("bookit_writer_template.html", bookList=bookList)


@app.route("/buy_book", methods=['GET', 'POST'])
def buy_book():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book_db")
    bookList = cursor.fetchall()
    return render_template("buy_book.html", bookList=bookList)


@app.route("/buy_category_template", methods=['GET', 'POST'])
def buy_category_template():
    category = request.args.get('cat')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book_db WHERE category=%s", (category,))
    bookList = cursor.fetchall()
    return render_template("buy_category_template.html", bookList=bookList)


@app.route("/buy_writer_template", methods=['GET', 'POST'])
def buy_writer_template():
    writer = request.args.get('writer')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book_db WHERE author=%s", (writer,))
    bookList = cursor.fetchall()
    return render_template("buy_writer_template.html", bookList=bookList)


@app.route("/bookit_subpage", methods=['GET', 'POST'])
def bookit_subpage():
    bookID = request.args.get('id')
    user_email = session['user_email']

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book_db WHERE ID=%s", (bookID,))
    bookList = cursor.fetchall()

    # book_name = bookList[0][1]
    # print (book_name)
    date = datetime.now()

    if request.method == "POST":
        q = request.form['quantity']
        print(q)

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notification_table (bookID,user_email,quantity,date)VALUES (%s,%s,%s,%s)",
            (bookID, user_email, q, date))

        conn.commit()

    return render_template("bookit_subpage.html", bookList=bookList)


if __name__ == '__main__':
    app.run()







#
# @app.route("/bookit_children",methods=['GET','POST'])
# def child():
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM book_db WHERE category='Children'")
#     bookList=cursor.fetchall()
#     return  render_template("bookit_children.html",bookList=bookList)
#
# @app.route("/bookit_cooking",methods=['GET','POST'])
# def cooking():
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM book_db WHERE category='Cooking'")
#     bookList=cursor.fetchall()
#     return  render_template("bookit_cooking.html",bookList=bookList)
#
# @app.route("/bookit_fantasy",methods=['GET','POST'])
# def fantasy():
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM book_db WHERE category='Fantasy'")
#     bookList=cursor.fetchall()
#     return  render_template("bookit_fantasy.html",bookList=bookList)
#
#
#
# @app.route("/bookit_Mystery",methods=['GET','POST'])
# def mystery():
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM book_db WHERE category='Mystery'")
#     bookList=cursor.fetchall()
#     return  render_template("bookit_Mystery.html",bookList=bookList)
#
# @app.route("/bookit_Novel",methods=['GET','POST'])
# def novel():
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM book_db WHERE category='Novel'")
#     bookList=cursor.fetchall()
#     return  render_template("bookit_Novel.html",bookList=bookList)
#
#
#
# @app.route("/bookit_religion",methods=['GET','POST'])
# def religion():
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM book_db WHERE category='Religion'")
#     bookList=cursor.fetchall()
#     return  render_template("bookit_religion.html",bookList=bookList)
#
# @app.route("/bookit_scienceFiction",methods=['GET','POST'])
# def science():
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM book_db WHERE category='Science Fiction'")
#     bookList=cursor.fetchall()
#     return  render_template("bookit_scienceFiction.html",bookList=bookList)
#
#
# @app.route("/bookit_HumayunAhmed",methods=['GET','POST'])
# def himu():
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM book_db WHERE author='Humayun Ahmed'")
#     bookList=cursor.fetchall()
#     return  render_template("bookit_HumayunAhmed.html",bookList=bookList)
#
# @app.route("/bookit_jafor",methods=['GET','POST'])
# def jafor():
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM book_db WHERE author='Muhammed Zafar Iqbal'")
#     bookList=cursor.fetchall()
#     return  render_template("bookit_jafor.html",bookList=bookList)
#
# @app.route("/bookit_Agatha",methods=['GET','POST'])
# def agatha():
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM book_db WHERE author='Agatha Cristie'")
#     bookList=cursor.fetchall()
#     return  render_template("bookit_Agatha.html",bookList=bookList)
#
#
# @app.route("/bookit_Sharat",methods=['GET','POST'])
# def sharat():
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM book_db WHERE author='Sharat Chandra'")
#     bookList=cursor.fetchall()
#     return  render_template("bookit_Sharat.html",bookList=bookList)
