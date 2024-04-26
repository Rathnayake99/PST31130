from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5 import uic
import sys
import sqlite3
import bcrypt

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
               fullname TEXT NOT NULL,
               username TEXT NOT NULL,
               password TEXT NOT NULL)''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS restaurants(
               rName TEXT NOT NULL)''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS items(
               code INTEGER PRIMARY KEY,
               iName TEXT NOT NULL,
               iPrice TEXT NOT NULL)''')

class LoginUI(QMainWindow):
    def __init__(self):
        super(LoginUI, self).__init__()
        uic.loadUi("loginForm.ui", self)

        self.pushButton_2.clicked.connect(self.openSignupForm)
        self.pushButton.clicked.connect(self.login)


    def openSignupForm(self):
        self.hide()
        signup_ui.show()

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if username != '' and password != '':
            cursor.execute('SELECT password FROM users WHERE username=?',[username])
            result = cursor.fetchone()
            if result:
                if bcrypt.checkpw(password.encode('utf-8'),result[0]):
                    print('logged in successfull')
                    self.hide()
                    dashboard_ui.show()
                else:
                    print('Invalid password')
            else:
                print('Invalid username')
        else:
            print('All data required')


class DashboardUI(QMainWindow):
    def __init__(self):
        super(DashboardUI, self).__init__()
        uic.loadUi("dashboard.ui", self)

        self.pushButton.clicked.connect(self.restaurant)
    
    def restaurant(self):
        self.hide()
        restaurant_ui.show()

class SignupUI(QMainWindow):
    def __init__(self):
        super(SignupUI, self).__init__()
        uic.loadUi("signupForm.ui", self)

        self.pushButton_2.clicked.connect(self.goBackToLogin)

    def goBackToLogin(self):
        username = self.lineEdit.text()
        fullname = self.lineEdit_3.text()
        password = self.lineEdit_2.text()

        if username != '' and password != '' and fullname != '':
            cursor.execute('SELECT username FROM users WHERE username=?',[username])
            if cursor.fetchone() is not None:
                print("Username already exists.")
            else:
                encodePassword = password.encode('utf-8')
                hashedPassword = bcrypt.hashpw(encodePassword,bcrypt.gensalt())
                cursor.execute('INSERT INTO users VALUES (?,?,?)',[fullname,username,hashedPassword])
                conn.commit()
                print('success')
                self.lineEdit.setText("")
                self.lineEdit_3.setText("")
                self.lineEdit_2.setText("")
                self.hide()
                login_ui.show()
        else:
            print('All fields are required')

class RestaurantUI(QMainWindow):
    def __init__(self):
        super(RestaurantUI, self).__init__()
        uic.loadUi("restaurant.ui", self)
        self.load_items()

        self.pushButton.clicked.connect(self.createRestaurant)

    def createRestaurant(self):
        rName = self.lineEdit.text()
        if rName != '':
            cursor.execute('SELECT rName FROM restaurants WHERE rName=?',[rName])
            if cursor.fetchone() is not None:
                print("Restaurant already exists.")
            else:
                cursor.execute('INSERT INTO restaurants VALUES (?)',[rName])
                conn.commit()
                print('success')
                self.load_items()
                
        else:
            print('Restaurant Name is required')

    def load_items(self):
        self.comboBox.clear()
        cursor.execute("SELECT rName FROM restaurants")
        items = cursor.fetchall()
        for item in items:
            self.comboBox.addItem(item[0])   
            

       


app = QApplication(sys.argv)
login_ui = LoginUI()
signup_ui = SignupUI()
dashboard_ui = DashboardUI()
restaurant_ui = RestaurantUI()
login_ui.show()
sys.exit(app.exec_())
