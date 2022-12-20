from cProfile import label
import importlib
from tkinter import *
from turtle import bgcolor, title
from PIL import Image, ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import billsClass
from billing import BillClass
from supBillEntry import supBillEntry
from customers_for_employees import customerClass
import sqlite3
from tkinter import ttk, messagebox
from tkinter.messagebox import askyesno
import os
import time
# from sales import salesclass


class CRM:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1650x900+0+0")
        self.root.title("Business Management System")
        self.root.config(bg="white")
        # title
        self.icon_title = PhotoImage(file="images/logo1.png")
        title = Label(self.root, text="Business Management System", image=self.icon_title, compound=LEFT,
                      font=("SF Pro Rounded", 40, "bold"), bg="white", fg="black", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)

        # btn logout
        btn_logout = Button(self.root, command=self.logout, text="Logout", font=(
            "SF Pro Rounded", 15, "bold"), bg="blue", cursor="hand2").place(x=1280, y=10, height=40, width=125)

        # clock
        self.lbl_clock = Label(self.root, text="Welcome to Garwhal Marbles BMS\t\t Date:DD-MM-YYYY\t\t Time:HH:MM:SS",
                               font=("SF Pro Rounded", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # Left Menu
        self.MenuLogo = Image.open("images/menu_im.png")
        self.MenuLogo = self.MenuLogo.resize(
            (158, 158))
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)
        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=240, height=665)
        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        # Image for buttons
        self.icon_side = PhotoImage(file="images/side.png")

        # Buttons
        lbl_menu = Label(LeftMenu, text="Menu", font=(
            "SF Pro Rounded", 25, "bold"), bg="#FAD02C").pack(side=TOP, fill=X)
        btn_billing = Button(LeftMenu, text="Billing", command=self.billing, image=self.icon_side, compound=LEFT, anchor="w", padx=20, font=(
            "SF Pro Rounded", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_supplier = Button(LeftMenu, text="Suppliers", command=self.supplier, image=self.icon_side, compound=LEFT, anchor="w", padx=20, font=(
            "SF Pro Rounded", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_category = Button(LeftMenu, text="Categories", command=self.category, image=self.icon_side, compound=LEFT, anchor="w", padx=20, font=(
            "SF Pro Rounded", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_product = Button(LeftMenu, text="Products", command=self.product, image=self.icon_side, compound=LEFT, anchor="w", padx=20, font=(
            "SF Pro Rounded", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_bills = Button(LeftMenu, text="Bills", command=self.bills, image=self.icon_side, compound=LEFT, anchor="w", padx=20, font=(
            "SF Pro Rounded", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_customer = Button(LeftMenu, text="Customers", command=self.cust, image=self.icon_side, compound=LEFT, anchor="w", padx=20, font=(
            "SF Pro Rounded", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_supBillEntry = Button(LeftMenu, text="Supplier Bills", command=self.supBill, image=self.icon_side, compound=LEFT, anchor="w", padx=20, font=(
            "SF Pro Rounded", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_SuppPayment = Button(LeftMenu, text="Stock payment",  image=self.icon_side, compound=LEFT, anchor="w", padx=20, font=(
            "SF Pro Rounded", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_lead = Button(LeftMenu, text="Leads", image=self.icon_side, compound=LEFT, anchor="w", padx=20, font=(
            "SF Pro Rounded", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_returns = Button(LeftMenu, text="Returns", image=self.icon_side, compound=LEFT, anchor="w", padx=20, font=(
            "SF Pro Rounded", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_exit = Button(LeftMenu, text="Exit", command=self.exit, image=self.icon_side, compound=LEFT, anchor="w", padx=20, font=(
            "SF Pro Rounded", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)

        # Content

        self.lbl_supplier = Label(
            self.root, text="Total Suppliers\n[ 0 ]", bd=5, relief=RIDGE, bg="#FAD02C", fg="black", font=("SF Pro Rounded", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)

        self.lbl_category = Label(
            self.root, text="Total Categories\n[ 0 ]", bd=5, relief=RIDGE, bg="#FAD02C", fg="black", font=("SF Pro Rounded", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, height=150, width=300)

        self.lbl_product = Label(
            self.root, text="Total Products\n[ 0 ]", bd=5, relief=RIDGE, bg="#FAD02C", fg="black", font=("SF Pro Rounded", 20, "bold"))
        self.lbl_product.place(x=300, y=120, height=150, width=300)

        # footer
        lbl_footer = Label(self.root, text="BMS-Business Management System | Bespoked Inhouse\n For any tech issue contact IT Dept",
                           font=("SF Pro Rounded", 12), bg="#4d636d", fg="white")
        lbl_footer.pack(side=BOTTOM, fill=X)
        self.update_content()


# ================================================================================================================================================================

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def bills(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = billsClass(self.new_win)

    def billing(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = BillClass(self.new_win)

    def cust(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = customerClass(self.new_win)

    def supBill(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supBillEntry(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database=r'crm.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            product = cur.fetchall()
            self.lbl_product.config(
                text=f'Total Products\n[ {str(len(product))} ]')

            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(
                text=f'Total Suppliers\n[ {str(len(supplier))} ]')

            cur.execute("select * from category")
            category = cur.fetchall()
            self.lbl_category.config(
                text=f'Total Categories\n[ {str(len(category))} ]')

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(
                text=f"Welcome to Garwhal Marbles BMS\t\t Date: {str(date_)}\t\t Time:{str(time_)}")
            self.lbl_clock.after(200, self.update_content)

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to :{str(ex)}", parent=self.root)

    def logout(self):
        answer = askyesno(title='confirmation',
                          message='Are you sure that you want to quit?')
        if answer:
            self.root.destroy()
            os.system("python login.py ")

    def exit(self):
        answer = askyesno(title='confirmation',
                          message='Are you sure that you want to Exit?')
        if answer:
            self.root.destroy()
            os.system("python login.py ")


if __name__ == "__main__":
    root = Tk()
    obj = CRM(root)
    root.mainloop()
