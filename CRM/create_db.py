import sqlite3


def create_db():
    con = sqlite3.connect(database=r'crm.db')
    cur = con.cursor()

    # Employee table
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT, name text, email text, gender text, contact text, dob text, doj text, pass text, utype text, address text, salary text)")
    con.commit()

    # Supplier table

    cur.execute(
        "CREATE TABLE IF NOT EXISTS supplier(gst INTEGER PRIMARY KEY, name text, contact text, desc text)")
    con.commit()

    # Category table

    cur.execute(
        "CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT, name text)")
    con.commit()

    # Product table

    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT, Category text, name text, price text, qty text, unit text,points REAL,labCharge REAL, status text)")
    con.commit()

    # Customer Table

    cur.execute("CREATE TABLE IF NOT EXISTS customer(cid INTEGER PRIMARY KEY AUTOINCREMENT, CustName text, CustMob text,CustStatus text,CustType text, CustAdd text,CustDesc text,  )")
    con.commit()

    # Lead Table

    cur.execute("CREATE TABLE IF NOT EXISTS lead(lid INTEGER PRIMARY KEY AUTOINCREMENT, LeadName text, LeadMob text,LeadType text, LeadAdd text,LeadDesc text, LeadDate text )")
    con.commit()

    # Supplier bill Table

    cur.execute(
        "CREATE TABLE IF NOT EXISTS supBill(bid INTEGER PRIMARY KEY AUTOINCREMENT, billName text, supp text, amt text,date text )")
    con.commit()

    # Pending Orders Table

    cur.execute(
        "CREATE TABLE IF NOT EXISTS pendOrder(pendid INTEGER PRIMARY KEY AUTOINCREMENT, pendsupp text, pendsitem text, amt text,date text )")
    con.commit()


create_db()
