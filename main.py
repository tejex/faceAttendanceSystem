import subprocess
import tkinter as tk
import util 
import cv2
from PIL import Image, ImageTk
import datetime
import os

class App:
    def __init__(self) -> None:
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")
        
        self.loginButtonMain = util.getButton(self.main_window,"Login", "blue", self.login, fg="black")
        self.loginButtonMain.place(x=750,y=300)
        
        self.registerUserButtonMain = util.getButton(self.main_window, "Register New User", "gray", self.registerUser, fg="black")
        self.registerUserButtonMain.place(x=750,y=400)
        
        self.webCamLabel = util.getImageLabel(self.main_window)
        self.webCamLabel.place(x=10,y=0,width=700,height=500)
        
        self.addWebcam(self.webCamLabel)
        
        self.dbDirectory = './data/peopleIKnow'
        
        if not os.path.exists(self.dbDirectory):
            os.mkdir(self.dbDirectory)
        
        self.logPath = './log.txt'
        
    
    def addWebcam(self,label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        
        self._label = label
        self.processWebcam()
    
    def processWebcam(self):
        
        ret, frame = self.cap.read()
        self.most_recentCaptureArr = frame
        
        img_ = cv2.cvtColor(self.most_recentCaptureArr, cv2.COLOR_BGR2RGB)
        
        self.most_recentCaptureArrPIL = Image.fromarray(img_)
        imageTk = ImageTk.PhotoImage(image=self.most_recentCaptureArrPIL)
        
        self._label.imageTk = imageTk
        self._label.configure(image=imageTk)
        
        self._label.after(20, self.processWebcam)
        

    def registerUser(self):
        self.registerNewUserWindow = tk.Toplevel(self.main_window)
        self.registerNewUserWindow.geometry("1200x520+350+100")

        self.enterUserNameTextbox = util.getEntryText(self.registerNewUserWindow)
        self.enterUserNameTextbox.place(x=750,y=150)
        
        self.textLabel = util.getTextlabel(self.registerNewUserWindow,"Please input username")
        self.textLabel.place(x=750,y=70)
        
        self.registerUserButton = util.getButton(self.registerNewUserWindow,"Accept User", "blue", self.acceptNewUser, fg="black")
        self.registerUserButton.place(x=750,y=300)
        
        self.tryAgainButton = util.getButton(self.registerNewUserWindow,"Try Again", "blue", self.tryAgainMethod, fg="black")
        self.tryAgainButton.place(x=750,y=400)
        
        self.photoCaptureLabel = util.getImageLabel(self.registerNewUserWindow)
        self.photoCaptureLabel.place(x=10,y=0,width=700,height=500)
        
        self.addImageToLabel(self.photoCaptureLabel)
            
    def login(self):
        unknownImagePath = './.tmp.jpg'
        cv2.imwrite(unknownImagePath, self.most_recentCaptureArr)
        
        output = subprocess.check_output(["face_recognition", self.dbDirectory, unknownImagePath])
        output = str(output)
        name = output[output.rindex(",")+1:len(output)-3]
        
        if name in ['unknown_person', 'no_persons_found']:
            util.messageBox("Who are you? Please Register or Try Again : )")
        else:
            util.messageBox("Welcome back", "Welcome {}".format(name))
            with open(self.logPath,'a') as f:
                f.write('{}{}\n'.format(name, datetime.datetime.now()))
                f.close()
                
        os.remove(unknownImagePath)    
    
    def addImageToLabel(self, label):
        imageTk = ImageTk.PhotoImage(image=self.most_recentCaptureArrPIL)
        label.imageTk = imageTk
        label.configure(image=imageTk)
        
        self.newUserCapture = self.most_recentCaptureArr.copy()
        
    def tryAgainMethod(self):
        self.registerNewUserWindow.destroy() 
    
    def acceptNewUser(self):
        #getting the name the user inputted into the text field
        name = self.enterUserNameTextbox.get(1.0,"end-1c")
        #saving the image the user has taken into our database which is just the folder (people we know)
        cv2.imwrite(os.path.join(self.dbDirectory,'{}.jpg'.format(name)), self.newUserCapture)
        
        util.messageBox("Capture Result: ","User Registered Successfully!")
        self.registerNewUserWindow.destroy()
        
    def start(self):
        self.main_window.mainloop()
    
    
if __name__ == "__main__":
    app = App()
    app.start()


