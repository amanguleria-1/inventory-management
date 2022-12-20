from cProfile import label
from curses.textpad import Textbox
# import imp
import importlib
from itertools import product
import re
from selectors import SelectorKey
import string
from tkinter import *
from turtle import bgcolor, title, update
from unittest import result
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
# from tkmacosx import Button
import os
import tempfile
import time
from tkinter.messagebox import askyesno


class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1650x900+0+0")
        self.root.title("Business Management System")
        self.root.config(bg="white")
        self.cart_list = []
        self.chk_print = 0

        # title
        self.icon_title = PhotoImage(file="images/logo1.png")
        title = Label(self.root, text="Business Management System", image=self.icon_title, compound=LEFT,
                      font=("SF Pro Rounded", 40, "bold"), bg="white", fg="black", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)

        # btn logout
        btn_logout = Button(self.root, command=self.logout, text="Logout", font=(
            "SF Pro Rounded", 15, "bold"), bg="red", fg="yellow", cursor="hand2").place(x=1280, y=10, height=40, width=125)

        # clock
        self.lbl_clock = Label(self.root, text="Welcome to Garwhal Marbles BMS\t\t Date:DD-MM-YYYY\t\t Time:HH:MM:SS",
                               font=("SF Pro Rounded", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # Product Frame
        productFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        productFrame1.place(x=10, y=110, width=410, height=530)

        pTitle = Label(productFrame1, text="All Products",
                       font=("SF Pro Rounded", 20, "bold"), bg="#262626", fg="white").pack(side=TOP, fill=X)

        # Product Search Frame
        self.var_search = StringVar()
        productFrame2 = Frame(productFrame1, bd=2, relief=RIDGE, bg="white")
        productFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search = Label(productFrame2, text="Search Products (By name)", font=(
            "SF Pro Rounded", 15, "bold"), bg="white", fg="green").place(x=2, y=5)
        lbl_name = Label(productFrame2, text="Product Name:", font=(
            "SF Pro Rounded", 15, "bold"), bg="white").place(x=5, y=48)
        txt_search = Entry(productFrame2, bd=2, text=self.var_search, relief=RIDGE, font=(
            "SF Pro Rounded", 15), bg="lightgray").place(x=122, y=47, width=150, height=28)
        btn_search = Button(productFrame2, text="Search", command=self.search, font=(
            "SF Pro Rounded", 15, "bold"), bg="#2196f3", fg="Black", cursor="hand2").place(x=280, y=45, width=100, height=25)
        btn_show_all = Button(productFrame2, text="Show All", command=self.show, font=(
            "SF Pro Rounded", 15, "bold"), bg="white", fg="black", cursor="hand2").place(x=280, y=15, width=100, height=25)
        productFrame3 = Frame(productFrame1, bd=3, relief=RIDGE)
        productFrame3.place(x=2, y=140,  width=398, height=385)
        scrolly = Scrollbar(productFrame3, orient=VERTICAL)
        scrollx = Scrollbar(productFrame3, orient=HORIZONTAL)
        self.productTable = ttk.Treeview(productFrame3, columns=(
            "pid", "name", "price", "qty", "unit", "points", "labCharge", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)
        self.productTable.heading("pid", text="PID")
        self.productTable.heading("name", text="Name")
        self.productTable.heading("price", text="Price")
        self.productTable.heading("qty", text="Stock")
        self.productTable.heading("unit", text="Unit")
        self.productTable.heading("points", text="Points")
        self.productTable.heading("labCharge", text="Lab. Charge")
        self.productTable.heading("status", text="Status")
        self.productTable["show"] = "headings"

        self.productTable.column("pid", width=45)
        self.productTable.column("name", width=100)
        self.productTable.column("price", width=80)
        self.productTable.column("qty", width=80)
        self.productTable.column("unit", width=80)
        self.productTable.column("points", width=80)
        self.productTable.column("labCharge", width=80)
        self.productTable.column("status", width=60)
        self.productTable.pack(fill=BOTH, expand=1)
        self.productTable.bind("<ButtonRelease-1>", self.get_data)
        lbl_note = Label(
            productFrame3, text="Note: Enter Qty 0 to Remove the Product from Cart ", font=(
                "SF Pro Rounded", 15, "bold"), anchor='w', bg="white", fg="red").pack(side=BOTTOM, fill=X)

        # Customer Frame
        customerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        customerFrame.place(x=425, y=110, width=530, height=317)
        self.var_cust_name = StringVar()
        self.var_contact = StringVar()
        self.var_customer_type = StringVar()
        self.var_Member_status = StringVar()
        self.var_address = StringVar()
        self.var_careOf = StringVar()
        self.var_careOf_mob_no = StringVar()
        self.var_del_chrg = StringVar()
        self.var_unit = StringVar()
        self.var_points = StringVar()
        self.var_lab_chrg = DoubleVar()
        self.tot_var_lab_chrg = DoubleVar()
        self.var_payment_type = StringVar()
        cTitle = Label(customerFrame, text="Customer Details",
                       font=("SF Pro Rounded", 15, "bold"), bg="#262626", fg="white").pack(side=TOP, fill=X)
        lbl_Customer_name = Label(customerFrame, text="Name:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=5, y=35)
        txt_Customer_name = Entry(customerFrame, bd=2, text=self.var_cust_name, font=(
            "SF Pro Rounded", 13), bg="lightgray").place(x=55, y=35, width=180, height=22)

        lbl_Contact = Label(customerFrame, text="Contact No:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=240, y=35)
        txt_Contact = Entry(customerFrame, bd=2, text=self.var_contact, font=(
            "SF Pro Rounded", 13), bg="lightgray").place(x=327, y=35, width=140, height=22)

        lbl_Customer_Type = Label(customerFrame, text="C. Type:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=5, y=75)
        cmb_Customer_Type = ttk.Combobox(customerFrame, values=(
            "--Select--", "Walk-in", "Owner",  "Supplier", "Mason"), textvariable=self.var_customer_type, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_Customer_Type.place(x=72, y=75, width=180)
        cmb_Customer_Type.current(0)

        lbl_Member_status = Label(customerFrame, text="M. Status:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=255, y=75)
        cmb_Member_status = ttk.Combobox(customerFrame, values=(
            "--Select--", "Registered", "Unregistered"), textvariable=self.var_Member_status, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_Member_status.place(x=332, y=75, width=180)
        cmb_Member_status.current(0)

        lbl_address = Label(customerFrame, text="Address:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=5, y=110)
        txt_address = Entry(customerFrame, bd=2, text=self.var_address, font=(
            "SF Pro Rounded", 13), bg="lightgray").place(x=72, y=110, width=450, height=50)

        lbl_payment_type = Label(customerFrame, text="Payment Type:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=5, y=175)
        cmb_payment_type = ttk.Combobox(customerFrame, values=(
            "--Select--", "Prepaid", "C.O.D", "Credit", "Advance", "Cheque"), textvariable=self.var_payment_type, state="readonly", justify=CENTER, font=(
            "SF Pro Rounded", 12))
        cmb_payment_type.place(x=120, y=175, width=180)
        cmb_payment_type.current(0)

        lbl_care_of = Label(customerFrame, text="Care of:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=5, y=205)
        txt_care_of = Entry(customerFrame, bd=2, text=self.var_careOf, font=(
            "SF Pro Rounded", 13), bg="lightgray").place(x=72, y=205, width=220, height=22)

        lbl_care_of_mob_no = Label(customerFrame, text="C.O mob no:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=295, y=205)
        txt_care_of_mob_no = Entry(customerFrame, bd=2, text=self.var_careOf_mob_no, font=(
            "SF Pro Rounded", 13), bg="lightgray").place(x=385, y=205, width=135, height=22)

        lbl_delivery_charges = Label(customerFrame, text="Delivery Charges:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=5, y=240)
        txt_del_charges = Entry(customerFrame, bd=2, text=self.var_del_chrg, font=(
            "SF Pro Rounded", 13), bg="lightgray").place(x=130, y=245, width=160, height=22)

        lbl_labour_charges = Label(customerFrame, text="Labour Charges:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=5, y=270)
        txt_lab_charges = Entry(customerFrame, bd=2, text=self.tot_var_lab_chrg, state="readonly", font=(
            "SF Pro Rounded", 13), bg="lightgray").place(x=130, y=275, width=160, height=22)

        btn_fetch = Button(customerFrame, text="Fetch", command=self.show, font=(
            "SF Pro Rounded", 15, "bold"), bg="white", fg="black", cursor="hand2").place(x=470, y=35, width=50, height=25)
        # Cart Frame

        cal_cart_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        cal_cart_Frame.place(x=425, y=430, width=530, height=360)

        cart_Frame = Frame(cal_cart_Frame, bd=3, relief=RIDGE)
        cart_Frame.place(x=2, y=0,  width=525, height=355)
        self.cartTitle = Label(cart_Frame, text="Cart \t Total Products: 0",
                               font=("SF Pro Rounded", 15, "bold"), bg="lightgray", fg="black")
        self.cartTitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)
        self.cartTable = ttk.Treeview(cart_Frame, columns=(
            "pid", "name", "price", "qty", "unit", "points", "labCharge", "totalPoints", "Amount"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.cartTable.xview)
        scrolly.config(command=self.cartTable.yview)
        self.cartTable.heading("pid", text="PID")
        self.cartTable.heading("name", text="Name")
        self.cartTable.heading("price", text="Price")
        self.cartTable.heading("qty", text="Qty.")
        self.cartTable.heading("unit", text="Unit")
        self.cartTable.heading("points", text="Point Value")
        self.cartTable.heading("labCharge", text="Lab. Charges")
        self.cartTable.heading("totalPoints", text="Points Earned")
        self.cartTable.heading("Amount", text="Amount")
        self.cartTable["show"] = "headings"

        self.cartTable.column("pid", width=40)
        self.cartTable.column("name", width=100)
        self.cartTable.column("price", width=90)
        self.cartTable.column("qty", width=40)
        self.cartTable.column("unit", width=60)
        self.cartTable.column("points", width=80)
        self.cartTable.column("labCharge", width=80)
        self.cartTable.column("totalPoints", width=80)
        self.cartTable.column("Amount", width=90)
        self.cartTable.pack(fill=BOTH, expand=1)
        self.cartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        # ADD To Cart Frame
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = DoubleVar()
        self.var_qty = DoubleVar()
        self.var_pro_unit = StringVar()
        self.var_pro_lab_chrg = DoubleVar()
        self.var_stock = DoubleVar()
        self.var_totsum = DoubleVar()

        add_cart_widget_Frame = Frame(
            self.root, bd=2, relief=RIDGE, bg="white")
        add_cart_widget_Frame.place(x=10, y=640, width=410, height=150)
        p_name = Label(add_cart_widget_Frame, text="Product Name:", font=(
            "SF Pro Rounded", 15, "bold"), bg="white", fg="black").place(x=0, y=3)
        txt_p_name = Entry(add_cart_widget_Frame, textvariable=self.var_pname, font=(
            "SF Pro Rounded", 15, "bold"), bg="lightgray", fg="black", relief=RIDGE,  state="readonly").place(x=115, y=3, width=190, height=25)

        p_price = Label(add_cart_widget_Frame, text="Price Per Qty:", font=(
            "SF Pro Rounded", 15, "bold"), bg="white", fg="black").place(x=0, y=30)
        txt_p_price = Entry(add_cart_widget_Frame, textvariable=self.var_price, relief=RIDGE, font=(
            "SF Pro Rounded", 15, "bold"), bg="lightgray").place(x=115, y=28, width=190, height=25)

        p_qty = Label(add_cart_widget_Frame, text="Quantity:", font=(
            "SF Pro Rounded", 15, "bold"), bg="white", fg="black").place(x=0, y=60)
        txt_p_qty = Entry(add_cart_widget_Frame, textvariable=self.var_qty, relief=RIDGE,  font=(
            "SF Pro Rounded", 15, "bold"), bg="lightgray").place(x=115, y=58, width=190, height=25)

        self.lbl_instock = Label(add_cart_widget_Frame, text="In Stock:", font=(
            "SF Pro Rounded", 15, "bold"), bg="white", fg="black")
        self.lbl_instock.place(x=0, y=95)

        btn_clear_cart = Button(add_cart_widget_Frame, text="Clear", font=(
            "SF Pro Rounded", 15, "bold"), relief=RIDGE, command=self.clear_cart,  cursor="hand2").place(x=150, y=90, height=20, width=150)
        btn_add_cart = Button(add_cart_widget_Frame, text="Add | Update", command=self.add_update_cart, font=(
            "SF Pro Rounded", 15, "bold"), relief=RIDGE,  cursor="hand2").place(x=150, y=110, height=20, width=150)

        # Billing Area
        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billFrame.place(x=955, y=110, width=483, height=530)
        pTitle = Label(billFrame, text="Bill Area",
                       font=("SF Pro Rounded", 20, "bold"), bg="#262626", fg="white").pack(side=TOP, fill=X)
        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        # Billing Buttons
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billMenuFrame.place(x=955, y=640, width=483, height=150)

        self.lbl_amt = Label(billMenuFrame, text="Bill Amount(Rs)\n0.00",
                             font=("SF Pro Rounded", 15, "bold"), bg="#3f51b5", fg="white")
        self.lbl_amt.place(x=1, y=5, width=160, height=74)

        self.lbl_del_charge = Label(billMenuFrame, text="Delivery Charges(Rs)\n0.00",
                                    font=("SF Pro Rounded", 15, "bold"), bg="#3f51b5", fg="white")
        self.lbl_del_charge.place(x=162, y=5, width=160, height=74)

        self.lbl_net_pay = Label(billMenuFrame, text="Net Payment(Rs)\n0.00",
                                 font=("SF Pro Rounded", 15, "bold"), bg="#3f51b5", fg="white")
        self.lbl_net_pay.place(x=323, y=5, width=160, height=74)
# ===
        btn_print = Button(billMenuFrame, text="Print", command=self.print_bill,
                           font=("SF Pro Rounded", 15, "bold"), fg="black", cursor="hand2")
        btn_print.place(x=1, y=80, width=160, height=74)

        btn_clear_all = Button(billMenuFrame, text="Clear All",
                               font=("SF Pro Rounded", 15, "bold"), command=self.clear_all, fg="black", cursor="hand2")
        btn_clear_all.place(x=162, y=80, width=160, height=74)

        btn_generate = Button(billMenuFrame, text="Generate bill", command=self.generate_bill,
                              font=("SF Pro Rounded", 15, "bold"), fg='black', cursor="hand2")
        btn_generate.place(x=323, y=80, width=160, height=74)

        self.show()
        self.update_date_and_time()

        # All Functions

    def show(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            cur.execute(
                "select pid, name, price, qty, unit, points, labCharge, status from product where status='Active'")
            rows = cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def search(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror(
                    "Error", "Search Input should be required", parent=self.root)
            else:
                cur.execute("select pid, name, price, qty, points, labCharge, status from product where name LIKE '%" +
                            self.var_search.get()+"%' and status='Active'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.productTable.delete(
                        *self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert('', END, values=row)
                else:
                    messagebox.showerror(
                        "Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.productTable.focus()
        content = (self.productTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock:{str(row[3])}")
        self.var_stock.set(row[3])
        self.var_unit.set(row[4])
        self.var_points.set(row[5])
        self.var_lab_chrg.set(row[6])
        # self.var_qty.set('0')

    def get_data_cart(self, ev):
        f = self.cartTable.focus()
        content = (self.cartTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock:{str(row[3])}")
        self.var_qty.set(row[3])
        self.var_unit.set(row[4])
        self.var_points.set(row[5])

    def add_update_cart(self):
        if self.var_pid.get() == "":
            messagebox.showerror(
                "Error", "Please Select Product", parent=self.root)
        elif self.var_del_chrg.get() == "":
            messagebox.showerror(
                "Error", "Please mention delivery charges(Type 0 for Free Delivery)", parent=self.root)
            return
        elif self.var_qty.get() == "":
            messagebox.showerror(
                "Error", "Quantity is required", parent=self.root)
        elif self.var_qty.get() > self.var_stock.get():
            messagebox.showerror(
                "Error", "Insufficient Stock ", parent=self.root)
        else:
            price_cal = (float(self.var_qty.get()) *
                         float(self.var_price.get()))
            points_cal = (float(self.var_qty.get()) *
                          float(self.var_points.get()))
            lab_charge = ((self.var_qty.get()) *
                          (self.var_lab_chrg.get()))
            self.tot_var_lab_chrg.set(lab_charge)
            price_cal += lab_charge
            # pid,name,price,qty,amount,stock

            cart_data = [self.var_pid.get(), self.var_pname.get(),
                         self.var_price.get(), self.var_qty.get(), self.var_unit.get(), self.var_points.get(), lab_charge, points_cal, price_cal, self.var_stock.get()]
            print("This is cart data", cart_data)

            # ============ update cart==========
            present = 'no'
            index_ = 0

            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = 'yes'
                    break
                index_ += 1
            # print(index_)
            if present == 'yes':
                op = messagebox.askyesno(
                    "Confirm", "Product Already present. Do you want to Update/Remove from cart?")
                if op == True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        self.cart_list[index_][2] = self.var_price.get()
                        self.cart_list[index_][3] = self.var_qty.get()
                        self.cart_list[index_][4] = self.var_unit.get()
                        self.cart_list[index_][5] = self.var_points.get()
                        self.cart_list[index_][6] = lab_charge
                        self.cart_list[index_][7] = points_cal
                        self.cart_list[index_][8] = price_cal
                        self.cart_list[index_][9] = self.var_stock.get()
            else:
                self.cart_list.append(cart_data)

            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amt = 0
        self.net_pay = 0
        self.del_charge = 0
        self.total_points = 0
        # if self.var_del_chrg.get() == '':
        #     messagebox.showerror(
        #         "Error", "Please mention delivery charges(Type 0 for Free Delivery)", parent=self.root)
        #     return
        self.del_charge = float(self.var_del_chrg.get())
        for row in self.cart_list:
            self.total_points = self.total_points+float(row[7])
            self.bill_amt = self.bill_amt+float(row[8])
        self.net_pay = self.bill_amt + self.del_charge
        self.lbl_amt.config(text=f"Bill Amount(Rs)\n{str(self.bill_amt)}")
        self.lbl_del_charge.config(
            text=f"Delivery Charges(Rs)\n{str(self.del_charge)}")
        self.lbl_net_pay.config(text=f"Net Amount(Rs)\n{str(self.net_pay)}")
        self.cartTitle.config(
            text=f"Cart \t Total Products: {str(len(self.cart_list))}")

    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cart_list:
                self.cartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def generate_bill(self):

        if self.var_customer_type.get() == 'Walk-in':
            # ====Bill Top==
            self.bill_top()
            # ====Bill Middle==
            self.bill_middle()
            # ====Bill Bottom==
            self.bill_bottom()
            fp = open(f'bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showinfo(
                "Saved", "Your bill has been generated and saved sucesfully", parent=self.root)
            self.chk_print = 1
        if self.var_cust_name.get() == '' or self.var_contact.get() == '' or self.var_address == '' or self.var_payment_type == '--Select--':
            messagebox.showerror(
                "Error", "Customer details required", parent=self.root)
        elif len(self.cart_list) <= 0:
            messagebox.showerror(
                "Error", "Add Products in Cart to Continue", parent=self.root)

        else:

            # ====Bill Top==
            self.bill_top()
            # ====Bill Middle==
            self.bill_middle()
            # ====Bill Bottom==
            self.bill_bottom()
            fp = open(f'bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showinfo(
                "Saved", "Your bill has been generated and saved sucesfully", parent=self.root)
            self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + \
            int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
        \t\t\tGarwhal Marbles
        \t Phone No. 0135-2773412 , Dehradun-248007
        {str("="*47)}
        Customer Name: {self.var_cust_name.get()}
        Ph no :{self.var_contact.get()}
        Address :{self.var_address.get()}
        Payment Type:{self.var_payment_type.get()}
        Bill No: {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
        {str("="*47)}
        \t\tProduct\tPrice\tQTY\tAmount
        {str("="*47)}
        '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)


# [self.var_pid.get(), self.var_pname.get(),
        #  self.var_price.get(), self.var_qty.get(), self.var_unit.get(), self.var_points.get(), self.var_lab_chrg.get(), points_cal, price_cal, self.var_stock.get()]
# [self.var_pid.get(), self.var_pname.get(),
        #  self.var_price.get(), self.var_qty.get(), price_cal, self.var_stock.get()]
#  cart_data = [self.var_pid.get(), self.var_pname.get(),
        #  self.var_price.get(), self.var_qty.get(), self.var_unit.get(), self.var_points.get(), lab_charge, points_cal, price_cal, self.var_stock.get()]


    def bill_middle(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                # pid,name,price,qty,amount,stock
                pid = row[0]
                name = row[1]
                price = row[2]
                qty = float(row[9])-float(row[3])
                if float(row[3]) == float(row[9]):
                    status = "Inactive"
                if float(row[3]) != float(row[9]):
                    status = "Active"
                amt = float(row[2])*float(row[3])
                amt = str(amt)
                self.txt_bill_area.insert(
                    END, "\n\t\t"+name+"\t"+price+"\t"+row[3]+"\t"+amt)
                # Update product in product table
                cur.execute("Update product set qty=?,status=? where pid=?", (
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def bill_bottom(self):
        bill_bottom_temp = f'''
        {str("="*47)}
        Points Earned\t\t\t\tRs.{self.total_points}
        Bill Amount\t\t\t\tRs.{self.bill_amt}
        Delivery Charges\t\t\t\tRs.{self.del_charge}
        Net Payment\t\t\t\tRs.{self.net_pay}
        {str("="*47)}\n
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set(0)
        self.lbl_instock.config(text=f"In Stock:")
        self.var_stock.set(0.0)
        self.var_qty.set(0.0)

    def clear_all(self):
        del self.cart_list[:]
        self.var_cust_name.set('')
        self.var_contact.set('')
        self.var_customer_type.set('--Select--')
        self.var_address.set('')
        self.var_Member_status.set('--Select--')
        self.var_del_chrg.set('0')
        self.var_careOf.set('')
        self.var_careOf_mob_no.set('')
        self.txt_bill_area.delete('1.0', END)
        self.var_search.set('')
        self.cartTitle.config(
            text=f"Cart \t Total Products: 0")
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print = 0

    def update_date_and_time(self):
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(
            text=f"Welcome to Garwhal Marbles BMS\t\t Date:{str(date_)}\t\t Time:{str(time_)}")
        self.lbl_clock.after(200, self.update_date_and_time)

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo(
                "Print", "Please wait while printing", parent=self.root)
            new_file = tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file, 'print')
        if self.chk_print == 0:
            messagebox.showerror(
                "Print", "Please generate bill to print the receipt", parent=self.root)

    def logout(self):
        answer = askyesno(title='confirmation',
                          message='Are you sure that you want to quit?')
        if answer:
            self.root.destroy()
            os.system("python login.py")


if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()
