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
               code INTEGER NOT NULL,
               iName TEXT NOT NULL,
               iPrice INTEGER NOT NULL,
               rName TEXT NOT NULL)''')

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
        self.pushButton_3.clicked.connect(self.saveItem)
        self.pushButton_7.clicked.connect(self.searchItem)
        self.pushButton_4.clicked.connect(self.removeItem)
        self.pushButton_5.clicked.connect(self.updateItem)
        self.pushButton_2.clicked.connect(self.deleteRestaurant)

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

    def saveItem(self):
        iCode = int(self.lineEdit_4.text())
        iName = self.lineEdit_2.text()
        iPrice = int(self.lineEdit_3.text())
        rName = self.comboBox.currentText()

        if iCode != '' and iName != '' and iPrice != '' and rName != '':
            cursor.execute('SELECT Code FROM items WHERE rName=? AND Code=?',[rName,iCode])
            if cursor.fetchone() is not None:
                print("Item coad is already exists.")
            else:
                cursor.execute('INSERT INTO items VALUES (?,?,?,?)',[iCode,iName,iPrice,rName])
                conn.commit()
                print('success')
                self.clearItemsFileds()
                print('success')
        else:
            print('All fields are required')

    def clearItemsFileds(self):
        self.lineEdit_4.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")


    def searchItem(self):
        iCode = self.lineEdit_4.text()
        rName = self.comboBox.currentText()
        if iCode != '' and rName != '':
            try:
                iCode = int(iCode)
                cursor.execute('SELECT * FROM items WHERE Code=? AND rName=?', [iCode,rName])
                item = cursor.fetchone()
                if item:
                    self.lineEdit_2.setText(item[1])  # Populate item name
                    self.lineEdit_3.setText(str(item[2]))
                    self.comboBox.setCurrentText(item[3])  # Populate item price
                    # You may need to populate the ComboBox here based on your data model
                else:
                    print("Item not found.")
                    self.clearItemsFileds()
            except ValueError:
                print("Item code must be an integer.")
                self.clearItemsFileds()
        else:
            print("Please enter an item code.")
            self.clearItemsFileds()
       
    def removeItem(self):
        try:
            iCode = int(self.lineEdit_4.text())
            rName = self.comboBox.currentText()
        except ValueError:
            print("Item code must be an integer.")
            return
        if iCode != '' and rName != '':
            cursor.execute('SELECT * FROM items WHERE Code=? AND rName=?', [iCode,rName])
            item = cursor.fetchone()
            if item:
                cursor.execute('DELETE FROM items WHERE Code=? AND rName=?', [iCode,rName])
                conn.commit()
                print('Item with code {} removed successfully.'.format(iCode))
            else:
                print("Item with code {} not found.".format(iCode))
        else:
            print('All fields are required')

    def updateItem(self):
        
        rName = self.comboBox.currentText()
        iName = self.lineEdit_2.text()
        
        try:
            iCode = int(self.lineEdit_4.text())
            iPrice = int(self.lineEdit_3.text())
        except ValueError:
            print("Item code must be an integer.")
            return
        if iCode != '' and iName != '' and iPrice != '' and rName != '':
            cursor.execute('SELECT * FROM items WHERE Code=? AND rName=?', [iCode,rName])
            item = cursor.fetchone()
            if item:
                # Update the item details
                cursor.execute('UPDATE items SET iName=?,iPrice=? WHERE Code=? AND rName=?', [iName, iPrice, iCode,rName])
                conn.commit()
                print("Success", "Item details updated successfully.")
            else:
                print("Warning", "Item with code {} not found.".format(iCode))
        else:
            print('All fields are required')

    def deleteRestaurant(self):
        rName = self.comboBox.currentText()
        if rName != '':
            try:
                cursor.execute('DELETE FROM items WHERE rName=?', [rName])
                cursor.execute('DELETE FROM restaurants WHERE rName=?', [rName])
                conn.commit()
                self.load_items()
                print("Data removed successfully.")
            except sqlite3.Error as e:
                print("Error:", e)
        else:
            print('Select restaurant name')


app = QApplication(sys.argv)
login_ui = LoginUI()
signup_ui = SignupUI()
dashboard_ui = DashboardUI()
restaurant_ui = RestaurantUI()
dashboard_ui.show()
sys.exit(app.exec_())
