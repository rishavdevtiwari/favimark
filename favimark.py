from tkinter import*
from tkinter import messagebox
import sqlite3

#login window, initial window visible to the user
root=Tk()
root.title("favimark/login") #title
root.geometry('700x700') #size
root.iconbitmap('login.ico') #icon of window
root.resizable(0,0) #non-resizable

#box centered in the page that contains the login UI
frame = Frame(root, bg='white', highlightbackground='black', highlightthickness=1)
frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.6)

#Title included on the top
title_label = Label(frame, text="LOG IN/SIGN IN", font=('Arial', 18), bg='white')
title_label.pack(pady=60)

#username entry for authentication
username_label = Label(frame, text="Username", font=('Arial', 12), bg='white')
username_label.pack()
username_entry = Entry(frame, font=('Arial', 12))
username_entry.pack()

#password entry for authentication
password_label = Label(frame, text="Password", font=('Arial', 12), bg='white')
password_label.pack()
password_entry = Entry(frame, show='*', font=('Arial', 12))
password_entry.pack()

#show password checkbox that calls 'showpassword' function
show_password_var = IntVar()
show_password_checkbox = Checkbutton(frame, text="Show", variable=show_password_var, command=lambda: show_password(password_entry, show_password_var))
show_password_checkbox.pack()

def display_items(roots):
    text_widget = Text(roots, width=100, height=20)
    text_widget.pack(fill=BOTH,expand=True)
    
    conn = sqlite3.connect('favimark.db')
    c = conn.cursor()
    c.execute("SELECT * FROM favourites")
    items = c.fetchall()
    conn.close()
    
    # Clear the text widget
    text_widget.delete('1.0', END)
    
    # Display the database items
    for item in items:
        text_widget.insert(END, f"Name: {item[0]}\nType: {item[1]}\nDescription: {item[2]}\n\n")

def login():
    if username_entry.get() == 'favimarko' and password_entry.get() == 'qwerty':
        roots = Toplevel(root)
        roots.geometry('800x600')
        roots.title("favimark/Dashboard")

        # Create a frame to hold the buttons and entry box
        top_frame = Frame(roots, bg='white')
        top_frame.pack(side=TOP, fill=X, padx=10, pady=10)

        # Create a frame to hold the buttons
        button_frame = Frame(top_frame, bg='white')
        button_frame.pack(side=LEFT)

        # Create the buttons
        add_button = Button(button_frame, text="ADD", command=add_item, font=('Arial', 12), bg='grey', fg='white')
        add_button.pack(side=LEFT, padx=10)

        edit_button = Button(button_frame, text="EDIT", command=edit_item, font=('Arial', 12), bg='grey', fg='white')
        edit_button.pack(side=LEFT, padx=10)

        delete_button = Button(button_frame, text="DELETE", command=delete_item, font=('Arial', 12), bg='grey', fg='white')
        delete_button.pack(side=LEFT, padx=10)

        # Create a frame to hold the entry box and search button
        search_frame = Frame(top_frame, bg='white')
        search_frame.pack(side=RIGHT)

        search_entry = Entry(search_frame, font=('Arial', 12))
        search_entry.pack(side=LEFT, padx=10)

        search_button = Button(search_frame, text=" SEARCH ", font=('Arial', 12), bg='grey', fg='white')
        search_button.pack(side=LEFT, padx=10)
        
        display_items(roots)

    else:
        messagebox.showerror('Warning', 'Invalid username or password')
        
def add_item():
    global newe1, newe2, newe3, additem
    additem = Toplevel()
    additem.geometry('400x400')
    additem.title("favimark/ADD-ITEMS")
    name_label=Label(additem,text="Mark your favourites",)
    name_label.pack()
    newe1=Text(additem,height=1,width=40)
    newe1.pack()
    type_label=Label(additem,text="Type (Book/Movie/Anime/Manga/Manhua/Shows)")
    type_label.pack()
    newe2=Text(additem,height=1,width=40)
    newe2.pack()
    desc_label=Label(additem,text="Descripton/Review")
    desc_label.pack()
    newe3=Text(additem,height=10,width=40)
    newe3.pack()
    addnew=Button(additem,text=" ADD ",command=create, bg='grey', fg='white')
    addnew.pack()
    display_items()
    
def create():
    conn=sqlite3.connect('favimark.db')
    c=conn.cursor()
    
    # Create table if it doesn't exist
    c.execute(
        '''CREATE TABLE IF NOT EXISTS favourites(
            fav_name text,
            fav_type text,
            fav_description text)'''
    )
    
    # Insert new item into the table
    c.execute('INSERT INTO favourites VALUES(?,?,?)',(newe1.get('1.0', END), newe2.get('1.0', END), newe3.get('1.0', END)))
    #newe1.get('1.0',END)-> newe1 is an text entry method, indexing required to retrieve values....!!!!!
    conn.commit()
    conn.close()
    
    # Clear the text boxes #->indexing starts from 1 in text boxes
    newe1.delete('1.0',END)
    newe2.delete('1.0',END)
    newe3.delete('1.0',END)
    display_items()
    
def edit_item():
    print("edititems")
    display_items()
def delete_item():
    print("deleteitems")
    display_items()
def search_item():
    print("searchitems")

def show_password(entry, var):
#var is the value received from checkbox that says "show"
#if var is True, then show the password
#if var is False, then hide the password

    if var.get() == 1:
        entry.config(show='')
    else:
        entry.config(show='*')
        
#login button when pressed redirects user to the new window which is favimark ko dashboard
login_button = Button(frame, text="Login", command=login, font=('Arial', 12), bg='grey', fg='white')
login_button.pack(pady=20)
#login button placed at last cuz login function was not declared mathi

mainloop()
    
