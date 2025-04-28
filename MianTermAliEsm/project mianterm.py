import tkinter

import sqlite3
from tkinter import messagebox
import re

def login():
    global session
    user = txtUser.get()
    pas = txtPass.get()    
    query = f'SELECT * FROM users WHERE username="{user}" AND password="{pas}"'
    result = cnt.execute(query)
    data = result.fetchall()
    if len(data) == 0:
        lblMsg.configure(text='Wrong username or password!!',fg='red')
    if data[0][1]=='admin':
        lblMsg.configure(text='Welcome to your account!',fg='green')
        session = data[0]
        txtUser.delete(0,'end')
        txtPass.delete(0,'end')
        btnLogin.configure(state='disabled')
        btnLogout.configure(state='active')
        btnDelete.configure(state='active')
        btnShop.configure(state='active')
        btnDelPanel.configure(state='active')
    else:
        lblMsg.configure(text='Welcome to your account!',fg='green')
        session = data[0]
        txtUser.delete(0,'end')
        txtPass.delete(0,'end')
        btnLogin.configure(state='disabled')
        btnLogout.configure(state='active')
        btnDelete.configure(state='active')
        btnShop.configure(state='active')
def logout():
    global session
    session = False
    lblMsg.configure(text='You are logged out now!',fg='green')
    btnLogin.configure(state='active')
    btnLogout.configure(state='disabled')
    btnShop.configure(state='disabled')
    btnDelPanel.configure(state='disabled')

def delAc():
    global session
    result = messagebox.askyesno(title='Delete Account',message='Are you sure?')
    if not result:
        lblMsg.configure(text='Delete canceled by user',fg='red')
        return
    query=f'DELETE FROM users WHERE id={session[0]}'
    cnt.execute(query)
    cnt.commit()
    lblMsg.configure(text='your account deleted!',fg='green')
    btnLogin.configure(state='active')
    btnLogout.configure(state='disabled')
    btnDelete.configure(state='disabled')


def signup():
    def signValidate(user,pas,cpas,addr):
        if user =='' or pas == '' or cpas =='' or addr == '':
            return False,"empty field error!"
        if pas!=cpas:
            return False,"password and confirm mismatch!"
        if len(pas) < 8:
            return False,"password length error!"
        sql = f'''SELECT * FROM users WHERE 
        username="{user.upper()}" or username="{user.lower}"  '''
        result = cnt.execute(sql)
        data = result.fetchall()
        if len(data) > 0:
            return False,"username already exist"
        #---------re----------
        exp = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(exp,pas):
            return False,"invalid password!"
        return True,""
    
    def newUser():
        user = txtUser.get()
        pas = txtPass.get()
        cpas = txtcPass.get()
        addr = txtAddr.get()
        result,msg = signValidate(user,pas,cpas,addr)
        if result == False:
            lblMsg.configure(text=msg,fg='red')
        else:
            sql = f'''INSERT INTO users (username,password,address,grade)
            VALUES ("{user}","{pas}","{addr}",0)'''
            cnt.execute(sql)
            cnt.commit()
            lblMsg.configure(text='submit done!',fg='green')
            txtUser.delete(0,'end')
            txtPass.delete(0,'end')
            txtcPass.delete(0,'end')
            txtAddr.delete(0,'end')

    winSignup = tkinter.Toplevel(win)
    winSignup.title('Signup Panel')
    winSignup.geometry('300x250')
    lblUser=tkinter.Label(winSignup,text='Username: ')
    lblUser.pack()
    txtUser=tkinter.Entry(winSignup)
    txtUser.pack()
    lblPass=tkinter.Label(winSignup,text='Password: ')
    lblPass.pack()
    txtPass=tkinter.Entry(winSignup)
    txtPass.pack()
    lblcPass=tkinter.Label(winSignup,text='Password Confirm: ')
    lblcPass.pack()
    txtcPass=tkinter.Entry(winSignup)
    txtcPass.pack()
    lblAddr=tkinter.Label(winSignup,text='Address: ')
    lblAddr.pack()
    txtAddr=tkinter.Entry(winSignup)
    txtAddr.pack()
    lblMsg=tkinter.Label(winSignup,text='')
    lblMsg.pack()
    btnSignup=tkinter.Button(winSignup,text='Create Account', command=newUser)
    btnSignup.pack()
    winSignup.mainloop()
    
    
def delPanel():
    def panelDelete():
        global session
        uid=txtId.get()
        sql=f'DELETE FROM users WHERE id="{uid}"'
        cnt.execute(sql)
        cnt.commit()
        lblMsg.configure(text='User Account Deleted Successfully!',fg='green')
        lstbox.delete(0,'end')
        sql='SELECT id,username FROM users'
        result = cnt.execute(sql)
        data = result.fetchall()
        for data in data:
            text = f'ID:{data[0]} username:{data[1]}'
            lstbox.insert('end',text)
        
    winDelAccount = tkinter.Toplevel(win)
    winDelAccount.title('Delete Account Panel')
    winDelAccount.geometry('300x340')
    sql='SELECT id,username FROM users'
    result = cnt.execute(sql)
    data = result.fetchall()
    lstbox = tkinter.Listbox(winDelAccount,width=40,height=14)
    lstbox.pack()
    for data in data:
        text = f'ID:{data[0]} username:{data[1]}'
        lstbox.insert('end',text)
    lblId=tkinter.Label(winDelAccount,text='Enter ID: ')
    lblId.pack()
    txtId=tkinter.Entry(winDelAccount)
    txtId.pack()
    lblMsg=tkinter.Label(winDelAccount,text='')
    lblMsg.pack()
    btnDelAccount=tkinter.Button(winDelAccount,text='Delete Account',command=panelDelete)
    btnDelAccount.pack()

    winDelAccount.mainloop()    


def getAllproducts():
    sql='SELECT * FROM products'
    result=cnt.execute(sql)
    products = result.fetchall()
    return products
    

def shopPanel():
    def buyProduct():
        pid = txtid.get()
        pnum = txtnum.get()
        sqlp = f'SELECT * FROM products WHERE id="{pid}"'
        result = cnt.execute(sqlp)
        Rproduct = result.fetchall()
        sql = f'''INSERT INTO carts (Pid,pname,userid,price,buyNumbers)
        VALUES ("{Rproduct[0][0]}","{Rproduct[0][1]}","{session[0]}","{Rproduct[0][2]}","{pnum}")'''
        cnt.execute(sql)
        cnt.commit()
        query = f'UPDATE products SET numbers=numbers-"{pnum}" WHERE id="{pid}"'
        cnt.execute(query)
        cnt.commit()
        sqlp = f'SELECT * FROM products WHERE id="{pid}"'
        result = cnt.execute(sqlp)
        Rproduct = result.fetchall()
        lstbox.delete(0,'end')
        products = getAllproducts()
        for product in products:
            text = f'id:{product[0]} name:{product[1]} price:{product[2]} number:{product[3]}'
            lstbox.insert('end',text)
        # sql1=f'''INSERT INTO carts (id,numbers)
        # VALUES ("{pid}","{pnum}")
        # '''
        # cnt.execute(sql1)
        # cnt.commit()
        # sql2 = f'''
        # INSERT INTO products WHERE id="{pid}", (numbers)
        # VALUES (numbers-{pnum})'''
        # cnt.execute(sql2)
        # cnt.commit()
        lblMsg2.configure(text='your product add to shopping card successfully',fg='green')
    
    winShop=tkinter.Toplevel(win)
    winShop.title('Shop Panel')
    winShop.geometry('400x480')
    lstbox=tkinter.Listbox(winShop,width=50,height=20)
    lstbox.pack()
    products = getAllproducts()
    for product in products:
        text = f'id:{product[0]} name:{product[1]} price:{product[2]} number:{product[3]}'
        lstbox.insert('end',text)
    lblid=tkinter.Label(winShop,text='id:')
    lblid.pack()
    txtid=tkinter.Entry(winShop)
    txtid.pack()
    lblnum=tkinter.Label(winShop,text='number:')
    lblnum.pack()
    txtnum=tkinter.Entry(winShop)
    txtnum.pack()
    lblMsg2=tkinter.Label(winShop,text='')
    lblMsg2.pack()
    btnBuy=tkinter.Button(winShop,text='Buy',command=buyProduct)
    btnBuy.pack()

    winShop.mainloop()
 
    
def carts():
    winCarts=tkinter.Toplevel(win)
    winCarts.title('Shopping Carts')
    winCarts.geometry('380x300')
    sql = f'SELECT * FROM carts WHERE userid="{session[0]}"'
    result = cnt.execute(sql)
    data = result.fetchall()
    lstbox = tkinter.Listbox(winCarts,width=60,height=14)
    lstbox.pack()
    for data in data:
        text = f'id:{data[1]} name:{data[2]} price:{data[4]} buy number:{data[5]}'
        lstbox.insert('end',text)
        

#-----------------------------main------------------------------
# sql='''CREATE TABLE products (
#         id INTEGER PRIMARY KEY,
#         pname VARCHAR(30) NOT NULL,
#         price INTEGER NOT NULL,
#         numbers INTEGER NOT NULL,
#         reserve VARCHAR(40)
#         )'''
# sql = ''' INSERT INTO products(pname,price,numbers)
#         VALUES("Hp Laptop 2020",1300,80)
# '''
# sql='''CREATE TABLE carts (
#         id INTEGER PRIMARY KEY,
#         Pid INTEGER,
#         pname VARCHAR(30),
#         userid INTEGER,
#         price INTEGER,
#         buyNumbers INTEGER
#         )'''
    
session = False
cnt = sqlite3.connect('shop.db')
# cnt.execute(sql)
# cnt.commit()
win = tkinter.Tk()
win.title('Login Panel')
win.geometry('400x300')
lblUser=tkinter.Label(win,text='Username: ')
lblUser.pack()
txtUser=tkinter.Entry(win)
txtUser.pack()
lblPass=tkinter.Label(win,text='Password: ')
lblPass.pack()
txtPass=tkinter.Entry(win,show='*')
txtPass.pack()
lblMsg=tkinter.Label(win,text='')
lblMsg.pack()
btnLogin=tkinter.Button(win,text='Login',command=login)
btnLogin.pack()
btnLogout=tkinter.Button(win,text='Logout',state='disabled',command=logout)
btnLogout.pack()
btnDelete=tkinter.Button(win,text='Delete account!',state='disabled',command=delAc)
btnDelete.pack()
btnSignup=tkinter.Button(win,text='Signup',command=signup)
btnSignup.pack()
btnShop=tkinter.Button(win,text='Shop',state='disabled',command=shopPanel)
btnShop.pack()
btnCarts=tkinter.Button(win,text='Shopping Carts',command=carts)
btnCarts.pack()
btnDelPanel=tkinter.Button(win,text='Delete Panel',state='disabled',command=delPanel)
btnDelPanel.pack()

win.mainloop()




























