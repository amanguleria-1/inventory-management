from ast import Str
from cProfile import label
from distutils.cmd import Command
from doctest import master
from email.headerregistry import Address
import importlib
# from msilib import*
from pickle import FRAME
from selectors import SelectorKey
import string
from tkinter import *
from tkinter import ttk, messagebox
from turtle import bgcolor, title, width
from typing_extensions import Self
from PIL import Image, ImageTk
from jmespath import search
import sqlite3
import time
from threading import Timer
from customers_for_employees import customerClass
import time


class leadClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Business Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # All Variables
        self.var_lead_id = StringVar()
        self.var_searchBy = StringVar()
        self.var_searchTxt = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        self.var_Lead_type = StringVar()
        self.var_address = StringVar()
        self.var_date = StringVar(
            master=self.root, value=time.strftime("%d-%m-%Y"))
        print(self.var_date.get())
        print(type(self.var_date))

# =================================options============
        lbl_search = Label(self.root, text="Search by :", font=(
            "SF Pro Rounded", 15), bg="white")
        lbl_search.place(x=720, y=50)

        lbl_search_field = Label(self.root, text="Enter details: ", font=(
            "SF Pro Rounded", 15), bg="white")
        lbl_search_field.place(x=708, y=80)

        cmb_search = ttk.Combobox(self.root, values=(
            "--Select--", "lid", "LeadMob", "LeadName"), textvariable=self.var_searchBy, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_search.place(x=810, y=50, width=180)
        cmb_search.current(0)

        txt_search = Entry(self.root, font=(
            "SF Pro Rounded", 12), textvariable=self.var_searchTxt, bg="lightyellow",).place(x=810, y=80)
        btn_search = Button(self.root, text="Search", command=self.search, font=(
            "SF Pro Rounded", 12), bg="#458B74", fg="black", cursor="hand2").place(x=990, y=79, width=100, height=28)

        # title
        title = Label(self.root, text="Lead Details", font=(
            "SF Pro Rounded", 20, "bold"), bg="#0f4d7d", fg="white").place(x=50, y=10, width=1000, height=40)

        # Content
# row0
        lbl_lead_id = Label(self.root, text="Lead ID:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=60)
        txt_lead_id = Entry(self.root, textvariable=self.var_lead_id, font=(
            "SF Pro Rounded", 15), bg="white", relief=RIDGE).place(x=180, y=60, width=180)


# row1
        lbl_lead_name = Label(self.root, text="Name:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=90)
        txt_lead_name = Entry(self.root, textvariable=self.var_name, font=(
            "SF Pro Rounded", 15), bg="white", relief=RIDGE).place(x=180, y=90, width=180)

 # row2
        lbl_contact = Label(self.root, text="Contact:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=120)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=(
            "SF Pro Rounded", 15), bg="white", relief=RIDGE).place(x=180, y=120, width=180)

 # row3

        lbl_lead_type = Label(self.root, text="Type:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=160)
        cmb_lead_type = ttk.Combobox(self.root, values=(
            "--Select--", "Company", "Owner",  "Supplier", "Mason"), textvariable=self.var_Lead_type, justify=CENTER, state="readonly", font=(
            "SF Pro Rounded", 12))
        cmb_lead_type.place(x=180, y=160)
        cmb_lead_type.current(0)
        # cmb_lead_type.current(0)

 # row4

        lbl_new_address = Label(self.root, text="Address:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=200)

        self.txt_address = Text(self.root,  font=(
            "SF Pro Rounded", 15), bg="white", relief=RIDGE)
        self.txt_address.place(x=180, y=200, width=300, height=30)

 # row5
        lbl_desc = Label(self.root, text="Description:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=240)

        self.txt_desc = Text(self.root, font=(
            "SF Pro Rounded", 15),  bg="white", relief=RIDGE)
        self.txt_desc.place(x=180, y=240, width=300, height=90)


# Buttons
        btn_add = Button(self.root, text="Save", command=self.add, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=180, y=335, width=110, height=30)
        btn_update = Button(self.root, text="Update", command=self.update, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=300, y=335, width=110, height=30)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=180, y=370, width=110, height=30)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=300, y=370, width=110, height=30)
        btn_converted = Button(self.root, text="Converted", command=self.converted, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=180, y=405, width=230, height=30)


# Lead Details
        lead_frame = Frame(self.root, bd=3, relief=RIDGE)
        lead_frame.place(x=490, y=120,  width=600, height=350)
        scrolly = Scrollbar(lead_frame, orient=VERTICAL)
        scrollx = Scrollbar(lead_frame, orient=HORIZONTAL)
        self.leadTable = ttk.Treeview(lead_frame, columns=(
            "lid", "LeadName", "LeadMob", "LeadType", "LeadAdd", "LeadDesc", "LeadDate"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.leadTable.xview)
        scrolly.config(command=self.leadTable.yview)
        self.leadTable.heading("lid", text="Lead ID")
        self.leadTable.heading("LeadName", text="Name")
        self.leadTable.heading("LeadMob", text="Mob No.")
        self.leadTable.heading("LeadType", text="Lead Type")
        self.leadTable.heading("LeadAdd", text="Address")
        self.leadTable.heading("LeadDesc", text="Desc.")
        self.leadTable.heading("LeadDate", text="Date")
        self.leadTable["show"] = "headings"

        self.leadTable.column("lid", width=90)
        self.leadTable.column("LeadName", width=100)
        self.leadTable.column("LeadMob", width=100)
        self.leadTable.column("LeadType", width=100)
        self.leadTable.column("LeadAdd", width=100)
        self.leadTable.column("LeadDesc", width=100)
        self.leadTable.column("LeadDate", width=100)
        self.leadTable.pack(fill=BOTH, expand=1)
        self.leadTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()
# Functions

    def add(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from lead where lid=?",
                        (self.var_name.get(),))
            row = cur.fetchone()
            if row != None:
                messagebox.showerror(
                    "Error", "This Lead ID is already assigned, try different", parent=self.root)
            else:
                cur.execute("Insert into lead(lid, LeadName, LeadMob, LeadType,LeadAdd, LeadDesc, LeadDate)values(?,?,?,?,?,?,?)", (
                    self.var_lead_id.get(),
                    self.var_name.get(),
                    self.var_contact.get(),
                    self.var_Lead_type.get(),
                    self.txt_address.get('1.0', END),
                    self.txt_desc.get('1.0', END),
                    self.var_date.get(),
                ))
                con.commit()
                messagebox.showinfo(
                    "Success", "Lead generated succesfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            cur.execute("select * from lead")
            rows = cur.fetchall()
            self.leadTable.delete(*self.leadTable.get_children())
            for row in rows:
                self.leadTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.leadTable.focus()
        content = (self.leadTable.item(f))
        row = content['values']
        self.var_lead_id.set(row[0]),
        self.var_name.set(row[1]),
        self.var_contact.set(row[2]),
        self.var_Lead_type.set(row[3]),
        self.txt_address.delete('1.0', END),
        self.txt_address.insert(END, row[4]),
        self.txt_desc.delete('1.0', END),
        self.txt_desc.insert(END, row[5]),
        self.var_date.set(row[6]),

    def update(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_lead_id.get() == "":
                messagebox.showerror(
                    "Error", "Lead ID is required", parent=self.root)
            else:
                cur.execute("Select * from lead where lid=?",
                            (self.var_lead_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Lead Id", parent=self.root)
                else:
                    cur.execute("Update lead set LeadName=?, LeadMob=?, LeadType=?, LeadAdd=?, LeadDesc=?, LeadDate=? where lid=?", (
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.var_Lead_type.get(),
                        self.txt_address.get('1.0', END),
                        self.txt_desc.get('1.0', END),
                        self.var_date.get(),
                        self.var_lead_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Lead updated succesfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_lead_id.get() == "":
                messagebox.showerror(
                    "Error", "Lead Id is required", parent=self.root)
            else:
                cur.execute("Select * from lead where lid=?",
                            (self.var_lead_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Lead ID", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from lead where lid=?",
                                    (self.var_lead_id.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Delete", "Lead deleted sucessfully", parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def clear(self):
        self.var_lead_id.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.var_Lead_type.set("--Select--")
        self.txt_address.delete('1.0', END)
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
                cur.execute("select * from lead where " +
                            self.var_searchBy.get()+" LIKE '%"+self.var_searchTxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.leadTable.delete(
                        *self.leadTable.get_children())
                    for row in rows:
                        self.leadTable.insert('', END, values=row)
                else:
                    messagebox.showerror(
                        "Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def converted(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = customerClass(self.new_win)


if __name__ == "__main__":
    root = Tk()
    obj = leadClass(root)
    root.mainloop()
