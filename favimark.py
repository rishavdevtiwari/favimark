from tkinter import*
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import uuid

text_widget=None
current_user_id=None

# Function to toggle password visibility
def toggle_password(entry, button):
    """Toggle password visibility and change eye button icon"""
    if entry.cget('show') == '*':
        entry.config(show='')  # Show password
        button.config(image=eye_closed_icon)  # Change to closed eye
        button.image = eye_closed_icon  # Prevent garbage collection
    else:
        entry.config(show='*')  # Hide password
        button.config(image=eye_open_icon)  # Change to open eye
        button.image = eye_open_icon  # Prevent garbage collection

# Function to toggle between Login and Register
def toggle_mode():
    global is_login
    is_login = not is_login
    title_label.config(text="LOG IN / SIGN IN" if is_login else "SIGN UP / REGISTER")
    login_button.config(text="Login" if is_login else "Sign Up", command=login if is_login else register)
    toggle_button.config(text="New to favimark? Register ..." if is_login else "Already Registered? Sign In ...")
    
    # Show/hide confirm password field dynamically
    if is_login:
        confirm_password_label.grid_remove()
        confirm_password_frame.grid_remove()
        frame.place(relwidth=0.6, relheight=0.7)  # Resize frame for login
    else:
        confirm_password_label.grid()
        confirm_password_frame.grid()
        frame.place(relwidth=0.6, relheight=0.8)  # Resize frame for signup

def login():
    global current_user_id
    username = username_entry.get()
    password = password_entry.get()
    
    conn = sqlite3.connect("favimarko.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        current_user_id = user[0]
        dashboard()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

def register():
    # Retrieve data from entry fields
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Check if fields are empty
    if username == "" or password == "" or confirm_password == "":
        messagebox.showerror("Error", "Fields cannot be empty")
        return

    # Check if passwords match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    # Generate a unique user ID
    user_id = str(uuid.uuid4())[:8]

    try:
        # Connect to the database
        conn = sqlite3.connect("favimarko.db")
        cursor = conn.cursor()

        # Create the users and favourites tables if they don't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            user_id TEXT PRIMARY KEY, 
                            username TEXT UNIQUE, 
                            password TEXT)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS favourites (
                            user_id TEXT, 
                            fav_name TEXT, 
                            fav_type TEXT, 
                            fav_description TEXT,
                            FOREIGN KEY(user_id) REFERENCES users(user_id))''')

        # Insert user data into the users table
        cursor.execute("INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)", 
                       (user_id, username, password))

        conn.commit()

        messagebox.showinfo("Success", "Registration Successful! Please log in.")
        toggle_mode()  # Assuming this function is defined to switch to the login screen

    except sqlite3.IntegrityError:
        # Catch integrity errors like duplicate usernames
        messagebox.showerror("Error", "Username already exists")
    except sqlite3.Error as e:
        # Catch any other database-related errors
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        # Ensure the connection is closed
        conn.close()


# Create main window
root = Tk()
root.title("favimark | Login")
root.geometry('700x700')
root.iconbitmap('login.ico')
root.resizable(False, False)

# ✅ Use PIL to load and resize images properly
try:
    eye_open_img = Image.open("eye_open.png").resize((20, 20))  # Resize image
    eye_open_icon = ImageTk.PhotoImage(eye_open_img)

    eye_closed_img = Image.open("eye_close.png").resize((20, 20))  
    eye_closed_icon = ImageTk.PhotoImage(eye_closed_img)
except Exception as e:
    print("Error loading images:", e)
    exit()

# Frame for login form
frame = Frame(root, bg='white', highlightbackground='grey', highlightthickness=2)
frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.7)

frame.grid_columnconfigure(0, weight=1)

# Title
title_label = Label(frame, text="LOG IN / SIGN IN", font=('Arial', 16, 'bold'), bg='white')
title_label.grid(row=0, column=0, pady=15, columnspan=2)

# Profile Image
image = PhotoImage(file="profile.png").subsample(4, 4)
image_label = Label(frame, image=image, bg='white')
image_label.grid(row=1, column=0, pady=10, columnspan=2)

# Username Entry
username_label = Label(frame, text="Username", font=('Arial', 12, 'bold'), bg='white', anchor='w')
username_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=40)
username_entry = Entry(frame, font=('Arial', 12), bd=3)
username_entry.grid(row=3, column=0, columnspan=2, padx=40, pady=5, ipadx=5, ipady=3, sticky="ew")

# Password Entry
password_label = Label(frame, text="Password", font=('Arial', 12, 'bold'), bg='white', anchor='w')
password_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=40)

# Password Frame (Entry + Eye Button)
password_frame = Frame(frame, bg="white")
password_frame.grid(row=5, column=0, columnspan=2, padx=40, pady=5, sticky="ew")

password_entry = Entry(password_frame, show='*', font=('Arial', 12), bd=3, width=20)
password_entry.pack(side="left", fill="x", expand=True, ipadx=5, ipady=3)

eye_button = Button(password_frame, image=eye_open_icon, command=lambda: toggle_password(password_entry, eye_button), bd=0, bg='white', activebackground='white')
eye_button.pack(side="right", padx=5)

# Confirm Password Entry (Only for Signup)
confirm_password_label = Label(frame, text="Confirm Password", font=('Arial', 12, 'bold'), bg='white', anchor='w')
confirm_password_label.grid(row=6, column=0, columnspan=2, sticky="w", padx=40)

confirm_password_frame = Frame(frame, bg="white")
confirm_password_frame.grid(row=7, column=0, columnspan=2, padx=40, pady=5, sticky="ew")

confirm_password_entry = Entry(confirm_password_frame, show='*', font=('Arial', 12), bd=3, width=20)
confirm_password_entry.pack(side="left", fill="x", expand=True, ipadx=5, ipady=3)

confirm_eye_button = Button(confirm_password_frame, image=eye_open_icon, command=lambda: toggle_password(confirm_password_entry, confirm_eye_button), bd=0, bg='white', activebackground='white')
confirm_eye_button.pack(side="right", padx=5)

# Hide confirm password initially
confirm_password_label.grid_remove()
confirm_password_frame.grid_remove()

# Login/Signup Button
is_login = True
login_button = Button(frame, text="Login", command=login, font=('Arial', 12), bg='grey', fg='white', bd=3)
login_button.grid(row=8, column=0, columnspan=2, padx=40, pady=15, ipadx=15, ipady=5, sticky="ew")

# Toggle Button
toggle_button = Button(frame, text="New to favimark? Register ...", command=toggle_mode, font=('Arial', 10), fg='blue', bg='white', bd=0)
toggle_button.grid(row=9, column=0, columnspan=2, pady=10)

#   FUNCTION TO DISPLAY DASHBOARD OF FAVIMARK
#->CONTAINS 4 BUTTONS AND ONE INTERFACE BELOW IT
#->MADE FULL SCREEN FOR BETTER UI
#->ROOTS IS USED AS THE WINDOW HERE.
       
def dashboard():
    global roots  # Giving roots window a global scope to access it from other windows
    roots = Toplevel(root)
    roots.geometry('800x800')
    roots.title("favimark/Dashboard")

    # Align everything at the top of the page
    top_frame = Frame(roots, bg='white')
    top_frame.pack(side=TOP, fill=BOTH, padx=1, pady=10, expand=True)

    # UI for buttons which aligns CRUD buttons at the top of the page using top_frame
    button_frame_crud = Frame(top_frame, bg='white')
    button_frame_crud.pack(side=LEFT, fill=X)  # Use fill=X to stretch horizontally

    # Use grid layout for buttons and align them to the left side
    add_button = Button(button_frame_crud, text="ADD", command=add_item, font=('Arial', 12), bg='grey', fg='white', bd=3)
    add_button.grid(row=0, column=0, padx=10, sticky='w')  # Align left

    edit_button = Button(button_frame_crud, text="EDIT", command=edit_prompt, font=('Arial', 12), bg='grey', fg='white', bd=3)
    edit_button.grid(row=0, column=1, padx=10, sticky='w')  # Align left

    search_button = Button(button_frame_crud, text=" SEARCH ", command=search_prompt, font=('Arial', 12), bg='grey', fg='white', bd=3)
    search_button.grid(row=0, column=2, padx=10, sticky='w')  # Align left

    delete_button = Button(button_frame_crud, text="DELETE", command=delete_prompt, font=('Arial', 12), bg='grey', fg='white', bd=3)
    delete_button.grid(row=0, column=3, padx=10, sticky='w')  # Align left

    # UI for exit button
    button_frame_exit = Frame(top_frame, bg='white')
    button_frame_exit.pack(side=RIGHT, fill=X, padx=10)  # This frame is only for the exit button

    # Load exit button image (exit.png should be in the same directory or specify the full path)
    exit_image = Image.open('exit.png').resize((50, 50))  # Make sure exit.png is in the correct location
    exit_icon = ImageTk.PhotoImage(exit_image)

    # Create an Exit button with the image
    exit_button = Button(button_frame_exit, image=exit_icon, command=roots.destroy, bd=0)
    exit_button.image = exit_icon  # Keep a reference to the image to prevent garbage collection

    # Grid the exit button in the far-right position
    exit_button.grid(row=0, column=999, padx=10, sticky='e')  # column=999 will push it to the far-right

    # Display the items in the dashboard (assuming this function works as intended)
    display_items(roots)

#   FUNCTION TO DISPLAY ITEMS IN DASHBOARD
#->CREATES AN INTERFACE TO DISPLAY ITEMS IN SHORT LISTS IF DOESNT EXIST
#->OVERWRITES NEWER DATA FROM DATABASE TO DASHBOARD

def display_items(roots):
    global text_widget  # Declare text_widget as global to access it across functions
    
    if text_widget is None or not text_widget.winfo_exists():
        # Create frame and text widget with scrollbar as before
        item_frame = Frame(roots)
        item_frame.pack(fill=BOTH, expand=True)

        text_widget = Text(item_frame, wrap=WORD, width=100, height=50)
        text_widget.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(item_frame, orient=VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        text_widget.config(yscrollcommand=scrollbar.set)
    else:
        # Clear previous content in text widget
        text_widget.delete('1.0', END)

    # Fetch user-specific data from the database
    try:
        conn = sqlite3.connect('favimarko.db')
        c = conn.cursor()
        c.execute("SELECT fav_name, fav_type, fav_description FROM favourites WHERE user_id=?", (current_user_id,))
        items = c.fetchall()

        if not items:
            text_widget.insert(END, "No items found for the current user.\n")
        else:
            # Format and display the items
            item_text = "".join(f"{i+1}. Name: {item[0]}\n   Type: {item[1]}\n   Description: {item[2]}\n\n" for i, item in enumerate(items))
            text_widget.insert(END, item_text)

        conn.close()

    except sqlite3.Error as e:
        # Handle database errors
        text_widget.insert(END, f"Error fetching data: {e}\n")
        conn.close()

    # Automatically scroll to the bottom of the text widget
    text_widget.yview(END)

#   FUNCTION TO ADD ITEMS TO DATABASE
#->CREATES A NEW WINDOW FOR ADDING ITEMS TO DATABASE
#->ASKS FOR ITEM NAME, TYPE AND DESCRIPTION
#->ADDS ITEM TO DATABASE IF ALL FIELDS ARE FILLED
#->IF ANY FIELD IS LEFT BLANK, A MESSAGE BOX APPEARS
#->UPON COMPLETION, SUCCESSFUL ADDITION MESSAGE BOX APPEARS
#->AFTER CLICKING OK ON IT, ADD WINDOW CLOSES AND DASHBOARD REDIRECTION
        
def add_item():
    global newe1, newe2, newe3, additem
    additem = Toplevel()
    additem.geometry('400x400')
    additem.iconbitmap('add.ico')
    additem.title("favimark/ADD-ITEMS")
    name_label=Label(additem,text="Mark your favourites",)
    name_label.pack(pady=10)
    newe1=Entry(additem,bd=5)
    newe1.pack()
    type_label=Label(additem,text="Type (Book/Movie/Anime/Manga/Manhua/Shows)")
    type_label.pack(pady=10)
    newe2=Entry(additem,bd=5)
    newe2.pack()
    desc_label=Label(additem,text="Review. eg:Good/Decent/Excellent")
    desc_label.pack(pady=10)
    newe3=Entry(additem,bd=5)
    newe3.pack()
    addnew=Button(additem,text=" ADD ",command=create, bg='grey', fg='white',bd=5)
    addnew.pack(pady=20)

#   SUB-FUNCTION OF ADD ITEM FUNCTIONALITY
#-> ADDS ITEMS TO THE DATABASE
#-> THIS FUNCTION PROVIDES THE SUCCESFUL COMPLETION MESSAGE BOX.

def create():
    # Ensure 'current_user_id' is set globally when the user logs in
    if not current_user_id:  # Make sure there is a logged-in user
        messagebox.showwarning("Login Error", "No user is logged in!")
        return

    # Check if any field is empty
    if not newe1.get() or not newe2.get() or not newe3.get():
        # If any field is empty, show a warning message
        messagebox.showwarning("Input Error", "Please enter values for all fields.")
        return  # Do not add the record if fields are empty

    try:
        # Connect to the database
        conn = sqlite3.connect('favimarko.db')
        c = conn.cursor()

        # Create table if it doesn't exist (already done earlier)
        c.execute('''
            CREATE TABLE IF NOT EXISTS favourites(
                user_id TEXT,
                fav_name TEXT,
                fav_type TEXT,
                fav_description TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')

        # Insert new item into the table with the logged-in user's ID
        c.execute('INSERT INTO favourites (user_id, fav_name, fav_type, fav_description) VALUES (?, ?, ?, ?)',
                  (current_user_id, newe1.get(), newe2.get(), newe3.get()))

        # Commit the transaction and close the connection
        conn.commit()

        # Success message
        messagebox.showinfo('Success', 'Item created successfully')
        
        # Close the connection
        conn.close()

        # Refresh the displayed items to show the new item
        display_items(roots)

        # Clear the input fields
        newe1.delete(0, END)
        newe2.delete(0, END)
        newe3.delete(0, END)

        # Close the add item window
        additem.destroy()

    except sqlite3.Error as e:
        # Handle any errors during database interaction
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    
#   EDIT ITEMS IN FAVIMARK
#-> THIS FUNCTION PROVIDES THE EDIT ITEM WINDOW PROMPT
#-> ASKS THE ID OF THE RECORD WHICH THE USER WANTS TO EDIT
#-> AFTER CLICKING ON PROCEED TO EDIT REDIRECTS TO ANOTHER WINDOW

def edit_prompt():
    global edit_prompt_window,edite1
    edit_prompt_window = Toplevel()
    edit_prompt_window.title('Edit Prompt')
    edit_prompt_window.geometry('350x350')
    edit_prompt_window.iconbitmap('edit.ico')
    edit_text=Label(edit_prompt_window,text="Enter the ID of the records you want to edit.")
    edit_text.pack(pady=50)
    edite1=Entry(edit_prompt_window,bd=5)
    edite1.pack()
    edit=Button(edit_prompt_window,text="PROCEED TO EDIT",command=edit_item,bg='grey', fg='white',bd=5)
    edit.pack(pady=10)

#AFTER CLICKING ON PROCEED TO EDIT, THIS FUNCTION IS CALLED
#->SIMILAR TO ADD ITEMS FUNCTION
#->DISPLAYS THE DATA OF THE ID NUMBER ENTERED BY THE USER WHICH CAN BE EDITED
#->AFTER EDITING IT, SUCCESFUL COMPLETION MESSAGEBOX APPEARS
#->AFTER WHICH THIS EDIT PROMPT APPEARS AGAIN.
  
def edit_item():
    global neweditse1, neweditse2, neweditse3, edite1, edit_prompt_window, edit_window
    
    # Ensure 'current_user_id' is set globally when the user logs in
    if not current_user_id:  # Make sure there is a logged-in user
        messagebox.showwarning("Login Error", "No user is logged in!")
        return
    
    # Check if any field is empty
    if not edite1.get():
        messagebox.showwarning("Input Error", "Please enter ID of the record you want to edit.")
        return  # Do not proceed if no ID is entered

    # Open the edit window for the user
    edit_window = Toplevel()
    edit_window.title('favimark/EDIT_ITEMS')
    edit_window.geometry('400x400')
    edit_window.iconbitmap('edit.ico')

    name_label = Label(edit_window, text="Edit your marked favourites")
    name_label.pack(pady=10)

    neweditse1 = Entry(edit_window, bd=5)
    neweditse1.pack()

    type_label = Label(edit_window, text="Edit the Type (Book/Movie/Anime/Manga/Manhua/Shows)")
    type_label.pack(pady=10)

    neweditse2 = Entry(edit_window, bd=5)
    neweditse2.pack()

    desc_label = Label(edit_window, text="Edit Review")
    desc_label.pack(pady=10)

    neweditse3 = Entry(edit_window, bd=5)
    neweditse3.pack()

    edit_add = Button(edit_window, text=" SAVE ", command=update, bg='grey', fg='white', bd=5)
    edit_add.pack(pady=20)

    # ERROR HANDLING: Check if the record belongs to the logged-in user
    try:
        conn = sqlite3.connect('favimarko.db')
        c = conn.cursor()
        oid = edite1.get()
        
        # Fetch record by OID and ensure it belongs to the logged-in user
        c.execute('SELECT * FROM favourites WHERE oid=? AND user_id=?', (oid, current_user_id))
        result = c.fetchall()
        
        if result:
            for i in result:
                neweditse1.insert(0, i[1])  # Insert fav_name
                neweditse2.insert(0, i[2])  # Insert fav_type
                neweditse3.insert(0, i[3])  # Insert fav_description
        else:
            messagebox.showerror('Error', 'Record not found or does not belong to the current user')
            edit_window.destroy()
            return
    except sqlite3.Error as e:
        messagebox.showerror('Error', e)
    finally:
        if conn:
            conn.close()
            
#   AFTER EDITS ARE MADE AND SAVE BUTTON IS PRESSED THIS FUNCTION IS CALLED
#->THIS FUNCTION USES SQL CODE TO MAKE CHANGES TO THE RESPECTIVE RECORD ACCORDINGLY
#->AFTER WHICH THE MESSAGEBOX APPEARS WITH A SUCCESSFUL MESSAGE
    
def update():
    global neweditse1, neweditse2, neweditse3, edite1
    
    # Ensure 'current_user_id' is set globally when the user logs in
    if not current_user_id:  # Make sure there is a logged-in user
        messagebox.showwarning("Login Error", "No user is logged in!")
        return
    
    # Check if any field is empty
    if not neweditse1.get() or not neweditse2.get() or not neweditse3.get():
        messagebox.showwarning("Edited Val Error", "Please do not leave edited values empty!")
        return  # Do not proceed if any field is empty
    
    try:
        conn = sqlite3.connect('favimarko.db')
        c = conn.cursor()
        
        # Update the record in the database, making sure it belongs to the logged-in user
        c.execute('''UPDATE favourites SET
                     fav_name = :a,
                     fav_type = :b,
                     fav_description = :c
                     WHERE oid = :oid AND user_id = :user_id''',
                  {
                      "a": neweditse1.get(),
                      "b": neweditse2.get(),
                      "c": neweditse3.get(),
                      "oid": edite1.get(),
                      "user_id": current_user_id
                  })
        
        conn.commit()

        # Check if any rows were updated (this confirms the item belongs to the user and was updated)
        if c.rowcount > 0:
            messagebox.showinfo('Successful Edition', 'Item edited successfully')
        else:
            messagebox.showerror('Error', 'Failed to edit item. Make sure it belongs to the current user.')

        conn.close()

        # Refresh the displayed items
        display_items(roots)

        # Clear the input fields and close the edit window
        edite1.delete(0, END)
        edit_window.destroy()
        edit_prompt_window.destroy()

    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")
    
#   DELETE RECORDS IN FAVIMARK
#->FIRST A PROMPT APPEARS SIMILAR TO EDIT PROMPT 
#->UPON ENTERING ID OF RECORD WE WANT TO DELETE
#->SUCCESSFULLY DELETED MESSAGE APPEARS
#->THEN RECORD IS DELETED, WINDOW IS CLOSED AND DASHBOARD IS OVERWRITTEN 
#->OVERWRITTEN DASHBOARD HAS THAT RECORD DELETED

def delete_prompt():
    global delete_prompt_window,dele1
    delete_prompt_window = Toplevel()
    delete_prompt_window.title('Delete Prompt')
    delete_prompt_window.geometry('350x350')
    delete_prompt_window.iconbitmap('delete.ico')
    del_text=Label(delete_prompt_window,text="Enter the ID of the records you want to delete.")
    del_text.pack(pady=50)
    dele1=Entry(delete_prompt_window,bd=5)
    dele1.pack()
    deletee=Button(delete_prompt_window,text=" DELETE ",command=delete_item, font=('Arial', 10), bg='red', fg='white',bd=5)
    deletee.pack(pady=10)
    
#DELETE_ITEM FUNCTION IS USED TO DELETE THE RECORDS FROM THE DATABASE 
#THEN DASHBOARD IS REFRESHED TO SHOW THAT THE RECORD HAS BEEN ERASED 

def delete_item():
    # Ensure 'current_user_id' is set globally when the user logs in
    if not current_user_id:  # Make sure there is a logged-in user
        messagebox.showwarning("Login Error", "No user is logged in!")
        return
    
    # Check if any field is empty
    if not dele1.get():
        messagebox.showwarning("Records Input Error", "Please enter the ID of the record you want to delete.")
        return  # Do not proceed if no ID is entered
    
    conn = sqlite3.connect('favimarko.db')
    c = conn.cursor()
    oid = dele1.get()
    
    # Ask for confirmation before deleting
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete record ID {oid}?")
    if not confirm:
        return  # If user selects "No", exit function without deleting
    
    try:
        # Check if the record belongs to the logged-in user
        c.execute('SELECT * FROM favourites WHERE oid=? AND user_id=?', (oid, current_user_id))
        result = c.fetchall()
        
        if not result:
            messagebox.showwarning("Deletion Error", f"Record ID {oid} does not belong to the current user.")
            return  # Exit if the record doesn't belong to the logged-in user
        
        # If the record belongs to the user, delete it
        c.execute('DELETE FROM favourites WHERE oid=? AND user_id=?', (oid, current_user_id))
        conn.commit()

        # Check if any row was actually deleted
        if c.rowcount == 0:
            messagebox.showwarning("Deletion Error", f"Record with ID {oid} does not exist.")
            return  # Exit if the record doesn't exist
        
        # Update OID of remaining items (adjust the IDs after deletion)
        c.execute('SELECT oid FROM favourites WHERE oid>? AND user_id=?', (oid, current_user_id))
        remaining_items = c.fetchall()
        for item in remaining_items:
            new_oid = item[0] - 1  # Decrement OID by 1 to update the record
            c.execute('UPDATE favourites SET oid=? WHERE oid=? AND user_id=?', (new_oid, item[0], current_user_id))
            conn.commit()

        messagebox.showinfo('Successful Deletion', 'Item deleted successfully')

    except sqlite3.Error as e:
        messagebox.showerror('Error', str(e))

    finally:
        conn.close()
        display_items(roots)  # Refresh the list of items after deletion
        delete_prompt_window.destroy()


#SEARCH BUTTON'S FUNCTIONALITY
#   SEARCH MARKED FAVOURITES IN FAVIMARK
#->PROMPT WINDOW APPEARS
#->TWO BUTTONS, SEARCH BY ID AND SEARCH BY TYPE
#->SEARCH BY ID HAS ONE FUNCTION TO CARRY FUNCTIONALITY
#->SEARCH BY TYPE HAS ONE FUNCTION TO CARRY FUNCTIONALITY

def search_prompt():
    global search_what
    search_what=Toplevel()
    search_what.title('Search Prompt')
    search_what.geometry('350x350')
    search_what.iconbitmap('search.ico')
    search_id_label=Label(search_what,text="Click below to search by ID")
    search_id_label.pack(pady=20)
    search_id_button=Button(search_what,text="Search by ID",command=search_by_id,bg='grey', fg='white',bd=3)
    search_id_button.pack()
    search_title_label=Label(search_what,text="Click below to search by Type")
    search_title_label.pack(pady=20)
    search_title_button=Button(search_what,text="Search by Type",command=search_by_type,bg='grey', fg='white',bd=3)
    search_title_button.pack()
   
#THIS IS THE SEARCH BY ID PROMPT WHERE USER ENTERS ID OF RECORD THEY WANT TO VIEW
#THEN REDIRECTED TO ANOTHER WINDOW
 
def search_by_id():
    global searchbyid, idsearch_entry
    searchbyid = Toplevel()
    searchbyid.iconbitmap('search.ico')
    searchbyid.title('Search by ID')
    searchbyid.geometry('400x400')
    idsearch_label = Label(searchbyid, text="Enter the ID of the record you want to search")
    idsearch_label.pack(pady=30)
    idsearch_entry = Entry(searchbyid,bd=5)
    idsearch_entry.pack()
    idsearch_button = Button(searchbyid, text="Search", command=idsearch,bg='grey', fg='white',bd=3)
    idsearch_button.pack(pady=10)
    search_what.iconify()

#THIS FUNCTION PROVIDES USER WITH ANOTHER WINDOW THAT RETRIEVES DATA FROM DATABASE
#SQL IS USED TO RETRIEVE DATA AND DISPLAY IN THE NEW WINDOW
#ONLY ONE RECORD IS SHOWN BECAUSE ONE RECORD HAS ONE ID, ID IS UNIQUE

def idsearch():
    # Ensure 'current_user_id' is set globally when the user logs in
    if not current_user_id:  # Make sure there is a logged-in user
        messagebox.showwarning("Login Error", "No user is logged in!")
        return

    # Check if ID search field is empty
    if not idsearch_entry.get():
        messagebox.showwarning("Search ID Error", "Please enter ID of the record you want to search.")
        return  # Do not search if the ID is empty

    global idsearch_window
    id = idsearch_entry.get()

    # Create a new window to display the search results
    idsearch_window = Toplevel()
    idsearch_window.title('Search Result')
    idsearch_window.geometry('700x500')
    idsearch_window.iconbitmap('search.ico')

    result_label = Label(idsearch_window, text="Search Result")
    result_label.pack(pady=10)

    result_text = Text(idsearch_window)
    result_text.pack(pady=10)

    # Button to exit
    exit_button = Button(idsearch_window, text="Exit", command=idsearch_exit, font=('Arial', 12), bg='red', fg='white', bd=3)
    exit_button.pack(pady=10)

    try:
        # Retrieve the record by ID for the current user
        conn = sqlite3.connect('favimarko.db')
        c = conn.cursor()
        c.execute('SELECT fav_name, fav_type, fav_description FROM favourites WHERE rowid=? AND user_id=?', (id, current_user_id))
        record = c.fetchone()
        conn.close()

        if record:
            item_name = record[0]         # Name field
            item_type = record[1]         # Type field
            item_description = record[2]  # Description field

            result_text.insert(INSERT, f"Name: {item_name}\n\n---Type: {item_type}\n\n---Description: {item_description}\n\n")
        else:
            result_text.insert(INSERT, "Record not found or it does not belong to the current user.")
        
        result_text.config(state=DISABLED)
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", str(e))
    
    # Iconify the search window (this line seems to be related to a global `searchbyid` window, but it can be used conditionally)
    # If `searchbyid` is a valid window, you can use this, else it can be removed if not defined.
    try:
        searchbyid.iconify()
    except NameError:
        pass  # If searchbyid is not defined, no action is taken

#   UPON CLICKING EXIT BUTTON, THIS FUNCTION CALLED
#->CLOSES THREE WINDOWS OF SEARCH

def idsearch_exit():
        idsearch_window.destroy()
        searchbyid.destroy()
        search_what.destroy()

#SEARCH BY TYPE PROMPT
#USER ENTERS THE TYPE OF ITEMS THEY WANT TO SEARCH FOR
#FOR EXAMPLE: BOOK,MOVIE,ANIME,MANGA,MANHUA
#->THEN THE TYPESEARCH FUNCTION IS CALLED
#->WHICH USES SQL TO SEARCH ALL RECORDS WITH THAT TYPE
    
def search_by_type():
    global searchbytype, typesearch_entry
    searchbytype = Toplevel()
    searchbytype.iconbitmap('search.ico')
    searchbytype.title('Search by Type')
    searchbytype.geometry('400x400')
    typesearch_label = Label(searchbytype, text="Enter the Type of the record you want to search")
    typesearch_label.pack(pady=30)
    typesearch_entry = Entry(searchbytype,bd=5)
    typesearch_entry.pack()
    typesearch_button = Button(searchbytype, text="Search", command=typesearch,bg='grey', fg='white',bd=3)
    typesearch_button.pack(pady=10)
    search_what.iconify()

#IMPLEMENTATION OF SQL TO SEARCH ALL RECORDS WITH THE GIVEN TYPE
#THEN MULTIPLE RECORDS ARE SHOWN BASED OFF OF HOW MANY RECORDS HAVE SAME TYPE
#WINDOWS HAVE TO BE MANUALLY CLOSED, OR WE CAN PRESS A BUTTON BELOW THE PAGE TO QUIT.

def typesearch():
    # Ensure 'current_user_id' is set globally when the user logs in
    if not current_user_id:  # Make sure there is a logged-in user
        messagebox.showwarning("Login Error", "No user is logged in!")
        return

    # Check if any field is empty
    if not typesearch_entry.get():
        messagebox.showwarning("Type Search Error", "Please enter the type of the record you want to search.")
        return

    global typesearch_window
    type = typesearch_entry.get()

    # Create a new window to display the search results
    typesearch_window = Toplevel()
    typesearch_window.title('Search Result')
    typesearch_window.geometry('700x500')
    typesearch_window.iconbitmap('search.ico')

    result_label = Label(typesearch_window, text="Search Result")
    result_label.pack(pady=10)
    result_text = Text(typesearch_window)
    result_text.pack(pady=10)

    # Button to exit
    exit_button = Button(typesearch_window, text="Exit", command=typesearch_exit, font=('Arial', 12), bg='red', fg='white', bd=3)
    exit_button.pack(pady=10)

    try:
        # Retrieve the records by type for the current user
        conn = sqlite3.connect('favimarko.db')
        c = conn.cursor()
        c.execute('SELECT fav_name, fav_type, fav_description FROM favourites WHERE fav_type=? AND user_id=?', (type, current_user_id))
        records = c.fetchall()
        conn.close()

        if records:
            for i, record in enumerate(records, start=1):
                item_name = record[0]         # Name field
                item_type = record[1]         # Type field
                item_description = record[2]  # Description field

                result_text.insert(INSERT, f"{i}. Name: {item_name}\n\n---Type: {item_type}\n\n---Description: {item_description}\n\n")
        else:
            result_text.insert(INSERT, "No records found for this type.")
        
        result_text.config(state=DISABLED)
    
    except sqlite3.Error as e:
        messagebox.showerror("Error", str(e))
    
    # Iconify the search window
    try:
        searchbytype.iconify()
    except NameError:
        pass  # If searchbytype is not defined, no action is taken

#UPON CLICKING EXIT BUTTON, THIS FUNCTION CALLED
#->CLOSES THREE WINDOWS OF SEARCH
  
def typesearch_exit():
    searchbytype.destroy()
    search_what.destroy()
    typesearch_window.destroy()
    
def logout():
    global current_user_id
    current_user_id = None  # Reset current user
    dashboard.destroy()  # Close the dashboard window
    print("User logged out successfully.")
    
mainloop()