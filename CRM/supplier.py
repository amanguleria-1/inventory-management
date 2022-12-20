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


class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Business Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # All Variables
        self.var_searchBy = StringVar()
        self.var_searchTxt = StringVar()

        self.var_sup_gst = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

# =============================================Search Frame========================================
        # self.root = LabelFrame(self.root, text="Search Employee", font=(
        #     "SF Pro Rounded", 12, "bold"), bg="white", bd=2, relief=RIDGE)
        # self.root.place(x=250, y=10, width=600, height=70)

# =================================options============
        lbl_search = Label(self.root, text="Search By GST:", font=(
            "SF Pro Rounded", 15), bg="white")
        lbl_search.place(x=670, y=80)

        txt_search = Entry(self.root, font=(
            "SF Pro Rounded", 12), textvariable=self.var_searchTxt, bg="lightyellow",).place(x=810, y=80)
        btn_search = Button(self.root, text="Search", command=self.search, font=(
            "SF Pro Rounded", 12), bg="#458B74", fg="black", cursor="hand2").place(x=990, y=79, width=100, height=28)

        # title
        title = Label(self.root, text="Supplier Details", font=(
            "SF Pro Rounded", 20, "bold"), bg="#0f4d7d", fg="white").place(x=50, y=10, width=1000, height=40)

        # Content
# row1
        lbl_supplier_gst = Label(self.root, text="GST No", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=80)
        txt_supplier_gst = Entry(self.root, textvariable=self.var_sup_gst, font=(
            "SF Pro Rounded", 15), bg="white").place(x=180, y=80, width=180)

 # row2
        lbl_name = Label(self.root, text="Name", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=120)
        txt_name = Entry(self.root, textvariable=self.var_name, font=(
            "SF Pro Rounded", 15), bg="white").place(x=180, y=120, width=180)

 # row3
        lbl_contact = Label(self.root, text="Contact", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=160)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=(
            "SF Pro Rounded", 15), bg="white").place(x=180, y=160, width=180)
 # row4
        lbl_desc = Label(self.root, text="Description", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=200)

        self.txt_desc = Text(self.root, font=(
            "SF Pro Rounded", 15), bg="white")
        self.txt_desc.place(x=180, y=200, width=300, height=90)


# Buttons
        btn_add = Button(self.root, text="Save", command=self.add, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=180, y=305, width=110, height=30)
        btn_update = Button(self.root, text="Update", command=self.update, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=300, y=305, width=110, height=30)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=420, y=305, width=110, height=30)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=550, y=305, width=110, height=30)


# Supplier Details
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=670, y=120,  width=400, height=350)
        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)
        self.supplierTable = ttk.Treeview(emp_frame, columns=(
            "gst", "name", "contact", "desc"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)
        self.supplierTable.heading("gst", text="GST no.")
        self.supplierTable.heading("name", text="Name")
        self.supplierTable.heading("contact", text="Contact")
        self.supplierTable.heading("desc", text="Desc")
        self.supplierTable["show"] = "headings"

        self.supplierTable.column("gst", width=90)
        self.supplierTable.column("name", width=100)
        self.supplierTable.column("contact", width=100)
        self.supplierTable.column("desc", width=100)
        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()
# Functions

    def add(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_sup_gst.get() == "":
                messagebox.showerror(
                    "Error", "GST must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where gst=?",
                            (self.var_sup_gst.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error", "This gst no is already assigned,try different", parent=self.root)
                else:
                    cur.execute("Insert into supplier(gst, name, contact, desc)values(?,?,?,?)", (
                        self.var_sup_gst.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END),
                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Supplier added succesfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            cur.execute("select * from supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.supplierTable.focus()
        content = (self.supplierTable.item(f))
        row = content['values']
        print(row)
        self.var_sup_gst.set(row[0]),
        self.var_name.set(row[1]),
        self.var_contact.set(row[2]),
        self.txt_desc.delete('1.0', END),
        self.txt_desc.insert(END, row[3]),

    def update(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_sup_gst.get() == "":
                messagebox.showerror(
                    "Error", "GST no. is required", parent=self.root)
            else:
                cur.execute("Select * from supplier where gst=?",
                            (self.var_sup_gst.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid GST no.", parent=self.root)
                else:
                    cur.execute("Update supplier set name=?, contact=?, desc=? where gst=?", (
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END),
                        self.var_sup_gst.get(),
                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Supplier updated succesfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_sup_gst.get() == "":
                messagebox.showerror(
                    "Error", "GST no. is required", parent=self.root)
            else:
                cur.execute("Select * from supplier where gst=?",
                            (self.var_sup_gst.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid GST no.", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from supplier where gst=?",
                                    (self.var_sup_gst.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Delete", "Supplier deleted sucessfully", parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def clear(self):
        self.var_sup_gst.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.var_searchTxt.set("")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_searchTxt.get() == "":
                messagebox.showerror(
                    "Error", "GST no. should be required", parent=self.root)
            else:
                cur.execute("select * from supplier where gst=?",
                            (self.var_searchTxt.get(),))
                row = cur.fetchone()
                if row != 0:
                    self.supplierTable.delete(
                        *self.supplierTable.get_children())
                else:
                    messagebox.showerror(
                        "Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()
