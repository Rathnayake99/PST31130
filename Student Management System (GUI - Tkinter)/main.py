import sqlite3
import bcrypt
from tkinter import *
from tkinter import messagebox, Label, Entry, Button, ttk

con = sqlite3.connect('student.db')
cursor = con.cursor()


cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
               username TEXT NOT NULL PRIMARY KEY, 
               password TEXT NOT NULL)''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS students(
               id INTEGER PRIMARY KEY,
               name TEXT NOT NULL,
               gender TEXT NOT NULL,
               age INTEGER NOT NULL,
               date VARCHAR NOT NULL,
               mid INTEGER NOT NULL,
               end INTEGER NOT NULL,
               gpa FLOAT NOT NULL)''')





class LoginPage(Tk):
    def __init__(self):
        super().__init__()

        self.title('Login')
        self.geometry('525x500+300+200')
        self.configure(bg='#fff')
        self.resizable(False,False)
        self.heading =   Label(text="Sign in",fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
        self.heading.place(x=215,y=5)

        self.user = Entry(width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
        self.user.place(x=150,y=150)
        self.user.insert(0,'Username')

        self.underLine = Frame(width=255,height=2,bg='black',).place(x=148,y=170)

        self.password = Entry(width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
        self.password.place(x=150,y=220)
        self.password.insert(0,'Password')

        self.underLine = Frame(width=255,height=2,bg='black',).place(x=148,y=240)

        self.login = Button(width=34,cursor='hand2',height=2,padx=7,text='Sign in',bg='#57a1f8',fg='white',border=0,command=self.login).place(x=150,y=270)
        self.Label=Label(text='Don\'t have an account?',fg='black',bg='white',font=('Microsoft YaHei UI Light',9)).place(x=148,y=340)

        self.signUp = Button(width=6,padx=7,text='Sign up',bg='white',fg='#57a1f8',cursor='hand2',border=0,command=self.goToSignup).place(x=290,y=340)

    def goToSignup(self):
        self.user.delete(0, 'end')
        self.password.delete(0, 'end')
        self.user.insert(0,'Username')
        self.password.insert(0,'Password')
        self.withdraw()
        signUp = SignupPage(self)
        signUp.mainloop()

    def login(self):
        username = self.user.get()
        password = self.password.get()

        if username != '' and password != '':
            cursor.execute('SELECT password FROM users WHERE username=?',[username])
            result = cursor.fetchone()
            if result:
                if bcrypt.checkpw(password.encode('utf-8'),result[0]):
                    self.user.delete(0, 'end')
                    self.password.delete(0, 'end')
                    self.user.insert(0,'Username')
                    self.password.insert(0,'Password')
                    self.withdraw()
                    dashboard = Dashboard(self)
                    dashboard.mainloop()
                else:
                    messagebox.showerror('Error','Invalid password.')
            else:
                messagebox.showerror('Error','Invalid username.')
        else:
            messagebox.showerror('Error','All fields are required.')


class SignupPage(Toplevel):
    def __init__(self,master):
        super().__init__(master)
        self.master = master

        self.title('SignUp')
        self.geometry('525x500+300+200')

        self.configure(bg='#fff')
        self.resizable(False,False)

        self.heading =   Label(self,text="Sign Up",fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
        self.heading.place(x=215,y=5)

        self.user = Entry(self,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
        self.user.place(x=150,y=150)
        self.user.insert(0,'Username')

        self.underLine = Frame(self,width=255,height=2,bg='black',).place(x=148,y=170)

        self.password = Entry(self,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
        self.password.place(x=150,y=220)
        self.password.insert(0,'Password')

        self.underLine = Frame(self,width=255,height=2,bg='black',).place(x=148,y=240)

        self.signup = Button(self,width=34,cursor='hand2',height=2,padx=7,text='Sign Up',bg='#57a1f8',fg='white',border=0,command=self.signup).place(x=150,y=270)
        self.Label=Label(self,text='You have an account?',fg='black',bg='white',font=('Microsoft YaHei UI Light',9)).place(x=148,y=340)

        self.backToLogin = Button(self,width=6,padx=7,text='Login',bg='white',fg='#57a1f8',cursor='hand2',border=0,command=self.backToLogin).place(x=290,y=340)

    def backToLogin(self):
        self.user.delete(0, 'end')
        self.password.delete(0, 'end')
        self.user.insert(0,'Username')
        self.password.insert(0,'Password')
        self.destroy()
        self.master.deiconify()

    def signup(self):
        username = self.user.get()
        password = self.password.get()

        if username != '' and password != '':
            cursor.execute('SELECT username FROM users WHERE username=?',[username])
            if cursor.fetchone() is not None:
                messagebox.showerror('Error', f"'{username}' name already exists.")

            else:
                encodePassword = password.encode('utf-8')
                hashedPassword = bcrypt.hashpw(encodePassword,bcrypt.gensalt())
                cursor.execute('INSERT INTO users VALUES (?,?)',[username,hashedPassword])
                con.commit()
                messagebox.showinfo('Message','User added successful!')
                self.user.delete(0, 'end')
                self.password.delete(0, 'end')
                self.user.insert(0,'Username')
                self.password.insert(0,'Password')
                self.destroy()
                self.master.deiconify()
        else:
            messagebox.showerror('Error','All fields are required.')
    

class Dashboard(Toplevel):
    def __init__(self,master):
        super().__init__(master)
        self.master = master

        self.title('Dashboard')
        self.geometry('1250x750')
        self.left_frame = LabelFrame(self, text="Student Records", width=400, height=550)
        self.left_frame.place(x=30, y=60)

        self.signUp_label = Label(self,text='Student Management',font=('Microsoft YaHei UI Light',23,'bold')).pack()

        Label(self.left_frame, text="ID:",font=('Microsoft YaHei UI Light',15,'bold')).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.id_entry = Entry(self.left_frame,font=('Microsoft YaHei UI Light',15,'bold'))
        self.id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        Label(self.left_frame, text="Name:",font=('Microsoft YaHei UI Light',15,'bold')).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.name_entry = Entry(self.left_frame,font=('Microsoft YaHei UI Light',15,'bold'))
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        Label(self.left_frame, text="Gender:",font=('Microsoft YaHei UI Light',15,'bold')).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.gender_combobox = ttk.Combobox(self.left_frame, values=["Male", "Female"],font=('Microsoft YaHei UI Light',15,'bold'),width=18)
        self.gender_combobox.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        Label(self.left_frame, text="Age:",font=('Microsoft YaHei UI Light',15,'bold')).grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.age_entry = Entry(self.left_frame,font=('Microsoft YaHei UI Light',15,'bold'))
        self.age_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        Label(self.left_frame, text="Enroll Date:",font=('Microsoft YaHei UI Light',15,'bold')).grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.enroll_date_entry = Entry(self.left_frame,font=('Microsoft YaHei UI Light',15,'bold'))
        self.enroll_date_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        Label(self.left_frame, text="Midterm:",font=('Microsoft YaHei UI Light',15,'bold')).grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.midterm_entry = Entry(self.left_frame,font=('Microsoft YaHei UI Light',15,'bold'))
        self.midterm_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')

        Label(self.left_frame, text="Final:",font=('Microsoft YaHei UI Light',15,'bold')).grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.final_entry = Entry(self.left_frame,font=('Microsoft YaHei UI Light',15,'bold'))
        self.final_entry.grid(row=6, column=1, padx=5, pady=5, sticky='w')

        Label(self.left_frame, text="GPA:",font=('Microsoft YaHei UI Light',15,'bold')).grid(row=7, column=0, padx=5, pady=5, sticky='w')
        self.gpa_entry = Entry(self.left_frame,font=('Microsoft YaHei UI Light',15,'bold'))
        self.gpa_entry.grid(row=7, column=1, padx=5, pady=5, sticky='w')

        # Buttons
        self.add_button = Button(self.left_frame, text="Add", width=10,font=('Microsoft YaHei UI Light',15,'bold'))
        self.add_button.grid(row=8, column=0, padx=5, pady=5)

        self.update_button = Button(self.left_frame, text="Update", width=10,font=('Microsoft YaHei UI Light',15,'bold'))
        self.update_button.grid(row=8, column=1, padx=5, pady=5)

        self.delete_button = Button(self.left_frame, text="Delete", width=10,font=('Microsoft YaHei UI Light',15,'bold'))
        self.delete_button.grid(row=9, column=0, padx=5, pady=5)

        self.clear_button = Button(self.left_frame, text="Clear", width=10,font=('Microsoft YaHei UI Light',15,'bold'))
        self.clear_button.grid(row=9, column=1, padx=5, pady=5)

        self.search_button = Button(self.left_frame, text="Search", width=10,font=('Microsoft YaHei UI Light',15,'bold'))
        self.search_button.grid(row=10, column=0, padx=5, pady=5)

        self.display_button = Button(self.left_frame, text="Display", width=10,font=('Microsoft YaHei UI Light',15,'bold'))
        self.display_button.grid(row=10, column=1, padx=5, pady=5)


        
        self.student_tree = ttk.Treeview(self, columns=("ID", "Name", "Gender", "Age", "Enroll Date", "Midterm", "Final", "GPA"),height=25)


        self.student_tree.heading("#0", text="Index")
        self.student_tree.heading("ID", text="ID")
        self.student_tree.heading("Name", text="Name")
        self.student_tree.heading("Gender", text="Gender")
        self.student_tree.heading("Age", text="Age")
        self.student_tree.heading("Enroll Date", text="Enroll Date")
        self.student_tree.heading("Midterm", text="Midterm")
        self.student_tree.heading("Final", text="Final")
        self.student_tree.heading("GPA", text="GPA")
        
        self.student_tree.column("#0", width=0, stretch=False) 
        self.student_tree.column("ID", width=50, stretch=False)
        self.student_tree.column("Name", width=200, stretch=False)
        self.student_tree.column("Gender", width=100, stretch=False)
        self.student_tree.column("Age", width=50, stretch=False)
        self.student_tree.column("Enroll Date", width=100, stretch=False)
        self.student_tree.column("Midterm", width=100, stretch=False)
        self.student_tree.column("Final", width=100, stretch=False)
        self.student_tree.column("GPA", width=50, stretch=False)
        
        self.student_tree.place(x=450, y=67)





app = LoginPage()
app.mainloop()