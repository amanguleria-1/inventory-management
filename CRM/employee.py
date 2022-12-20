from cProfile import label
from doctest import master
import importlib
# from msilib import*
from pickle import FRAME
from tkinter import *
from tkinter import ttk, messagebox
from turtle import bgcolor, title, width
from typing_extensions import Self
from PIL import Image, ImageTk
from jmespath import search
import sqlite3


class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Business Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # All Variables
        self.var_searchBy = StringVar()
        self.var_searchTxt = StringVar()
        self.var_emp_id = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_age = StringVar()
        self.var_contact = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_password = StringVar()
        self.var_utype = StringVar()
        self.var_aadhar = StringVar()
        self.var_address = StringVar()
        self.var_salary = StringVar()

# =============================================Search Frame========================================
        SearchFrame = LabelFrame(self.root, text="Search Employee", font=(
            "SF Pro Rounded", 12, "bold"), bg="white", bd=2, relief=RIDGE)
        SearchFrame.place(x=250, y=10, width=600, height=70)

# =================================options============
        cmb_search = ttk.Combobox(SearchFrame, values=(
            "--Select--", "Name", "Email",  "Contact"), textvariable=self.var_gender, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)
        txt_search = Entry(SearchFrame, font=(
            "SF Pro Rounded", 12), textvariable=self.var_searchTxt, bg="lightyellow",).place(x=200, y=9)
        btn_search = Button(SearchFrame, text="Search", command=self.search, font=(
            "SF Pro Rounded", 12), bg="#458B74", fg="black", cursor="hand2").place(x=380, y=8, width=150, height=30)

        # title
        title = Label(self.root, text="Employee Details", font=(
            "SF Pro Rounded", 15), bg="#0f4d7d", fg="white").place(x=50, y=100, width=1000)

        # Content
        # row1
        lbl_empid = Label(self.root, text="Employee ID", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=150)
        lbl_gender = Label(self.root, text="Gender", font=(
            "SF Pro Rounded", 15), bg="white").place(x=425, y=150)
        lbl_contact = Label(self.root, text="Contact", font=(
            "SF Pro Rounded", 15), bg="white").place(x=775, y=150)

        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=(
            "SF Pro Rounded", 15), bg="white").place(x=150, y=150, width=180)
        cmb_gender = ttk.Combobox(self.root, values=(
            "--Select--", "Male", "Female", "Other"), textvariable=self.var_gender, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=(
            "SF Pro Rounded", 15), bg="white").place(x=850, y=150, width=180)

        # row2
        lbl_name = Label(self.root, text="Name", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=190)
        lbl_dob = Label(self.root, text="D.O.B", font=(
            "SF Pro Rounded", 15), bg="white").place(x=425, y=190)
        lbl_doj = Label(self.root, text="D.O.J", font=(
            "SF Pro Rounded", 15), bg="white").place(x=775, y=190)

        txt_name = Entry(self.root, textvariable=self.var_name, font=(
            "SF Pro Rounded", 15), bg="white").place(x=150, y=190, width=180)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=(
            "SF Pro Rounded", 15), bg="white").place(x=500, y=190, width=180)
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=(
            "SF Pro Rounded", 15), bg="white").place(x=850, y=190, width=180)

 # row3
        lbl_email = Label(self.root, text="Email", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=230)
        lbl_pass = Label(self.root, text="Password", font=(
            "SF Pro Rounded", 15), bg="white").place(x=425, y=230)
        lbl_utype = Label(self.root, text="User Type", font=(
            "SF Pro Rounded", 15), bg="white").place(x=775, y=230)

        txt_email = Entry(self.root, textvariable=self.var_email, font=(
            "SF Pro Rounded", 15), bg="white").place(x=150, y=230, width=180)
        txt_pass = Entry(self.root, textvariable=self.var_password, font=(
            "SF Pro Rounded", 15), bg="white").place(x=500, y=230, width=180)
        cmb_utype = ttk.Combobox(self.root, values=(
            "--Select--", "Admin", "Sales Executive", "Driver", "Labour", "Logistics Handler", "Accounts", "D2D sales person"), textvariable=self.var_utype, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_utype.place(x=850, y=230, width=180)
        cmb_utype.current(0)
 # row4
        lbl_address = Label(self.root, text="Address", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=270)
        lbl_salary = Label(self.root, text="Salary", font=(
            "SF Pro Rounded", 15), bg="white").place(x=425, y=270)

        self.txt_address = Text(self.root, font=(
            "SF Pro Rounded", 15), bg="white")
        self.txt_address.place(x=150, y=270, width=250, height=60)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=(
            "SF Pro Rounded", 15), bg="white").place(x=500, y=270, width=180)

# Buttons
        btn_add = Button(self.root, text="Save", command=self.add, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=500, y=305, width=110, height=30)
        btn_update = Button(self.root, text="Update", command=self.update, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=620, y=305, width=110, height=30)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=740, y=305, width=110, height=30)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=860, y=305, width=110, height=30)


# Employee Details
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)
        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)
        self.EmployeeTable = ttk.Treeview(emp_frame, columns=(
            "eid", "name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        self.EmployeeTable.heading("eid", text="Emp ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="D.O.B")
        self.EmployeeTable.heading("doj", text="D.O.J")
        self.EmployeeTable.heading("pass", text="Password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")

        self.EmployeeTable["show"] = "headings"

        self.EmployeeTable.column("eid", width=90)
        self.EmployeeTable.column("name", width=100)
        self.EmployeeTable.column("email", width=100)
        self.EmployeeTable.column("gender", width=100)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("dob", width=100)
        self.EmployeeTable.column("doj", width=100)
        self.EmployeeTable.column("pass", width=100)
        self.EmployeeTable.column("utype", width=100)
        self.EmployeeTable.column("address", width=100)
        self.EmployeeTable.column("salary", width=100)
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()
# Functions

    def add(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror(
                    "Error", "Employee ID is required", parent=self.root)
            elif self.var_name.get() == "":
                messagebox.showerror("Error", "Name is required")
            elif self.var_contact.get() == "":
                messagebox.showerror("Error", "Contact is required")
            else:
                cur.execute("Select * from employee where eid=?",
                            (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error", "This Employee Id already assigned,try different", parent=self.root)
                else:
                    cur.execute("Insert into employee(eid, name, email, gender, contact, dob, doj, pass, utype, address, salary)values(?,?,?,?,?,?,?,?,?,?,?)", (
                        self.var_emp_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_password.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0', END),
                        self.var_salary.get(),

                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Employee added succesfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            cur.execute("select * from employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        content = (self.EmployeeTable.item(f))
        row = content['values']
        print(row)
        self.var_emp_id.set(row[0]),
        self.var_name.set(row[1]),
        self.var_email.set(row[2]),
        self.var_gender.set(row[3]),
        self.var_contact.set(row[4]),
        self.var_dob.set(row[5]),
        self.var_doj.set(row[6]),
        self.var_password.set(row[7]),
        self.var_utype.set(row[8]),
        self.txt_address.delete('1.0', END),
        self.txt_address.insert(END, row[9]),
        self.var_salary.set(row[10]),

    def update(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror(
                    "Error", "Employee ID is required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",
                            (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Employee ID", parent=self.root)
                else:
                    cur.execute("Update employee set name=?, email=?, gender=?, contact=?, dob=?, doj=?, pass=?, utype=?, address=?, salary=? where eid=?", (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_password.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0', END),
                        self.var_salary.get(),
                        self.var_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Employee updated succesfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror(
                    "Error", "Employee ID is required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",
                            (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Employee ID", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from employee where eid=?",
                                    (self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Delete", "Deleted sucessfully", parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("--Select--")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_password.set("")
        self.var_utype.set("--Select--")
        self.txt_address.delete('1.0', END)
        self.var_salary.set("")
        self.var_searchTxt.set("")
        self.var_searchBy.set("--select--")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_searchBy.get() == "--Select--":
                messagebox.showerror(
                    "Error", "Select Search By option", parent=self.root)
            elif self.var_searchTxt.get() == "":
                messagebox.showerror(
                    "Error", "Search Input should be recquired", parent=self.root)
            else:
                cur.execute("select * from employee where " +
                            self.var_searchBy.get()+" LIKE '%"+self.var_searchTxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(
                        *self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror(
                        "Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()
