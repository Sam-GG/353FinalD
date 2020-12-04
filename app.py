from flask import Flask, render_template, url_for, request, redirect, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '9043'
app.config['MYSQL_DATABASE_DB'] = '353final'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#efficient way to create and test connection everytime needed
def createConnection():
    try:
        con = mysql.connect()
        cur = con.cursor()
    except Exception as e:
        print(e)
    return con, cur

@app.route('/')
def index():
    return render_template('menu.html')
#Employee webpage

@app.route('/employeesOnly')
def employeePage():
    return render_template('employeePage.html')
#Is my order ready? page

@app.route('/isOrderReady')
def orderReadyPage():
    return render_template('orderReadyPage.html')

#Return menu table from database to client
@app.route('/menu', methods=['GET'])
def displayMenu():
    conn = createConnection()
    sql = 'SELECT * FROM menu'
    try:
        conn[1].execute(sql)
    except Exception as e:
        print(e)
    return jsonify(conn[1].fetchall())

#Add new products to the menu
@app.route('/addProduct', methods=['POST'])
def addProduct():
    #Get params for the new menu item from client
    product = request.json['name']
    price = request.json['price']
    #Insert into menu table in database
    sql = "INSERT INTO menu (ProductName, Price) VALUES ('" + product + "', " + price + ")"
    conn = createConnection()
    try:
        conn[1].execute(sql)
        conn[0].commit()
    except Exception as e:
        print(e)
        return('Error occurred.')
    else:
        return ('Success.')

#Delete products from menu
@app.route('/deleteProduct', methods=['POST'])
def deleteProduct():
    product = request.json['name']
    product = str(product)
    print(product)
    print(type(product))
    #query a delete from the menu table
    sql = "DELETE FROM menu WHERE ProductName = (%s)"
    conn = createConnection()
    try:
        conn[1].execute(sql, (product,))
        conn[0].commit()
    except Exception as e:
        print(e)
        return('Error occurred. Make sure the name is correct.')
    else:
        return('Success.')

#Add orders from a cart to orders table
@app.route('/order', methods=['POST'])
def submitOrder():
    cartList = request.json['cart']
    customer = request.json['customer']
    #creates an order table for a single customer, named after their name
    conn = createConnection()
    sql = "CREATE TABLE order_" + customer + " (ProductName varchar(128), Price FLOAT)"
    try:
        conn[1].execute(sql)
        conn[0].commit()
    except Exception as e:
        print(e)
    #Iterate and insert the products from cartList into the table
    print(cartList)
    for item in cartList:
        sql = "INSERT INTO order_" + customer + " (ProductName, Price) VALUES ('"+item[0]+"', "+item[1]+")"
        try:
            conn[1].execute(sql)
            conn[0].commit()
        except Exception as e:
            print(e)




if __name__ == "__main__":
    app.run(debug=True)