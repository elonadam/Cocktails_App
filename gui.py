from tkinter import *
from tkinter import messagebox
from cocktail_Manager import CocktailManager  # Replace with your class import
from cocktail import Cocktail  # Replace with your class import

# Define colors for the dark theme
THEME_COLOR = "#1E1E1E"  # Dark gray background
#THEME_COLOR = "#0F0F0F"  # obsidian black background
BUTTON_COLOR_PRIMARY = "#2E2E2E"  # Darker gray for buttons
BUTTON_COLOR_SECONDARY = "#3A3A3A"  # Lighter gray for secondary buttons
TEXT_COLOR = "#FFFFFF"  # White text for visibility
FONT_HEADER = ("Helvetica", 20, "bold")
FONT_BODY = ("Helvetica", 14)
FONT_BUTTON = ("Helvetica", 16, "bold")


class CocktailAppGUI:

    def __init__(self, manager: CocktailManager):
        self.manager = manager

        # Window setup
        self.window = Tk()
        self.window.title("Bartender's Cocktail Book")
        self.window.config(background="#0F0F0F", padx=0, pady=0)

        # Add an "X" button to close the app
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)

        # Canvas for displaying cocktails
        self.canvas = Canvas(bg=THEME_COLOR, width=480, height=480, highlightthickness=0)
        self.canvas_text = self.canvas.create_text(200, 150, width=380, fill=TEXT_COLOR)
        self.canvas.grid(row=0, column=0, columnspan=2, pady=0)

        self.background_image = PhotoImage(file="images/bg_img.png")
        # Add the background image to the Canvas
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")
        self.canvas.grid(row=0, column=0, columnspan=2, pady=0)

        # Icons for buttons (ensure the paths are correct)
        add_cocktail_icon = PhotoImage(file="images/add clear 100.png")
        search_cocktail_icon = PhotoImage(file="images/search_icon_100.png")
        edit_cocktail_icon = PhotoImage(file="images/edit clear 100.png")
        view_cocktail_icon = PhotoImage(file="images/view clear 100.png")

        # Buttons
        self.add_button = Button(
            command=self.add_cocktail,
            image=add_cocktail_icon,
            bg=BUTTON_COLOR_PRIMARY,
            activebackground=BUTTON_COLOR_PRIMARY,
            borderwidth=0,
            highlightthickness=0
        )
        self.add_button.image = add_cocktail_icon  # Prevent garbage collection
        self.add_button.grid(row=1, column=0, padx=10, pady=10)

        self.view_button = Button(
            command=self.view_cocktails,
            image=view_cocktail_icon,
            bg=BUTTON_COLOR_PRIMARY,
            activebackground=BUTTON_COLOR_PRIMARY,
            borderwidth=0,
            highlightthickness=0
        )
        self.view_button.image = view_cocktail_icon
        self.view_button.grid(row=1, column=1, padx=10, pady=10)

        self.edit_button = Button(
            command=self.edit_cocktail,
            image=edit_cocktail_icon,
            bg=BUTTON_COLOR_PRIMARY,
            activebackground=BUTTON_COLOR_PRIMARY,
            borderwidth=0,
            highlightthickness=0
        )
        self.edit_button.image = edit_cocktail_icon
        self.edit_button.grid(row=2, column=0, padx=10, pady=10)

        self.search_button = Button(
            command=self.search_cocktail,
            image=search_cocktail_icon,
            bg=BUTTON_COLOR_PRIMARY,
            activebackground=BUTTON_COLOR_PRIMARY,
            borderwidth=0,
            highlightthickness=0
        )
        self.search_button.image = search_cocktail_icon
        self.search_button.grid(row=2, column=1, padx=10, pady=10)

        # Make the grid layout responsive
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(3, weight=1)

        # Start the GUI loop
        self.window.mainloop()

    def close_app(self):
        """
        Handles the closing of the application when the 'X' button is clicked.
        """
        if messagebox.askyesno("Exit", "Are you sure you want to exit the application?"):
            self.window.destroy()

    def create_scrollable_frame(self, popup):
        """
        Creates a scrollable frame inside a popup window.
        """
        canvas = Canvas(popup, bg=THEME_COLOR, highlightthickness=0)
        scrollbar = Scrollbar(popup, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=THEME_COLOR)

        # Configure canvas scroll region to match the frame's size
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        return scrollable_frame

    def create_input_field(self, popup, label_text, row):
        Label(popup, text=label_text, bg=THEME_COLOR, fg=TEXT_COLOR, font=FONT_BODY).grid(row=row, column=0, sticky="w")
        entry = Entry(popup, width=30, bg="#2E2E2E", fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
        entry.grid(row=row, column=1)
        return entry

    def add_cocktail(self):
        popup = Toplevel(self.window)
        popup.title("Add New Cocktail")
        popup.config(padx=20, pady=20, bg=THEME_COLOR)

        # Input fields
        name_entry = self.create_input_field(popup, "Name:", 0)
        abv_entry = self.create_input_field(popup, "ABV (%):", 1)
        ingredients_entry = self.create_input_field(popup, "Ingredients (comma-separated):", 2)
        instructions_entry = self.create_input_field(popup, "Instructions:", 3)

        Label(popup, text="Is Easy to Make (yes/no):", bg=THEME_COLOR, fg=TEXT_COLOR, font=FONT_BODY).grid(row=4,
                                                                                                           column=0,
                                                                                                           sticky="w")
        easy_entry = Entry(popup, width=30, bg="#2E2E2E", fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
        easy_entry.grid(row=4, column=1)

        Label(popup, text="Method:", bg=THEME_COLOR, fg=TEXT_COLOR, font=FONT_BODY).grid(row=5, column=0, sticky="w")
        method_var = StringVar(value="Shaken")
        method_dropdown = OptionMenu(popup, method_var, "Shaken", "Stirred")
        method_dropdown.config(bg=BUTTON_COLOR_SECONDARY, fg=TEXT_COLOR, font=FONT_BODY, highlightthickness=0)
        method_dropdown["menu"].config(bg=BUTTON_COLOR_SECONDARY, fg=TEXT_COLOR)
        method_dropdown.grid(row=5, column=1)

        add_button = Button(
            popup,
            text="Add",
            command=lambda: self.save_cocktail(
                name_entry.get(),
                abv_entry.get(),
                ingredients_entry.get(),
                instructions_entry.get(),
                easy_entry.get(),
                method_var.get(),
                popup),
            bg=BUTTON_COLOR_PRIMARY,
            fg=TEXT_COLOR,
            font=FONT_BUTTON
        )
        add_button.grid(row=6, column=0, columnspan=2, pady=20)

        # Cancel button
        Button(
            popup,
            text="Cancel",
            command=popup.destroy,
            bg="gray",
            fg=TEXT_COLOR,
            font=FONT_BUTTON
        ).grid(row=7, column=0, columnspan=2)

    def save_cocktail(self, name, abv, ingredients, instructions, easy, method, popup):
        """
        Saves a new cocktail to the CocktailManager.
        """
        try:
            # Parse inputs
            abv = float(abv)
            ingredients = [item.strip() for item in ingredients.split(",")]
            is_easy = easy.lower() in ["yes", "y", "true"]
            method = method.capitalize()

            # Create and add cocktail
            new_cocktail = Cocktail(
                name=name,
                abv=abv,
                ingredients=ingredients,
                instructions=instructions,
                is_easy_to_make=is_easy,
                method=method,
            )
            self.manager.add_cocktail(new_cocktail)
            messagebox.showinfo(title="Success", message=f"Cocktail '{name}' added!")
            popup.destroy()
        except ValueError:
            messagebox.showerror(title="Error", message="Invalid input. Please check your entries.")

    def view_cocktails(self):
        """
        Displays all cocktails in a scrollable frame inside a new window.
        """
        # Create a new popup window
        popup = Toplevel(self.window)
        popup.title("Cocktail Book")
        popup.config(padx=20, pady=20, bg=THEME_COLOR)

        # Scrollable frame setup
        scrollable_frame = self.create_scrollable_frame(popup)

        # List all cocktails
        if not self.manager.cocktail_book:
            Label(scrollable_frame, text="No cocktails available!", bg=THEME_COLOR, fg=TEXT_COLOR, font=FONT_BODY).pack(
                pady=10)
        else:
            for name, details in self.manager.cocktail_book.items():
                Label(
                    scrollable_frame,
                    text=f"{name} - {details['method']} - {details['abv']}%",
                    bg=THEME_COLOR,
                    fg=TEXT_COLOR,
                    font=FONT_BODY,
                    anchor="w",
                    justify="left",
                ).pack(fill="x", padx=10, pady=5)

    def edit_cocktail(self):
        """
        Opens a popup to select and edit an existing cocktail.
        """
        if not self.manager.cocktail_book:
            messagebox.showinfo("Info", "No cocktails available to edit.")
            return

        # Popup to select a cocktail
        popup = Toplevel(self.window)
        popup.title("Edit Cocktail")
        popup.config(padx=20, pady=20, bg=THEME_COLOR)

        Label(popup, text="Select a Cocktail to Edit:", bg=THEME_COLOR, fg=TEXT_COLOR, font=FONT_BODY).grid(row=0,
                                                                                                            column=0,
                                                                                                            pady=10)

        # Dropdown to select a cocktail
        cocktail_names = list(self.manager.cocktail_book.keys())
        selected_cocktail = StringVar()
        selected_cocktail.set(cocktail_names[0])  # Default selection

        dropdown = OptionMenu(popup, selected_cocktail, *cocktail_names)
        dropdown.config(bg=BUTTON_COLOR_SECONDARY, fg=TEXT_COLOR, font=FONT_BODY, highlightthickness=0)
        dropdown["menu"].config(bg=BUTTON_COLOR_SECONDARY, fg=TEXT_COLOR)
        dropdown.grid(row=1, column=0, pady=10)

        # Continue button
        Button(
            popup,
            text="Edit",
            command=lambda: self.open_edit_form(selected_cocktail.get(), popup),
            bg=BUTTON_COLOR_PRIMARY,
            fg=TEXT_COLOR,
            font=FONT_BUTTON,
        ).grid(row=2, column=0, pady=20)

    def open_edit_form(self, cocktail_name, parent_popup):
        """
        Opens a form pre-filled with the selected cocktail's details for editing.
        """
        parent_popup.destroy()  # Close the selection popup

        # Get the selected cocktail details
        cocktail = self.manager.get_cocktail(cocktail_name)
        if not cocktail:
            messagebox.showerror("Error", f"Cocktail '{cocktail_name}' not found.")
            return

        # Open edit popup
        popup = Toplevel(self.window)
        popup.title(f"Edit {cocktail_name}")
        popup.config(padx=20, pady=20, bg=THEME_COLOR)

        # Pre-filled fields for each attribute
        name_entry = self.create_input_field(popup, "Name:", 0)
        name_entry.insert(0, cocktail["name"])

        abv_entry = self.create_input_field(popup, "ABV (%):", 1)
        abv_entry.insert(0, str(cocktail["abv"]))

        ingredients_entry = self.create_input_field(popup, "Ingredients (comma-separated):", 2)
        ingredients_entry.insert(0, ", ".join(cocktail["ingredients"]))

        instructions_entry = self.create_input_field(popup, "Instructions:", 3)
        instructions_entry.insert(0, cocktail["instructions"])

        easy_entry = self.create_input_field(popup, "Is Easy to Make (yes/no):", 4)
        easy_entry.insert(0, "Yes" if cocktail["is_easy_to_make"] else "No")

        method_entry = self.create_input_field(popup, "Method (Shaken/Stirred):", 5)
        method_entry.insert(0, cocktail["method"])

        # Submit button to save changes
        Button(
            popup,
            text="Save Changes",
            command=lambda: self.save_changes(
                cocktail_name, name_entry.get(), abv_entry.get(), ingredients_entry.get(),
                instructions_entry.get(), easy_entry.get(), method_entry.get(), popup
            ),
            bg=BUTTON_COLOR_PRIMARY,
            fg=TEXT_COLOR,
            font=FONT_BUTTON,
        ).grid(row=6, column=0, columnspan=2, pady=20)

    def save_changes(self, old_name, name, abv, ingredients, instructions, easy, method, popup):
        """
        Saves the edited cocktail details to the CocktailManager.
        """
        try:
            # Parse inputs
            abv = float(abv)
            ingredients = [item.strip() for item in ingredients.split(",")]
            is_easy = easy.lower() in ["yes", "y", "true"]

            # Update the cocktail
            updated_data = {
                "name": name,
                "abv": abv,
                "ingredients": ingredients,
                "instructions": instructions,
                "is_easy_to_make": is_easy,
                "method": method.capitalize(),
            }
            self.manager.edit_cocktail(old_name, updated_data)

            # Show success message and close popup
            messagebox.showinfo(title="Success", message=f"Cocktail '{name}' updated successfully!")
            popup.destroy()
        except ValueError:
            messagebox.showerror(title="Error", message="Invalid input. Please check your entries.")

    def perform_search(self, category, name_query, scrollable_frame):
        """
        Performs a search for cocktails either by category or by name and displays the results.
        """
        # Clear the scrollable frame
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Filter cocktails by category
        if category == "All Cocktails":
            filtered_cocktails = list(self.manager.cocktail_book.keys())
        elif category == "Favorites":
            filtered_cocktails = [name for name, details in self.manager.cocktail_book.items() if
                                  details["is_favorite"]]
        elif category == "Easy to Make":
            filtered_cocktails = [name for name, details in self.manager.cocktail_book.items() if
                                  details["is_easy_to_make"]]
        elif category == "Stirred":
            filtered_cocktails = [name for name, details in self.manager.cocktail_book.items() if
                                  details["method"] == "Stirred"]
        elif category == "Shaken":
            filtered_cocktails = [name for name, details in self.manager.cocktail_book.items() if
                                  details["method"] == "Shaken"]
        elif category == "Haven't Tried":
            filtered_cocktails = [name for name, details in self.manager.cocktail_book.items() if
                                  details["times_made"] == 0]
        else:
            filtered_cocktails = []

        # Further filter by name query (case-insensitive)
        name_query = name_query.strip().lower()
        if name_query:
            results = [name for name in filtered_cocktails if name_query in name.lower()]
        else:
            results = filtered_cocktails

        # Display the results
        if not results:
            Label(scrollable_frame, text="No cocktails found.", bg=THEME_COLOR, fg=TEXT_COLOR, font=FONT_BODY).pack(
                pady=10)
        else:
            for name in results:
                Button(
                    scrollable_frame,
                    text=name,
                    command=lambda n=name: self.confirm_make_cocktail(n),
                    bg=BUTTON_COLOR_SECONDARY,
                    fg=TEXT_COLOR,
                    font=FONT_BODY,
                    anchor="w"
                ).pack(fill="x", padx=10, pady=5)

    def search_cocktail(self):
        """
        Opens a popup to search for cocktails by category or name.
        """
        popup = Toplevel(self.window)
        popup.title("Search Cocktail")
        popup.config(padx=20, pady=20, bg=THEME_COLOR)

        # Search by Category Section
        Label(popup, text="Choose a category:", bg=THEME_COLOR, fg=TEXT_COLOR, font=FONT_BODY).grid(row=0, column=0,
                                                                                                    pady=10)

        categories = ["All Cocktails", "Favorites", "Easy to Make", "Stirred", "Shaken", "Haven't Tried"]
        selected_category = StringVar()
        selected_category.set(categories[0])  # Default selection

        dropdown = OptionMenu(popup, selected_category, *categories)
        dropdown.config(bg=BUTTON_COLOR_SECONDARY, fg=TEXT_COLOR, font=FONT_BODY, highlightthickness=0)
        dropdown["menu"].config(bg=BUTTON_COLOR_SECONDARY, fg=TEXT_COLOR)
        dropdown.grid(row=1, column=0, pady=10)

        # Search by Name Section
        Label(popup, text="Search by name:", bg=THEME_COLOR, fg=TEXT_COLOR, font=FONT_BODY).grid(row=2, column=0,
                                                                                                 pady=10)

        # Entry for user input
        name_entry = Entry(popup, width=30, bg="#2E2E2E", fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
        name_entry.grid(row=3, column=0, pady=10)

        # Scrollable frame setup
        canvas = Canvas(popup, bg=THEME_COLOR, highlightthickness=0)
        scrollbar = Scrollbar(popup, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=THEME_COLOR)

        # Bind the scrollable frame to the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Place the canvas and scrollbar
        canvas.grid(row=4, column=0, sticky="nsew")
        scrollbar.grid(row=4, column=1, sticky="ns")

        # Bind events to update search results dynamically
        name_entry.bind("<KeyRelease>",
                        lambda event: self.perform_search(selected_category.get(), name_entry.get(), scrollable_frame))
        selected_category.trace("w", lambda *args: self.perform_search(selected_category.get(), name_entry.get(),
                                                                       scrollable_frame))

        # Cancel button
        Button(
            popup,
            text="Cancel",
            command=popup.destroy,
            bg="gray",
            fg=TEXT_COLOR,
            font=FONT_BUTTON,
        ).grid(row=5, column=0, pady=10)

        # Configure row and column resizing for the scrollable content
        popup.grid_rowconfigure(4, weight=1)
        popup.grid_columnconfigure(0, weight=1)

        # Initially perform the search to populate with all cocktails
        self.perform_search(selected_category.get(), name_entry.get(), scrollable_frame)

    def confirm_make_cocktail(self, cocktail_name):
        """
        Asks the user if they want to make the selected cocktail and handles updates.
        """
        # Confirmation popup
        confirm_popup = Toplevel(self.window)
        confirm_popup.title("Confirm")
        confirm_popup.config(padx=20, pady=20, bg=THEME_COLOR)

        Label(
            confirm_popup,
            text=f"Do you want to make '{cocktail_name}'?",
            bg=THEME_COLOR,
            fg=TEXT_COLOR,
            font=FONT_BODY,
        ).pack(pady=10)

        Button(
            confirm_popup,
            text="Yes",
            command=lambda: self.make_cocktail(cocktail_name, confirm_popup),
            bg=BUTTON_COLOR_PRIMARY,
            fg=TEXT_COLOR,
            font=FONT_BUTTON,
        ).pack(side=LEFT, padx=10)

        Button(
            confirm_popup,
            text="No",
            command=confirm_popup.destroy,
            bg=BUTTON_COLOR_PRIMARY,
            fg=TEXT_COLOR,
            font=FONT_BUTTON,
        ).pack(side=RIGHT, padx=10)

    def make_cocktail(self, cocktail_name, parent_popup):
        parent_popup.destroy()

        cocktail = self.manager.cocktail_book[cocktail_name]
        self.manager.edit_cocktail(cocktail_name, {"times_made": cocktail["times_made"] + 1})

        detail_popup = Toplevel(self.window)
        detail_popup.title(f"{cocktail_name} Details")
        detail_popup.config(padx=20, pady=20, bg=THEME_COLOR)

        details = (
            f"Name: {cocktail_name}\n"
            f"ABV: {cocktail['abv']}%\n"
            f"Ingredients: {', '.join(cocktail['ingredients'])}\n"
            f"Instructions: {cocktail['instructions']}\n"
            f"Favorite: {'Yes' if cocktail['is_favorite'] else 'No'}\n"
            f"Personal Notes: {cocktail.get('personal_notes', 'None')}"
        )
        # Ask to add to favorites and personal notes
        Label(detail_popup, text=details, bg=THEME_COLOR, fg=TEXT_COLOR, font=FONT_BODY, justify="left").pack(pady=10)
        # Use Radio buttons for explicit Yes/No choice
        Label(detail_popup, text="Add to Favorites?", bg=THEME_COLOR, fg=TEXT_COLOR, font=FONT_BODY).pack(pady=10)
        self.is_favorite_var = BooleanVar(value=cocktail["is_favorite"])
        Radiobutton(detail_popup, text="Yes", variable=self.is_favorite_var, value=True, bg=THEME_COLOR, fg=TEXT_COLOR,
                    font=FONT_BODY, selectcolor=BUTTON_COLOR_SECONDARY).pack(anchor="w")
        Radiobutton(detail_popup, text="No", variable=self.is_favorite_var, value=False, bg=THEME_COLOR, fg=TEXT_COLOR,
                    font=FONT_BODY, selectcolor=BUTTON_COLOR_SECONDARY).pack(anchor="w")

        Label(detail_popup, text="Add a Personal Note:", bg=THEME_COLOR, fg=TEXT_COLOR, font=FONT_BODY).pack(pady=10)
        personal_note = Entry(detail_popup, width=40,
                              bg="#2E2E2E",
                              fg=TEXT_COLOR,
                              insertbackground=TEXT_COLOR)
        personal_note.insert(0, cocktail.get("personal_notes", ""))  # Pre-fill existing note
        personal_note.pack()

        Button(
            detail_popup,
            text="Save",
            command=lambda: self.save_additional_updates(cocktail_name, self.is_favorite_var.get(), personal_note.get(),
                                                         detail_popup),
            bg=BUTTON_COLOR_PRIMARY,
            fg=TEXT_COLOR,
            font=FONT_BUTTON,
        ).pack(pady=20)

    def save_additional_updates(self, cocktail_name, is_favorite, personal_note, popup):
        """
        Saves the favorite status and personal note for a cocktail.
        """
        self.manager.edit_cocktail(cocktail_name, {"is_favorite": is_favorite, "personal_notes": personal_note})
        messagebox.showinfo(title="Success", message=f"Updates saved for '{cocktail_name}'!")
        popup.destroy()
