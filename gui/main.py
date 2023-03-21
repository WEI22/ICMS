import os
import sys, datetime
import shutil
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from passlib.hash import django_pbkdf2_sha256 as handler
from PIL import Image
from datetime import datetime

# Add Ui Codes
import PassSettings
import Register
import Guide
import Record
import Upload
import Home
import Detected
import User
import Edit

# Global Varibles
dir_GUI = os.getcwd()
dir_WEBUI = dir_GUI[:dir_GUI.rfind('\\')]
db_path = "/home/pi/ICMS/webui/db.sqlite3"
media_path = "/home/pi/ICMS/webui/media"
image_path = "/home/pi/ICMS/gui/Image/Saved"
login_status = False
current_mode = "Add Data"
user_id = None
user_name = ""
edit_data = []

# Utility function to allow switching between activities
class PageWindow(QtWidgets.QDialog):
    gotoSignal = QtCore.pyqtSignal(str)
    
    def goto(self, name):
        self.retrieveRecord()
        self.updateRecord()
        self.gotoSignal.emit(name)
    
    # Sidebar utilities
    def sidebar(self):
        self.ui.logo.clicked.connect(self.logoClicked)
        labels = ['home', 'info', 'record', 'upload']
        for label in labels:
            getattr(self.ui,'title_' + label + '_text').clicked.connect(getattr(self,label+'Clicked'))
            getattr(self.ui,'title_' + label + '_img').clicked.connect(getattr(self,label+'Clicked'))
    def logoClicked(self):
        if login_status:
            self.goto('user')
        else:
            self.goto('register')
    def infoClicked(self):
        self.goto('guide')
    def homeClicked(self):
        if login_status:
            self.goto('home')
        else:
            self.goto('register')
    def recordClicked(self):
        if login_status:
            self.goto('record')
        else:
            self.goto('register')
    def uploadClicked(self):
        if login_status:
            self.goto('user')
        else:
            self.goto('register')
        
    def retrieveRecord(self):
        pass
    
    def updateRecord(self):
        pass
    

##########################################################################################################################################.
# Login/Signup window
class WindowRegister(PageWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Register.Ui_Dialog()
        self.ui.setupUi(self)
        self.sidebar()
        self.set = PassSettings.PassSettings()
        self.ui.login_btn.clicked.connect(self.loginClicked)
        self.ui.login_forget.clicked.connect(self.forgetClicked)
        self.con = sqlite3.connect(db_path)
        self.checkAccount(self.set.get1(),self.set.get2())
        self.ui.login_error.hide()
        
    # Sidebar utilities
    def sidebar(self):
        self.ui.logo.clicked.connect(self.logoClicked)
        labels = ['home', 'info', 'record', 'upload']
        for label in labels:
            getattr(self.ui,'title_' + label + '_text').clicked.connect(getattr(self,label+'Clicked'))
            getattr(self.ui,'title_' + label + '_img').clicked.connect(getattr(self,label+'Clicked'))
    def loginCheck(self):
        if login_status == False:
            self.ui.login_error.setText('<html><head/><body><p><span style=" font-size:10pt; color:#ff0000;">Please login first</span></p></body></html>')
            self.ui.login_error.show()
        return login_status
    def logoClicked(self):
        if login_status:
            self.goto('user')
        else:
            self.ui.login_error.hide()
            self.goto('register')
    def infoClicked(self):
        self.ui.login_error.hide()
        self.goto('guide')
    def homeClicked(self):
        if self.loginCheck():
            self.ui.login_error.hide()
            self.goto('home')
    def recordClicked(self):
        if self.loginCheck():
            self.ui.login_error.hide()
            self.goto('record')
    def uploadClicked(self):
        if self.loginCheck():
            self.ui.login_error.hide()
            self.goto('user')
    
    # Login/Sign up Section
    # Error Message
    def errorMsg(self, msg):
        if msg == 'login':
            self.ui.login_error.setText('<html><head/><body><p><span style=" font-size:10pt; color:#ff0000;">Wrong credentials</span></p></body></html>')
            self.ui.login_error.show()
        elif msg == 'forget':
            errorMsg = QtWidgets.QMessageBox()
            errorMsg.setIcon(QtWidgets.QMessageBox.Question)
            errorMsg.setWindowTitle('Forget password?')
            errorMsg.setText('Well good luck finding it')
            errorMsg.exec_()
        
    # Login
    def checkAccount(self, loginDetails, loginPass):
        cur = self.con.cursor()
        email = cur.execute("SELECT email FROM auth_user")
        email = list(map(lambda x: x[0], email))
        username = cur.execute("SELECT username FROM auth_user")
        username = list(map(lambda x: x[0], username))
        global user_name
        if loginDetails in email:
            file = open('Log.txt','w')
            user_name = cur.execute(f"SELECT username FROM auth_user WHERE email='{loginDetails}'").fetchone()[0]
            temp = list(map(lambda x: x[0], user_name))
            user_name = ""
            for i in temp:
                user_name = user_name + i
        if loginDetails in username:
            user_name = loginDetails
        if loginDetails in email or loginDetails in username:
            user_password = cur.execute(f"SELECT password FROM auth_user WHERE email='{loginDetails}' OR username='{loginDetails}'").fetchone()[0]
            global user_id
            user_id = cur.execute(f"SELECT id FROM auth_user WHERE email='{loginDetails}' OR username='{loginDetails}'")
            user_id = list(map(lambda x: x[0], user_id))[0]
            salt = user_password.split("$")[2]
            password = handler.hash(loginPass, rounds=390000, salt=salt)
            if password == user_password:
                global login_status
                login_status = True
                if self.ui.login_remember.isChecked():
                    self.set.add(loginPass,loginDetails)
                self.goto('user')
                return
        self.errorMsg('login')
    
    # Sign up
    def forgetClicked(self):
        self.errorMsg('forget')
    
    # Login/Sign up utility function
    def loginClicked(self):
        loginEmail = self.ui.login_email_text.text()
        loginPass = self.ui.login_password_text.text()
        self.ui.login_email_text.setText('')
        self.ui.login_password_text.setText('')
        self.checkAccount(loginEmail, loginPass)
    
##########################################################################################################################################.
# How to use page
class WindowGuide(PageWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Guide.Ui_Dialog()
        self.ui.setupUi(self)
        self.sidebar()
        
##########################################################################################################################################.
# Past records (Link to database)
class WindowRecord(PageWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Record.Ui_Dialog()
        self.ui.setupUi(self)
        self.sidebar()
        
        # Record from database
        self.record = {'date' : [] , 'pest' : [] , 'host' : [], 'total': []}
        self.showId = []

        # Retrieve and update records
        self.retrieveRecord()
        self.updateRecord()
        
        self.ui.record_search_btn.clicked.connect(self.searchClicked)
        
    # Retrieve data from database
    def retrieveRecord(self):
        
        dates = [date[0] for date in sqlite3.connect(db_path).execute("SELECT date_created FROM web_image ORDER BY time_created")]
        pests = [pest[0] for pest in sqlite3.connect(db_path).execute("SELECT pest FROM web_image ORDER BY time_created")]
        hosts = [host[0] for host in sqlite3.connect(db_path).execute("SELECT host FROM web_image ORDER BY time_created")]
        totals = [total[0] for total in sqlite3.connect(db_path).execute("SELECT number FROM web_image ORDER BY time_created")]
            
        self.record = {'date' : dates, 'pest' : pests, 'host' : hosts, 'total': totals}
        self.showId = [1 for i in range(len(dates))]
    
    # Update data to screen
    def updateRecord(self):
        labels = ['date', 'host', 'pest', 'total']
        while len(self.record['date']) < 10:
            self.record['date'].append('')
            self.record['pest'].append('')
            self.record['host'].append('')
            self.record['total'].append('')
        for i in range(10):
            for label in labels:
                if str(self.record[label][i]) == "" or self.showId[i] == 0:
                    getattr(self.ui, 'record_table_' + label + str(i+1)).hide()
                else:
                    getattr(self.ui, 'record_table_' + label + str(i+1)).show()
                    getattr(self.ui, 'record_table_' + label + str(i+1)).setText(str(self.record[label][i]))
                
    def searchClicked(self):
        labels = ['date', 'host', 'pest', 'total']
        search_text = self.ui.record_search.text()
        self.showId = [0 for i in range(10)]
        for i in range(10):
            for label in labels:
                if search_text in str(self.record[label][i]):
                    self.showId[i] = 1
        self.updateRecord()
    
##########################################################################################################################################.
# Upload window
class WindowUpload(PageWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Upload.Ui_Dialog()
        self.ui.setupUi(self)
        self.sidebar()
        self.ui.upload_image.clicked.connect(self.uploadImg)
        
    def successMsg(self, name):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('Successfully uploaded image')
        filename = name[name.rfind('/')+1 : len(name)]
        msg.setText('Successfully uploaded ' + filename)
        msg.exec_()
        
    def uploadImg(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image File', r'C:\\', 'Image Files (*.jpg *.jpeg *.png)')
        if filename == '':
            return
        shutil.copy(filename, media_path)
        self.goto('detected')
        self.successMsg(filename)
        

##########################################################################################################################################.
# Home window
class WindowHome(PageWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Home.Ui_Dialog()
        self.ui.setupUi(self)
        self.sidebar()

##########################################################################################################################################.
# Pest detected window
class WindowDetected(PageWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Detected.Ui_Dialog()
        self.ui.setupUi(self)
        self.sidebar()

##########################################################################################################################################.
# User window
class WindowUser(PageWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = User.Ui_Dialog()
        self.ui.setupUi(self)
        self.sidebar()
        self.ui.user_title.setText('Hello, ' + user_name + '!')
        
        # Record from database
        self.record = {'date' : [] , 'pest' : [] , 'host' : [], 'total': [], 'img': []}
        self.showId = [0,0,0,0,0]
        self.cur = -1
        
        self.retrieveRecord()
        self.updateRecord()
        self.edit()
        self.delete()
        self.add()
        self.ui.user_profile.clicked.connect(self.profileClicked)
        self.ui.user_search_btn.clicked.connect(self.searchClicked)
    
    # Retrieve data from database
    def retrieveRecord(self):
#         self.record = {'date' : ['27/12/2022','28/12/2022']
#          , 'pest' : ['Aphids','Grasshopper']
#          , 'host' : ['Aphelandra','Cucumber']
#          , 'total': ['5','2']
#          , 'img' : ['Step1.png','Step2.png']}
        dates = [date[0] for date in sqlite3.connect(db_path).execute("SELECT date_created FROM web_image ORDER BY time_created")]
        pests = [pest[0] for pest in sqlite3.connect(db_path).execute("SELECT pest FROM web_image ORDER BY time_created")]
        hosts = [host[0] for host in sqlite3.connect(db_path).execute("SELECT host FROM web_image ORDER BY time_created")]
        totals = [total[0] for total in sqlite3.connect(db_path).execute("SELECT number FROM web_image ORDER BY time_created")]
        imgs = [img[0] for img in sqlite3.connect(db_path).execute("SELECT image FROM web_image ORDER BY time_created")]
        
        self.record = {'date' : dates, 'pest' : pests, 'host' : hosts, 'total': totals, 'img': imgs}
        self.showId = [1 for i in range(len(dates))]
        
                  
    # Update data to screen
    def updateRecord(self):
        labels = ['date', 'host', 'pest', 'total','img']
        extra = ['trash','edit']
        
        while len(self.record['date']) <= 5:
            self.record['date'].append('')
            self.record['pest'].append('')
            self.record['host'].append('')
            self.record['total'].append('')
            self.record['img'].append('')
            self.showId.append(0)
        for i in range(5):
            for label in labels:
                if self.record[label][i] == '' or self.showId[i] == 0:
                    getattr(self.ui,'user_'+label+str(i+1)).hide()
                    if label == 'img':
                        for obj in extra:
                            getattr(self.ui,'user_'+obj+str(i+1)).hide()
                else:
                    getattr(self.ui,'user_'+label+str(i+1)).show()
                    if label == 'img':
                        imgName = self.record['img'][i]
                        imgPath = media_path+'\\'+ imgName[imgName.rfind('/')+1:]
                        img = Image.open(imgPath)
                        img.thumbnail((150,150))
                        img.save(imgPath)
                        getattr(self.ui,'user_'+label+str(i+1)).setPixmap(QtGui.QPixmap(imgPath))
                        for obj in extra:
                            getattr(self.ui,'user_'+obj+str(i+1)).show()
                    else:
                        getattr(self.ui,'user_'+label+str(i+1)).setText(str(self.record[label][i]))
                        
    def edit(self):
        for i in range(5):
            getattr(self.ui, 'user_edit'+str(i+1)).clicked.connect(getattr(self,'editClicked'+str(i+1)))
        
    def delete(self):
        for i in range(5):
            getattr(self.ui, 'user_trash'+str(i+1)).clicked.connect(getattr(self,'deleteClicked'+str(i+1)))
    
    def add(self):
        self.ui.user_add.clicked.connect(self.addClicked)
        
    def editClicked1(self):
        self.cur = 0
        self.editSelection(0)
    def editClicked2(self):
        self.cur = 1
        self.editSelection(1)
    def editClicked3(self):
        self.cur = 2
        self.editSelection(2)
    def editClicked4(self):
        self.cur = 3
        self.editSelection(3)
    def editClicked5(self):
        self.cur = 4
        self.editSelection(4)
        
    def deleteClicked1(self):
        self.cur = 0
        self.deleteSelection(0)
    def deleteClicked2(self):
        self.cur = 1
        self.deleteSelection(1)
    def deleteClicked3(self):
        self.cur = 2
        self.deleteSelection(2)
    def deleteClicked4(self):
        self.cur = 3
        self.deleteSelection(3)
    def deleteClicked5(self):
        self.cur = 4
        self.deleteSelection(4)
    
    def addClicked(self):
        global current_mode
        current_mode = "Add Data"
        self.window = WindowEdit()
        self.window.submit.connect(self.addText)
        self.window.show()
    
    def addText(self, txt):
        items = txt.split('///$///')
        items[2] = 'images/'+items[2]
        items.insert(0,user_id)
        items.insert(0,'here')
        items.insert(4,1)
        items.insert(6,datetime.now().strftime("%Y-%m-%d"))
        items.append(datetime.now().strftime("%H:%M:%S"))
        data = tuple(items)
        
        sql = 'INSERT INTO web_image(location,author,host,number,cum_num,image,date_created,pest,time_created) VALUES(?,?,?,?,?,?,?,?,?)'
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute(sql, data)
        con.commit()
            
        self.retrieveRecord()
        self.updateRecord()
    
    def editSelection(self, i):
        global current_mode
        current_mode = "Edit Data"
        labels = ['host', 'total', 'pest', 'img']
        global edit_data
        edit_data = []
        for label in labels:
            edit_data.append(self.record[label][i])
         
        self.window = WindowEdit()
        self.window.submit.connect(self.editText)
        self.window.show()
    
    def editText(self, txt):
        labels = ['host', 'total', 'pest']
        oldImg = self.record['img'][self.cur]
        oldImg = oldImg[oldImg.rfind('/')+1:]
        items = txt.split('///$///')
        for i,label in enumerate(labels):
            if label != 'img':
                items.append(self.record[label][self.cur])
        
        if items[2] != oldImg:
            try:
                # os.remove(image_path+'\\'+oldImg)
                os.remove(media_path+'\\'+oldImg)
            except:
                pass
        
        items[2] = 'images/' + items[2]

        data = tuple(items)    
        sql = 'UPDATE web_image SET host = ?, number = ?, image = ?, pest = ? WHERE host = ? AND number = ? AND pest = ?'
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute(sql, data)
        con.commit()
        self.retrieveRecord()
        self.updateRecord()
    
    def deleteSelection(self, i):
        delWindow = QtWidgets.QMessageBox()
        delWindow.setWindowTitle('Delete record ' + str(i+1))
        delWindow.setText('Are you sure you want to delete?')
        delWindow.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        delWindow.setDefaultButton(QtWidgets.QMessageBox.No)
        delWindow.buttonClicked.connect(self.deleteText)
        delWindow.exec_()
            
    def deleteText(self, txt):
        if txt.text() == '&Yes':
            labels = ['host', 'total', 'pest']
            items = []
            oldImg = self.record['img'][self.cur]
            oldImg = oldImg[oldImg.rfind('/')+1:]
            for i,label in enumerate(labels):
                items.append(self.record[label][self.cur])
        
            try:
                # os.remove(image_path+'\\'+oldImg)
                os.remove(media_path+'\\'+oldImg)
            except:
                pass
    
            data = tuple(items)    
            sql = 'DELETE FROM web_image WHERE host = ? AND number = ? AND pest = ?'    
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            cur.execute(sql, data)
            con.commit()
            self.retrieveRecord()
            self.updateRecord()
        
    def profileClicked(self):
        profile = QtWidgets.QMessageBox()
        profile.setWindowTitle('User Profile')
        profile.setText('Logout?')
        profile.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        profile.setDefaultButton(QtWidgets.QMessageBox.No)
        profile.buttonClicked.connect(self.logout)
        profile.exec_()
    
    def logout(self, txt):
        if txt.text() == '&Yes':
            self.set = PassSettings.PassSettings()
            self.set.clear()
            global login_status
            login_status = False
            self.goto('register')
    
    def searchClicked(self):
        labels = ['date', 'host', 'pest', 'total','img']
        search_text = self.ui.user_search.text()
        self.showId = [0 for i in range(10)]
        for i in range(5):
            for label in labels:
                if search_text in str(self.record[label][i]):
                    self.showId[i] = 1
        self.updateRecord()

##########################################################################################################################################.
# Edit window
class WindowEdit(PageWindow):
    submit = QtCore.pyqtSignal(str)
    
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Edit.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(current_mode)
        self.ui.edit_image.setPixmap(QtGui.QPixmap(os.getcwd()+"/Image/Upload/Upload.png"))
        labels = ['host', 'total', 'pest', 'img']
        global edit_data
        if current_mode == "Edit Data":
            self.ui.edit_host.setText(edit_data[0])
            self.ui.edit_total.setText(str(edit_data[1]))
            self.ui.edit_pest.setText(edit_data[2])
            self.file = edit_data[3]
            edit_data[3] = media_path + '\\' + edit_data[3][edit_data[3].rfind('/')+1:]
            self.ui.edit_image.setPixmap(QtGui.QPixmap(edit_data[3]))
        else:
            self.ui.edit_image.clicked.connect(self.imageClicked)
        self.ui.edit_btn.clicked.connect(self.submitClicked)
    
    def imageClicked(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image File', r'C:\\', 'Image Files (*.jpg *.jpeg *.png)')
        if filename == "":
            return
        self.ui.edit_image.setPixmap(QtGui.QPixmap(filename))
        self.file = filename
        
    def submitClicked(self):
        submit = QtWidgets.QMessageBox()
        submit.setWindowTitle('Edit data')
        submit.setText('Confirm?')
        submit.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        submit.setDefaultButton(QtWidgets.QMessageBox.No)
        submit.buttonClicked.connect(self.submitData)
        submit.exec_()
        
    
    def submitData(self, txt):
        if txt.text() == '&Yes':
            if current_mode != "Edit Data":
                try:
                    #shutil.copy(self.file,image_path)
                    shutil.copy(self.file,media_path)
                except:
                    i = 1;
                    while True:
                        try:
                            if i == 100:
                                break
                            # shutil.copy(self.file+str(i),image_path)
                            shutil.copy(self.file+str(i),media_path)
                            self.file += str(i)
                            break
                        except:
                            i += 1
            filename = self.file[self.file.rfind('/')+1:]
            line = self.ui.edit_host.text() + '///$///' + self.ui.edit_total.text() + '///$///' + filename + '///$///' + self.ui.edit_pest.text()
                  
            self.submit.emit(line)
            self.close()
        
##########################################################################################################################################.
# Template window
# class WindowTemplate(PageWindow):
#     def __init__(self, parent = None):
#         QtWidgets.QWidget.__init__(self,parent)
#         self.ui = UiName.Ui_Dialog() # Change name of Ui Here
#         self.ui.setupUi(self)
#         self.sidebar()
        
##########################################################################################################################################.
# Class for main window -> Different activity will be on this window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.m_pages = {}
        
        self.register(WindowRegister(), 'register')
        self.register(WindowGuide(), 'guide')
        self.register(WindowRecord(), 'record')
        self.register(WindowUpload(), 'upload')
        self.register(WindowHome(), 'home')
        self.register(WindowDetected(), 'detected')
        self.register(WindowUser(), 'user')
        
        # Login page (Remember me option)
        if login_status:
            self.goto('home')
        else:
            self.goto('register')
    
    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)
            
    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.showMaximized()
            self.setWindowTitle(widget.windowTitle())

class main():
    app = QtWidgets.QApplication(sys.argv) 
    myapp = MainWindow()
    myapp.show() 
    sys.exit(app.exec_())
    
# Initialise main window
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv) 
#     myapp = MainWindow()
#     myapp.show() 
#     sys.exit(app.exec_())
