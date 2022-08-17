from tkinter import *
import tkinter.ttk as ttk
import csv
import os  # accessing the os functions
import check_camera
import Capture_Image
import Train_Image
import Recognize

root = Tk()
root.title("Attendance System ")
root.resizable(0, 0)
# Window size
appWidth = 852
appHeight = 480
font = "Times New Roman"


screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

x = int((screenWidth / 2) - (appWidth / 2))
y = int((screenHeight / 2) - (appHeight / 2))

# window pops up on center of the screen
root.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')

myLabel1 = Label(root, text="Attendance detail",
                 font=("Calibri", 15), fg="Blue", anchor=N)  # Title
myLabel1.place(relx=0.2,rely=0.0)
TableMargin = Frame(root, width=500)
TableMargin.place(relx=0.0,rely=0.05)

scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("ID", "Name", "Date",'Time'), height=400, selectmode="extended",
                    yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('ID', text="ID", anchor=W)
tree.heading('Name', text="Name", anchor=W)
tree.heading('Date', text="Date", anchor=W)
tree.heading('Time', text="Time", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=120)
tree.column('#2', stretch=NO, minwidth=0, width=120)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.pack()
with open('Attendance/test.csv') as f:
  reader = csv.DictReader(f, delimiter=',')

  for row in reader:

     id = row['Id']
     name = row['Name']
     dt = row['Date']
     ti = row['Time']
     tree.insert("", 0, values=( id,name, dt,ti))

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False



global Output1,Output2,Output3,entry1,entry2,button_generate5,mystring1,mystring2



# --------------------------------------------------------------
# calling the take image function form capture image.py file

def CaptureFaces():
    global Output1, Output2, Output3, entry1, entry2, button_generate5,mystring1,mystring2
    Output6.config(text="")
    Output1 = Label(root, text="Enter Name And ID of student:", font=("Calibri", 12), fg="red")
    Output1.place(relx=0.68, rely=0.63)
    Output2 = Label(root, text="ID:", font=("Calibri", 15))
    Output2.place(relx=0.68, rely=0.7)
    Output3 = Label(root, text="Name:", font=("Calibri", 15))
    Output3.place(relx=0.68, rely=0.8)
    mystring1 = StringVar(root)
    mystring2 = StringVar(root)

    entry1 = Entry(root,textvariable = mystring1)
    entry1.place(relx=0.78, rely=0.7)

    entry2 = Entry(root,textvariable = mystring2)
    entry2.place(relx=0.78, rely=0.8)
    button_generate5 = Button(root, text="Submit", padx=43,command=lambda :submit())
    button_generate5.place(relx=0.76, rely=0.9)






def submit():
    global Output1, Output2, Output3, entry1, entry2, button_generate5,mystring1,mystring2
    x1=mystring1.get()
    x2=mystring2.get()
    if x1!='' and x2!='':
        if (is_number(x1) and x2.isalpha()):
            Output1.destroy()
            Output2.destroy()
            Output3.destroy()
            entry1.destroy()
            entry2.destroy()
            button_generate5.destroy()
            Output6.config(text="Capturing")
            Capture_Image.takeImages(x1, x2)
            Output6.config(text="Captured")






# -----------------------------------------------------------------
# calling the train images from train_images.py file

def Trainimages():
    Output6.config(text="Training")
    Train_Image.TrainImages()
    Output6.config(text="Trained")



# --------------------------------------------------------------------
# calling the recognize_attendance from recognize.py file
global filename
filename=''
def RecognizeFaces():
    global filename
    filename=Recognize.recognize_attendence()
    Output6.config(text="Recognized")


def refresh():
    global filename
    if filename!='':
        with open(filename) as f:
            reader = csv.DictReader(f, delimiter=',')

            for row in reader:
                id = row['Id']
                name = row['Name']
                dt = row['Date']
                ti = row['Time']
                tree.insert("", 0, values=(id, name, dt, ti))
        os.remove(filename)
        filename=''
    Output6.config(text="Updated")

button_generate1 = Button(root, text="Capture Faces", padx=20,command=lambda :CaptureFaces())
button_generate1.place(relx=0.76,rely=0.2)
button_generate2 = Button(root, text="Train Images", padx=26,command=lambda :Trainimages())
button_generate2.place(relx=0.76,rely=0.3)
button_generate3 = Button(root, text="Recognize\nAttendance", padx=33,command=lambda :RecognizeFaces())
button_generate3.place(relx=0.76,rely=0.4)


button_generate3 = Button(root, text="Update", padx=43,command=lambda :refresh())
button_generate3.place(relx=0.76,rely=0.53)

Output6 = Label(root, text="", font=("Calibri", 12), fg="red")
Output6.place(relx=0.8, rely=0.8)

root.mainloop()
