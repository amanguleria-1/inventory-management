from cProfile import label
from cgitb import text
from doctest import master
import importlib
# from msilib import*
from pickle import FRAME
from textwrap import indent
from time import sleep
from tkinter import *
from tkinter import ttk, messagebox
from turtle import bgcolor, title, width
from typing_extensions import Self
from PIL import Image, ImageTk
from jmespath import search
import sqlite3
import os


class billsClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Business Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        self.bill_list = []
        self.var_invoice = StringVar()
        # ===title
        lbl_title = Label(self.root, text="View Customer Bill", font=(
            "SF Pro Rounded", 30, "bold"), bg='#184a45', fg='white', bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=10)
        lbl_invoice = Label(self.root, text="Invoice No:", font=(
            "SF Pro Rounded", 15), bg="white").place(x=50, y=100)
        txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=(
            "SF Pro Rounded", 15), bg="light grey").place(x=135, y=100, width=180, height=28)
        btn_search = Button(self.root, text="Search", command=self.search, font=(
            "SF Pro Rounded", 15, "bold"), bg="#2196f3", fg="black", cursor="hand2").place(x=340, y=100, width=120, height=28)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=(
            "SF Pro Rounded", 15, "bold"), bg="light grey", fg="black", cursor="hand2").place(x=460, y=100, width=120, height=28)

        sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_Frame.place(x=50, y=140, width=200, height=330)

        scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
        self.sales_list = Listbox(sales_Frame, font=(
            "SF Pro Rounded", 15, "bold"), bg="white", yscrollcommand=scrolly)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH, expand=1)
        self.sales_list.bind("<ButtonRelease-1>", self.get_data)

        # Bill Area
        bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=280, y=140, width=650, height=330)

        lbl_title = Label(bill_Frame, text="Customer Bill Area", font=(
            "SF Pro Rounded", 20, "bold"), bg='#184a45', fg='white', relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=10)

        scrolly2 = Scrollbar(sales_Frame, orient=VERTICAL)
        self.bill_area = Text(bill_Frame, font=(
            "SF Pro Rounded", 15, "bold"), bg="lightyellow", yscrollcommand=scrolly2.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)
        self.show()

# ====================================================================================================================================

    def show(self):
        del self.bill_list[:]
        self.sales_list.delete(0, END)
        # print(os.listdir('bill'))
        for i in os.listdir('bill'):
            if i.split('.')[-1] == 'txt':
                self.sales_list.insert(END, i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self, ev):
        index_ = self.sales_list.curselection()
        file_name = self.sales_list.get(index_)
        # print(file_name)
        self.bill_area.delete('1.0', END)
        fp = open(f'bill/{file_name}', 'r')
        for i in fp:
            self.bill_area.insert(END, i)
        fp.close()

    def search(self):
        if self.var_invoice.get() == "":
            messagebox.showerror(
                "Error", "Invoice Number should be required", parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                # print("yes")
                fp = open(f'bill/{self.var_invoice.get()}.txt', 'r')
                self.bill_area.delete('1.0', END)
                for i in fp:
                    self.bill_area.insert(END, i)
                fp.close()
            else:
                messagebox.showerror(
                    "Error", "Invalid Invoice Number", parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0', END)


if __name__ == "__main__":
    root = Tk()
    obj = billsClass(root)
    root.mainloop()
