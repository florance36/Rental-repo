import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3


# --- Database Setup ---
def setup_database():
    conn = sqlite3.connect("rental_books.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rentals (
        id INTEGER,  -- Make it just an integer without AUTOINCREMENT
        book_title TEXT,
        renter_name TEXT,
        category TEXT,
        rental_date TEXT,
        cost REAL,
        PRIMARY KEY (id)  -- id is the primary key, but won't auto-increment
    )
    """)
    conn.commit()
    return conn, cursor


def open_book_title_popup():
    # Create a new pop-up window
    popup_window = tk.Toplevel(main_window)
    popup_window.title("Choose a Book Title")
    popup_window.geometry("400x300")

    # Set the background color for the pop-up window
    popup_window.config(bg="#D2B48C")  # Light brown background (#D2B48C)

    # List of predefined book titles
    book_titles = [
        "A Court of Thorns and Roses - Sarah J. Maas", "A Little Life - Hanya Yanagihara",
        "After - Anna Todd", "After We Collided - Anna Todd", "After Ever Happy - Anna Todd",
        "After We Fell - Anna Todd", "All Your Perfects - Colleen Hoover", "American Dirt - Jeanine Cummins",
        "Animal Farm - George Orwell",
        "Aristotle and Dante Discover the Secrets of the Universe - Benjamin Alire Sáenz",
        "Becoming - Michelle Obama", "Big Little Lies - Liane Moriarty", "Bird Box - Josh Malerman",
        "Brida - Paulo Coelho", "Bringing Down the Duke - Evie Dunmore", "Circe - Madeline Miller",
        "Confess - Colleen Hoover", "Crime and Punishment - Fyodor Dostoevsky", "Crossfire - Sylvia Day",
        "Daisy Jones and The Six - Taylor Jenkins Reid", "Divergent - Veronica Roth",
        "Don't You Dare - Cecelia M. McCollum", "Everything I Never Told You - Celeste Ng",
        "Fear and Loathing in Las Vegas - Hunter S. Thompson", "Fifty Shades of Grey - E.L. James",
        "Fifty Shades Darker - E.L. James", "Fifty Shades Freed - E.L. James",
        "For You - Cecelia M. McCollum", "Good Company - Cynthia Sweeney", "Goodbye Stranger - Rebecca Stead",
        "Harry Potter and the Sorcerer's Stone - J.K. Rowling", "Holes - Louis Sachar",
        "House of Earth and Blood - Sarah J. Maas", "I Am Malala - Malala Yousafzai",
        "I Still Believe - Jeremy Camp", "If I Stay - Gayle Forman", "It Ends with Us - Colleen Hoover",
        "It's Kind of a Funny Story - Ned Vizzini", "John Green - The Fault in Our Stars",
        "Looking for Alaska - John Green", "Man's Search for Meaning - Viktor Frankl",
        "Memoirs of a Geisha - Arthur Golden", "Middlesex - Jeffrey Eugenides",
        "Misery - Stephen King", "Mockingjay - Suzanne Collins", "Murder on the Orient Express - Agatha Christie",
        "My Sister's Keeper - Jodi Picoult", "Never Let Me Go - Kazuo Ishiguro",
        "Normal People - Sally Rooney", "One Day - David Nicholls", "One Last Thing - Cecelia M. McCollum",
        "Outlander - Diana Gabaldon", "Pride and Prejudice - Jane Austen", "Red Queen - Victoria Aveyard",
        "Reminders of Him - Colleen Hoover", "Requiem - Lauren Oliver", "Shatter Me - Tahereh Mafi",
        "Six of Crows - Leigh Bardugo", "Small Great Things - Jodi Picoult", "Slaughterhouse-Five - Kurt Vonnegut",
        "Sophie’s World - Jostein Gaarder", "The 5th Wave - Rick Yancey", "The Alchemist - Paulo Coelho",
        "The Bell Jar - Sylvia Plath", "The Book Thief - Markus Zusak", "The Catcher in the Rye - J.D. Salinger",
        "The Chronicles of Narnia - C.S. Lewis", "The Cruel Prince - Holly Black",
        "The Fault in Our Stars - John Green",
        "The Girl on the Train - Paula Hawkins", "The Great Gatsby - F. Scott Fitzgerald",
        "The Hating Game - Sally Thorne", "The Hate U Give - Angie Thomas",
        "The Hunger Games - Suzanne Collins", "The Maze Runner - James Dashner", "The Midnight Library - Matt Haig",
        "The Night Circus - Erin Morgenstern", "The Nightingale - Kristin Hannah", "The Notebook - Nicholas Sparks",
        "The Seven Husbands of Evelyn Hugo - Taylor Jenkins Reid", "The Song of Achilles - Madeline Miller",
        "The Tattooist of Auschwitz - Heather Morris", "The Time Traveler's Wife - Audrey Niffenegger",
        "The Turning Point - Cecelia M. McCollum", "Throne of Glass - Sarah J. Maas",
        "To All the Boys I've Loved Before - Jenny Han",
        "To Kill a Mockingbird - Harper Lee", "Twilight - Stephenie Meyer", "Verity - Colleen Hoover",
        "Where the Crawdads Sing - Delia Owens", "Where the Forest Meets the Stars - Glendy Vanderah",
        "Wicked - Gregory Maguire", "You - Caroline Kepnes", "You & Me at the End of the World - Brianna Bourne"
    ]

    # Function to insert selected book title into book_title Entry
    def select_book_title(selected_title):
        book_title.delete(0, tk.END)  # Clear existing text
        book_title.insert(0, selected_title)  # Insert selected title
        popup_window.destroy()  # Close pop-up window after selection

    # Function to filter list based on search input
    def search_books(event=None):
        search_term = search_var.get().lower()  # Get the search term
        filtered_titles = [title for title in book_titles if search_term in title.lower()]  # Filter titles
        update_listbox(filtered_titles)  # Update the Listbox with filtered titles
        if search_term:
            clear_button.pack(side="right", padx=10)  # Show the clear button when there is input
        else:
            clear_button.pack_forget()  # Hide the clear button when the search term is empty

    # Function to update Listbox with filtered titles
    def update_listbox(filtered_titles):
        listbox.delete(0, tk.END)  # Clear existing items in Listbox
        for title in filtered_titles:
            listbox.insert(tk.END, title)  # Insert filtered titles

    # Create a frame to hold the search bar and the "X" button
    frame = tk.Frame(popup_window, bg="#D2B48C")  # Set background color for frame (#D2B48C)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Create a frame for the search entry and the "X" button
    search_frame = tk.Frame(frame, bg="#D2B48C")  # The frame will hold the search entry and the X button
    search_frame.pack(pady=10, fill="x")

    # Create a search bar Entry widget with "Search..." text that disappears on click
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Courier", 10), width=40, bg="#FAFAD2",
                            fg="#000000")  # Light yellow bg (#FAFAD2), black text (#000000)
    search_entry.insert(0, "Search...")

    # Create a clear button to reset the search
    clear_button = tk.Button(search_frame, text="X", font=("Courier", 10), bg="#FF6347", fg="white",
                             command=lambda: search_var.set(''))
    clear_button.pack(side="right")
    # Pack the search entry first
    search_entry.pack(side="left", padx=(0, 30), fill="x")

    # Pack the clear button to the top-right of the search frame, ensuring there's a little space
    clear_button.pack(side="right", padx=5, pady=5)

    # Function to handle placeholder disappearance
    def on_focus_in(event):
        if search_var.get() == "Search...":
            search_var.set("")  # Clear the placeholder when focused

    def on_focus_out(event):
        if search_var.get() == "":
            search_var.set("Search...")  # Restore placeholder if the entry is empty

    # Bind the focus events to handle placeholder behavior
    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)

    # Bind the key release event to filter the list as the user types
    search_entry.bind("<KeyRelease>", search_books)

    # Create a frame to hold the Listbox and Scrollbar
    listbox_frame = tk.Frame(frame, bg="#D2B48C")  # Set background color for listbox_frame (#D2B48C)
    listbox_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Create a vertical scrollbar
    scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")

    # Create Listbox to show the titles
    listbox = tk.Listbox(listbox_frame, font=("Courier", 10), width=40, height=7, yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # Add items to the Listbox initially
    update_listbox(book_titles)

    # Pack Listbox and Scrollbar
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Bind function to select a title when clicked
    listbox.bind("<Double-1>", lambda event: select_book_title(listbox.get(listbox.curselection())))

    # Add a close button
    close_button_frame = tk.Frame(popup_window, bg="#D2B48C")
    close_button_frame.pack(side="bottom", fill="x", pady=(0, 0))  # Position the button at the bottom

    # Add the "Close" button to the frame
    close_button = tk.Button(close_button_frame, text="Close", font=("Courier", 10), bg="#FF6347", fg="#FFFFFF",
                             command=popup_window.destroy)
    close_button.pack(pady=5)


# --- CRUD Operation Functions ---

def add_rental():
    title = book_title.get()
    renter = renter_name.get()
    category = category_var.get()
    date = rental_date.get()
    rental_id_val = rental_id.get()  # Get the rental ID entered by the user

    # Check if the required fields are filled
    if not rental_id_val or not title or not renter or not category or not date:
        messagebox.showerror("Input Error", "All fields including Rental ID are required.")
        return

    try:
        # Check if the rental_id already exists in the database
        cursor.execute("SELECT id FROM rentals WHERE id = ?", (rental_id_val,))
        if cursor.fetchone():
            messagebox.showerror("Input Error",
                                 f"Rental ID {rental_id_val} already exists. Please choose a different ID.")
            return

        # Insert the rental record with the manually entered rental_id
        cursor.execute(
            "INSERT INTO rentals (id, book_title, renter_name, category, rental_date, cost) VALUES (?, ?, ?, ?, ?, ?)",
            (rental_id_val, title, renter, category, date, calculate_cost(category)))
        conn.commit()  # Commit the changes
        update_rental_list()  # Refresh the rental list after adding
        messagebox.showinfo("Success", "Rental added successfully!")
    except Exception as e:
        messagebox.showerror("Database Error", f"Error adding rental: {e}")


def update_rental():
    rental_id_val = rental_id.get()

    # Check if the rental ID is provided
    if not rental_id_val:
        messagebox.showerror("Input Error", "Rental ID is required.")
        return

    # Function to open a new window to edit the rental details
    def open_edit_window():
        # Fetch current values from the database based on rental_id
        cursor.execute("SELECT * FROM rentals WHERE id = ?", (rental_id_val,))
        rental = cursor.fetchone()

        # If no rental with the given ID is found, show an error
        if not rental:
            messagebox.showwarning("Not Found", "No rental found with the given ID.")
            return

        # Create a new window for editing the rental details
        edit_window = tk.Toplevel(main_window)
        edit_window.title("Edit Rental Details")
        edit_window.geometry("400x400")
        edit_window.config(bg="#D2B48C")  # Light brown background color

        # Create a frame for the form
        form_frame = tk.Frame(edit_window, bg="#D2B48C")
        form_frame.place(relx=0.5, rely=0.4, anchor="center")

        # Function to open the book title selector
        def open_book_title_selector():
            popup_window = tk.Toplevel(edit_window)
            popup_window.title("Choose a Book Title")
            popup_window.geometry("400x300")
            popup_window.config(bg="#D2B48C")

            # Function to handle title selection
            def select_book_title(selected_title):
                book_title_entry.delete(0, tk.END)
                book_title_entry.insert(0, selected_title)
                popup_window.destroy()

            # Create and populate the Listbox
            book_titles = [
                "A Court of Thorns and Roses - Sarah J. Maas", "A Little Life - Hanya Yanagihara",
                "After - Anna Todd", "After We Collided - Anna Todd", "After Ever Happy - Anna Todd",
                "After We Fell - Anna Todd", "All Your Perfects - Colleen Hoover", "American Dirt - Jeanine Cummins",
                "Animal Farm - George Orwell",
                "Aristotle and Dante Discover the Secrets of the Universe - Benjamin Alire Sáenz",
                "Becoming - Michelle Obama", "Big Little Lies - Liane Moriarty", "Bird Box - Josh Malerman",
                "Brida - Paulo Coelho", "Bringing Down the Duke - Evie Dunmore", "Circe - Madeline Miller",
                "Confess - Colleen Hoover", "Crime and Punishment - Fyodor Dostoevsky", "Crossfire - Sylvia Day",
                "Daisy Jones and The Six - Taylor Jenkins Reid", "Divergent - Veronica Roth",
                "Don't You Dare - Cecelia M. McCollum", "Everything I Never Told You - Celeste Ng",
                "Fear and Loathing in Las Vegas - Hunter S. Thompson", "Fifty Shades of Grey - E.L. James",
                "Fifty Shades Darker - E.L. James", "Fifty Shades Freed - E.L. James",
                "For You - Cecelia M. McCollum", "Good Company - Cynthia Sweeney", "Goodbye Stranger - Rebecca Stead",
                "Harry Potter and the Sorcerer's Stone - J.K. Rowling", "Holes - Louis Sachar",
                "House of Earth and Blood - Sarah J. Maas", "I Am Malala - Malala Yousafzai",
                "I Still Believe - Jeremy Camp", "If I Stay - Gayle Forman", "It Ends with Us - Colleen Hoover",
                "It's Kind of a Funny Story - Ned Vizzini", "John Green - The Fault in Our Stars",
                "Looking for Alaska - John Green", "Man's Search for Meaning - Viktor Frankl",
                "Memoirs of a Geisha - Arthur Golden", "Middlesex - Jeffrey Eugenides",
                "Misery - Stephen King", "Mockingjay - Suzanne Collins",
                "Murder on the Orient Express - Agatha Christie",
                "My Sister's Keeper - Jodi Picoult", "Never Let Me Go - Kazuo Ishiguro",
                "Normal People - Sally Rooney", "One Day - David Nicholls", "One Last Thing - Cecelia M. McCollum",
                "Outlander - Diana Gabaldon", "Pride and Prejudice - Jane Austen", "Red Queen - Victoria Aveyard",
                "Reminders of Him - Colleen Hoover", "Requiem - Lauren Oliver", "Shatter Me - Tahereh Mafi",
                "Six of Crows - Leigh Bardugo", "Small Great Things - Jodi Picoult",
                "Slaughterhouse-Five - Kurt Vonnegut",
                "Sophie’s World - Jostein Gaarder", "The 5th Wave - Rick Yancey", "The Alchemist - Paulo Coelho",
                "The Bell Jar - Sylvia Plath", "The Book Thief - Markus Zusak",
                "The Catcher in the Rye - J.D. Salinger",
                "The Chronicles of Narnia - C.S. Lewis", "The Cruel Prince - Holly Black",
                "The Fault in Our Stars - John Green",
                "The Girl on the Train - Paula Hawkins", "The Great Gatsby - F. Scott Fitzgerald",
                "The Hating Game - Sally Thorne", "The Hate U Give - Angie Thomas",
                "The Hunger Games - Suzanne Collins", "The Maze Runner - James Dashner",
                "The Midnight Library - Matt Haig",
                "The Night Circus - Erin Morgenstern", "The Nightingale - Kristin Hannah",
                "The Notebook - Nicholas Sparks",
                "The Seven Husbands of Evelyn Hugo - Taylor Jenkins Reid", "The Song of Achilles - Madeline Miller",
                "The Tattooist of Auschwitz - Heather Morris", "The Time Traveler's Wife - Audrey Niffenegger",
                "The Turning Point - Cecelia M. McCollum", "Throne of Glass - Sarah J. Maas",
                "To All the Boys I've Loved Before - Jenny Han",
                "To Kill a Mockingbird - Harper Lee", "Twilight - Stephenie Meyer", "Verity - Colleen Hoover",
                "Where the Crawdads Sing - Delia Owens", "Where the Forest Meets the Stars - Glendy Vanderah",
                "Wicked - Gregory Maguire", "You - Caroline Kepnes", "You & Me at the End of the World - Brianna Bourne"
            ]

            listbox = tk.Listbox(popup_window, font=("Courier", 10), height=15)
            for title in book_titles:
                listbox.insert(tk.END, title)

            # Add Scrollbar
            scrollbar = ttk.Scrollbar(popup_window, orient="vertical", command=listbox.yview)
            listbox.config(yscrollcommand=scrollbar.set)

            # Pack Listbox and Scrollbar
            listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y")

            # Bind selection event
            listbox.bind("<Double-1>", lambda event: select_book_title(listbox.get(listbox.curselection())))

        # Labels and Entry widgets for editing
        tk.Label(form_frame, text="Book Title", font=("Courier", 10), bg="#D2B48C").grid(row=0, column=0, sticky="w",
                                                                                         pady=5)
        book_title_entry = tk.Entry(form_frame, font=("Courier", 10), width=30)
        book_title_entry.insert(0, rental[1])  # Display current book title
        book_title_entry.grid(row=0, column=1, pady=5)

        # Bind a click event to the Book Title entry
        book_title_entry.bind("<Button-1>", lambda event: open_book_title_selector())

        tk.Label(form_frame, text="Renter Name", font=("Courier", 10), bg="#D2B48C").grid(row=1, column=0, sticky="w",
                                                                                          pady=5)
        renter_name_entry = tk.Entry(form_frame, font=("Courier", 10), width=30)
        renter_name_entry.insert(0, rental[2])  # Display current renter name
        renter_name_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Category", font=("Courier", 10), bg="#D2B48C").grid(row=2, column=0, sticky="w",
                                                                                       pady=5)
        # Create a Combobox for the category field
        category_combobox = ttk.Combobox(form_frame, font=("Courier", 10), values=["Thin", "Medium", "Thick"],
                                         state="readonly")
        category_combobox.set(rental[3])  # Set the current category
        category_combobox.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Rental Date", font=("Courier", 10), bg="#D2B48C").grid(row=3, column=0, sticky="w",
                                                                                          pady=5)
        rental_date_entry = tk.Entry(form_frame, font=("Courier", 10), width=30)
        rental_date_entry.insert(0, rental[4])  # Display current rental date
        rental_date_entry.grid(row=3, column=1, pady=5)

        # Function to handle saving the updated details
        def save_update():
            updated_title = book_title_entry.get()
            updated_renter = renter_name_entry.get()
            updated_category = category_combobox.get()
            updated_date = rental_date_entry.get()

            if not updated_title or not updated_renter or not updated_category or not updated_date:
                messagebox.showerror("Input Error", "All fields are required.")
                return

            try:
                cursor.execute(
                    "UPDATE rentals SET book_title = ?, renter_name = ?, category = ?, rental_date = ?, cost = ? WHERE id = ?",
                    (updated_title, updated_renter, updated_category, updated_date, calculate_cost(updated_category),
                     rental_id_val))

                conn.commit()

                if cursor.rowcount == 0:
                    messagebox.showwarning("Not Found", "No rental found with the given ID.")
                else:
                    messagebox.showinfo("Success", "Rental updated successfully!")
                    update_rental_list()
                    edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Database Error", f"Error updating rental: {e}")

        # Create Save and Cancel buttons
        button_frame = tk.Frame(edit_window, bg="#D2B48C")
        button_frame.place(relx=0.5, rely=0.8, anchor="center")

        save_button = tk.Button(button_frame, text="Save", font=("Courier", 10), bg="green", fg="white",
                                command=save_update)
        save_button.pack(side="left", padx=10)

        cancel_button = tk.Button(button_frame, text="Cancel", font=("Courier", 10), bg="red", fg="white",
                                  command=edit_window.destroy)
        cancel_button.pack(side="right", padx=10)

    # Open the edit window
    open_edit_window()


def delete_rental():
    rental_id_val = rental_id.get()

    if not rental_id_val:
        messagebox.showerror("Input Error", "Rental ID is required.")
        return

    try:
        cursor.execute("DELETE FROM rentals WHERE id = ?", (rental_id_val,))
        conn.commit()  # Commit the changes
        if cursor.rowcount == 0:
            messagebox.showwarning("Not Found", "No rental found with the given ID.")
        else:
            update_rental_list()  # Refresh the rental list after deleting
            messagebox.showinfo("Success", "Rental deleted successfully!")
    except Exception as e:
        messagebox.showerror("Database Error", f"Error deleting rental: {e}")


def delete_all_rentals():
    confirm = messagebox.askyesno("Confirm", "Are yu sure you want to delete all rentals?")
    if confirm:
        try:
            cursor.execute("DELETE FROM rentals")
            conn.commit()
            update_rental_list()
            messagebox.showinfo("Success", "All rentals deleted successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error deleting rentals: {e}")


def update_rental_list():
    try:
        # Clear existing rows in the Treeview
        for row in tree.get_children():
            tree.delete(row)

        total_cost = 0  # Initialize the total cost
        # Get rentals from the database, ordered by rental_id in ascending order (lowest to highest)
        cursor.execute("SELECT * FROM rentals ORDER BY id ASC")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)  # Insert the rentals into the treeview
            total_cost += row[5]  # Add the cost of the current rental (cost is in the 6th column)

        # Add an empty row to create a visual gap (optional)
        tree.insert("", "end", values=(" ", " ", " ", " ", " ", " "))  # Empty row for spacing

        # Insert a row for total cost
        # Insert the "Total Cost" row with a custom tag
        # Insert the "Total Cost" row with a custom tag
        tree.insert("", "end", 
                    values=("Total Cost:", "", "", "", "", f"{total_cost:.1f}"), 
                    tags=('total_cost',))  # Apply the 'total_cost' tag
        
        # Configure the tag to change the text color and background color
        tree.tag_configure('total_cost', 
                           foreground='#FFFFFF',  # Darker text color
                           background='#6B4226',  # Light background color for the row
                           font=('Courier', 11, 'bold'))  # Optional: bold and larger text
          # Darker color for the text


        # Adjust column width to ensure consistency across rows
        tree.column("#6", width=150, anchor="w")  # Align the cost column to the left (anchor="w")

    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching rentals: {e}")


def calculate_cost(category):
    """Calculate the rental cost based on category."""
    if category == "Thin":
        return 40
    elif category == "Medium":
        return 60
    elif category == "Thick":
        return 80
    return 0


def create_gradient(canvas, color1, color2, width, height, steps=100):
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)
    r_ratio = (r2 - r1) / steps
    g_ratio = (g2 - g1) / steps
    b_ratio = (b2 - b1) / steps
    for i in range(steps):
        nr = int(r1 + (r_ratio * i)) // 256
        ng = int(g1 + (g_ratio * i)) // 256
        nb = int(b1 + (b_ratio * i)) // 256
        color = f"#{nr:02x}{ng:02x}{nb:02x}"
        y1 = int(i * (height / steps))
        y2 = int((i + 1) * (height / steps))
        canvas.create_rectangle(0, y1, width, y2, outline="", fill=color)


# --- Main Application ---
# --- Main Application ---
def open_main_system():
    def logout():
        main_window.destroy()
        login_system()

    # Main Application Window
    global main_window, book_title
    main_window = tk.Tk()
    main_window.title("Rental Books")
    main_window.geometry("1100x800")
    main_window.configure(bg="#F7F3E9")

    # Title
    title_label = tk.Label(main_window, text="Rental Books", font=("Courier", 30, "bold"), bg="#F7F3E9", fg="#6B4226")
    title_label.pack()
    
    subtitle_label = tk.Label(main_window, text="Return Within 1 Week", font=("Courier", 12, "bold"), bg="#F7F3E9", fg="#6B4226")
    subtitle_label.pack()

    # Frames
    form_frame = tk.Frame(main_window, bg="#D2B48C", relief="raised", bd=2)
    form_frame.pack(pady=10, padx=10, fill="x")

    table_frame = tk.Frame(main_window, bg="#D2B48C", relief="raised", bd=2)
    table_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Input Form (Left side of form_frame)
    input_frame = tk.Frame(form_frame, bg="#D2B48C")
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    global book_title, renter_name, category_var, rental_date, rental_id, tree
    tk.Label(input_frame, text="Book Title:", font=("Courier", 11, "bold"), bg="#D2B48C", fg="#6B4226").grid(row=0,
                                                                                                             column=0,
                                                                                                             padx=10,
                                                                                                             pady=5,
                                                                                                             sticky="e")
    book_title = tk.Entry(input_frame, font=("Courier", 10), width=25)
    book_title.grid(row=0, column=1, padx=10, pady=5)

    # Bind the click event to open the pop-up
    book_title.bind("<Button-1>", lambda event: open_book_title_popup())

    tk.Label(input_frame, text="Renter Name:", font=("Courier", 11, "bold"), bg="#D2B48C", fg="#6B4226").grid(row=1,
                                                                                                              column=0,
                                                                                                              padx=10,
                                                                                                              pady=5,
                                                                                                              sticky="e")
    renter_name = tk.Entry(input_frame, font=("Courier", 10), width=25)
    renter_name.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Category:", font=("Courier", 11, "bold"), bg="#D2B48C", fg="#6B4226").grid(row=2,
                                                                                                           column=0,
                                                                                                           padx=10,
                                                                                                           pady=5,
                                                                                                           sticky="e")
    category_var = ttk.Combobox(input_frame, values=["Thin", "Medium", "Thick"], font=("Courier", 10), width=23)
    category_var.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Rental Date (YYYY-MM-DD):", font=("Courier", 11, "bold"), bg="#D2B48C",
             fg="#6B4226").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    rental_date = tk.Entry(input_frame, font=("Courier", 10), width=25)
    rental_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
    rental_date.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Rental ID (For Update/Delete):", font=("Courier", 11, "bold"), bg="#D2B48C",
             fg="#6B4226").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    rental_id = tk.Entry(input_frame, font=("Courier", 10), width=25)
    rental_id.grid(row=4, column=1, padx=10, pady=5)

    # CRUD Buttons (Right side of form_frame)
    crud_frame = tk.Frame(form_frame, bg="#D2B48C")
    crud_frame.grid(row=0, column=1, padx=360, pady=15, sticky="ne")

    tk.Button(crud_frame, text="Add Rental", font=("Courier", 10), bg="#6B4226", fg="white", width=15,
              command=add_rental).pack(pady=7)
    tk.Button(crud_frame, text="Update Rental", font=("Courier", 10), bg="#6B4226", fg="white", width=15,
              command=update_rental).pack(pady=7)
    tk.Button(crud_frame, text="Delete Rental", font=("Courier", 10), bg="#6B4226", fg="white", width=15,
              command=delete_rental).pack(pady=7)
    tk.Button(crud_frame, text="Clear Rentals", font=("Courier", 10), bg="#6B4226", fg="white", width=15,
              command=delete_all_rentals).pack(pady=7)

    # Logout Button
    logout_button = tk.Button(main_window, text="Logout", font=("Courier", 10), bg="#FF6347", fg="white",
                              command=logout, width=10)
    logout_button.place(x=950, y=50)

    style = ttk.Style()
    style.configure("Treeview", 
                    background="#F5DEB3", 
                    fieldbackground="#F5DEB3", 
                    foreground="black", 
                    font=("Courier", 10))  # Change font size of entries here

    style.configure("Treeview.Heading", 
                    background="#6B4226",  # Set background color of heading
                    foreground="#6B4226",  # Set text color of heading
                    font=("Courier", 11, "bold"))  # Change font size and make it bold
    style.map("Treeview", background=[("selected", "#6B4226")])

    # Rental Table (Below form_frame)
    tree = ttk.Treeview(table_frame, columns=("ID", "Book Title", "Renter", "Category", "Date", "Cost"),
                        show="headings", height=15)
    tree.heading("ID", text="ID")
    tree.heading("Book Title", text="Book Title")
    tree.heading("Renter", text="Renter")
    tree.heading("Category", text="Category")
    tree.heading("Date", text="Rental Date")
    tree.heading("Cost", text="Cost (Pesos)")

    for col in ("ID", "Book Title", "Renter", "Category", "Date", "Cost"):
        tree.column(col, width=100)

    tree.tag_configure('odd', background='#FFF5E1')  # Odd rows
    tree.tag_configure('even', background='#F5DEB3')  # Even rows

    tree.pack(fill="both", expand=True)
    update_rental_list()

    main_window.mainloop()


def gradient(canvas, color1, color2, width, height):
    # Creates a gradient background
    gradient_steps = 100
    for i in range(gradient_steps):
        color = canvas.winfo_rgb(color1)
        red = color[0] // 256
        green = color[1] // 256
        blue = color[2] // 256
        delta = canvas.winfo_rgb(color2)
        dr = (delta[0] // 256 - red) / gradient_steps
        dg = (delta[1] // 256 - green) / gradient_steps
        db = (delta[2] // 256 - blue) / gradient_steps
        color_hex = f'#{int(red + dr * i):02x}{int(green + dg * i):02x}{int(blue + db * i):02x}'
        canvas.create_rectangle(0, height * i / gradient_steps, width, height * (i + 1) / gradient_steps,
                                fill=color_hex, outline="")


# --- Login System ---
user_data = { "flor" : "12"}  # Dictionary to store registered users


def register_user(sign_up_window, new_username_entry, new_password_entry):
    new_username = new_username_entry.get()
    new_password = new_password_entry.get()
    if new_username and new_password:
        if new_username in user_data:
            messagebox.showerror("Error", "Username already exists. Please choose another one.")
        else:
            user_data[new_username] = new_password
            messagebox.showinfo("Sign Up Successful", f"User '{new_username}' registered successfully!")
            sign_up_window.destroy()
    else:
        messagebox.showerror("Error", "Please fill in all fields")


def open_sign_up(login_window):
    sign_up_window = tk.Toplevel(login_window)
    sign_up_window.title("Sign Up")
    sign_up_window.geometry("300x300")
    sign_up_window.configure(bg="#FAC482")

    tk.Label(sign_up_window, text="Sign Up", font=("Colonna MT", 20, "bold"), bg="#FAC482", fg="#6B4226").pack(pady=10)
    tk.Label(sign_up_window, text="New Username", font=("GothicE", 14), fg="#6B4226", bg="#FAC482").pack(pady=10)
    new_username_entry = tk.Entry(sign_up_window, font=("Courier", 14), width=25, bd=2, relief="groove")
    new_username_entry.pack(pady=5)
    tk.Label(sign_up_window, text="New Password", font=("GothicE", 14), fg="#6B4226", bg="#FAC482").pack(pady=10)
    new_password_entry = tk.Entry(sign_up_window, font=("Courier", 14), width=25, bd=2, relief="groove", show="*")
    new_password_entry.pack(pady=5)
    tk.Button(sign_up_window, text="Register", font=("GothicE", 14, "bold"), fg="white", bg="#6B4226", width=20,
              command=lambda: register_user(sign_up_window, new_username_entry, new_password_entry)).pack(pady=20)


# --- Login System ---
def login_system():
    def verify_credentials():
        username = username_entry.get()
        password = password_entry.get()
        if username in user_data and user_data[username] == password:
            messagebox.showinfo("Login Successful", "Today a reader, tomorrow a leader. - Margaret Fuller")
            login_window.destroy()
            open_main_system()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def resize_gradient(event):
        canvas.delete("all")
        gradient(canvas, "#E09B60", "#8C4718", event.width, event.height)

    login_window = tk.Tk()
    login_window.title("Login - Marg's Rental Books")
    login_window.geometry("400x500")

    canvas = tk.Canvas(login_window, width=500, height=500, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    gradient(canvas, "#E09B60", "#8C4718", 400, 500)
    canvas.bind("<Configure>", resize_gradient)

    frame = tk.Frame(login_window, bg="#FAC482", bd=2)
    frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400)

    tk.Label(frame, text="Marg's Rental Books", font=("Courier", 14, "bold"), bg="#FAC482", fg="#6B4226").pack(pady=10)

    tk.Label(frame, text="Username", font=("Courier", 14, "bold"), fg="#6B4226", bg="#FAC482").pack(pady=10)
    username_entry = tk.Entry(frame, font=("Courier", 14, "bold"), width=20, bd=2, relief="groove", bg="#FAC482", fg="#6B4226")

    username_entry.pack(pady=5)
    tk.Label(frame, text="Password", font=("Courier", 14, "bold"), fg="#6B4226", bg="#FAC482").pack(pady=10)
    password_entry = tk.Entry(frame, font=("Courier", 14, "bold"), width=20, bd=2, relief="groove", show="*", bg="#FAC482", fg="#6B4226")
    password_entry.pack(pady=5)
    tk.Button(frame, text="Log In", font=("Courier", 14, "bold"), fg="white", bg="#6B4226", width=20,
              command=verify_credentials).pack(pady=20)

    tk.Button(frame, text="Sign Up", font=("GothicE", 14, "bold"), fg="white", bg="#6B4226", width=15,
              command=lambda: open_sign_up(login_window)).pack(pady=10)

    login_window.mainloop()
# --- Start Application ---
if __name__ == "__main__":
    conn, cursor = setup_database()
    login_system()

