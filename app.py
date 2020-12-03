from flask import Flask, render_template
import sqlalchemy

app = Flask(__name__)

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

    

if __name__ == "__main__":
    app.run(debug=True)