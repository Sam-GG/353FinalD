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
    print(cartList)
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
        print(item)
        sql = "INSERT INTO order_" + customer + " (ProductName, Price) VALUES ('"+item[0]+"', "+item[1]+")"
        try:
            conn[1].execute(sql)
            conn[0].commit()
        except Exception as e:
            print(e)
            return('Error. Use valid symbols for name')
    return('Success.')
        
#Display active orders
@app.route('/activeOrders', methods=['GET'])
def getActiveOrders():
    #SQL commands to display all the customer order tables to the client page in order FIFO
    #Select all tables that have the 'order_' prefix and return their names
    sql = """SELECT TABLE_NAME
    FROM information_schema.tables
    WHERE table_name like '%order%'
    ORDER BY CREATE_TIME DESC"""
    conn = createConnection()
    try:
        conn[1].execute(sql)
        orders = conn[1].fetchall()
    except Exception as e:
        print(e)
        return('Error retrieving orders.')
    formatted_orders = []
    for order in orders:
        formatted_orders.append(order[0].split('_')[1])
    print(formatted_orders)
    return jsonify(formatted_orders)

#Return Order information of a given customer to the employee page
@app.route('/displayOrder', methods = ['POST'])
def displayOrder():
    name = request.json['name'].strip()
    sql = 'SELECT * FROM order_'+name
    conn = createConnection()
    try:
        conn[1].execute(sql)
        order = conn[1].fetchall()
        print(order)
    except Exception as e:
        print(e)
        return('Error displaying order')
    return(jsonify(order))

#Complete's an order. 
#Drops the customers order table and adds them to the table of completed orders
@app.route('/completeOrder', methods = ['POST'])
def completeOrder():
    customerName = request.json['name'].strip()
    tableName = 'order_' + customerName
    sql = 'DROP TABLE '+tableName
    conn = createConnection()
    try:
        conn[1].execute(sql)
        conn[0].commit()
        sql_2 = 'INSERT INTO completed (name) VALUES (%s)'
        conn[1].execute(sql_2, customerName)
        conn[0].commit()
    except Exception as e:
        print(e)
        return('Error completing order.')
    return('Success.')

#Checks to see if customer's name is in the table of completed orders
@app.route('/checkOrderReady', methods = ['POST'])
def checkOrderReady():
    name = request.json['name']
    sql = 'SELECT * FROM completed'
    conn = createConnection()
    try:
        conn[1].execute(sql)
        completed = conn[1].fetchall()
    except Exception as e:
        print(e)
    if (name,) in completed:
        return('Order completed!')
    else:
        return('Order not ready.')

if __name__ == "__main__":
    app.run(debug=True)