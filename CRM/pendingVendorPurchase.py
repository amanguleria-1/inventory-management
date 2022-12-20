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
import os
import tempfile
import time


class pendingVendorPurchase:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1650x900+0+0")
        self.root.title("Business Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        # ---------------
        self.var_searchBy = StringVar()
        self.var_searchTxt = StringVar()
        self.var_cat = StringVar()
        self.var_supplier = StringVar()
        self.var_prod = StringVar()
        self.var_quantUnit = StringVar()
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_stock = StringVar()
        self.var_date = StringVar(
            master=self.root, value=time.strftime("%d-%m-%Y"))
        self.cat_list = []
        self.sup_list = []
        self.prod_list = []
        self.bill_list = []
        self.quantUnit_list = ['--Select--', 'kg', 'MT', 'bags', 'piece']
        self.fetch_cat_sup()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.bill_amt = StringVar()

        product_Frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=480, height=400)

        # TITLE_______
        title = Label(product_Frame, text="Pending Orders", font=(
            "SF Pro Rounded", 20, "bold"), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        # Column 1--------------
        lbl_date = Label(product_Frame, text="Date:", font=(
            "SF Pro Rounded", 15), bg="white", fg="black").place(x=30, y=50)
        lbl_supplier = Label(product_Frame, text="Supplier:", font=(
            "SF Pro Rounded", 15), bg="white", fg="black").place(x=30, y=100)
        lbl_category = Label(product_Frame, text="Category:", font=(
            "SF Pro Rounded", 15), bg="white", fg="black").place(x=30, y=150)
        lbl_product_name = Label(product_Frame, text="Product Name:", font=(
            "SF Pro Rounded", 15), bg="white", fg="black").place(x=30, y=200)
        lbl_quantity = Label(product_Frame, text="Quantity:", font=(
            "SF Pro Rounded", 15), bg="white", fg="black").place(x=30, y=250)

        # Column 2--------------
        txt_date = Entry(product_Frame, textvariable=self.var_date,  font=(
            "SF Pro Rounded", 12), bg="lightyellow").place(x=150, y=50, width=200)
        cmb_supplier = ttk.Combobox(product_Frame, values=self.sup_list, textvariable=self.var_supplier, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_supplier.place(x=150, y=100, width=200)
        cmb_supplier.current(0)

        cmb_cat = ttk.Combobox(product_Frame, values=self.cat_list, textvariable=self.var_cat, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_cat.place(x=150, y=150, width=200)
        cmb_cat.current(0)

        cmb_product = ttk.Combobox(product_Frame, values=self.prod_list, textvariable=self.var_prod, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_product.place(x=150, y=200, width=200)
        cmb_product.current(0)

        cmb_quantUnit = ttk.Combobox(product_Frame, values=self.quantUnit_list, textvariable=self.var_quantUnit, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_quantUnit.place(x=360, y=250, width=80)
        cmb_quantUnit.current(0)

        txt_quantity = Entry(product_Frame, textvariable=self.var_qty,  font=(
            "SF Pro Rounded", 12), bg="lightyellow").place(x=150, y=250, width=200)

        # Buttons
        btn_add = Button(product_Frame, text="Add", command=self.add, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=10, y=300, width=100, height=40)
        btn_preview = Button(product_Frame, text="Preview", command=self.preview,  font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=120, y=300, width=100, height=40)
        btn_clear_all = Button(product_Frame, text="Clear all", command=self.clear_all, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=230, y=300, width=100, height=40)
        btn_clear = Button(product_Frame, text="Clear", command=self.clear, font=(
            "SF Pro Rounded", 12), bg="#E3CF57", fg="black", cursor="hand2").place(x=340, y=300, width=100, height=40)
        btn_save = Button(product_Frame, text="Save Invoice", command=self.save_bill, font=(
            "SF Pro Rounded", 12, "bold"), bg="#E3CF57", fg="black", cursor="hand2").place(x=10, y=350, width=430, height=40)

        # Inventory table
        productFrame3 = Frame(self.root, bd=3, relief=RIDGE)
        productFrame3.place(x=972, y=10,  width=460, height=785)
        ITitle = Label(productFrame3, text="Current Inventory",
                       font=("SF Pro Rounded", 20, "bold"), bg="#262626", fg="white").pack(side=TOP, fill=X)
        scrolly = Scrollbar(productFrame3, orient=VERTICAL)
        scrollx = Scrollbar(productFrame3, orient=HORIZONTAL)
        self.productTable = ttk.Treeview(productFrame3, columns=(
            "pid", "Category", "name", "price", "qty", "unit", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)
        self.productTable.heading("pid", text="PID")
        self.productTable.heading("Category", text="Category")
        self.productTable.heading("name", text="Name")
        self.productTable.heading("price", text="Price")
        self.productTable.heading("qty", text="Qty.")
        self.productTable.heading("unit", text="Unit")
        self.productTable.heading("status", text="Status")
        self.productTable["show"] = "headings"

        self.productTable.column("pid", width=45)
        self.productTable.column("Category", width=100)
        self.productTable.column("name", width=100)
        self.productTable.column("price", width=100)
        self.productTable.column("qty", width=45)
        self.productTable.column("unit", width=45)
        self.productTable.column("status", width=80)
        self.productTable.pack(fill=BOTH, expand=1)
        self.productTable.bind("<ButtonRelease-1>", self.get_data_inventory)

# ===============================================Cart============

        cal_cart_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        cal_cart_Frame.place(x=10, y=410, width=480, height=380)

        cart_Frame = Frame(cal_cart_Frame, bd=3, relief=RIDGE)
        cart_Frame.place(x=0, y=0,  width=480, height=470)
        self.cartTitle = Label(cart_Frame, text="Items in Invoice",
                               font=("SF Pro Rounded", 20, "bold"), bg="lightgray", fg="black")
        self.cartTitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)
        self.cartTable = ttk.Treeview(cart_Frame, columns=(
            "name", "unit", "price", "qty", "Amount"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.cartTable.xview)
        scrolly.config(command=self.cartTable.yview)
        self.cartTable.heading("name", text="Name")
        self.cartTable.heading("unit", text="Unit")
        self.cartTable.heading("price", text="Price")
        self.cartTable.heading("qty", text="Qty.")
        self.cartTable.heading("Amount", text="Amount")
        self.cartTable["show"] = "headings"

        self.cartTable.column("name", width=100)
        self.cartTable.column("unit", width=50)
        self.cartTable.column("price", width=90)
        self.cartTable.column("qty", width=60)
        self.cartTable.column("Amount", width=90)
        self.cartTable.pack(fill=BOTH, expand=1)
        self.cartTable.bind("<ButtonRelease-1>", self.get_data)

        # Purchase Order List Area
        pendingPurchase = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        pendingPurchase.place(x=490, y=10, width=480, height=780)
        pTitle = Label(pendingPurchase, text="Pending Purchase Orders",
                       font=("SF Pro Rounded", 20, "bold"), bg="#262626", fg="white").pack(side=TOP, fill=X)
        scrolly = Scrollbar(pendingPurchase, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(pendingPurchase, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        self.purchaseList = Listbox(pendingPurchase, font=(
            "SF Pro Rounded", 15, "bold"), bg="white", yscrollcommand=scrolly)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.purchaseList.yview)
        self.purchaseList.pack(fill=BOTH, expand=1)
        self.purchaseList.bind("<ButtonRelease-1>", self.get_data)
        scrolly.config(command=self.txt_bill_area.yview)

        # Functions
        self.show()

    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("--Select--")
        self.prod_list.append("--Select--")
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            cur.execute("Select name from supplier ")
            sup = cur.fetchall()
            if len(sup) > 0:
                for i in sup:
                    self.sup_list.append(i[0])
            cur.execute("Select name from category")
            cat = cur.fetchall()
            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("--Select--")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute(
                "Select name from product")
            prod = cur.fetchall()
            if len(prod) > 0:
                for i in prod:
                    self.prod_list.append(i[0])
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.cartTable.focus()
        content = (self.cartTable.item(f))
        row = content['values']
        self.var_prod.set(row[0])
        self.var_quantUnit.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])

    def get_data_inventory(self, ev):
        f = self.productTable.focus()
        content = (self.productTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[2])
        self.var_price.set(row[3])
        self.var_stock.set(row[4])
        print("In stock", self.var_stock.get())

    def add(self):
        if self.var_quantUnit.get() == "--Select--":
            messagebox.showerror(
                "Error", "Please Enter valid unit", parent=self.root)
        else:
            con = sqlite3.connect(database=r'crm.db')
            cur = con.cursor()
            cur.execute("select qty from product where name LIKE '%" +
                        self.var_prod.get()+"%'")
            currentStock = cur.fetchone()
            price_cal = float(int(self.var_qty.get()) *
                              float(self.var_price.get()))
            cart_data = [self.var_prod.get(), self.var_quantUnit.get(),
                         self.var_price.get(), self.var_qty.get(), price_cal, currentStock[0]]
            print(cart_data)
            # name,unit,price,qty,amount,stock
         # ============ update cart==========
            present = 'no'
            index_ = 0
            for row in self.bill_list:
                if self.var_prod.get() == row[0]:
                    present = 'yes'
                    break
                index_ += 1

            if present == 'yes':
                op = messagebox.askyesno(
                    "Confirm", "Product Already present. Do you want to Update/Remove from cart?")
                if op == True:
                    if self.var_qty.get() == "0":
                        self.bill_list.pop(index_)
                    else:
                        self.bill_list[index_][2] = self.var_quantUnit.get()
                        self.bill_list[index_][3] = self.var_price.get()
                        self.bill_list[index_][4] = self.var_qty.get()
                        self.bill_list[index_][5] = self.var_stock.get()

            if present == 'no':
                self.bill_list.append(cart_data)
            self.show_cart()
            print(self.bill_list)

    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.bill_list:
                self.cartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def clear_all(self):
        del self.bill_list[:]
        self.var_cat.set("--Select--")
        self.var_supplier.set("--Select--")
        self.var_price.set("")
        self.var_prod.set("--Select--")
        self.var_quantUnit.set("--Select--")
        self.var_qty.set("")
        self.var_searchTxt.set("")
        self.var_searchBy.set("--Select--")
        self.var_stock.set('')

    def clear(self):
        del self.bill_list[:]
        self.var_price.set("")
        self.var_prod.set("--Select--")
        self.var_quantUnit.set("--Select--")
        self.var_qty.set("")
        self.var_stock.set('')

    def preview(self):
        fp = open(f'SupplierBill/{str(self.invoice)}.txt', 'w')
        fp.write(self.txt_bill_area.get('1.0', END))
        fp.close()

    def save_bill(self):
        if len(self.bill_list) == 0:
            messagebox.showerror(
                "Error", "Add items to save invoice", parent=self.root)
        else:
            self.invoice = StringVar(
                master=self.root, value=time.strftime("%d-%m-%Y")+" " + time.strftime("%H:%M"))
            self.invoice = self.var_supplier.get()+"("+self.invoice.get()+")"
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()
            self.preview
            messagebox.showinfo(
                "Saved", "Bill has been saved", parent=self.root)
            self.show()

    def bill_top(self):
        self.invoice = StringVar(
            master=self.root, value=time.strftime("%d-%m-%Y")+" "+time.strftime("%H:%M"))
        self.invoice = self.var_supplier.get()+"("+self.invoice.get()+")"
        bill_top_temp = f'''
        \t\t\tGarwhal Marbles
        \t Phone No. 0135-2773412 , Dehradun-248007
        {str("="*47)}
        Supplier Name: {self.var_supplier.get()}
        Bill No: {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
        {str("="*47)}
        \t\tProduct\tUnit\tPrice\tQTY\tAmount
        {str("="*47)}
        '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    def bill_middle(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            for row in self.bill_list:
                # name,unit,price,qty,amount,stock
                #     cart_data = [self.var_prod.get(), self.var_quantUnit.get(),
                #  self.var_price.get(), self.var_qty.get(), price_cal, currentStock[0]]
                name = row[0]
                unit = row[1]
                price = row[2]
                qty = int(float(row[3]))+int(float(row[5]))
                amt = float(row[2])*int(row[3])
                amt = str(amt)
                self.bill_amt = amt
                self.txt_bill_area.insert(
                    END, "\n\t\t"+name+"\t"+unit+"\t"+price+"\t"+row[3]+"\t"+amt)
                # Update product in product table
                cur.execute("Update product set qty=? where name=?", (
                    qty,
                    name
                ))
                con.commit()
            con.close()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def bill_bottom(self):
        bill_bottom_temp = f'''
        {str("="*47)}
        Bill Amount\t\t\t\tRs.{self.bill_amt}
        {str("="*47)}\n
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def show(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            rows = cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = pendingVendorPurchase(root)
    root.mainloop()
