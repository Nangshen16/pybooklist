from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

@app.route('/')
def Index():
     mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="book_db")
     cursor = mydb.cursor()
     
     cursor.execute('SELECT * FROM books')
     books = cursor.fetchall()
    
     return render_template('index.html', books=books)

@app.route('/add', methods=["POST"])
def add():  
    if request.method == "POST":
        title = request.form["title"]   
        author = request.form["author"]         
        price = request.form["price"] 
        
        if 'photo' not in request.files:
            msg = 'No file part' 
            
        file = request.files['photo']
        
        if file.filename == '':
            msg = "No selected file" 
            
        if file:
            
            file.save(f'static/images/{file.filename}')
            
            filename = file.filename
            msg = 'File uploaded sucessfully'
            
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="book_db")
        cursor = mydb.cursor()
     
        cursor.execute('INSERT INTO books (title,author, photo, price, cdate, mdate) VALUES (%s, %s, %s, %s, now(), now() )', (title,author, filename, price))
        mydb.commit()
    
        return redirect(url_for('Index'))  
    
@app.route('/delete/<string:book_id>', methods=['GET'])
def delete(book_id):
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="book_db")
    cursor = mydb.cursor()
    
    sql = "DELETE FROM books WHERE id=" + book_id
    
    cursor.execute(sql)
    mydb.commit()
    
    return redirect(url_for('Index'))

@app.route('/upd/<string:book_id>', methods=['GET'])
def upd(book_id):
    
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="book_db")
    cursor = mydb.cursor()
    
    sql= " SELECT * FROM books WHERE id =" + book_id
    
    cursor.execute(sql)
    book = cursor.fetchone()
    
    return render_template('upd.html', book=book)


@app.route('/update', methods=['POST'])
def update():
    id = request.form['id']   
    title = request.form['title']   
    author = request.form['author']   
    price = request.form['price']   
    
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="book_db")
    cursor = mydb.cursor()
    
    sql = "UPDATE books SET title=%s, author=%s, price=%s, mdate=now() WHERE id=" + id
    
    cursor.execute(sql,(title,author,price))
    mydb.commit()
    
    return redirect(url_for('Index'))

    




if __name__ == "__main__":
    app.run( host='NSHs-MacBook-Pro.local', port=5600, debug=True)  