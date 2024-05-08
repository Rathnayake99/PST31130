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
        self.geometry('1250x650')
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
        self.add_button = Button(self.left_frame, text="Add", width=10,font=('Microsoft YaHei UI Light',15,'bold'),command=self.addStudent)
        self.add_button.grid(row=8, column=0, padx=5, pady=5)

        self.update_button = Button(self.left_frame, text="Update", width=10,font=('Microsoft YaHei UI Light',15,'bold'),command=self.updateStudent)
        self.update_button.grid(row=8, column=1, padx=5, pady=5)

        self.delete_button = Button(self.left_frame, text="Delete", width=10,font=('Microsoft YaHei UI Light',15,'bold'),command=self.deleteStudent)
        self.delete_button.grid(row=9, column=0, padx=5, pady=5)

        self.clear_button = Button(self.left_frame, text="Clear", width=10,font=('Microsoft YaHei UI Light',15,'bold'))
        self.clear_button.grid(row=9, column=1, padx=5, pady=5)

        self.search_button = Button(self.left_frame, text="Search", width=10,font=('Microsoft YaHei UI Light',15,'bold'),command=self.searchById)
        self.search_button.grid(row=10, column=0, padx=5, pady=5)

        self.display_button = Button(self.left_frame, text="Display", width=10,font=('Microsoft YaHei UI Light',15,'bold'),command=self.display)
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

        self.student_tree.tag_configure("evenrow", background="#f0f0f0")
        self.student_tree.tag_configure("oddrow", background="#4CCD99")
        
        self.student_tree.place(x=450, y=67)

    def addStudent(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        gender = self.gender_combobox.get()
        age = self.age_entry.get()
        eDate = self.enroll_date_entry.get()
        mid = self.midterm_entry.get()
        end = self.final_entry.get()
        gpa = self.gpa_entry.get()

        if id != '' and name != '' and gender != '' and age != '' and eDate != '' and mid != '' and end != '' and gpa != '':
            try:
                checkedId = int(id)
                checkedAge = int(age)
                checkedMid = int(mid)
                checkedEnd = int(end)
                checkedGPA = float(gpa)

                cursor.execute('SELECT id FROM students where id=?',[checkedId])
                result = cursor.fetchall()
                if not result:
                    cursor.execute('INSERT INTO students VALUES (?,?,?,?,?,?,?,?)',[checkedId,name,gender,checkedAge,eDate,checkedMid,checkedEnd,checkedGPA])
                    con.commit()
                    messagebox.showinfo('Message','Student added successfull')
                else:
                    messagebox.showerror('Error','This id is already exists.')

            except ValueError:
                messagebox.showerror("Error", "Integer or float type error")

        else:
            messagebox.showerror('Error','All fields are required!')

    def display(self):
        
        try:
            self.student_tree.delete(*self.student_tree.get_children())
            cursor.execute('SELECT * FROM students')
            rows = cursor.fetchall()

            for i, row in enumerate(rows, start=1):
                tags = ("evenrow",) if i % 2 == 0 else ("oddrow",)
                self.student_tree.insert("", "end", values=row, tags=tags)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def updateStudent(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        gender = self.gender_combobox.get()
        age = self.age_entry.get()
        eDate = self.enroll_date_entry.get()
        mid = self.midterm_entry.get()
        end = self.final_entry.get()
        gpa = self.gpa_entry.get()

        if id != '' and name != '' and gender != '' and age != '' and eDate != '' and mid != '' and end != '' and gpa != '':
            try:
                checkedId = int(id)
                checkedAge = int(age)
                checkedMid = int(mid)
                checkedEnd = int(end)
                checkedGPA = float(gpa)

                cursor.execute('SELECT id FROM students WHERE id=?', [checkedId])
                result = cursor.fetchall()
                if result:
                    cursor.execute('UPDATE students SET name=?, gender=?, age=?, date=?, mid=?, end=?, gpa=? WHERE id=?',
                                   (name, gender, checkedAge, eDate, checkedMid, checkedEnd, checkedGPA, checkedId))
                    con.commit()
                    messagebox.showinfo('Success', 'Student information updated successfully')
                else:
                    messagebox.showerror('Error', 'Student with this ID does not exist.')

            except ValueError:
                messagebox.showerror("Error", "Please enter valid integer or float values")
        else:
            messagebox.showerror('Error', 'All fields are required!')

    def deleteStudent(self):
        id = self.id_entry.get()

        if id != '':
            try:
                checkedId = int(id)

                cursor.execute('SELECT id FROM students WHERE id=?', [checkedId])
                result = cursor.fetchall()

                if result:
                    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this student?")

                    if confirmation:
                        cursor.execute('DELETE FROM students WHERE id=?', [checkedId])
                        con.commit()
                        messagebox.showinfo('Success', 'Student deleted successfully')

                else:
                    messagebox.showerror('Error', 'Student with this ID does not exist.')

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer ID")

        else:
            messagebox.showerror('Error', 'Please enter the ID of the student to be deleted')

    def searchById(self):
        id = self.id_entry.get()
        if id != '':
            try:
                checkedId = int(id)
                

                cursor.execute('SELECT id FROM students WHERE id=?', [checkedId])
                result = cursor.fetchall()

                if result:
                    self.student_tree.delete(*self.student_tree.get_children())
                    cursor.execute('SELECT * FROM students WHERE id=?', [checkedId])
                    rows = cursor.fetchall()

                    for i, row in enumerate(rows, start=1):
                        tags = ("evenrow",) if i % 2 == 0 else ("oddrow",)
                        self.student_tree.insert("", "end", values=row, tags=tags)

                else:
                    messagebox.showerror('Error', 'Student with this ID does not exist.')

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer ID")

        else:
            messagebox.showerror('Error', 'Please enter the ID of the student to be search')


app = LoginPage()
app.mainloop()