#(single line #) ->separation of correlated functionalities
##(double line #) ->separation of different functionalities

from tkinter import*
from tkinter import messagebox #Displaying error, success messages
import sqlite3 #database
from PIL import Image, ImageTk #images, for UI
import uuid #generating random user ids for newer users in favimark app

text_widget=None #initializing dashboard window to none 
current_user_id=None #logged in user id reset everytime, so no clashing happens between user ids

###################################################################################################################################################
###################################################################################################################################################

# toggle show and hide password (buttons are images)

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

###################################################################################################################################################
###################################################################################################################################################

# Toggling functionality for switching between Register and sign in

def toggle_mode():
    global is_login
    is_login = not is_login
    title_label.config(text="LOG IN / SIGN IN" if is_login else "SIGN UP / REGISTER")
    login_button.config(text="Login" if is_login else "Sign Up", command=login if is_login else register)
    toggle_button.config(text="New to favimark? Register ..." if is_login else "Already Registered? Sign In ...")
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    confirm_password_entry.delete(0,END)
    
    # Show/hide confirm password field dynamically
    if is_login:
        confirm_password_label.grid_remove()
        confirm_password_frame.grid_remove()
        frame.place(relwidth=0.6, relheight=0.7)   # Resize frame for login
        login_button.config(text="Login", image=LoginImage, compound='left', command=login)

        
    else:
        confirm_password_label.grid()
        confirm_password_frame.grid()
        frame.place(relwidth=0.6, relheight=0.8)  # Resize frame for signup
        login_button.config(text="Sign Up", image=SignUpImage, compound='left', command=register)
        
    # Update the frame's background image after resizing
    update_frame_bg()

###################################################################################################################################################
###################################################################################################################################################

#Login Functionality for favimark

def login():
    global current_user_id
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect("favimark.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT user_id FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            current_user_id = user[0]
            root.iconify()
            dashboard()
        else:
            response = messagebox.askyesno("User Not Found", "Username does not exist. Do you want to sign up?")
            if response:  # If "Yes" is clicked
                toggle_mode()  # Switch to the signup screen

    except sqlite3.OperationalError as e:
            response = messagebox.askyesno("User Not Found", "User does not exist. Do you want to sign up?")
            if response:  # If "Yes" is clicked
                toggle_mode()  # Switch to the signup screen
    finally:
        conn.close()

###################################################################################################################################################
###################################################################################################################################################

#Register/Signup functionality for favimark

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
        conn = sqlite3.connect("favimark.db")
        cursor = conn.cursor()

        # Create the users and favourites tables if they don't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            user_id TEXT PRIMARY KEY, 
                            username TEXT UNIQUE, 
                            password TEXT)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS favourites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT, 
                    user_record_id INTEGER,  -- Unique record ID per user
                    fav_name TEXT, 
                    fav_type TEXT, 
                    fav_description TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id))''')

        # Insert user data into the users table
        cursor.execute("INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)", 
                       (user_id, username, password))

        conn.commit()

        messagebox.showinfo("Success", "Registration Successful! Please log in.")
        toggle_mode()  

    except sqlite3.IntegrityError:
        # Catch integrity errors like duplicate usernames
        messagebox.showerror("Error", "Username already exists")
    except sqlite3.Error as e:
        # Catch any other database-related errors
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        # Ensure connection is closed
        conn.close()

###################################################################################################################################################
###################################################################################################################################################

# Creation of root/main window running on mainloop() till the end

root = Tk()
root.title("favimark | Login")
root.geometry('700x700')
root.iconbitmap('login.ico')#icon
root.resizable(False, False)

# Open and resize the background image to match the window dimensions
bg_image = Image.open("bookbackground_grass.png") #using image modules
bg_image = bg_image.resize((700, 700), Image.Resampling.LANCZOS)
login_Image = ImageTk.PhotoImage(bg_image)

# Create and place the Label to cover the entire window
login_background = Label(root, image=login_Image)
login_background.place(x=0, y=0, relwidth=1, relheight=1)

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

frame_width = int(0.6 * 700)
frame_height = int(0.7 * 700)

login_bg = Image.open("blue background.png") 
login_bg = login_bg.resize((frame_width, frame_height), Image.Resampling.LANCZOS)
login_bg_photo = ImageTk.PhotoImage(login_bg)

bg_label = Label(frame, image=login_bg_photo)
bg_label.image = login_bg_photo 
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

frame.grid_columnconfigure(0, weight=1)

def update_frame_bg():
    
    frame.update_idletasks()
    
    frame_width = frame.winfo_width()
    frame_height = frame.winfo_height()
    
    new_bg = Image.open("blue background.png") 
     
    new_bg = new_bg.resize((frame_width, frame_height), Image.Resampling.LANCZOS)
    new_bg_photo = ImageTk.PhotoImage(new_bg)
    bg_label.config(image=new_bg_photo)
    bg_label.image = new_bg_photo  

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
LoginImage = PhotoImage(file = "login image-50.png")
SignUpImage = PhotoImage(file = "signup image.png")
is_login = True
login_button = Button(frame, text="LOGIN", command=login, font=('Arial', 12), bg='grey', fg='white', bd=3, image = LoginImage, compound = 'left' )
login_button.grid(row=8, column=0, columnspan=2, padx=40, pady=15, ipadx=15, ipady=5, sticky="ew")

# Toggle Button
toggle_button = Button(frame, text="New to favimark? Register ...", command=toggle_mode, font=('Arial', 10), fg='blue', bg='white', bd=3)
toggle_button.grid(row=9, column=0, columnspan=2, pady=10)

###################################################################################################################################################

#   FUNCTION TO DISPLAY DASHBOARD OF FAVIMARK
#->CONTAINS 4 BUTTONS AND ONE INTERFACE BELOW IT
#->MADE FULL SCREEN FOR BETTER UI
#->ROOTS IS USED AS THE WINDOW HERE.
       
def dashboard():
    global roots  # Giving roots window a global scope to access it from other windows
    roots = Toplevel(root)
    roots.state('zoomed')
    roots.title("favimark/Dashboard")
    
    # Load and set the dashboard background image
    dashboard_bg = Image.open("dashboard.png")  # Replace with your background file name
    width = roots.winfo_screenwidth()
    height = roots.winfo_screenheight()
    dashboard_bg = dashboard_bg.resize((width, height), Image.Resampling.LANCZOS)
    dashboard_bg_photo = ImageTk.PhotoImage(dashboard_bg)
    
    # Create a Label to hold the background image and place it so that it covers the entire dashboard
    bg_label_dashboard = Label(roots, image=dashboard_bg_photo)
    bg_label_dashboard.image = dashboard_bg_photo  # Keep a reference to avoid garbage collection
    bg_label_dashboard.place(x=0, y=0, relwidth=1, relheight=1)

    # Align everything at the top of the page
    top_frame = Frame(roots, bg='#f0f0f0')
    top_frame.pack(side=TOP, fill=BOTH, padx=1, pady=10, expand=True)

    # UI for buttons which aligns CRUD buttons at the top of the page using top_frame
    button_frame_crud = Frame(top_frame, bg='#f0f0f0')
    button_frame_crud.pack(side=LEFT, fill=X)  # Use fill=X to stretch horizontally
    AddImage = PhotoImage(file = "addImage.png")
    EditImage = PhotoImage(file = "editImage.png")
    SearchImage = PhotoImage(file = "searchImage.png")   
    DeleteImage = PhotoImage(file = "deleteImage.png")
    
    # Use grid layout for buttons and align them to the left side
    add_button = Button(button_frame_crud, text="ADD", command=add_item, font=('Arial', 12), bg='#f0f0f0', fg='black', bd=3, image = AddImage, compound = 'left' )
    add_button.grid(row=0, column=0, padx=10, sticky='w')  # Align left
    add_button.image = AddImage  # Keep a persistent reference

    edit_button = Button(button_frame_crud, text="EDIT", command=edit_prompt, font=('Arial', 12), bg='#f0f0f0', fg='black', bd=3, image = EditImage, compound = 'left' )
    edit_button.grid(row=0, column=1, padx=10, sticky='w')  # Align left
    edit_button.image = EditImage  # Keep a persistent reference

    search_button = Button(button_frame_crud, text=" SEARCH ", command=search_prompt, font=('Arial', 12), bg='#f0f0f0', fg='black', bd=3, image = SearchImage, compound = 'left' )
    search_button.grid(row=0, column=2, padx=10, sticky='w')  # Align left
    search_button.image = SearchImage  # Keep a persistent reference

    delete_button = Button(button_frame_crud, text="DELETE", command=delete_prompt, font=('Arial', 12), bg='#f0f0f0', fg='black', bd=3, image = DeleteImage, compound = 'left' )
    delete_button.grid(row=0, column=3, padx=10, sticky='w')  # Align left
    delete_button.image = DeleteImage  # Keep a persistent reference

    # UI for exit button
    button_frame_exit = Frame(top_frame, bg='#f0f0f0')
    button_frame_exit.pack(side=RIGHT, fill=X, padx=10)  # This frame is only for the exit button

    # Load exit button image (exit.png should be in the same directory or specify the full path)
    exit_image = Image.open('exitImage.png').resize((50, 50))  # Make sure exit.png is in the correct location
    ExitImage = ImageTk.PhotoImage(exit_image)

    # Create an Exit button with the image
    exit_button = Button(button_frame_exit, text = 'EXIT', font=('Arial', 12, 'bold'), image=ExitImage, compound = 'left', command=logout, bd=3)
    exit_button.image = ExitImage  # Keep a reference to the image to prevent garbage collection

    # Grid the exit button in the far-right position
    exit_button.grid(row=0, column=999, padx=10, sticky='e')  # column=999 will push it to the far-right
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    # Display the items in the dashboard (assuming this function works as intended)
    display_items(roots)

###################################################################################################################################################
###################################################################################################################################################

#   FUNCTION TO DISPLAY ITEMS IN DASHBOARD
#->CREATES AN INTERFACE TO DISPLAY ITEMS IN SHORT LISTS IF DOESNT EXIST
#->OVERWRITES NEWER DATA FROM DATABASE TO DASHBOARD

def display_items(roots):
    global text_widget  # Declare text_widget as global to access it across functions
    
    if text_widget is None or not text_widget.winfo_exists():
        # Create frame and text widget with scrollbar as before
        item_frame = Frame(roots)
        item_frame.pack(fill=BOTH, expand=True)
        
        review_bg = Image.open("review_bg.png") 
        review_bg = review_bg.resize((700, 500), Image.Resampling.LANCZOS)
        review_bg_photo = ImageTk.PhotoImage(review_bg)
        
        bg_label_review = Label(item_frame, image=review_bg_photo)
        bg_label_review.image = review_bg_photo 
        bg_label_review.place(x=0, y=0, relwidth=1, relheight=1)

        text_widget = Text(item_frame, wrap=WORD, width=100, height=50, bg = '#f0f0f0')
        text_widget.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(item_frame, orient=VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        text_widget.config(yscrollcommand=scrollbar.set)
    else:
        text_widget.delete('1.0', END)

    #user-specific data from database
    try:
        conn = sqlite3.connect('favimark.db')
        c = conn.cursor()
        c.execute("SELECT user_record_id, fav_name, fav_type, fav_description FROM favourites WHERE user_id=?", (current_user_id,))
        items = c.fetchall()

        if not items:
            text_widget.insert(END, "No items found for the current user.\n")
        else:
            # Format and display the items
            item_text = "".join(f"{item[0]}. Name: {item[1]}\n   Type: {item[2]}\n   Description: {item[3]}\n\n" for i, item in enumerate(items))
            text_widget.insert(END, item_text)

        conn.close()

    except sqlite3.Error as e:
        # Handle database errors
        text_widget.insert(END, f"Error fetching data: {e}\n")
        conn.close()

    # Automatically scroll to the bottom of the text widget
    text_widget.yview(END)

###################################################################################################################################################
###################################################################################################################################################

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
    
    bg = Image.open("add background.png")  # Replace with your background image file
    bg = bg.resize((400, 400), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg)
    
    # Create a Label for the background image and place it to fill the window
    bg_label = Label(additem, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    
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

###################################################################################################################################################

#   SUB-FUNCTION OF ADD ITEM FUNCTIONALITY
#-> ADDS ITEMS TO THE DATABASE
#-> THIS FUNCTION PROVIDES THE SUCCESFUL COMPLETION MESSAGE BOX.

def create():

    # Check if any field is empty
    if not newe1.get() or not newe2.get() or not newe3.get():
        # If any field is empty, show a warning message
        messagebox.showwarning("Input Error", "Please enter values for all fields.")
        return  # Do not add the record if fields are empty

    try:
        # Connect to the database
        conn = sqlite3.connect('favimark.db')
        c = conn.cursor()

        # Create table if it doesn't exist (already done earlier)
        c.execute('''
            CREATE TABLE IF NOT EXISTS favourites(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                fav_name TEXT,
                fav_type TEXT,
                fav_description TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')

        # Get the next record number for the user
        c.execute("SELECT COALESCE(MAX(user_record_id), 0) + 1 FROM favourites WHERE user_id=?", (current_user_id,))
        next_record_id = c.fetchone()[0]

        # Insert new record with the user-specific record ID
        c.execute('INSERT INTO favourites (user_id, user_record_id, fav_name, fav_type, fav_description) VALUES (?, ?, ?, ?, ?)',
                (current_user_id, next_record_id, newe1.get(), newe2.get(), newe3.get()))


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
 
 ###################################################################################################################################################
 ###################################################################################################################################################
    
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
    
    bg = Image.open("edit background.png")  # Use the same background image file
    bg = bg.resize((350, 350), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg)
    bg_label = Label(edit_prompt_window, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()  # Ensure it's in the back
    
    edit_text=Label(edit_prompt_window,text="Enter the ID of the records you want to edit.")
    edit_text.pack(pady=50)
    edite1=Entry(edit_prompt_window,bd=5)
    edite1.pack()
    edit=Button(edit_prompt_window,text="PROCEED TO EDIT",command=edit_item,bg='grey', fg='white',bd=5)
    edit.pack(pady=10)

###################################################################################################################################################

#AFTER CLICKING ON PROCEED TO EDIT, THIS FUNCTION IS CALLED
#->SIMILAR TO ADD ITEMS FUNCTION
#->DISPLAYS THE DATA OF THE ID NUMBER ENTERED BY THE USER WHICH CAN BE EDITED
#->AFTER EDITING IT, SUCCESFUL COMPLETION MESSAGEBOX APPEARS
#->AFTER WHICH THIS EDIT PROMPT APPEARS AGAIN.
  
def edit_item():
    global neweditse1, neweditse2, neweditse3, edite1, edit_prompt_window, edit_window
    
    # Check if any field is empty
    if not edite1.get():
        messagebox.showwarning("Input Error", "Please enter ID of the record you want to edit.")
        return  # Do not proceed if no ID is entered

    # Open the edit window for the user
    edit_window = Toplevel()
    edit_window.title('favimark/EDIT_ITEMS')
    edit_window.geometry('400x400')
    edit_window.iconbitmap('edit.ico')
    
    bg = Image.open("edit background.png")  # Replace with your background image file for editing
    bg = bg.resize((400, 400), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg)
    bg_label = Label(edit_window, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


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
        conn = sqlite3.connect('favimark.db')
        c = conn.cursor()
        oid = edite1.get()
        
        print(f"Editing record ID: {oid} for user_id: {current_user_id}") #debugging purposes  # Debugging Output
        c.execute('SELECT * FROM favourites WHERE user_record_id=? AND user_id=?', (oid, current_user_id))
        result = c.fetchall()
        print(f"Record fetched: {result}")  # Debugging purposes
        
        if result:
            for i in result:
                neweditse1.insert(0, i[3])  # Insert fav_name
                neweditse2.insert(0, i[4])  # Insert fav_type
                neweditse3.insert(0, i[5])  # Insert fav_description
        else:
            messagebox.showerror('Error', 'Record not found or does not belong to the current user')
            edit_window.destroy()
            return
    except sqlite3.Error as e:
        messagebox.showerror('Error', e)
    finally:
        if conn:
            conn.close()
     
###################################################################################################################################################     
            
#   AFTER EDITS ARE MADE AND SAVE BUTTON IS PRESSED THIS FUNCTION IS CALLED
#->THIS FUNCTION USES SQL CODE TO MAKE CHANGES TO THE RESPECTIVE RECORD ACCORDINGLY
#->AFTER WHICH THE MESSAGEBOX APPEARS WITH A SUCCESSFUL MESSAGE
    
def update():
    global neweditse1, neweditse2, neweditse3, edite1
    
    # Check if any field is empty
    if not neweditse1.get() or not neweditse2.get() or not neweditse3.get():
        messagebox.showwarning("Edited Val Error", "Please do not leave edited values empty!")
        return  # Do not proceed if any field is empty
    
    try:
        conn = sqlite3.connect('favimark.db')
        c = conn.cursor()
            
            # Ensure a valid record ID is entered
        if not edite1.get():
                messagebox.showwarning("Edit Error", "No record ID entered!")
                return  

            # Ensure all fields are filled before updating - error handling
        if not neweditse1.get() or not neweditse2.get() or not neweditse3.get():
                messagebox.showwarning("Edit Error", "Please do not leave fields empty!")
                return  

        try:
            conn = sqlite3.connect('favimark.db')
            c = conn.cursor()
            
            # Convert ID to an integer (ensuring it's valid)
            record_id = int(edite1.get().strip())

            # Perform update only if the record exists
            c.execute('''UPDATE favourites SET
                        fav_name = ?,
                        fav_type = ?,
                        fav_description = ?
                        WHERE user_record_id = ? AND user_id = ?''',
                    (neweditse1.get(), neweditse2.get(), neweditse3.get(), record_id, current_user_id))
            
            conn.commit()

            if c.rowcount > 0:  # Check if any row was actually updated
                messagebox.showinfo('Success', 'Item updated successfully!')
            else:
                messagebox.showerror('Error', 'No matching record found!')

            conn.close()

            # Refresh the displayed items
            display_items(roots)

            # Close edit window
            edit_window.destroy()
            edit_prompt_window.destroy()

        except ValueError:
            messagebox.showerror('Input Error', 'Record ID must be a number!')
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")

###################################################################################################################################################
###################################################################################################################################################
    
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
    
    bg = Image.open("delete background.png")  # Replace with your background image file
    bg = bg.resize((350, 350), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg)
    bg_label = Label(delete_prompt_window, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to prevent garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()  # Ensure the image is at the back of all other widgets
    
    del_text=Label(delete_prompt_window,text="Enter the ID of the records you want to delete.")
    del_text.pack(pady=50)
    dele1=Entry(delete_prompt_window,bd=5)
    dele1.pack()
    deletee=Button(delete_prompt_window,text=" DELETE ",command=delete_item, font=('Arial', 10), bg='red', fg='white',bd=5)
    deletee.pack(pady=10)
    
###################################################################################################################################################    
    
#DELETE_ITEM FUNCTION IS USED TO DELETE THE RECORDS FROM THE DATABASE 
#THEN DASHBOARD IS REFRESHED TO SHOW THAT THE RECORD HAS BEEN ERASED 

def delete_item():
    global current_user_id  # Ensure 'current_user_id' is set globally when the user logs in
    
    # Check if any field is empty
    if not dele1.get():
        messagebox.showwarning("Records Input Error", "Please enter the ID of the record you want to delete.")
        return  
    
    conn = sqlite3.connect('favimark.db')
    c = conn.cursor()
    oid = dele1.get()
    
    # Ask for confirmation before deleting
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete record ID {oid}?")
    if not confirm:
        return  
    
    try:
        # Step 1: Check if the record belongs to the logged-in user
        c.execute('SELECT id FROM favourites WHERE user_record_id=? AND user_id=?', (oid, current_user_id))
        record = c.fetchone()

        if not record:
            messagebox.showwarning("Deletion Error", f"Record ID {oid} does not belong to the current user.")
            return  
        
        print(f"Deleting {oid} for user {current_user_id}")  # Debugging

        # Step 2: Delete the record
        c.execute('DELETE FROM favourites WHERE user_record_id=? AND user_id=?', (oid, current_user_id))
        conn.commit()

        # Step 3: Fetch and renumber remaining records for the user
        c.execute("SELECT id FROM favourites WHERE user_id = ? ORDER BY user_record_id", (current_user_id,))
        userrecordidrecords = c.fetchall()

        # Step 4.1: Update user_record_id sequentially
        for index, (record_id,) in enumerate(userrecordidrecords, start=1):
            c.execute("UPDATE favourites SET user_record_id = ? WHERE id = ?", (index, record_id))

        conn.commit()
        
        c.execute("SELECT id FROM favourites ORDER BY id")
        idrecords = c.fetchall()
        
        # Step 4.2: Renumber the `id` values sequentially
        for index, (old_id,) in enumerate(idrecords, start=1):
            c.execute("UPDATE favourites SET id = ? WHERE id = ?", (index, old_id))

        conn.commit()

        messagebox.showinfo('Successful Deletion', 'Item deleted successfully')

    except sqlite3.Error as e:
        messagebox.showerror('Error', str(e))

    finally:
        conn.close()
        display_items(roots)  # Refresh the list of items after deletion
        delete_prompt_window.destroy()

###################################################################################################################################################
###################################################################################################################################################

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
    
    bg = Image.open("search background.png")  # Replace with your background image file
    bg = bg.resize((350, 350), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg)
    bg_label = Label(search_what, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()  # Send the background to the back

    search_id_label=Label(search_what,text="Click below to search by ID")
    search_id_label.pack(pady=20)
    search_id_button=Button(search_what,text="Search by ID",command=search_by_id,bg='grey', fg='white',bd=3)
    search_id_button.pack()
    search_title_label=Label(search_what,text="Click below to search by Type")
    search_title_label.pack(pady=20)
    search_title_button=Button(search_what,text="Search by Type",command=search_by_type,bg='grey', fg='white',bd=3)
    search_title_button.pack()
   
###################################################################################################################################################   
   
#THIS IS THE SEARCH BY ID PROMPT WHERE USER ENTERS ID OF RECORD THEY WANT TO VIEW
#THEN REDIRECTED TO ANOTHER WINDOW
 
def search_by_id():
    global searchbyid, idsearch_entry
    searchbyid = Toplevel()
    searchbyid.iconbitmap('search.ico')
    searchbyid.title('Search by ID')
    searchbyid.geometry('400x400')
    
    bg = Image.open("search background.png")  # Use the same or different background image
    bg = bg.resize((400, 400), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg)
    bg_label = Label(searchbyid, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()
    
    idsearch_label = Label(searchbyid, text="Enter the ID of the record you want to search")
    idsearch_label.pack(pady=30)
    idsearch_entry = Entry(searchbyid,bd=5)
    idsearch_entry.pack()
    idsearch_button = Button(searchbyid, text="Search", command=idsearch,bg='grey', fg='white',bd=3)
    idsearch_button.pack(pady=10)
    search_what.iconify()

###################################################################################################################################################

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
        conn = sqlite3.connect('favimark.db')
        c = conn.cursor()
        c.execute('SELECT fav_name, fav_type, fav_description FROM favourites WHERE user_record_id=? AND user_id=?', (id, current_user_id))
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
    try:
        searchbyid.iconify()
    except NameError:
        pass 

###################################################################################################################################################

#   UPON CLICKING EXIT BUTTON, THIS FUNCTION CALLED
#->CLOSES THREE WINDOWS OF SEARCH

def idsearch_exit():
        idsearch_window.destroy()
        searchbyid.destroy()
        search_what.destroy()
        
###################################################################################################################################################        

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
    
    bg = Image.open("search background.png")  # Use the same or a different background image
    bg = bg.resize((400, 400), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg)
    bg_label = Label(searchbytype, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()
    
    typesearch_label = Label(searchbytype, text="Enter the Type of the record you want to search")
    typesearch_label.pack(pady=30)
    typesearch_entry = Entry(searchbytype,bd=5)
    typesearch_entry.pack()
    typesearch_button = Button(searchbytype, text="Search", command=typesearch,bg='grey', fg='white',bd=3)
    typesearch_button.pack(pady=10)
    search_what.iconify()

###################################################################################################################################################

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
    
    bg = Image.open("search background.png")  # Replace with your image file
    bg = bg.resize((700, 500), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg)
    bg_label = Label(typesearch_window, image=bg_photo)
    bg_label.image = bg_photo  # Keep reference
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()  # Send to back so other widgets appear on top  

    result_label = Label(typesearch_window, text="Search Result")
    result_label.pack(pady=10)
    result_text = Text(typesearch_window)
    result_text.pack(pady=10)

    # Button to exit
    exit_button = Button(typesearch_window, text="Exit", command=typesearch_exit, font=('Arial', 12), bg='red', fg='white', bd=3)
    exit_button.pack(pady=10)

    try:
        # Retrieve the records by type for the current user
        conn = sqlite3.connect('favimark.db')
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
    
    try:
        searchbytype.iconify()
    except NameError:
        pass  

###################################################################################################################################################

#UPON CLICKING EXIT BUTTON, THIS FUNCTION CALLED
#->CLOSES THREE WINDOWS OF SEARCH
  
def typesearch_exit():
    searchbytype.destroy()
    search_what.destroy()
    typesearch_window.destroy()

###################################################################################################################################################
    
def logout(): #imp
    global current_user_id
    exit=messagebox.askyesno('Logout_prompt','Do you want to logout?')
    if exit:
        current_user_id = None  # Reset current user
        roots.destroy()  # Close the dashboard window
        root.deiconify()
    
mainloop()