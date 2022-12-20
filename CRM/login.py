from cProfile import label
import email
import string
from tkinter import *
from tkinter import messagebox
from tkinter.font import BOLD
from turtle import bgcolor, title, width
from PIL import ImageTk
import os
import sqlite3


class login_system:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Garwhal Marbles BMS")
        self.root.geometry("1650x900+0+0")

        # ===images====
        self.image = ImageTk.PhotoImage(file="images/menu_im.png")
        self.lbl_image = Label(
            self.root, image=self.image, bd=0).place(x=150, y=50)

        # ===Login Frame===
        Login_frame = Frame(self.root, bd=2, relief=RIDGE)
        Login_frame.place(x=900, y=60, width=450, height=550)

        title = Label(Login_frame, text="Garwhal Marbles BMS", font=(
            "Elephant", 30, "bold")).place(x=0, y=30, relwidth=1)

        self.logo = ImageTk.PhotoImage(file="images/logo1.png")
        self.lbl_logo = Label(Login_frame, image=self.logo,
                              bd=0).place(x=170, y=75)

        lbl_user = Label(Login_frame, text="Emloyee ID:", font=(
            "Andalus", 20, "bold"), bg="white").place(x=50, y=150)
        self.employee_id = StringVar()
        self.password = StringVar()
        txt_employee_id = Entry(Login_frame, textvariable=self.employee_id, font=(
            "times new roman", 15), bg="#ECECEC").place(x=50, y=190, width=250)

        lbl_pass = Label(Login_frame, text="Password:", font=(
            "Andalus", 20, "bold"), bg="white").place(x=50, y=230)
        txt_pass = Entry(Login_frame, textvariable=self.password, show="*",
                         font=("times new roman", 15), bg="#ECECEC").place(x=50, y=270, width=250)

        btn_login = Button(Login_frame, command=self.login, text="Log In", font=("Arial Rounded MT Bold", 15),
                           bg="#00B0F0", activebackground="#00B0F0", cursor="hand2").place(x=50, y=350, width=350, height=35)

        hr = Label(Login_frame, bg="light grey").place(
            x=50, y=440, width=350, height=2)
        or_ = Label(Login_frame, text="OR", bg="white", font=(
            "times new roman", 15, "bold")).place(x=205, y=430)

        btn_forget = Button(Login_frame, command=self.forget_window, text="Forget Password ?", font=(
            "times new roman", 15, "bold"), bd=0, cursor="hand2", fg="blue").place(x=165, y=490)

    def login(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror(
                    "Error", "All Fields are required", parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?",
                            (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                if user == None:
                    messagebox.showerror(
                        "Error", "Invalid Username or Password ", parent=self.root)
                else:
                    if user[0] == "Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python emp_dash.py")

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def forget_window(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        if self.employee_id.get() == "":
            messagebox.showerror(
                "Error", "Employee ID is required", parent=self.root)
        else:
            cur.execute("select email from employee where eid=?",
                        (self.employee_id.get(),))
            email = cur.fetchone()
            if email == None:
                messagebox.showerror(
                    "Error", "Invalid Employee ID, try again ", parent=self.root)
            else:
                self.var_otp = StringVar()
                self.var_new_pass = StringVar()
                self.var_conf_pass = StringVar()
                self.forget_win = Toplevel(self.root)
                self.forget_win.title("Reset Password")
                self.forget_win.geometry("425x300+400+250")
                self.forget_win.focus_force()
                title = Label(self.forget_win, text="Reset Password",
                              font=("goudy old style", 15, BOLD), bg="#ECECEC").pack(side=TOP, fill=X)
                lbl_reset = Label(
                    self.forget_win, text="Enter OTP sent on registered email", font=("times new roman", 15, "bold")).place(x=20, y=60)
                txt_reset = Entry(self.forget_win, textvariable=self.var_otp, font=(
                    "times new roman", 15), bg="lightyellow", relief=RIDGE).place(x=20, y=90, width=250, height=30)

                self.btn_reset = Button(self.forget_win, text="SUBMIT", font=(
                    "times new roman", 15, "bold"), bg="lightblue", cursor="hand2", borderwidth=0).place(x=285, y=90, width=120, height=30)

                lbl_new_pass = Label(
                    self.forget_win, text="Enter New Password", font=("times new roman", 15, "bold")).place(x=20, y=120)
                txt_new_pass = Entry(self.forget_win, textvariable=self.var_new_pass, font=(
                    "times new roman", 15), bg="lightyellow", relief=RIDGE).place(x=20, y=150, width=250, height=30)

                lbl_con_pass = Label(
                    self.forget_win, text="Confirm New Password", font=("times new roman", 15, "bold")).place(x=20, y=180)
                txt_con_pass = Entry(self.forget_win, textvariable=self.var_conf_pass, font=(
                    "times new roman", 15), bg="lightyellow", relief=RIDGE).place(x=20, y=210, width=250, height=30)

                self.conf_pass_reset = Button(self.forget_win, text="Update", state=DISABLED, font=(
                    "times new roman", 15, "bold"), bg="lightblue", cursor="hand2", borderwidth=0).place(x=25, y=250, width=120, height=30)


root = Tk()
obj = login_system(root)
root.mainloop()
