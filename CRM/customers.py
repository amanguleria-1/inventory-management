from cProfile import label
from distutils.cmd import Command
from doctest import master
from email.headerregistry import Address
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
import time
from threading import Timer


class customerClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Business Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # All Variables
        self.var_cust_id = StringVar()
        self.var_searchBy = StringVar()
        self.var_searchTxt = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        self.var_Member_status = StringVar()
        self.var_Customer_type = StringVar()
        self.var_address = StringVar()
        self.address_list = ["Aman"]

# =============================================Search Frame========================================
        # self.root = LabelFrame(self.root, text="Search Customer", font=(
        #     "SF Pro Rounded", 12, "bold"), bg="white", bd=2, relief=RIDGE)
        # self.root.place(x=250, y=10, width=600, height=70)

# =================================options============
        lbl_search = Label(self.root, text="Search by :", font=(
            "SF Pro Rounded", 15), bg="white")
        lbl_search.place(x=720, y=50)

        lbl_search_field = Label(self.root, text="Enter details: ", font=(
            "SF Pro Rounded", 15), bg="white")
        lbl_search_field.place(x=708, y=80)

        cmb_search = ttk.Combobox(self.root, values=(
            "--Select--", "cid", "CustMob", "CustName"), textvariable=self.var_searchBy, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_search.place(x=810, y=50, width=180)
        cmb_search.current(0)

        txt_search = Entry(self.root, font=(
            "SF Pro Rounded", 12), textvariable=self.var_searchTxt, bg="lightyellow",).place(x=810, y=80)
        btn_search = Button(self.root, text="Search", command=self.search, font=(
            "SF Pro Rounded", 12), bg="#458B74", fg="black", cursor="hand2").place(x=990, y=79, width=100, height=28)

        # title
        title = Label(self.root, text="Customer Details", font=(
            "SF Pro Rounded", 20, "bold"), bg="#0f4d7d", fg="white").place(x=50, y=10, width=1000, height=40)

        # Content
# row0
        lbl_cust_name = Label(self.root, text="Customer ID:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=60)
        txt_cust_name = Entry(self.root, textvariable=self.var_cust_id, font=(
            "SF Pro Rounded", 15), bg="white", relief=RIDGE).place(x=180, y=60, width=180)

# row1
        lbl_cust_name = Label(self.root, text="Name:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=90)
        txt_cust_name = Entry(self.root, textvariable=self.var_name, font=(
            "SF Pro Rounded", 15), bg="white", relief=RIDGE).place(x=180, y=90, width=180)

 # row2
        lbl_contact = Label(self.root, text="Contact:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=120)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=(
            "SF Pro Rounded", 15), bg="white", relief=RIDGE).place(x=180, y=120, width=180)

 # row3
        lbl_Member_status = Label(self.root, text="Member Status:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=160)
        cmb_Member_status = ttk.Combobox(self.root, values=(
            "--Select--", "Registered", "Unregistered"), textvariable=self.var_Member_status,  state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_Member_status.place(x=180, y=160)
        cmb_Member_status.current(0)
 # row4
        lbl_cust_type = Label(self.root, text="Customer Type:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=200)
        cmb_Cust_type = ttk.Combobox(self.root, values=(
            "--Select--", "Company", "Owner",  "Supplier", "Mason"), textvariable=self.var_Customer_type,  state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_Cust_type.place(x=180, y=200)
        cmb_Cust_type.current(0)
        # cmb_Cust_type.current(0)

 # row5
        lbl_addresses = Label(self.root, text="Addresses:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=240)

        cmb_addresses = ttk.Combobox(self.root, values=(
            "--Choose--", self.address_list), justify=CENTER,  state="readonly", font=(
            "SF Pro Rounded", 12))
        cmb_addresses.place(x=180, y=240)
        cmb_addresses.current(0)

 # row6
        lbl_new_address = Label(self.root, text="New Address:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=280)

        self.txt_new_address = Text(self.root,  font=(
            "SF Pro Rounded", 15), bg="white", relief=RIDGE)
        self.txt_new_address.place(x=180, y=280, width=300, height=30)

 # row7
        lbl_desc = Label(self.root, text="Description:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=320)

        self.txt_desc = Text(self.root, font=(
            "SF Pro Rounded", 15),  bg="white", relief=RIDGE)
        self.txt_desc.place(x=180, y=320, width=300, height=90)


# Buttons
        btn_add = Button(self.root, text="Save", command=self.add, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=190, y=420, width=110, height=30)
        btn_update = Button(self.root, text="Update", command=self.update, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=310, y=420, width=110, height=30)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=190, y=455, width=110, height=30)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=310, y=455, width=110, height=30)
        btn_add_new_address = Button(self.root, text="Add", command=self.add_new_address, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=485, y=280, width=110, height=30)


# Customer Details
        cust_frame = Frame(self.root, bd=3, relief=RIDGE)
        cust_frame.place(x=600, y=120,  width=490, height=350)
        scrolly = Scrollbar(cust_frame, orient=VERTICAL)
        scrollx = Scrollbar(cust_frame, orient=HORIZONTAL)
        self.customerTable = ttk.Treeview(cust_frame, columns=(
            "cid", "CustName", "CustMob", "CustStatus", "CustType", "CustAdd", "CustDesc"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.customerTable.xview)
        scrolly.config(command=self.customerTable.yview)
        self.customerTable.heading("cid", text="Cust. ID")
        self.customerTable.heading("CustName", text="Name")
        self.customerTable.heading("CustMob", text="Mob No.")
        self.customerTable.heading("CustStatus", text="Member Status")
        self.customerTable.heading("CustType", text="Cust. Type")
        self.customerTable.heading("CustAdd", text="Address")
        self.customerTable.heading("CustDesc", text="Desc.")
        self.customerTable["show"] = "headings"

        self.customerTable.column("cid", width=90)
        self.customerTable.column("CustName", width=100)
        self.customerTable.column("CustMob", width=100)
        self.customerTable.column("CustStatus", width=100)
        self.customerTable.column("CustType", width=100)
        self.customerTable.column("CustAdd", width=100)
        self.customerTable.column("CustDesc", width=100)
        self.customerTable.pack(fill=BOTH, expand=1)
        self.customerTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()
# Functions

    def add(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            # if self.var_cust_id.get() == "":
            #     messagebox.showerror(
            #         "Error", "Cust. id must be required", parent=self.root)

            cur.execute("Select * from customer where cid=?",
                        (self.var_name.get(),))
            row = cur.fetchone()
            if row != None:
                messagebox.showerror(
                    "Error", "This Customer id no is already assigned,try different", parent=self.root)
            else:
                cur.execute("Insert into customer(cid, CustName, CustMob,CustStatus, CustType,CustAdd, CustDesc)values(?,?,?,?,?,?,?)", (
                    self.var_cust_id.get(),
                    self.var_name.get(),
                    self.var_contact.get(),
                    self.var_Member_status.get(),
                    self.var_Customer_type.get(),
                    self.var_address.get(),
                    self.txt_desc.get('1.0', END),
                ))
                con.commit()
                messagebox.showinfo(
                    "Success", "customer added succesfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            cur.execute("select * from customer")
            rows = cur.fetchall()
            self.customerTable.delete(*self.customerTable.get_children())
            for row in rows:
                self.customerTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.customerTable.focus()
        content = (self.customerTable.item(f))
        row = content['values']
        print(row)
        self.var_cust_id.set(row[0]),
        self.var_name.set(row[1]),
        self.var_contact.set(row[2]),
        self.var_Member_status.set(row[3]),
        self.var_Customer_type.set(row[4]),
        self.var_address.set(row[5]),
        self.txt_desc.delete('1.0', END),
        self.txt_desc.insert(END, row[6]),

    def update(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_cust_id.get() == "":
                messagebox.showerror(
                    "Error", "Cust. ID is required", parent=self.root)
            else:
                cur.execute("Select * from customer where cid=?",
                            (self.var_cust_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Cust. Id", parent=self.root)
                else:
                    cur.execute("Update customer set CustName=?, CustMob=?, CustStatus=?, CustType=?, CustDesc=? where cid=?", (
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.var_Member_status.get(),
                        self.var_Customer_type.get(),
                        self.txt_desc.get('1.0', END),
                        self.var_cust_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "customer updated succesfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_cust_id.get() == "":
                messagebox.showerror(
                    "Error", "Cust. Id is required", parent=self.root)
            else:
                cur.execute("Select * from customer where cid=?",
                            (self.var_cust_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Cust. Id", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from customer where cid=?",
                                    (self.var_cust_id.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Delete", "customer deleted sucessfully", parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def add_new_address(self):
        txt = self.var_address.get()
        if txt != None:
            self.address_list.append(txt)
        print(txt)
        print(self.address_list)

    def clear(self):
        self.var_cust_id.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.var_Member_status.set("--Select--")
        self.var_Customer_type.set("--Select--")
        self.var_address.set("")
        self.txt_new_address.delete('1.0', END)
        self.txt_desc.delete('1.0', END)
        self.var_searchTxt.set("")
        self.var_searchBy.set("--Select--")

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
                    "Error", "Search Input should be required", parent=self.root)
            else:
                cur.execute("select * from customer where " +
                            self.var_searchBy.get()+" LIKE '%"+self.var_searchTxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.customerTable.delete(
                        *self.customerTable.get_children())
                    for row in rows:
                        self.customerTable.insert('', END, values=row)
                else:
                    messagebox.showerror(
                        "Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = customerClass(root)
    root.mainloop()
