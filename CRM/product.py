from cProfile import label
from cgitb import text
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


class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Business Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        # ---------------
        self.var_searchBy = StringVar()
        self.var_searchTxt = StringVar()
        self.var_cat = StringVar()
        self.var_pid = StringVar()
        self.var_supplier = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.quantUnit_list = ['--Select--', 'kg', 'MT', 'bags', 'piece']
        self.fetch_cat_sup()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_del_chrg = StringVar()
        self.var_points = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.var_quantUnit = StringVar()

        product_Frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)

        # TITLE_______
        title = Label(product_Frame, text="Manage Product Details", font=(
            "SF Pro Rounded", 15), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        # Column 1--------------
        # lbl_supplier = Label(product_Frame, text="Supplier", font=(
        #     "SF Pro Rounded", 15), bg="white", fg="black").place(x=30, y=60)
        lbl_category = Label(product_Frame, text="Category", font=(
            "SF Pro Rounded", 15), bg="white", fg="black").place(x=30, y=80)
        lbl_product_name = Label(product_Frame, text="Product Name", font=(
            "SF Pro Rounded", 15), bg="white", fg="black").place(x=30, y=120)
        lbl_price = Label(product_Frame, text="Price", font=(
            "SF Pro Rounded", 15), bg="white", fg="black").place(x=30, y=160)
        lbl_quantity = Label(product_Frame, text="Quantity", font=(
            "SF Pro Rounded", 15), bg="white", fg="black").place(x=30, y=200)
        lbl_points = Label(product_Frame, text="Points", font=(
            "SF Pro Rounded", 15), bg="white", fg="black").place(x=30, y=240)
        lbl_del_charges = Label(product_Frame, text="Labour Charges", font=(
            "SF Pro Rounded", 15), bg="white", fg="black").place(x=30, y=280)
        lbl_status = Label(product_Frame, text="Status", font=(
            "SF Pro Rounded", 15), bg="white", fg="black").place(x=30, y=320)

        cmb_cat = ttk.Combobox(product_Frame, values=self.cat_list, textvariable=self.var_cat, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_cat.place(x=150, y=80, width=200)
        cmb_cat.current(0)

        cmb_quantUnit = ttk.Combobox(product_Frame, values=self.quantUnit_list, textvariable=self.var_quantUnit, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_quantUnit.place(x=360, y=240, width=80)
        cmb_quantUnit.current(0)

        txt_name = Entry(product_Frame, textvariable=self.var_name,  font=(
            "SF Pro Rounded", 12), bg="lightyellow").place(x=150, y=120, width=200)
        txt_price = Entry(product_Frame, textvariable=self.var_price,  font=(
            "SF Pro Rounded", 12), bg="lightyellow").place(x=150, y=160, width=200)
        txt_quantity = Entry(product_Frame, textvariable=self.var_qty,  font=(
            "SF Pro Rounded", 12), bg="lightyellow").place(x=150, y=200, width=200)
        txt_points = Entry(product_Frame, textvariable=self.var_points,  font=(
            "SF Pro Rounded", 12), bg="lightyellow").place(x=150, y=240, width=200)
        txt_del_charges = Entry(product_Frame, textvariable=self.var_del_chrg,  font=(
            "SF Pro Rounded", 12), bg="lightyellow").place(x=150, y=280, width=200)

        cmb_status = ttk.Combobox(product_Frame, values=(
            "--Select--", "Active", "Inactive"), textvariable=self.var_status, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_status.place(x=150, y=320, width=200)
        cmb_status.current(0)

        # Buttons
        btn_add = Button(product_Frame, text="Save", command=self.add, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=10, y=400, width=100, height=40)
        btn_update = Button(product_Frame, text="Update", command=self.update, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=120, y=400, width=100, height=40)
        btn_delete = Button(product_Frame, text="Delete", command=self.delete, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=230, y=400, width=100, height=40)
        btn_clear = Button(product_Frame, text="Clear", command=self.clear, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=340, y=400, width=100, height=40)

# =============================================Search Frame========================================
        SearchFrame = LabelFrame(self.root, text="Search Product", font=(
            "SF Pro Rounded", 12, "bold"), bg="white", bd=2, relief=RIDGE)
        SearchFrame.place(x=480, y=10, width=600, height=80)
# ===============================================options============
        cmb_search = ttk.Combobox(SearchFrame, values=(
            "--Select--",  "Category", "Name"), textvariable=self.var_searchBy, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)
        txt_search = Entry(SearchFrame, font=(
            "SF Pro Rounded", 12), textvariable=self.var_searchTxt, bg="lightyellow",).place(x=200, y=10)
        btn_search = Button(SearchFrame, text="Search", command=self.search, font=(
            "SF Pro Rounded", 12), bg="#458B74", fg="black", cursor="hand2").place(x=380, y=10, width=150, height=30)


# ==================Product Details==================================
        product_Frame = Frame(self.root, bd=3, relief=RIDGE)
        product_Frame.place(x=480, y=100, width=600, height=390)
        scrolly = Scrollbar(product_Frame, orient=VERTICAL)
        scrollx = Scrollbar(product_Frame, orient=HORIZONTAL)
        self.product_table = ttk.Treeview(product_Frame, columns=(
            "pid",  "Category",  "name", "price", "qty", "unit", "points", "labCharge", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)
        self.product_table.heading("pid", text="Product ID")
        self.product_table.heading("Category", text="Category")
        self.product_table.heading("name", text="Product Name")
        self.product_table.heading("price", text="Product Price")
        self.product_table.heading("qty", text="Quantity")
        self.product_table.heading("unit", text="Unit")
        self.product_table.heading("points", text="Points")
        self.product_table.heading("labCharge", text="Lab. Charges")
        self.product_table.heading("status", text="Status")

        self.product_table["show"] = "headings"

        self.product_table.column("pid", width=90)
        self.product_table.column("Category", width=100)
        # self.product_table.column("Supplier", width=100)
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=100)
        self.product_table.column("qty", width=100)
        self.product_table.column("unit", width=100)
        self.product_table.column("points", width=100)
        self.product_table.column("labCharge", width=100)
        self.product_table.column("status", width=100)
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)
        self.show()
        # Functions

    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("--Select--")
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            cur.execute("Select name from category ")
            cat = cur.fetchall()
            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("--Select--")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("Select name from supplier ")
            sup = cur.fetchall()
            if len(sup) > 0:
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def add(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_cat.get() == "--Select--" or self.var_name.get() == "--Select--" or self.var_quantUnit.get() == "--Select--":
                messagebox.showerror(
                    "Error", "All fields are required", parent=self.root)
            else:
                cur.execute("Select * from product where name=?",
                            (self.var_name.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error", "Product already present,try different", parent=self.root)
                else:
                    cur.execute("Insert into product( Category, name, price, qty,unit,points,labCharge, status)values(?,?,?,?,?,?,?,?)", (
                        self.var_cat.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_quantUnit.get(),
                        self.var_points.get(),
                        self.var_del_chrg.get(),
                        self.var_status.get(),

                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Product added succesfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.product_table.focus()
        content = (self.product_table.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_name.set(row[2])
        self.var_price.set(row[3])
        self.var_qty.set(row[4])
        self.var_quantUnit.set(row[5])
        self.var_points.set(row[6])
        self.var_del_chrg.set(row[7])
        self.var_status.set(row[8])

    def update(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_cat.get() == "--Select--" or self.var_name.get() == "--Select--" or self.var_quantUnit.get() == "--Select--":
                messagebox.showerror(
                    "Error", "Please fill details carefully", parent=self.root)
            elif self.var_pid.get() == "":
                messagebox.showerror(
                    "Error", "Please select product from list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",
                            (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Product ID", parent=self.root)
                else:
                    cur.execute("Update product set Category=?, name=?, price=?, qty=?,unit=?,points=?,labCharge=?, status=? where pid=?", (
                        self.var_cat.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_quantUnit.get(),
                        self.var_points.get(),
                        self.var_del_chrg.get(),
                        self.var_status.get(),
                        self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Product updated succesfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror(
                    "Error", "Select product from list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",
                            (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Product ID", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from product where pid=?",
                                    (self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Delete", "Deleted sucessfully", parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def clear(self):
        self.var_cat.set("--Select--")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_quantUnit.set("--Select--")
        self.var_status.set("--Select--")
        self.var_pid.set("")
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
                cur.execute("select * from product where " +
                            self.var_searchBy.get()+" LIKE '%"+self.var_searchTxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_table.delete(
                        *self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror(
                        "Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()
