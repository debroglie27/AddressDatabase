# **************** Developed By: ARIJEET DE ******************
# Last Updated: 29-03-2023

import os
import smtplib
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
from dotenv import load_dotenv, set_key
from cryptography.fernet import Fernet

# conn = sqlite3.connect('./address_book.db')
# c = conn.cursor()

# # Use this query in case to know details inside the database
# query = "SELECT * FROM sqlite_master"
# c.execute(query)
# print(c.fetchall())
# conn.commit()
# conn.close()

# ADDRESS TABLE
# c.execute('''CREATE TABLE addresses(
#           first_name text,
#           last_name text,
#           address text,
#           city text,
#           state text,
#           zipcode integer)''')

# USERS TABLE
# c.execute('''CREATE TABLE users(
#            Username text PRIMARY KEY,
#            Password text,
#            email_id text)''')

# ADMIN: Arijeet
# Secret Key: 12345

# Users = ['Arijeet', 'Mrinal', 'Nibedita', 'Hritesh', 'Shubham', 'Prajnanshu', 'Manish']
# Password = ['1234', '1967', '1969', '1999', '1010', '1998', '007']


# 1. Login Window
class WinLogin:

    def __init__(self, master, title):
        self.root = master
        self.root.title(title)
        self.root.geometry("370x230+450+150")
        self.root.resizable(width=False, height=False)

        # Bullet Symbol
        self.bullet_symbol = "\u2022"

        # Register the username_placeholder_vanish function
        username_placeholder_vanish_func = self.root.register(self.username_placeholder_vanish)
        # Register the password_placeholder_vanish function
        password_placeholder_vanish_func = self.root.register(self.password_placeholder_vanish)

        # Username Label and Entry
        self.username_label = Label(self.root, text="Username:", font=('Helvetica', 15))
        self.username_label.grid(row=0, column=0, padx=10, pady=(30, 0))
        self.username_entry = Entry(self.root, fg="#BFBFBF", font=('Helvetica', 15), validate="focusin", validatecommand=username_placeholder_vanish_func)
        self.username_entry.grid(row=0, column=1, padx=10, pady=(30, 0), columnspan=3)

        # Password Label and Entry
        self.password_label = Label(self.root, text="Password:", font=('Helvetica', 15))
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = Entry(self.root, fg="#BFBFBF", font=('Helvetica', 15), validate="focusin", validatecommand=password_placeholder_vanish_func)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

        # Login Button
        self.login_button = Button(self.root, text="Login", bg="#90EE90", font=('Helvetica', 11), command=self.login_check)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=20, padx=(35, 0), ipadx=6)

        # SignUp Button
        self.signup_button = Button(self.root, text="SignUp", bg="#add8e6", font=('Helvetica', 11),
                                    command=lambda: self.forgot_signup_window(WinSignup, "SignUp Window"))
        self.signup_button.grid(row=2, column=2, columnspan=2, pady=20, padx=(0, 50), ipadx=6)

        # Forgot Password Button
        self.forgot_pass_button = Button(self.root, text="Forgot Password?", fg="blue", relief=FLAT,
                                         command=lambda: self.forgot_signup_window(WinForgotPass, "Forgot Password Window"))
        self.forgot_pass_button.grid(row=3, column=1, padx=(0, 30), columnspan=2)

        # Placeholder for our Entry Boxes and also giving a message to distinguish
        self.username_entry.insert(0, "Username")
        self.password_entry.insert(0, "Password")

        # Loading our .env file
        env_path = Path(env_file_path)
        load_dotenv(dotenv_path=env_path)

        # Getting the ENCRYPTION_KEY
        key = os.environ.get('ENCRYPTION_KEY')
        self.cipher_suite = Fernet(key)

    def username_placeholder_vanish(self):
        if self.username_entry.get() == "Username":
            # Deleting the Placeholder and making foreground "black"
            self.username_entry.delete(0, END)
            self.username_entry.config(fg="black")

    def password_placeholder_vanish(self):
        if self.password_entry.get() == "Password":
            # Deleting the Placeholder, making foreground "black" and also the "show"
            self.password_entry.delete(0, END)
            self.password_entry.config(fg="black", show=self.bullet_symbol)

    def login_check(self):
        # Storing the Entry Boxes value in variables
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # Finding Password and OID for the given Username
            query = 'Select Password, oid from users where Username=?'
            c.execute(query, (username,))

            encrypted_password, oid = c.fetchone()

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!", parent=self.root)
            return

        # Decrypting original Password
        original_password = self.cipher_suite.decrypt(encrypted_password).decode()

        if password == original_password:
            self.new_window(WinHome, "Home Window", oid)
        else:
            messagebox.showerror("Error", "Incorrect!!! Username or Password", parent=self.root)

    def forgot_signup_window(self, _class, title):
        level = Tk()
        _class(level, title)
        self.root.destroy()

    def new_window(self, _class, title, oid):
        level = Tk()
        _class(level, title, oid)
        self.root.destroy()


# 2. Forgot Password Window
class WinForgotPass:

    def __init__(self, master, title):
        self.root = master
        self.root.title(title)
        self.root.geometry("360x200+450+150")
        self.root.resizable(width=False, height=False)

        # Instruction Label
        self.instruction_label = Label(self.root, text="Provide Your Email-id\nwhere password will be shared.", font=('Helvetica', 13), fg="green")
        self.instruction_label.grid(row=0, column=0, padx=65, pady=(20, 0), columnspan=4)

        # Email Label and Entry
        self.email_label = Label(self.root, text="Email:", font=('Helvetica', 15))
        self.email_label.grid(row=1, column=0, padx=10, pady=20)
        self.email_entry = Entry(self.root, font=('Helvetica', 15))
        self.email_entry.grid(row=1, column=1, padx=(0, 30), pady=20, columnspan=3)

        # Back Button
        self.back_button = Button(self.root, text="Back", bg="#add8e6", font=('Helvetica', 11), command=self.close_window)
        self.back_button.grid(row=2, column=0, columnspan=2, pady=10, padx=(40, 0), ipadx=10)

        # Send Button
        self.send_button = Button(self.root, text="Send", bg="#90EE90", font=('Helvetica', 11), command=self.email_check)
        self.send_button.grid(row=2, column=2, columnspan=2, pady=10, padx=(0, 60), ipadx=10)

        # Loading the Environment Variables from .env file
        env_path = Path(env_file_path)
        load_dotenv(dotenv_path=env_path)

        self.EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        self.EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

        # Getting the ENCRYPTION_KEY
        key = os.environ.get('ENCRYPTION_KEY')
        self.cipher_suite = Fernet(key)

    def email_check(self):
        # Displaying Message Informing that it will take time
        messagebox.showinfo("Information", "It may take some time\nPlease Wait!!!", parent=self.root)
        email = self.email_entry.get()

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # Finding Password for the given Email_id
            query = 'Select Password from users where email_id=?'
            c.execute(query, (email,))

            result = c.fetchone()

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
            return

        if result is None:
            messagebox.showerror("Error", "Incorrect!!! Email-id", parent=self.root)
        else:
            encrypted_password = result[0]
            # Decrypting Encrypted Password
            user_password = self.cipher_suite.decrypt(encrypted_password).decode()

            try:
                # Sending Email Code
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)

                    subject = 'Forgot Password: Address Database'
                    body = f'Dear User\n\nPlease find your Password of your Address Database Account\n\nPassword: {user_password}'

                    msg = f'Subject: {subject}\n\n{body}'

                    smtp.sendmail(self.EMAIL_ADDRESS, email, msg)

                    # Message to inform that Email has been sent
                    messagebox.showinfo("Information", "Mail has been sent Successfully:)", parent=self.root)
                    self.close_window()

            except smtplib.SMTPResponseException as e:
                error_code = e.smtp_code
                error_message = e.smtp_error
                messagebox.showerror(f"Error Code: {error_code}", f"Error Message: {error_message}\nPlease Try Again!",
                                     parent=self.root)

    def close_window(self):
        level = Tk()
        WinLogin(level, "Login Window")
        self.root.destroy()


# 3. Window for SignUp
class WinSignup:

    def __init__(self, master, title):
        self.root = master
        self.root.title(title)
        self.root.geometry('380x280+450+150')
        self.root.resizable(width=False, height=False)

        # Bullet Symbol
        self.bullet_symbol = "\u2022"

        # Username Label and Entry
        self.username_label = Label(self.root, text="Username:", font=('Helvetica', 15))
        self.username_label.grid(row=0, column=0, padx=10, pady=(30, 0), sticky=E)
        self.username_entry = Entry(self.root, font=('Helvetica', 15))
        self.username_entry.grid(row=0, column=1, padx=10, pady=(30, 0), columnspan=3)

        # Password Label and Entry
        self.password_label = Label(self.root, text="Password:", font=('Helvetica', 15))
        self.password_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky=E)
        self.password_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.password_entry.grid(row=1, column=1, padx=10, pady=(10, 0), columnspan=3)

        # Email Label and Entry
        self.email_label = Label(self.root, text="Email:", font=('Helvetica', 15))
        self.email_label.grid(row=2, column=0, padx=10, pady=10, sticky=E)
        self.email_entry = Entry(self.root, font=('Helvetica', 15))
        self.email_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=3)

        # Admin Secret Key
        self.secret_label = Label(self.root, text="Secret Key:", font=('Helvetica', 15))
        self.secret_label.grid(row=3, column=0, padx=10, pady=(20, 10), sticky=E)
        self.secret_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.secret_entry.grid(row=3, column=1, padx=10, pady=(20, 10), columnspan=3)

        # Back Button
        self.back_button = Button(self.root, text="Back", bg="#add8e6", font=('Helvetica', 11), command=self.close_window)
        self.back_button.grid(row=4, column=0, columnspan=2, pady=20, padx=(30, 0), ipadx=4)

        # Submit Button
        self.submit_button = Button(self.root, text="Submit", bg="#90EE90", font=('Helvetica', 11), command=self.signup_check)
        self.submit_button.grid(row=4, column=2, columnspan=2, pady=20, padx=(0, 60), ipadx=4)

        # Loading the Environment Variable from .env file
        env_path = Path(env_file_path)
        load_dotenv(dotenv_path=env_path)

        # Getting the ENCRYPTION_KEY
        key = os.environ.get('ENCRYPTION_KEY')
        self.cipher_suite = Fernet(key)

        # Getting the Secret Key
        self.encrypted_secret_key = os.environ.get('SECRET_KEY')

    def signup_check(self):
        # Storing the values of Entry Boxes
        username = self.username_entry.get()
        password = self.password_entry.get()
        email_id = self.email_entry.get()
        secret_key = self.secret_entry.get()

        # Clearing the Entry Boxes
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.secret_entry.delete(0, END)

        # Decrypting secret key
        original_secret_key = self.cipher_suite.decrypt(self.encrypted_secret_key).decode()

        if not secret_key == original_secret_key:
            messagebox.showerror("Error", "Secret Key Incorrect!!!", parent=self.root)
        else:
            # Encrypting the given password
            encrypted_password = self.cipher_suite.encrypt(password.encode())

            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                # Inserting Details of New User
                query = "Insert Into users(Username, Password, email_id) values(?, ?, ?)"
                c.execute(query, (username, encrypted_password, email_id))

                conn.commit()
                conn.close()

                # Displaying message informing that account was added successfully
                messagebox.showinfo("Information", "Account Successfully Added!!!", parent=self.root)

            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username Already Taken!\nPlease Enter Other Username", parent=self.root)
            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

        self.close_window()

    def close_window(self):
        level = Tk()
        WinLogin(level, "Login Window")
        self.root.destroy()


# 4. Home Window
class WinHome:

    def __init__(self, master, title, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title(title)
        self.root.geometry("377x360+450+120")
        self.root['bg'] = "#90EE90"
        self.root.resizable(width=False, height=False)

        self.head_label = Label(self.root, text="Welcome to Database", fg="purple", bg='#add8e6', bd=4, relief=GROOVE,
                                font=('Monotype Corsiva', 32, "bold"))
        self.head_label.pack(pady=(0, 10), ipadx=10, ipady=5)

        self.but_insert = Button(self.root, text="Insert", font=('Helvetica', 15), bg='#fdebd0',
                                 command=lambda: self.new_window(WinInsert, "Insert Window", self.user_oid))
        self.but_insert.pack(pady=(15, 0), ipadx=35)
        self.but_search = Button(self.root, text="Search", font=('Helvetica', 15), bg='#fdebd0',
                                 command=lambda: self.new_window(WinSearch, "Search Window", self.user_oid))
        self.but_search.pack(pady=(20, 0), ipadx=29)
        self.but_update = Button(self.root, text="Update", font=('Helvetica', 15), bg='#fdebd0',
                                 command=lambda: self.new_window(WinUpdate, "Update Window", self.user_oid))
        self.but_update.pack(pady=(20, 0), ipadx=29)
        self.but_delete = Button(self.root, text="Delete", font=('Helvetica', 15), bg='#fdebd0',
                                 command=lambda: self.new_window(WinDelete, "Delete Window", self.user_oid))
        self.but_delete.pack(pady=(20, 0), ipadx=32)

        # Create Menu
        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)

        # Add File Menu
        self.file_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="File", menu=self.file_menu)
        # Add File Menu Items
        self.file_menu.add_command(label="Insert", command=lambda: self.new_window(WinInsert, "Insert Window", self.user_oid))
        self.file_menu.add_command(label="Search", command=lambda: self.new_window(WinSearch, "Search Window", self.user_oid))
        self.file_menu.add_command(label="Update", command=lambda: self.new_window(WinUpdate, "Update Window", self.user_oid))
        self.file_menu.add_command(label="Delete", command=lambda: self.new_window(WinDelete, "Delete Window", self.user_oid))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Logout", command=lambda: self.logout(WinLogin, "Login Window"))
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Add Settings Menu
        self.settings_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Settings", menu=self.settings_menu)
        # Add Settings Menu Items
        self.settings_menu.add_command(label="User Details", command=lambda: self.new_window(WinUserDetails, "User Details", self.user_oid))
        self.settings_menu.add_command(label="Change Password", command=lambda: self.new_window(WinChangePassword, "Change Password", self.user_oid))

        # Only for Admin
        if self.user_oid == 1:
            # Add Admin Settings Menu
            self.admin_settings_menu = Menu(self.my_menu, tearoff=False)
            self.my_menu.add_cascade(label="Admin Settings", menu=self.admin_settings_menu)
            # Add Settings Menu Items
            self.admin_settings_menu.add_command(label="All User Details",
                                                 command=lambda: self.new_window(WinAllUserDetails, "All User Details", self.user_oid))
            self.admin_settings_menu.add_command(label="Change Secret Key",
                                                 command=lambda: self.new_window(WinChangeSecretKey, "Change Secret Key", self.user_oid))

        # Add Right Click Pop Up Menu
        self.my_popup_menu = Menu(self.root, tearoff=False)
        # Insert, Search, Update and Delete
        self.my_popup_menu.add_command(label="Insert", command=lambda: self.new_window(WinInsert, "Insert Window", self.user_oid))
        self.my_popup_menu.add_command(label="Search", command=lambda: self.new_window(WinSearch, "Search Window", self.user_oid))
        self.my_popup_menu.add_command(label="Update", command=lambda: self.new_window(WinUpdate, "Update Window", self.user_oid))
        self.my_popup_menu.add_command(label="Delete", command=lambda: self.new_window(WinDelete, "Delete Window", self.user_oid))
        self.my_popup_menu.add_separator()
        # User Details and Change Password
        self.my_popup_menu.add_command(label="User Details", command=lambda: self.new_window(WinUserDetails, "User Details", self.user_oid))
        self.my_popup_menu.add_command(label="Change Password", command=lambda: self.new_window(WinChangePassword, "Change Password", self.user_oid))
        self.my_popup_menu.add_separator()

        # Only for Admin
        if self.user_oid == 1:
            # All User Details and Change Secret Key
            self.my_popup_menu.add_command(label="All User Details",
                                           command=lambda: self.new_window(WinAllUserDetails, "All User Details", self.user_oid))
            self.my_popup_menu.add_command(label="Change Secret Key",
                                           command=lambda: self.new_window(WinChangeSecretKey, "Change Secret Key", self.user_oid))
            self.my_popup_menu.add_separator()

        # Logout and Exit
        self.my_popup_menu.add_command(label="Logout", command=lambda: self.logout(WinLogin, "Login Window"))
        self.my_popup_menu.add_command(label="Exit", command=root.quit)

        # Binding the Right click Pop Up Menu
        self.root.bind("<Button-3>", self.my_popup)

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # Finding Username for our Status Bar
            query = 'Select Username from users where OID=?'
            c.execute(query, (self.user_oid,))

            username = c.fetchone()[0]

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
            self.logout(WinLogin, "Login Window")
            return

        # Finding whether our user is an ADMIN or not
        if self.user_oid == 1:
            text = f'User: {username} (ADMIN) '
        else:
            text = f'User: {username} '

        # Add Status Bar
        self.status_bar = Label(self.root, text=text, anchor=E, bg="#dfdfdf")
        self.status_bar.pack(fill=X, side=BOTTOM, ipady=1)

    def my_popup(self, event):
        self.my_popup_menu.tk_popup(event.x_root, event.y_root)

    def logout(self, _class, title):
        level = Tk()
        _class(level, title)
        self.root.destroy()

    def new_window(self, _class, title, oid):
        level = Tk()
        _class(level, title, oid)
        self.root.destroy()


# 5. Window for User Details
class WinUserDetails:

    def __init__(self, master, title, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title(title)
        self.root.geometry("435x220+440+150")
        self.root.resizable(width=False, height=False)

        # Username Label and Entry
        self.username_label = Label(self.root, text="Username:", font=('Helvetica', 15))
        self.username_label.grid(row=0, column=0, padx=10, pady=(30, 0), sticky=E)
        self.username_entry = Entry(self.root, font=('Helvetica', 15), fg="green", width=19)
        self.username_entry.grid(row=0, column=1, padx=10, pady=(30, 0), sticky=W)

        # Email Label and Entry
        self.email_label = Label(self.root, text="Email:", font=('Helvetica', 15))
        self.email_label.grid(row=1, column=0, padx=10, pady=20, sticky=E)
        self.email_entry = Entry(self.root, font=('Helvetica', 15), fg="green", width=19)
        self.email_entry.grid(row=1, column=1, padx=10, pady=20, sticky=W)

        # Change Buttons
        self.change_button1 = Button(self.root, text="Change", font=('Helvetica', 10), bg="orange", command=lambda: self.change_entry(0))
        self.change_button1.grid(row=0, column=2, padx=5, pady=(30, 0))
        self.change_button2 = Button(self.root, text="Change", font=('Helvetica', 10), bg="orange", command=lambda: self.change_entry(1))
        self.change_button2.grid(row=1, column=2, padx=5, pady=20)

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # Finding Details of User
            query = 'Select Username, Email_id from users where OID=?'
            c.execute(query, (self.user_oid,))

            username, email = c.fetchone()

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
            self.close_window()
            return

        # Displaying Values in Username Entry and Email Entry
        self.username_entry.insert(0, username)
        self.email_entry.insert(0, email)

        # Making the Entry Boxes READ-ONLY
        self.username_entry.config(state="readonly")
        self.email_entry.config(state="readonly")

        # Back and Save Button Frame
        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=2, column=0, columnspan=3)

        # Back Button
        self.back_button = Button(self.button_frame, text="Back", bg="#add8e6", font=("Helvetica", 11), command=self.close_window)
        self.back_button.grid(row=0, column=0, padx=(20, 40), ipadx=5)

        # Save Button
        self.save_button = Button(self.button_frame, text="Save", bg="#90EE90", font=('Helvetica', 11), command=self.save_details)
        self.save_button.grid(row=0, column=1, pady=20, padx=(40, 0), ipadx=5)

    def close_window(self):
        level = Tk()
        WinHome(level, "Home Window", self.user_oid)
        self.root.destroy()

    def change_entry(self, val):
        if val == 0:
            self.username_entry.config(state=NORMAL)
        elif val == 1:
            self.email_entry.config(state=NORMAL)

    def save_details(self):
        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # Updating the database with new values
            query = "update users set Username = ?, Email_id = ? where OID = ?"
            e = (self.username_entry.get(), self.email_entry.get(), self.user_oid)
            c.execute(query, e)

            conn.commit()
            conn.close()

            # Message Informing Successful Saving
            messagebox.showinfo("Information", "Successfully Saved", parent=self.root)

            self.close_window()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username Already Taken!\nPlease Enter Other Username", parent=self.root)
        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)


# 6. Window for Changing Password
class WinChangePassword:

    def __init__(self, master, title, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title(title)
        self.root.geometry("450x280+440+150")
        self.root.resizable(width=False, height=False)

        # Bullet Symbol
        self.bullet_symbol = "\u2022"

        # Current Password Label and Entry
        self.current_password_label = Label(self.root, text="Current Password:", font=('Helvetica', 15))
        self.current_password_label.grid(row=0, column=0, padx=10, pady=(30, 20), sticky=E)
        self.current_password_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.current_password_entry.grid(row=0, column=1, padx=10, pady=(30, 20), sticky=W)

        # New Password Label and Entry
        self.new_password_label = Label(self.root, text="New Password:", font=('Helvetica', 15))
        self.new_password_label.grid(row=1, column=0, padx=10, pady=(20, 10), sticky=E)
        self.new_password_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.new_password_entry.grid(row=1, column=1, padx=10, pady=(20, 10), sticky=W)

        # Confirm Password Label and Entry
        self.confirm_password_label = Label(self.root, text="Confirm Password:", font=('Helvetica', 15))
        self.confirm_password_label.grid(row=2, column=0, padx=10, pady=(5, 0), sticky=E)
        self.confirm_password_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.confirm_password_entry.grid(row=2, column=1, padx=10, pady=(5, 0), sticky=W)

        # Back and Save Button Frame
        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=3, column=0, pady=20, columnspan=2)

        # Back Button
        self.back_button = Button(self.button_frame, text="Back", bg="#add8e6", font=("Helvetica", 11), command=self.close_window)
        self.back_button.grid(row=0, column=0, padx=(20, 40), ipadx=5)

        # Save Button
        self.save_button = Button(self.button_frame, text="Save", bg="#90EE90", font=('Helvetica', 11), command=self.change_password)
        self.save_button.grid(row=0, column=1, pady=20, padx=(30, 0), ipadx=5)

        # Loading the Environment Variables from .env file
        env_path = Path(env_file_path)
        load_dotenv(dotenv_path=env_path)

        # Getting the ENCRYPTION_KEY
        key = os.environ.get('ENCRYPTION_KEY')
        self.cipher_suite = Fernet(key)

    def close_window(self):
        level = Tk()
        WinHome(level, "Home Window", self.user_oid)
        self.root.destroy()

    def change_password(self):
        # Storing the values of Entry Boxes
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Clearing the Entry Boxes
        self.current_password_entry.delete(0, END)
        self.new_password_entry.delete(0, END)
        self.confirm_password_entry.delete(0, END)

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # Finding password for the given user
            query = "Select password from users where oid=?"
            c.execute(query, (self.user_oid,))

            encrypted_password = c.fetchone()[0]

            conn.commit()
            conn.close()

            # Decrypting Encrypted Password
            original_password = self.cipher_suite.decrypt(encrypted_password).decode()

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
            return

        if original_password != current_password:
            messagebox.showerror("Error", "Wrong Current Password!!!", parent=self.root)
        else:
            if new_password != confirm_password:
                messagebox.showerror("Error", "Confirm Password is not same\nas New Password!!!", parent=self.root)
            else:
                # Encrypting the password
                encrypted_confirm_password = self.cipher_suite.encrypt(confirm_password.encode())

                try:
                    conn = sqlite3.connect(database_file_path)
                    c = conn.cursor()

                    # Update password for the particular user_oid
                    query = "update users set password = ? where OID = ?"
                    c.execute(query, (encrypted_confirm_password, self.user_oid))

                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Information", "Password Changed Successfully!!!", parent=self.root)

                except sqlite3.OperationalError:
                    messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

        self.close_window()


# 7. Window for All User Details
class WinAllUserDetails:

    def __init__(self, master, title, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title(title)
        self.root.geometry("390x290+450+130")
        self.root.resizable(width=False, height=False)

        # Add some style
        self.style = ttk.Style()
        # Pick a theme
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                             background="white",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="#E3E3E3")

        self.style.map('Treeview',
                       background=[('selected', 'yellow')],
                       foreground=[('selected', 'black')])

        # Create TreeView Frame
        self.tree_frame = Frame(self.root)
        self.tree_frame.pack(pady=(20, 0), padx=10)

        # TreeView ScrollBar
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        # Create TreeView
        self.my_tree = ttk.Treeview(self.tree_frame, height=6, yscrollcommand=self.tree_scroll.set)
        self.my_tree.pack()

        # Configure ScrollBar
        self.tree_scroll.config(command=self.my_tree.yview)

        # Define our columns
        self.my_tree['columns'] = ("OID", "Username", "Email")

        # Format our columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("OID", anchor=CENTER, width=30)
        self.my_tree.column("Username", anchor=CENTER, width=100)
        self.my_tree.column("Email", anchor=CENTER, width=180)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=CENTER)
        self.my_tree.heading("OID", text="OID", anchor=CENTER)
        self.my_tree.heading("Username", text="Username", anchor=CENTER)
        self.my_tree.heading("Email", text="Email", anchor=CENTER)

        # Count Variable for number of records
        self.count = 0

        # Create Stripped row Tags
        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="lightblue")

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            c.execute("Select OID, Username, Email_id from users where oid <> 1")
            records = c.fetchall()

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
            self.close_window()
            return

        # Resetting the Count
        self.count = 0

        for record in records:
            if self.count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=str(self.count), text="", values=record, tags=("evenrow",))
            else:
                self.my_tree.insert(parent='', index='end', iid=str(self.count), text="", values=record, tags=("oddrow",))
            self.count += 1

        # Back and Remove Button Frame
        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=(20, 10))

        # Back Button
        self.back_button = Button(self.button_frame, text="Back", bg="#add8e6", font=("Helvetica", 11), command=self.close_window)
        self.back_button.grid(row=0, column=0, pady=10, padx=(5, 45), ipadx=5)

        # Remove Button
        self.remove_button = Button(self.button_frame, text="Remove", bg="orange", font=('Helvetica', 11), command=self.remove_user)
        self.remove_button.grid(row=0, column=1, pady=10, padx=(25, 0), ipadx=5)

    def close_window(self):
        level = Tk()
        WinHome(level, "Home Window", self.user_oid)
        self.root.destroy()

    def remove_user(self):
        if self.my_tree.focus():
            for record in self.my_tree.selection():
                # Getting the OID from the record
                oid = self.my_tree.item(record)['values'][0]

                try:
                    conn = sqlite3.connect(database_file_path)
                    c = conn.cursor()

                    c.execute("Delete from users where oid=?", (oid, ))

                    conn.commit()
                    conn.close()

                except sqlite3.OperationalError:
                    messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
                    return

                # removing the record from the treeview
                self.my_tree.delete(record)

                messagebox.showinfo("Information", "Successfully Removed!")
        else:
            messagebox.showinfo("Information", "Please select a record to remove!!!")


# 8. Window for Changing Secret Key
class WinChangeSecretKey:

    def __init__(self, master, title, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title(title)
        self.root.geometry("456x290+430+130")
        self.root.resizable(width=False, height=False)

        # Bullet Symbol
        self.bullet_symbol = "\u2022"

        # Current Password Label and Entry
        self.current_secret_key_label = Label(self.root, text="Current Secret Key:", font=('Helvetica', 15))
        self.current_secret_key_label.grid(row=0, column=0, padx=10, pady=(30, 10), sticky=E)
        self.current_secret_key_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.current_secret_key_entry.grid(row=0, column=1, padx=10, pady=(30, 10), sticky=W)

        # Forgot Secret Key Button
        self.forgot_secret_key_button = Button(self.root, text="Forgot Secret Key?", fg="blue", relief=FLAT,
                                               command=lambda: self.new_window(WinForgotSecretKey, "Forgot Secret Key Window", self.user_oid))
        self.forgot_secret_key_button.grid(row=1, column=0, columnspan=2)
        
        # New Password Label and Entry
        self.new_secret_key_label = Label(self.root, text="New Secret Key:", font=('Helvetica', 15))
        self.new_secret_key_label.grid(row=2, column=0, padx=10, pady=(15, 10), sticky=E)
        self.new_secret_key_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.new_secret_key_entry.grid(row=2, column=1, padx=10, pady=(15, 10), sticky=W)

        # Confirm Password Label and Entry
        self.confirm_secret_key_label = Label(self.root, text="Confirm Secret Key:", font=('Helvetica', 15))
        self.confirm_secret_key_label.grid(row=3, column=0, padx=10, pady=(5, 0), sticky=E)
        self.confirm_secret_key_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.confirm_secret_key_entry.grid(row=3, column=1, padx=10, pady=(5, 0), sticky=W)

        # Back and Save Button Frame
        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=4, column=0, pady=20, columnspan=2)

        # Back Button
        self.back_button = Button(self.button_frame, text="Back", bg="#add8e6", font=("Helvetica", 11), command=self.close_window)
        self.back_button.grid(row=0, column=0, padx=(10, 40), ipadx=5)

        # Save Button
        self.save_button = Button(self.button_frame, text="Save", bg="#90EE90", font=('Helvetica', 11), command=self.change_secret_key)
        self.save_button.grid(row=0, column=1, pady=20, padx=(30, 0), ipadx=5)

        # Loading the Environment Variables from .env file
        env_path = Path(env_file_path)
        load_dotenv(dotenv_path=env_path)

        # Getting the ENCRYPTION_KEY
        key = os.environ.get('ENCRYPTION_KEY')
        self.cipher_suite = Fernet(key)

        # Getting the Secret Key
        self.encrypted_secret_key = os.environ.get('SECRET_KEY')

    def new_window(self, _class, title, oid):
        level = Tk()
        _class(level, title, oid)
        self.root.destroy()

    def close_window(self):
        level = Tk()
        WinHome(level, "Home Window", self.user_oid)
        self.root.destroy()

    def change_secret_key(self):
        # Storing the values of Entry Boxes
        current_secret_key = self.current_secret_key_entry.get()
        new_secret_key = self.new_secret_key_entry.get()
        confirm_secret_key = self.confirm_secret_key_entry.get()

        # Clearing the Entry Boxes
        self.current_secret_key_entry.delete(0, END)
        self.new_secret_key_entry.delete(0, END)
        self.confirm_secret_key_entry.delete(0, END)

        # Decrypting secret key - self.encrypted_secret_key is from the __init__() method
        original_secret_key = self.cipher_suite.decrypt(self.encrypted_secret_key).decode()

        if current_secret_key != original_secret_key:
            messagebox.showerror("Error", "Wrong Current Secret Key!!!", parent=self.root)
            return
        else:
            if new_secret_key != confirm_secret_key:
                messagebox.showerror("Error", "Confirm Secret Key is not same\nas New Secret Key!!!", parent=self.root)
                return
            else:
                encrypted_confirm_secret_key = self.cipher_suite.encrypt(confirm_secret_key.encode()).decode()

                os.environ['SECRET_KEY'] = encrypted_confirm_secret_key
                set_key(env_file_path, "SECRET_KEY", os.environ["SECRET_KEY"])

                messagebox.showinfo("Information", "Secret Key Changed Successfully!!!", parent=self.root)

        self.close_window()


# 9. Window for Forgot Secret Key
class WinForgotSecretKey:

    def __init__(self, master, title, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title(title)
        self.root.geometry("360x200+450+150")
        self.root.resizable(width=False, height=False)

        # Instruction Label
        self.instruction_label = Label(self.root, text="Provide Your Email-id\nwhere Secret Key will be shared.",
                                       font=('Helvetica', 13), fg="green")
        self.instruction_label.grid(row=0, column=0, padx=57, pady=(20, 0), columnspan=4)

        # Email Label and Entry
        self.email_label = Label(self.root, text="Email:", font=('Helvetica', 15))
        self.email_label.grid(row=1, column=0, padx=10, pady=20)
        self.email_entry = Entry(self.root, font=('Helvetica', 15))
        self.email_entry.grid(row=1, column=1, padx=(0, 30), pady=20, columnspan=3)

        # Back Button
        self.back_button = Button(self.root, text="Back", bg="#add8e6", font=('Helvetica', 11), command=self.close_window)
        self.back_button.grid(row=2, column=0, columnspan=2, pady=10, padx=(40, 0), ipadx=10)

        # Send Button
        self.send_button = Button(self.root, text="Send", bg="#90EE90", font=('Helvetica', 11), command=self.email_check)
        self.send_button.grid(row=2, column=2, columnspan=2, pady=10, padx=(0, 60), ipadx=10)

        # Loading the Environment Variables from .env file
        env_path = Path(env_file_path)
        load_dotenv(dotenv_path=env_path)

        self.EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        self.EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

        # Getting the ENCRYPTION_KEY
        key = os.environ.get('ENCRYPTION_KEY')
        self.cipher_suite = Fernet(key)

        # Getting the Secret Key
        self.encrypted_secret_key = os.environ.get('SECRET_KEY')

    def email_check(self):
        messagebox.showinfo("Information", "It may take some time\nPlease Wait!!!", parent=self.root)
        email = self.email_entry.get()

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            query = 'select oid from users where email_id=?'
            c.execute(query, (email, ))

            oid = c.fetchone()

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
            return

        if oid is None or oid[0] != 1:
            messagebox.showerror("Error", "Incorrect! Email-id", parent=self.root)
        else:
            # Decrypting secret key
            secret_key = self.cipher_suite.decrypt(self.encrypted_secret_key).decode()

            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)

                    subject = 'Forgot Secret Key: Address Database'
                    body = f'Dear User\n\nPlease find the Secret Key of the Address Database Account\n\nSecret Key: {secret_key}'

                    msg = f'Subject: {subject}\n\n{body}'

                    smtp.sendmail(self.EMAIL_ADDRESS, email, msg)

                    messagebox.showinfo("Information", "Mail has been sent Successfully:)", parent=self.root)

            except smtplib.SMTPResponseException as e:
                error_code = e.smtp_code
                error_message = e.smtp_error
                messagebox.showerror(f"Error Code: {error_code}", f"Error Message: {error_message}\nPlease Try Again!",
                                     parent=self.root)

        self.close_window()

    def close_window(self):
        level = Tk()
        WinChangeSecretKey(level, "Change Secret Key", self.user_oid)
        self.root.destroy()


# 10. Insert Window
class WinInsert:

    def __init__(self, master, title, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title(title)
        self.root.geometry("395x330+440+140")
        self.root.resizable(width=False, height=False)

        # All Entry Boxes
        self.f_name = Entry(self.root, width=20, font=('Helvetica', 15))
        self.f_name.grid(row=0, column=1, pady=(15, 5), padx=(20, 0))
        self.l_name = Entry(self.root, width=20, font=('Helvetica', 15))
        self.l_name.grid(row=1, column=1, pady=5, padx=(20, 0))
        self.address = Entry(self.root, width=20, font=('Helvetica', 15))
        self.address.grid(row=2, column=1, pady=5, padx=(20, 0))
        self.city = Entry(self.root, width=20, font=('Helvetica', 15))
        self.city.grid(row=3, column=1, pady=5, padx=(20, 0))
        self.state = Entry(self.root, width=20, font=('Helvetica', 15))
        self.state.grid(row=4, column=1, pady=5, padx=(20, 0))
        self.zipcode = Entry(self.root, width=20, font=('Helvetica', 15))
        self.zipcode.grid(row=5, column=1, pady=5, padx=(20, 0))

        # All Labels
        self.f_name_label = Label(self.root, text="First Name:", font=('Helvetica', 15))
        self.f_name_label.grid(row=0, column=0, padx=(20, 0), pady=(15, 5), sticky=E)
        self.l_name_label = Label(self.root, text="Last Name:", font=('Helvetica', 15))
        self.l_name_label.grid(row=1, column=0, padx=(20, 0), pady=5, sticky=E)
        self.address_label = Label(self.root, text="Address:", font=('Helvetica', 15))
        self.address_label.grid(row=2, column=0, padx=(20, 0), pady=5, sticky=E)
        self.city_label = Label(self.root, text="City:", font=('Helvetica', 15))
        self.city_label.grid(row=3, column=0, padx=(20, 0), pady=5, sticky=E)
        self.state_label = Label(self.root, text="State:", font=('Helvetica', 15))
        self.state_label.grid(row=4, column=0, padx=(20, 0), pady=5, sticky=E)
        self.zipcode_label = Label(self.root, text="Zipcode:", font=('Helvetica', 15))
        self.zipcode_label.grid(row=5, column=0, padx=(20, 0), pady=5, sticky=E)

        # Back and Submit Button Frame
        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=6, column=0, pady=10, columnspan=2)

        # Back Button
        self.back_button = Button(self.button_frame, text="Back", bg="#add8e6", font=("Helvetica", 11), command=self.close_window)
        self.back_button.grid(row=0, column=0, padx=(20, 40), ipadx=5)

        # Submit Button
        self.submit_button = Button(self.button_frame, text="Submit", bg="#90EE90", font=('Helvetica', 11), command=self.submit)
        self.submit_button.grid(row=0, column=1, pady=20, padx=(30, 0), ipadx=5)

    def submit(self):
        if self.f_name.get() == self.l_name.get() == self.address.get() == self.city.get() == self.state.get() == self.zipcode.get() == '':
            messagebox.showwarning("Warning", "Please Fill The Details!", parent=self.root)
        else:
            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                query = "Insert Into addresses(first_name, last_name, address, city, state, zipcode) values(?, ?, ?, ?, ?, ?)"
                c.execute(query, (self.f_name.get(), self.l_name.get(), self.address.get(), self.city.get(), self.state.get(), self.zipcode.get()))

                conn.commit()
                conn.close()

            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
                return

            self.f_name.delete(0, END)
            self.l_name.delete(0, END)
            self.address.delete(0, END)
            self.city.delete(0, END)
            self.state.delete(0, END)
            self.zipcode.delete(0, END)

            messagebox.showinfo("Information", "Successfully Inserted", parent=self.root)

    def close_window(self):
        level = Tk()
        WinHome(level, "Home Window", self.user_oid)
        self.root.destroy()


# 11. Search Window
class WinSearch:

    def __init__(self, master, title, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title(title)
        self.root.geometry("530x365+400+150")
        self.root.resizable(width=False, height=False)

        # Our Search Label and Search Entry
        self.search_label = Label(self.root, text="Search:", anchor=E, font=('Helvetica', 15))
        self.search_label.grid(row=0, column=0, padx=(5, 0), pady=20)
        self.search_Entry = Entry(self.root, width=15, font=('Helvetica', 15))
        self.search_Entry.grid(row=0, column=1, padx=(0, 20), pady=20)

        # Drop Down Box for Search Type
        self.drop = ttk.Combobox(self.root, values=['Search by...', 'OID', 'First_Name', 'Last_Name', 'Address', 'City', 'State', 'Zipcode'],
                                 font=('helvetica', 11))
        self.drop.current(0)
        self.drop.grid(row=0, column=2, padx=(0, 27))

        # Buttons
        self.back_button = Button(self.root, text="Back", bg="#add8e6", font=('Helvetica', 11), command=self.close_window)
        self.back_button.grid(row=1, column=0, padx=(55, 0), pady=15, ipadx=5)
        self.search_button = Button(self.root, text="Search", bg="#90EE90", font=('Helvetica', 11), command=lambda: self.display())
        self.search_button.grid(row=1, column=1, pady=15, ipadx=5)
        self.show_all_button = Button(self.root, text="Show All", bg="orange", font=('Helvetica', 11), command=lambda: self.display(True))
        self.show_all_button.grid(row=1, column=2, padx=(15, 20), pady=15, ipadx=5)

        # Add some style
        self.style = ttk.Style()
        # Pick a theme
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                             background="white",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="#E3E3E3")

        self.style.map('Treeview',
                       background=[('selected', 'yellow')],
                       foreground=[('selected', 'black')])

        # Create TreeView Frame
        self.tree_frame = Frame(self.root)
        self.tree_frame.grid(row=2, column=0, columnspan=3, pady=20, padx=10)

        # TreeView ScrollBar
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        # Create TreeView
        self.my_tree = ttk.Treeview(self.tree_frame, height=7, yscrollcommand=self.tree_scroll.set)
        self.my_tree.pack()

        # Configure ScrollBar
        self.tree_scroll.config(command=self.my_tree.yview)

        # Define our columns
        self.my_tree['columns'] = ("OID", "F_Name", "L_Name", "Address", "City", "State", "Zipcode")

        # Format our columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("OID", anchor=CENTER, width=30)
        self.my_tree.column("F_Name", anchor=CENTER, width=80)
        self.my_tree.column("L_Name", anchor=CENTER, width=80)
        self.my_tree.column("Address", anchor=CENTER, width=80)
        self.my_tree.column("City", anchor=CENTER, width=80)
        self.my_tree.column("State", anchor=CENTER, width=80)
        self.my_tree.column("Zipcode", anchor=CENTER, width=60)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=CENTER)
        self.my_tree.heading("OID", text="OID", anchor=CENTER)
        self.my_tree.heading("F_Name", text="F_Name", anchor=CENTER)
        self.my_tree.heading("L_Name", text="L_Name", anchor=CENTER)
        self.my_tree.heading("Address", text="Address", anchor=CENTER)
        self.my_tree.heading("City", text="City", anchor=CENTER)
        self.my_tree.heading("State", text="State", anchor=CENTER)
        self.my_tree.heading("Zipcode", text="Zipcode", anchor=CENTER)

        # Count Variable for number of records
        self.count = 0

        # Create Stripped row Tags
        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="lightblue")

    def display(self, display_all=False):
        if self.search_Entry.get() == "" and not display_all:
            messagebox.showwarning("Warning", "Please Provide the Value to be Searched", parent=self.root)
            return

        selection = self.drop.get()
        if selection == 'Search by...' and not display_all:
            messagebox.showwarning("Warning", "Please Select an Option to be Searched!!!", parent=self.root)
            return

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            if display_all:
                c.execute("Select OID, * from addresses")
            else:
                query = "select OID, * from addresses where " + selection + " LIKE ?"
                value = '%'+self.search_Entry.get()+'%'
                c.execute(query, (value,))

            records = c.fetchall()

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
            return

        # Removing the Preexisting Records(if any)
        for rec in self.my_tree.get_children():
            self.my_tree.delete(rec)

        # Resetting the Count
        self.count = 0

        if records:
            for record in records:
                if self.count % 2 == 0:
                    self.my_tree.insert(parent='', index='end', iid=str(self.count), text="", values=record, tags=("evenrow",))
                else:
                    self.my_tree.insert(parent='', index='end', iid=str(self.count), text="", values=record, tags=("oddrow",))
                self.count += 1
        else:
            messagebox.showinfo("Information", "No Record Found!!!", parent=self.root)

        # Clearing the Entry Box and Resetting the Drop-Down Box
        self.search_Entry.delete(0, END)
        self.drop.current(0)

    def close_window(self):
        level = Tk()
        WinHome(level, "Home Window", self.user_oid)
        self.root.destroy()


# 12. Update Window
class WinUpdate:

    def __init__(self, master, title, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title(title)
        self.root.geometry("390x440+440+100")
        self.root.resizable(width=False, height=False)

        # Select Label and Entry Box
        self.select_label = Label(self.root, text="Select ID:", anchor=E, font=('Helvetica', 15))
        self.select_label.grid(row=0, column=0, padx=(20, 25), pady=(20, 10), ipadx=18)
        self.select_Entry = Entry(self.root, width=15, font=('Helvetica', 15))
        self.select_Entry.grid(row=0, column=1, padx=(0, 40), pady=(20, 10))

        # Back and Show Button
        self.back_button = Button(self.root, text="Back", bg="#add8e6", font=('Helvetica', 11), command=self.close_window)
        self.back_button.grid(row=1, column=0, padx=(90, 0), pady=(10, 30), ipadx=6)
        self.show_button = Button(self.root, text="Show", bg="orange", font=('Helvetica', 11), command=self.display)
        self.show_button.grid(row=1, column=1, padx=(0, 60), pady=(10, 30), ipadx=6)

        # Label and Entry Frame
        self.my_frame = Frame(self.root)
        self.my_frame.grid(row=2, column=0, columnspan=2)

        # All Entry Boxes
        self.f_name = Entry(self.my_frame, width=20, font=('Helvetica', 15))
        self.f_name.grid(row=0, column=1, pady=5)
        self.l_name = Entry(self.my_frame, width=20, font=('Helvetica', 15))
        self.l_name.grid(row=1, column=1, pady=5)
        self.address = Entry(self.my_frame, width=20, font=('Helvetica', 15))
        self.address.grid(row=2, column=1, pady=5)
        self.city = Entry(self.my_frame, width=20, font=('Helvetica', 15))
        self.city.grid(row=3, column=1, pady=5)
        self.state = Entry(self.my_frame, width=20, font=('Helvetica', 15))
        self.state.grid(row=4, column=1, pady=5)
        self.zipcode = Entry(self.my_frame, width=20, font=('Helvetica', 15))
        self.zipcode.grid(row=5, column=1, pady=5)

        # All Labels
        self.f_name_label = Label(self.my_frame, text="First Name:", font=('Helvetica', 15))
        self.f_name_label.grid(row=0, column=0, padx=(0, 20), pady=5, sticky=E)
        self.l_name_label = Label(self.my_frame, text="Last Name:", font=('Helvetica', 15))
        self.l_name_label.grid(row=1, column=0, padx=(0, 20), pady=5, sticky=E)
        self.address_label = Label(self.my_frame, text="Address:", font=('Helvetica', 15))
        self.address_label.grid(row=2, column=0, padx=(0, 20), pady=5, sticky=E)
        self.city_label = Label(self.my_frame, text="City:", font=('Helvetica', 15))
        self.city_label.grid(row=3, column=0, padx=(0, 20), pady=5, sticky=E)
        self.state_label = Label(self.my_frame, text="State:", font=('Helvetica', 15))
        self.state_label.grid(row=4, column=0, padx=(0, 20), pady=5, sticky=E)
        self.zipcode_label = Label(self.my_frame, text="Zipcode:", font=('Helvetica', 15))
        self.zipcode_label.grid(row=5, column=0, padx=(0, 20), pady=5, sticky=E)

        # Update Button
        self.update_button = Button(self.root, text="Update", bg="#90EE90", font=('Helvetica', 11), command=self.update)
        self.update_button.grid(row=3, column=0, pady=25, ipadx=10, columnspan=2)

    def display(self):
        self.f_name.delete(0, END)
        self.l_name.delete(0, END)
        self.address.delete(0, END)
        self.city.delete(0, END)
        self.state.delete(0, END)
        self.zipcode.delete(0, END)

        if self.select_Entry.get() == '':
            messagebox.showwarning("Warning", "Please Select an ID!", parent=self.root)
        else:
            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                c.execute("Select * from addresses where OID=?", self.select_Entry.get())
                record = c.fetchone()

                conn.commit()
                conn.close()

            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
                return

            if record is None:
                messagebox.showinfo("Information", "No Record Found!", parent=self.root)
            else:
                self.f_name.insert(0, record[0])
                self.l_name.insert(0, record[1])
                self.address.insert(0, record[2])
                self.city.insert(0, record[3])
                self.state.insert(0, record[4])
                self.zipcode.insert(0, record[5])

    def update(self):
        if self.select_Entry.get() == '':
            messagebox.showwarning("Warning", "Please Select an ID!", parent=self.root)
        elif (self.f_name.get(), self.l_name.get(), self.address.get(), self.city.get(),
              self.state.get(), self.zipcode.get()) == ('', '', '', '', '', ''):
            messagebox.showwarning("Warning", "Please Fill The Details!", parent=self.root)
        else:
            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                query = "update addresses set first_name = ?, last_name = ?, address = ?, city = ?, state = ?, zipcode = ? where OID = ?"
                placeholders = (self.f_name.get(), self.l_name.get(), self.address.get(), self.city.get(), self.state.get(),
                                self.zipcode.get(), self.select_Entry.get())
                c.execute(query, placeholders)

                conn.commit()
                conn.close()

            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
                return

            self.f_name.delete(0, END)
            self.l_name.delete(0, END)
            self.address.delete(0, END)
            self.city.delete(0, END)
            self.state.delete(0, END)
            self.zipcode.delete(0, END)
            self.select_Entry.delete(0, END)

            messagebox.showinfo("Information", "Successfully Updated", parent=self.root)

    def close_window(self):
        level = Tk()
        WinHome(level, "Home Window", self.user_oid)
        self.root.destroy()


# 13. Delete Window
class WinDelete:

    def __init__(self, master, title, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title(title)
        self.root.geometry("390x160+450+150")
        self.root.resizable(width=False, height=False)

        self.select_label = Label(self.root, text="Select ID:", font=('Helvetica', 15), anchor=E)
        self.select_label.grid(row=0, column=0, padx=(10, 38), pady=(20, 10), ipadx=10)
        self.select_Entry = Entry(self.root, width=17, font=('Helvetica', 15))
        self.select_Entry.grid(row=0, column=1, padx=(0, 40), pady=(20, 10))

        self.back_button = Button(self.root, text="Back", bg="#add8e6", font=('Helvetica', 11), command=self.close_window)
        self.back_button.grid(row=1, column=0, padx=(90, 0), pady=30, ipadx=10)
        self.del_button = Button(self.root, text="Delete", bg="orange", font=('Helvetica', 11), command=self.delete_record)
        self.del_button.grid(row=1, column=1, padx=(0, 50), pady=30, ipadx=10)

    def delete_record(self):
        if self.select_Entry.get() == '':
            messagebox.showwarning("Warning", "Please Select an ID!", parent=self.root)
        else:
            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                # Selecting address record for the given oid
                query1 = "Select * from addresses where oid=?"
                c.execute(query1, (self.select_Entry.get(),))

                record = c.fetchone()

                conn.commit()
                conn.close()

            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
                return

            if record is None:
                messagebox.showerror("Error", "No Record Found to Delete\nPlease Try Again!!!", parent=self.root)
            else:
                try:
                    conn = sqlite3.connect(database_file_path)
                    c = conn.cursor()

                    query2 = "Delete from addresses where oid=?"
                    c.execute(query2, (self.select_Entry.get(),))

                    conn.commit()
                    conn.close()

                except sqlite3.OperationalError:
                    messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
                    return

                self.select_Entry.delete(0, END)

                messagebox.showinfo("Information", "Successfully Deleted", parent=self.root)

    def close_window(self):
        level = Tk()
        WinHome(level, "Home Window", self.user_oid)
        self.root.destroy()


if __name__ == "__main__":
    # Declaring file paths
    env_file_path = "./.env"
    database_file_path = "./address_book.db"

    # Initialising the Interface
    root = Tk()

    # The First Window which appears
    WinLogin(root, "Login Window")

    mainloop()
