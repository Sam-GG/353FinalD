from flask import Flask, render_template, url_for, request, redirect, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '9043'
app.config['MYSQL_DATABASE_DB'] = '353Final'
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
    """ console.log(req.body.name)
    console.log(req.body)
    var product = req.body.name
    var price = req.body.price
    #Insert into menu table in database
    var sql = "INSERT INTO menu (ProductName, Price) VALUES ('" + product + "', " + price + ")"
    con.query(sql, function (err, result) {
        if (err) console.log(err);
        res.send('Success.'); """



if __name__ == "__main__":
    app.run(debug=True)