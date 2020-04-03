# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'host.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# Needs PyQt5 to run
# Pip install pyqt5 or equivalent should work

from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import selectors
import os
import time
import argparse
import threading
import select

SEND_SIZE = 1024

# Sockets that will be used for sending stuff
server_socket = None
peer_socket = None

# Variables that we will need for registration
username = None
serv_IP = None
serv_port = None

# .data ending is basically the same as a text file
descriptions_file = "descriptions.data"

textBoxText = "Please connect to a server to begin.\n"
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(925, 425)

        #### LAYOUT TO CONTAIN CONNECTION STUFF AND CHAT STUFF ####
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 900, 400))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.connectionLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.connectionLabel.setFont(font)
        self.connectionLabel.setObjectName("connectionLabel")
        self.verticalLayout.addWidget(self.connectionLabel)

        #### LAYOUT TO CONTAIN SERVER IP, PORT, USERNAME, AND CONNECT BUTTON ####
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        #### SERVER IP AND PORT STUFF ####
        self.serverIPLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.serverIPLabel.setObjectName("serverIPLabel")
        self.horizontalLayout.addWidget(self.serverIPLabel)
        self.serverIPText = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.serverIPText.setObjectName("serverIPText")
        self.horizontalLayout.addWidget(self.serverIPText)
        self.portNumberLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.portNumberLabel.setObjectName("portNumberLabel")
        self.horizontalLayout.addWidget(self.portNumberLabel)
        self.portNumberText = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.portNumberText.setObjectName("portNumberText")
        self.horizontalLayout.addWidget(self.portNumberText)

        #### USERNAME ENTERING PART ####
        self.usernameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.usernameLabel.setObjectName("usernameLabel")
        self.horizontalLayout.addWidget(self.usernameLabel)
        self.usernameText = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.usernameText.setObjectName("usernameText")
        self.horizontalLayout.addWidget(self.usernameText)

        #### CONNECT BUTTON ####
        self.connectButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.connectButton.setObjectName("connectButton")
        self.horizontalLayout.addWidget(self.connectButton)

        #### CREATE SERVER BUTTON ####
        self.createServerButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.createServerButton.setObjectName("createServerButton")
        self.horizontalLayout.addWidget(self.createServerButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        ####### CHATBOX AND MESSAGE ENTERING STARTS HERE #######
        self.chatWindow = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.chatWindow.setFont(font)
        self.chatWindow.setObjectName("chatWindow")
        self.verticalLayout.addWidget(self.chatWindow)

        #### CHAT BOX ####
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem6 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)

        self.verticalScrollbar = QtWidgets.QScrollBar(self.verticalLayoutWidget)


        self.outputText = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.outputText.sizePolicy().hasHeightForWidth())
        #self.outputText.setSizePolicy(sizePolicy)
        #self.outputText.setLineWrapMode(QtGui.QTextEdit.FixedPixelWidth)
        self.outputText.setLineWrapColumnOrWidth(80)
        self.outputText.setReadOnly(True)
        self.outputText.setObjectName("outputText")
        self.outputText.setVerticalScrollBar(self.verticalScrollbar)

        global textBoxText
        self.outputText.setPlaceholderText(textBoxText)
        self.horizontalLayout_6.addWidget(self.outputText)
        self.verticalLayout.addLayout(self.horizontalLayout_6)

        #### MESSAGE ENTERING THING ####
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem5 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.enterMessageLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.enterMessageLabel.setObjectName("enterMessageLabel")
        self.horizontalLayout_4.addWidget(self.enterMessageLabel)
        self.enterMessageText = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.enterMessageText.setObjectName("enterMessageText")
        self.horizontalLayout_4.addWidget(self.enterMessageText)
        self.sendButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout_4.addWidget(self.sendButton)
        self.clearButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout_4.addWidget(self.clearButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)

        #ADD ACTION LISTENERS FOR BUTTONS
        self.connectButton.clicked.connect(self.connect_button_clicked)
        self.createServerButton.clicked.connect(self.create_button_clicked)
        # self.searchButton.clicked.connect(self.search_button_clicked)
        self.sendButton.clicked.connect(self.send_button_clicked)
        self.clearButton.clicked.connect(self.clear_button_clicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def printAndSet(self, strText):
        global textBoxText
        print(strText)
        self.outputText.append(strText)
        #textBoxText = textBoxText + strText
        #self.outputText.setPlaceholderText(textBoxText)
    
    '''
# Method to connect to a provided IP and port. 
# Returns the connected socket if successful, or None if not successful
'''
    def connect_to(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        failedToConnect = False
        try:
            s.settimeout(5)
            self.printAndSet("Connecting to " + ip + ":" + str(port) + "...")
            s.connect((ip, int(port)))
        except:
            failedToConnect = True
            #self.printAndSet("Failed to connect.\n")

        if(not failedToConnect):
            #self.printAndSet("Successfully Connected!\n")
            global username
            s.sendall(username.encode())
            return s
        return None

    def close_and_end(self):
        global peer_socket
        global server_socket
        global username

        try:
            stringToSend = username + " " + "|||CLOSE|||"
            peer_socket.sendall(stringToSend.encode())
        except Exception as e:
            #self.printAndSet("Unable to send close message to any server: " + str(e))
            pass

        try:
            peer_socket.close()
            self.printAndSet("Closed Peer Connection")
        except Exception as e:
            #self.printAndSet("No peer connection to close: " + str(e))
            pass

        try:
            server_socket.close()
            self.printAndSet("Closed Server Connection")
        except Exception as e:
            #self.printAndSet("No hosted chatroom to close: " + str(e))
            pass

    def connect_button_clicked(self):
        global username, serv_IP, serv_port, peer_socket, textBoxText
        # THE CONNECT BUTTON IS PRESSED
        # CONNECTING CODE GOES HERE
        # GET serverIP AND PORT NUMBER. ETC
        # Probably serverIPText.getText() or similar

        if (peer_socket != None):
            #self.printAndSet("Closed previous connection.")
            self.close_and_end()
            peer_socket = None
            
        username = self.usernameText.text()
        serv_addr = self.serverIPText.text()
        serv_port = self.portNumberText.text()

        try:
            new_connection = self.connect_to(serv_addr, serv_port)
            if (new_connection != None):
                peer_socket = new_connection                    
                self.printAndSet("Connected to " + serv_addr + ":" + serv_port)
                #print(username.encode())
                #print(str(type(server_socket)))
                threading.Thread(target=self.accept_input_user).start()
                #server_socket.sendall(username.encode())
            else:
                self.printAndSet("Failed to connect")
        except Exception as e:
            print(str(type(peer_socket)))
            self.printAndSet("Failed to connect: " + str(e))

    def start_server(self):
        #THE GO BUTTON IS PRESSED
        global username, serv_IP, serv_port, server_socket, textBoxText

        if (server_socket != None):
            self.printAndSet("Closed previous connection.")
            self.close_and_end()
            server_socket = None

        username = self.usernameText.text()
        serv_IP = self.serverIPText.text()
        serv_port = int(self.portNumberText.text())

        if (username == "" or serv_IP == "" or serv_port == ""):
            self.printAndSet("Input unspecified, please include a server IP, port, and a username")
            return

        self.printAndSet("Creating server")
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((serv_IP, serv_port))
            server_socket.listen()
            self.printAndSet("Server started with IP " + serv_IP + " on port " + str(serv_port) + ". Waiting for connection.")
        except Exception as e:
            if (server_socket != None):
                server_socket.close()
            server_socket = None
            self.printAndSet("     Something went wrong with your server!     " + str(e) + "")

    def accept_input_user(self):
        global peer_socket
        if (peer_socket != None):
            while True:
                conn = peer_socket
                while True:
                    # Check to see if any data is here/arriving. If so, then do stuff with it.
                    ready = select.select([conn], [], [], 5)
                    if (ready[0]):
                        try:
                            dataSent = conn.recv(33000)
                        except:
                            # Most likely. this user disconnected, and so this thread will fail since the connection was closed.
                            return
                        if not dataSent:
                            break
                        # Do stuff w/ the message here
                        decodeData = dataSent.decode().split(" ")
                        # If they only sent a username (blank message) don't bother printing
                        if (len(decodeData) == 1):
                            break
                        # Otherwise, they sent an actual message, so format and print
                        fromUser = decodeData[0]
                        decodeData = decodeData[1:]
                        if (decodeData[0] == "|||CLOSE|||"):
                            #peer_socket.close()
                            self.printAndSet("Other user disconnected.")
                            self.close_and_end()
                            return
                        # Append received message to textbox
                        global textBoxText
                        stringToPrint = fromUser + ": "
                        for word in decodeData:
                            stringToPrint = stringToPrint + word + " "
                        self.printAndSet(stringToPrint)
            peer_socket.close()
            peer_socket = None

    def accept_input_server(self):
        global server_socket
        if (server_socket != None):
            while (True):
                conn, addr = server_socket.accept()
                global peer_socket
                peer_socket = conn
                with conn:
                    connUser = conn.recv(1024)
                    self.printAndSet("Connected to by user " + str(connUser.decode()) + " " + str(addr) + "")
                    #peer_socket = conn
                    while True:
                        dataSent = conn.recv(33000)
                        if not dataSent:
                            break
                        # Do stuff w/ the message here
                        decodeData = dataSent.decode().split(" ")
                        # If they only sent a username (blank message) don't bother printing
                        #if (len(decodeData) == 1):
                            #break
                        # Otherwise, they sent an actual message, so format and print
                        fromUser = decodeData[0]
                        decodeData = decodeData[1:]
                        print("Decode data = " + str(decodeData))
                        if (decodeData[0] == "|||CLOSE|||"):
                            #peer_socket.close()
                            self.printAndSet("Other user disconnected.")
                            #self.printAndSet("Closed Server Connection")
                            self.close_and_end()
                            return
                        # Append received message to textbox
                        global textBoxText
                        stringToPrint = fromUser + ": "
                        for word in decodeData:
                            stringToPrint = stringToPrint + word + " "
                        self.printAndSet(stringToPrint)
            peer_socket.close()
            peer_socket = None

    def create_button_clicked(self):
        self.start_server()
        threading.Thread(target=self.accept_input_server).start()

    def send_button_clicked(self):
        #THE SEND BUTTON IS PRESSED
        global username
        # Get text from the GUI bar
        msgToSend = self.enterMessageText.text()
        if (len(msgToSend.split(" ")) == 0):
            self.printAndSet("Please enter a message.")
            return
        
        # Send that message to whoever you are connected to
        global peer_socket
        if (peer_socket != None):
            self.printAndSet(username + ": " + msgToSend)
            msgToSend = username + " " + msgToSend
            #self.printAndSet("Sending message: ||||| " + msgToSend + " |||||\n")
            try:
                peer_socket.sendall(msgToSend.encode())
            except:
                self.printAndSet("Unfortunately, something went wrong with the connection, or your partner tried to connect to someone else.")
                peer_socket.close()
            self.enterMessageText.setText("")
            #self.printAndSet("Send button pressed\n")
        else:
            self.printAndSet("Not connected to a peer, so cannot send message.")

    def clear_button_clicked(self):
        #THE CLEAR BUTTON IS PRESSED
        self.outputText.clear()
        self.printAndSet("Chat window cleared.")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.connectionLabel.setText(_translate("MainWindow", "Connection"))
        self.serverIPLabel.setText(_translate("MainWindow", "Server IP:"))
        self.portNumberLabel.setText(_translate("MainWindow", "Port:"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.usernameLabel.setText(_translate("MainWindow", "Username:"))
        self.chatWindow.setText(_translate("MainWindow", "Chatroom"))
        self.enterMessageLabel.setText(_translate("MainWindow", "Enter Message:"))
        self.sendButton.setText(_translate("MainWindow", "Send"))
        self.clearButton.setText(_translate("MainWindow", "Clear Chat"))
        self.createServerButton.setText(_translate("MainWindow", "Create Server"))

        # TODO Temporary for testing, remove once completed
        self.serverIPText.setText("127.0.0.1")
        self.portNumberText.setText("54321")
        self.usernameText.setText("defaultUser")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowTitle("Host")
    MainWindow.show()
    app.exec_()
    ui.close_and_end()
    sys.exit()