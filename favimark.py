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
title_label = Label(frame, text="LOG IN/SIGN IN", font=('Arial', 18,'bold','italic'), bg='white')
title_label.pack(pady=60)

#username entry for authentication
username_label = Label(frame, text="Username", font=('Arial', 12,'bold'), bg='white')
username_label.pack()
username_entry = Entry(frame, font=('Arial', 12),bd=5) #bd : border size for text box
username_entry.pack()

#password entry for authentication
password_label = Label(frame, text="Password", font=('Arial', 12,'bold'), bg='white')
password_label.pack()
password_entry = Entry(frame, show='*', font=('Arial', 12),bd=5) #bd: border size for text box
password_entry.pack()

#show password checkbox that calls 'showpassword' function
show_password_var = IntVar()
show_password_checkbox = Checkbutton(frame, text="show", variable=show_password_var, command=lambda: show_password(password_entry, show_password_var),)
#lambda function used to pass parameters for show function
show_password_checkbox.pack(pady=5)

def login(): #this contains a separate window after user authentication
    if username_entry.get() == 'favimarko' and password_entry.get() == 'qwerty':
        root.iconify() #minimize root window
        dashboard() #dashboard opens a new windw if user authenticated 
        username_entry.delete(0,END)
        password_entry.delete(0,END)
    else:
        messagebox.showerror('Warning', 'Invalid username or password')

#   FUNCTION TO DISPLAY DASHBOARD OF FAVIMARK
#->CONTAINS 4 BUTTONS AND ONE INTERFACE BELOW IT
#->MADE FULL SCREEN FOR BETTER UI
#->ROOTS IS USED AS THE WINDOW HERE.
       
def dashboard():
        global roots #giving roots window a global scope to access it from other windows
        roots = Toplevel(root)
        roots.state('zoomed') # this will make it fullscreen
        roots.title("favimark/Dashboard")

        # aligns everything at the top of the page
        top_frame = Frame(roots, bg='white')
        top_frame.pack(side=TOP, fill=BOTH, padx=1, pady=10,expand=TRUE)

        # UI for buttons which aligns buttons at top of page using top_frame
        button_frame = Frame(top_frame, bg='white')
        button_frame.pack(side=LEFT)

        # Buttons-> add,edit,search,delete
        add_button = Button(button_frame, text="ADD", command=add_item, font=('Arial', 12), bg='grey', fg='white',bd=3)
        add_button.pack(side=LEFT, padx=10)

        edit_button = Button(button_frame, text="EDIT", command=edit_prompt, font=('Arial', 12), bg='grey', fg='white',bd=3)
        edit_button.pack(side=LEFT, padx=10)
        
        search_button = Button(button_frame, text=" SEARCH ", command=search_prompt, font=('Arial', 12), bg='grey', fg='white',bd=3)
        search_button.pack(side=LEFT, padx=10)

        delete_button = Button(button_frame, text="DELETE", command=delete_prompt, font=('Arial', 12), bg='grey', fg='white',bd=3)
        delete_button.pack(side=LEFT, padx=10)
        
        display_items(roots)

#   FUNCTION TO DISPLAY ITEMS IN DASHBOARD
#->CREATES AN INTERFACE TO DISPLAY ITEMS IN SHORT LISTS IF DOESNT EXIST
#->OVERWRITES NEWER DATA FROM DATABASE TO DASHBOARD

def display_items(roots):
    if 'text_widget' not in globals():
        #globals returns all variables with global scope
        item_frame = Frame(roots)
        item_frame.pack(fill=BOTH, expand=True)
        text_widget = Text(item_frame, width=100, height=50)
        text_widget.pack(fill=BOTH, expand=True)
        #if text widget does not exist
        #i.e there are no records to display
        #text widget is created as an interface
        #to display the records from the database
    else:
        text_widget.delete('1.0', END)
        #if text_widget exists, overwritten by this code

    conn = sqlite3.connect('favimark.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM favourites")#fetches data using rowid ->oid
    #in summary, all rows are fetched using fetchall
    items = c.fetchall()
    conn.close()

    for i, item in enumerate(items, start=1):#list starts from 1.
        #with enumerate, loop over iterable items
        #with automatic indexing along with it.
        #for loop unpacks tuples returned by enumerate
        item_id = item[3]
        item_name = item[0]
        item_type = item[1]
        item_description = item[2]

        text_widget.insert(END, f"{i}. Name: {item_name}\n\n---Type: {item_type}\n\n---Description: {item_description}\n\n")
        #no need to use config since overwriting and creating if not created automatically happens
        
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
    global neweditse1,neweditse2,neweditse3,edite1,edit_prompt_window,edit_window
    edit_window=Toplevel()
    edit_window.title('favimark/EDIT_ITEMS')
    edit_window.geometry('400x400')
    edit_window.iconbitmap('edit.ico')
    name_label=Label(edit_window,text="Edit your marked favourites",)
    name_label.pack(pady=10)
    neweditse1=Entry(edit_window,bd=5)
    neweditse1.pack()
    type_label=Label(edit_window,text="Edit the Type (Book/Movie/Anime/Manga/Manhua/Shows)")
    type_label.pack(pady=10)
    neweditse2=Entry(edit_window,bd=5)
    neweditse2.pack()
    desc_label=Label(edit_window,text="Edit Review")
    desc_label.pack(pady=10)
    neweditse3=Entry(edit_window,bd=5)
    neweditse3.pack()
    edit_add=Button(edit_window,text=" SAVE ",command=update, bg='grey', fg='white',bd=5)
    edit_add.pack(pady=20)
    #ERROR HANDLING OPTIMIZATION IN CASE RECORD IS NOT FOUND
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
            
#   AFTER EDITS ARE MADE AND SAVE BUTTON IS PRESSED THIS FUNCTION IS CALLED
#->THIS FUNCTION USES SQL CODE TO MAKE CHANGES TO THE RESPECTIVE RECORD ACCORDINGLY
#->AFTER WHICH THE MESSAGEBOX APPEARS WITH A SUCCESSFUL MESSAGE
    
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
    global idsearch_window
    id = idsearch_entry.get()
    # Create a new window to display the search results
    idsearch_window = Toplevel()
    idsearch_window.title('Search Result')
    idsearch_window.geometry('700x500')
    idsearch_window.iconbitmap('search.ico')
    
    # Display the search results
    result_label = Label(idsearch_window, text="Search Result")
    result_label.pack(pady=10)
    result_text = Text(idsearch_window)
    result_text.pack(pady=10)
    
    # BUTTON TO EXIT
    exit_button = Button(idsearch_window, text="Exit", command=idsearch_exit, font=('Arial', 12), bg='red',fg='white',bd=3)
    exit_button.pack()
    
    # Retrieve the record details from the database
    conn = sqlite3.connect('favimark.db')
    c = conn.cursor()
    c.execute('SELECT * FROM favourites WHERE rowid=?', (id,))
    record = c.fetchone()
    conn.close()
    
    # Display the record details
    if record:
        item_name = record[0]
        item_type = record[1]
        item_description = record[2]
        
        result_text.insert(INSERT, f"Name: {item_name}\n\n---Type: {item_type}\n\n---Description: {item_description}\n\n")
    else:
        result_text.insert(INSERT, "Record not found")
    
    result_text.config(state=DISABLED)
    
    # Iconify the search window
    searchbyid.iconify()

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
    global typesearch_window
    type = typesearch_entry.get()
    # Create a new window to display the search results
    typesearch_window = Toplevel()
    typesearch_window.title('Search Result')
    typesearch_window.geometry('700x500')
    typesearch_window.iconbitmap('search.ico')
    
    # Display the search results
    result_label = Label(typesearch_window, text="Search Result")
    result_label.pack()
    result_text = Text(typesearch_window)
    result_text.pack()
    
    # BUTTON TO EXIT
    exit_button = Button(typesearch_window, text="Exit", command=typesearch_exit, font=('Arial', 12), bg='red',fg='white',bd=3)
    exit_button.pack(pady=10)
    
    # Retrieve the record details from the database
    conn = sqlite3.connect('favimark.db')
    c = conn.cursor()
    c.execute('SELECT * FROM favourites WHERE fav_type=?', (type,))
    records = c.fetchall()
    conn.close()
    
    # Display the record details
    if records:
        for i, record in enumerate(records, start=1):
            item_name = record[0]
            item_type = record[1]
            item_description = record[2]
            
            result_text.insert(INSERT, f"{i}. Name: {item_name}\n\n---Type: {item_type}\n\n---Description: {item_description}\n\n")
    else:
        result_text.insert(INSERT, "Record not found")
    
    result_text.config(state=DISABLED)
    
    # Iconify the search window
    searchbytype.iconify()

#UPON CLICKING EXIT BUTTON, THIS FUNCTION CALLED
#->CLOSES THREE WINDOWS OF SEARCH
  
def typesearch_exit():
    searchbytype.destroy()
    search_what.destroy()
    typesearch_window.destroy()
    
#   SHOW PASSWORD FUNCTIONALITY
#->LOGIN PAGE-> SHOW PASSWORD BHANNE CHECKBOX CHA
#->UPON CLICKING THAT TWO VALUES ARE PASSED AS PARAMETERS HERE
#->ONE IS THE VALUE ENTERED WHICH IS THE PASSWORD,
#->ANOTHER IS THE VALUE 0F THE CHECKBOX
#->IF CHECKBOX KO VALUE IS TRUE THEN NON ENCRYPTED FORM IS DISPLAYED.

def show_password(entry, var):
#var is the value received from checkbox that says "show"
#if var is True, then show the password
#if var is False, then hide the password

    if var.get() == 1:
        entry.config(show='')
    else:
        entry.config(show='*')
        
#login button when pressed redirects user to the new window which is favimark ko dashboard
login_button = Button(frame, text="Login", command=login, font=('Arial', 12), bg='grey', fg='white',bd=3)
login_button.pack(pady=20)
#login button placed at last cuz login function was not declared mathi

mainloop() #root window keeps running in the background