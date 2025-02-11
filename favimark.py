from tkinter import*
from tkinter import messagebox
import sqlite3

#login window, initial window visible to the user
root=Tk()
root.title("favimark/login") #title
root.geometry('700x700')  # authentication section
root.iconbitmap('login.ico') #icon of window
root.resizable(0,0) #non-resizable

#box centered in the page that contains the login UI
frame = Frame(root, bg='white', highlightbackground='black', highlightthickness=1)
frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.6)

#Title included on the top and centered
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

def login(): #this contains a separate window after user authentication
    if username_entry.get() == 'favimarko' and password_entry.get() == 'qwerty':
        root.iconify() #minimize root window
        dashboard() #dashboard opens a new windw if user authenticated 
        username_entry.delete(0,END)
        password_entry.delete(0,END)
    else:
        messagebox.showerror('Warning', 'Invalid username or password')
        
def dashboard():
        global roots
        roots = Toplevel(root)
        roots.state('zoomed') # this will make it fullscreen
        roots.title("favimark/Dashboard")

        # aligns everything at the top of the page
        top_frame = Frame(roots, bg='white')
        top_frame.pack(side=TOP, fill=BOTH, padx=1, pady=10,expand=TRUE)

        # UI for buttons 
        button_frame = Frame(top_frame, bg='white')
        button_frame.pack(side=LEFT)

        # Buttons
        add_button = Button(button_frame, text="ADD", command=add_item, font=('Arial', 12), bg='grey', fg='white')
        add_button.pack(side=LEFT, padx=10)

        edit_button = Button(button_frame, text="EDIT", command=edit_prompt, font=('Arial', 12), bg='grey', fg='white')
        edit_button.pack(side=LEFT, padx=10)

        delete_button = Button(button_frame, text="DELETE", command=delete_prompt, font=('Arial', 12), bg='grey', fg='white')
        delete_button.pack(side=LEFT, padx=10)

        # search section
        search_frame = Frame(top_frame, bg='white') #keeps the search items aligned on the top right
        search_frame.pack(side=RIGHT)

        search_entry = Entry(search_frame, font=('Arial', 12))
        search_entry.pack(side=LEFT, padx=10)

        search_button = Button(search_frame, text=" SEARCH ", font=('Arial', 12), bg='grey', fg='white')
        search_button.pack(side=LEFT, padx=10)
        
        display_items(roots)

def display_items(roots):
    global text_widget
    if 'text_widget' not in globals():
        item_frame = Frame(roots)
        item_frame.pack(fill=BOTH, expand=True)
        text_widget = Text(item_frame, width=100, height=50)
        text_widget.pack(fill=BOTH, expand=True)
    else:
        text_widget.delete('1.0', END)

    conn = sqlite3.connect('favimark.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM favourites")
    items = c.fetchall()
    conn.close()

    for i, item in enumerate(items, start=1):
        item_id = item[3]
        item_name = item[0]
        item_type = item[1]
        item_description = item[2]

        text_widget.insert(END, f"{i}. Name: {item_name}\n\n---Type: {item_type}\n\n---Description: {item_description}\n\n")

def add_item():
    global newe1, newe2, newe3, additem
    additem = Toplevel()
    additem.geometry('400x400')
    additem.iconbitmap('add.ico')
    additem.title("favimark/ADD-ITEMS")
    name_label=Label(additem,text="Mark your favourites",)
    name_label.pack()
    newe1=Entry(additem)
    newe1.pack()
    type_label=Label(additem,text="Type (Book/Movie/Anime/Manga/Manhua/Shows)")
    type_label.pack()
    newe2=Entry(additem)
    newe2.pack()
    desc_label=Label(additem,text="Review. eg:Good/Decent/Excellent")
    desc_label.pack()
    newe3=Entry(additem)
    newe3.pack()
    addnew=Button(additem,text=" ADD ",command=lambda: create(additem), bg='grey', fg='white')
    addnew.pack()

def create(additem):
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
    c.execute('INSERT INTO favourites VALUES(?,?,?)',(newe1.get(), newe2.get(), newe3.get()))
    messagebox.showinfo('Success', 'Item created successfully')
    conn.commit()
    conn.close()
    
    # Clear the text boxes #->indexing starts from 1 in text boxes
    newe1.delete(0,END)
    newe2.delete(0,END)
    newe3.delete(0,END)
    additem.destroy()
    display_items(roots)

def edit_prompt():
    global edit_prompt_window,edite1
    edit_prompt_window = Toplevel()
    edit_prompt_window.title('Edit Prompt')
    edit_prompt_window.geometry('350x350')
    edit_prompt_window.iconbitmap('edit.ico')
    edit_text=Label(edit_prompt_window,text="Enter the ID of the records you want to edit.")
    edit_text.pack(pady=50)
    edite1=Entry(edit_prompt_window)
    edite1.pack()
    edit=Button(edit_prompt_window,text="PROCEED TO EDIT",command=edit_item)
    edit.pack(pady=10)
    
def edit_item():
    global neweditse1,neweditse2,neweditse3,edite1,edit_prompt_window,edit_window
    edit_window=Toplevel()
    edit_window.title('favimark/EDIT_ITEMS')
    edit_window.geometry('300x300')
    edit_window.iconbitmap('edit.ico')
    name_label=Label(edit_window,text="Edit your marked favourites",)
    name_label.pack()
    neweditse1=Entry(edit_window)
    neweditse1.pack()
    type_label=Label(edit_window,text="Edit the Type (Book/Movie/Anime/Manga/Manhua/Shows)")
    type_label.pack()
    neweditse2=Entry(edit_window)
    neweditse2.pack()
    desc_label=Label(edit_window,text="Edit Review")
    desc_label.pack()
    neweditse3=Entry(edit_window)
    neweditse3.pack()
    edit_add=Button(edit_window,text=" SAVE ",command=update, bg='grey', fg='white')
    edit_add.pack(pady=10)
    
    try:
        conn = sqlite3.connect('favimark.db')
        c = conn.cursor()
        oid=edite1.get()
        c.execute('SELECT * FROM favourites WHERE oid=?',(oid,))
        result = c.fetchall()
        if result:
            for i in result:
                neweditse1.insert(0, i[0])
                neweditse2.insert(0, i[1])
                neweditse3.insert(0, i[2])
        else:
            messagebox.showerror('Error', 'OID not found in database')
    except sqlite3.Error as e:
        messagebox.showerror('Error', e)
    finally:
        if conn:
            conn.close()
    
def update():
    global neweditse1,neweditse2,neweditse3,edite1
    conn=sqlite3.connect('favimark.db')
    c=conn.cursor()
    c.execute(
        """UPDATE favourites SET
        fav_name = :a,
        fav_type = :b,
        fav_description= :c
        WHERE oid= :oid
        """,
        {
            "a":neweditse1.get(), #exclude \n using end-1c and not END
            "b":neweditse2.get(),
            "c":neweditse3.get(),
            "oid":edite1.get(),
        },
    )
    messagebox.showinfo('Success', 'Item edited successfully')
    conn.commit()
    conn.close()
    edite1.delete(0,END)
    edit_window.destroy()
    edit_prompt_window.destroy()
    display_items(roots)

def delete_prompt():
    global delete_prompt_window,dele1
    delete_prompt_window = Toplevel()
    delete_prompt_window.title('Delete Prompt')
    delete_prompt_window.geometry('350x350')
    delete_prompt_window.iconbitmap('delete.ico')
    del_text=Label(delete_prompt_window,text="Enter the ID of the records you want to delete.")
    del_text.pack(pady=50)
    dele1=Entry(delete_prompt_window)
    dele1.pack()
    deletee=Button(delete_prompt_window,text=" DELETE ",command=delete_item)
    deletee.pack(pady=10)
    
def delete_item():
    conn = sqlite3.connect('favimark.db')
    c = conn.cursor()
    oid = dele1.get()
    try:
        c.execute('DELETE FROM favourites WHERE oid=?', (oid,))
        conn.commit()
        
        
        # Update OID of remaining items
        c.execute('SELECT oid FROM favourites WHERE oid>?', (oid,))
        remaining_items = c.fetchall()
        for item in remaining_items:
            new_oid = item[0] - 1
            c.execute('UPDATE favourites SET oid=? WHERE oid=?', (new_oid, item[0]))
            conn.commit()
        
        
        messagebox.showinfo('Success', 'Item deleted successfully')
    except sqlite3.Error as e:
        messagebox.showerror('Error', str(e))
    finally:
        conn.close()
        display_items(roots)
        delete_prompt_window.destroy()

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