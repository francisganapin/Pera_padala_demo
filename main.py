import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QApplication,QLineEdit
from PyQt6.QtCore import QTimer
from datetime import datetime
import os
from PyQt6 import QtCore, QtWidgets
import sqlite3
import threading
import time

from PyQt6.QtWidgets import QStackedWidget, QWidget, QStackedLayout
class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        try:
            # Load the UI file
            uic.loadUi('main.ui', self)
         

            # Set fixed size based on loaded UI
            self.setFixedSize(self.size())

            #conenct to database for login 
            self.conn = sqlite3.connect('database.db')
            self.cursor = self.conn.cursor()

            # Initialize the emergency label
            self.emergency_label_text = "Ganapin || Emergency Calls  "
            self.emergency_label = QLabel(self.emergency_label_text, self)
            self.emergency_label.setGeometry(QtCore.QRect(10, 10, 91, 16))
            
            #if you want target the lael name it setobject then put stylesheet

            self.emergency_label.setObjectName("emergencyLabel")
            # Create a timer to update the text
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_text)
            self.timer.start(200)  # Update every 200 milliseconds
            ##date today and time

            # Get current date and time
            # Initialize the date label
            self.date_label = QLabel(self)
            self.date_label.setGeometry(QtCore.QRect(120, 10, 150, 16))  # Adjusted width for longer text
            self.date_label.setObjectName('dateLabel')

        # Set up the timer to update the time every second
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.update_time)
            self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

        # Initialize the time display
            self.update_time()

            # Apply stylesheet
            self.setStyleSheet("""
                #emergencyLabel {
                    color: black;
                }
                #dateLabel {
                    color: black;
                }
            """)

        ###########################################
        #input on login page
            self.username_input.text()
            self.password_input.text()
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.login_bt.clicked.connect(self.check_credentials)
            self.home_bt.clicked.connect(self.show_page_2) #this will comeback to homepage 
            self.transfer_bt.clicked.connect(self.show_page_3)
            #self.transfer_money_bt.clicked.connect(self.bank_transfer)
            self.transfer_money_bt_2.clicked.connect(self.you_sure_page)
            self.no_go_to_blank_page.clicked.connect(self.blank_page_no)
            self.transfer_money_bt_yes.clicked.connect(self.transfer_page_yes)
            self.transfer_money_bt.clicked.connect(self.bank_transfer)
             # Initialize stacked widgets
            self.outer_stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')
            self.inner_stackedWidget = self.outer_stackedWidget.findChild(QStackedWidget, 'stackedWidget_2')

        # Initialize the stacked layout
            self.stacked_layout = QStackedLayout()

        # Find pages within the stacked widgets
            self.page_1 = self.outer_stackedWidget.findChild(QStackedWidget, 'stackedWidget')
            self.page_2 = self.outer_stackedWidget.findChild(QWidget, 'page_2')
            self.page_3 = self.outer_stackedWidget.findChild(QWidget, 'page_3')
            self.page_4 = self.outer_stackedWidget.findChild(QWidget, 'are_you_sure_page')
            self.blank_page = self.outer_stackedWidget.findChild(QWidget,'blank_page')
            self.transfer_page_2 = self.outer_stackedWidget.findChild(QWidget,'transfer_page_2')


        # have place holder 
            self.transfer_input_id = self.findChild(QLineEdit,'transfer_input_id')
            self.transfer_price_input =  self.findChild(QLineEdit,'transfer_price_input')
            self.transfer_price_input.setPlaceholderText('Enter Amount')
            self.transfer_input_id.setPlaceholderText("Enter another user")


            # Initialize user attribute
            self.user = None
            

        except FileNotFoundError:
            print("UI file 'main2.ui' not found.")

    def update_text(self):
        # Shift the text
        self.emergency_label_text = self.emergency_label_text[1:] + self.emergency_label_text[0]
        self.emergency_label.setText(self.emergency_label_text)

    def update_time(self):
        # Get current date and time
        now = datetime.now()
        # Format the date and time as "day | month | day_number | year hour:minute am/pm"
        dt_string = now.strftime("%A | %B | %d | %y %I:%M %p")
        # Update the label text
        self.date_label.setText(dt_string)

    def check_credentials(self):
        '''Check the credentials of the user'''
        self.user = self.username_input.text()
        password = self.password_input.text()

        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'database.db')
    
        with sqlite3.connect(file_path) as conn:
            self.cursor = conn.cursor()

            query = 'SELECT * FROM users WHERE username = ? AND password = ?'

            self.cursor.execute(query, (self.user, password))
            result = self.cursor.fetchone()

            if result:
                self.stackedWidget.setCurrentWidget(self.page_2)
                self.check_bank_update()
                self.dispaly_homepage()
            else:
                self.username_input.clear()
                self.password_input.clear()
                # Pop up invalid credentials
                self.invalid.setText('Invalid Credentials')
                QTimer.singleShot(3000, lambda: self.invalid.setText(''))

    def show_page_3(self):
        '''this page is for Rosas'''
        # Switch to page_2 in the stacked layout
        self.stackedWidget.setCurrentWidget(self.page_3)

    def show_page_2(self):

        self.stackedWidget.setCurrentWidget(self.page_2)

    def bank_transfer(self):
        transfer_id = self.transfer_input_id.text()
        transfer_amount = self.transfer_price_input.text()

        if not transfer_id or not transfer_amount:
            self.invalid_label_2.setText('Please fill in all fields correctly')
            QTimer.singleShot(3000, lambda: self.invalid.setText(''))
            return
        try:
            transfer_amount = float(transfer_amount)
        except ValueError:
            self.invalid_label_2.setText('Invalid amount')
            QTimer.singleShot(3000, lambda: self.invalid_label_2.setText(''))
            return
        # Define the path to the database file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'database.db')
        with sqlite3.connect(file_path) as conn:
            cursor = conn.cursor()
            # Check current user's balance
            cursor.execute('SELECT bank FROM users WHERE username = ?', (self.user,))
            result = cursor.fetchone()
            if result:
                current_balance = result[0]
                if current_balance < transfer_amount:
                    self.invalid_label_2.setText('Insufficient funds')
                    QTimer.singleShot(3000, lambda: self.invalid_label_2.setText(''))
                    return
                # Deduct from current user's balance
                new_balance = current_balance - transfer_amount
                cursor.execute('UPDATE users SET bank = ? WHERE username = ?', (new_balance, self.user))

                # Check if the recipient exists
                cursor.execute('SELECT bank FROM users WHERE username = ?', (transfer_id,))
                recipient_result = cursor.fetchone()
                
                if recipient_result:
                    # Add to recipient's balance
                    cursor.execute('UPDATE users SET bank = bank + ? WHERE username = ?', (transfer_amount, transfer_id))

                    # Commit the transaction
                    conn.commit()

                    self.invalid_label_2.setText('Transfer Successful')
                    QTimer.singleShot(3000, lambda: self.invalid_label_2.setText(''))
                    self.inner_stackedWidget.setCurrentWidget(self.blank_page)
                    # Update displayed balance
                    self.balance_label.setText(f'₱ {new_balance}')
                else:
                    self.invalid_label_2.setText('Recipient not found')
                    QTimer.singleShot(3000, lambda: self.invalid_label_2.setText(''))

            else:
                self.invalid_label_2.setText('Transfer failed')
                QTimer.singleShot(3000, lambda: self.invalid.setText(''))
    
    def poll_database(self):
        while True:
            self.check_bank_update()
            time.sleep(10)  # Check every 10 seconds

    def check_bank_update(self):
        # Define the path to the database file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'database.db')
        # Connect to the SQLite database
        with sqlite3.connect(file_path) as conn:

            self.cursor = conn.cursor()
            # Define the query to select the bank column
            query = 'SELECT  bank FROM users WHERE username = ?'
            self.cursor.execute(query, (self.user,))
            result = self.cursor.fetchone()
            if result:
                    bank = result[0]
                #convert the coount into string         
                    self.bank_display.setText(f'₱ {bank}')
                    self.balance_label.setText(f'₱ {bank}')
                    
    def dispaly_homepage(self):
        # Define the path to the database file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'database.db')
        # Connect to the SQLite database
        with sqlite3.connect(file_path) as conn:
            self.cursor = conn.cursor()
            # Define the query to select the bank column
            query = 'SELECT username,bank ,account,expiry FROM users WHERE username = ?'
            self.cursor.execute(query, (self.user,))
            result = self.cursor.fetchone()
            if result:
                username, bank,account,expiry = result
            #convert the coount into string   
                account_str = str(account)
            # Show only the last 4 digits of the account
                displayed_account = account_str[-4:] if len(account_str) > 4 else account_str
                self.display_account.setText(f'****  ****  ****  {displayed_account}')
                self.stackedWidget.setCurrentWidget(self.page_2)
                self.expiry_date.setText(f'{expiry}')
                self.username_display.setText(f'{username}!')
                self.balance_label.setText(f'₱ {bank}')

    
    def you_sure_page(self):
        '''This page is for Rosas'''
        transfer_id = self.transfer_input_id.text()
        transfer_amount = self.transfer_price_input.text()

        if transfer_id and transfer_amount:
            self.inner_stackedWidget.setCurrentWidget(self.page_4)
        else:
            self.validator_complete_details.setText('Please complete details')

    def blank_page_no(self):
        ''' if user dont accept  it goes to blank page'''
        self.inner_stackedWidget.setCurrentWidget(self.blank_page)

    def transfer_page_yes(self):
        self.inner_stackedWidget.setCurrentWidget(self.transfer_page_2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MyApp()
    main_app.show()
    sys.exit(app.exec())
    
