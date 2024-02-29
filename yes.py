import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import webbrowser
import random

class BoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Box Generator")
        self.current_button = None
        self.saved_texts = {"P2, P7, P8": {}, "P3": {}, "P4": {}}

        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Create loading screen
        self.loading_frame = tk.Frame(root, bg="black")
        self.loading_frame.grid(row=0, column=0, sticky="nsew")
        self.loading_frame.grid_rowconfigure(0, weight=1)
        self.loading_frame.grid_columnconfigure(0, weight=1)

        # Create loading circle
        self.loading_circle = ttk.Progressbar(self.loading_frame, mode="indeterminate", length=100)
        self.loading_circle.pack()

        # After 2 seconds, call method to fade in start button
        self.root.after(2000, self.fade_in_start_button)

    def fade_in_start_button(self):
        # Destroy loading elements
        self.loading_circle.stop()
        self.loading_circle.destroy()

        # Create start button
        self.start_button = tk.Button(self.loading_frame, text="Start", command=self.show_main_interface)
        self.start_button.configure(font=("Times New Roman", 16))
        self.start_button.pack(pady=10)

    def show_main_interface(self):
        # Destroy loading frame and start button
        self.loading_frame.destroy()
        self.start_button.destroy()

        # Calculate padding
        padding = 20

        # Configure root to fill the screen with padding
        self.root.geometry(f"{self.root.winfo_screenwidth() - padding*2}x{self.root.winfo_screenheight() - padding*2}+{padding}+{padding}")

        # Create main interface elements
        self.frame = tk.Frame(self.root, bg="light green")
        self.frame.pack(expand=True, fill="both")

        self.create_top_buttons()
        self.create_text_boxes()

        # Select section 1
        self.show_text_boxes("P2, P7, P8")

    def create_top_buttons(self):
        self.top_frame = tk.Frame(self.frame, bg="light green")
        self.top_frame.pack(side="top", fill="x")

        self.button1 = tk.Button(self.top_frame, text="P2, P7, P8", command=lambda: self.show_text_boxes("P2, P7, P8"))
        self.button1.pack(side="left", padx=10, pady=5)

        self.button2 = tk.Button(self.top_frame, text="P3", command=lambda: self.show_text_boxes("P3"))
        self.button2.pack(side="left", padx=10, pady=5)

        self.button3 = tk.Button(self.top_frame, text="P4", command=lambda: self.show_text_boxes("P4"))
        self.button3.pack(side="left", padx=10, pady=5)

    def create_text_boxes(self):
        self.text_frame = tk.Frame(self.frame, bg="light green")
        self.text_frame.pack(expand=True, fill="both")

        self.text_entries = {}
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day in days_of_week:
            label = tk.Label(self.text_frame, text=day, bg="light blue")
            label.grid(row=days_of_week.index(day), column=0, padx=5, pady=5)
            entry = tk.Entry(self.text_frame, font=("Times New Roman", 12))
            entry.grid(row=days_of_week.index(day), column=1, padx=5, pady=5)
            self.text_entries[day] = entry

        self.generate_button = tk.Button(self.frame, text="Generate", command=self.generate_text)
        self.generate_button.pack(side="bottom", pady=10)

    def show_text_boxes(self, button_num):
        if self.current_button:
            self.save_text(self.current_button)
        self.update_text_boxes(button_num)
        self.current_button = button_num
        messagebox.showinfo("Info", f"You're editing periods {button_num}")

    def update_text_boxes(self, button_num):
        for day, entry in self.text_entries.items():
            entry.delete(0, "end")
            if day in self.saved_texts[button_num]:
                entry.insert(0, self.saved_texts[button_num][day])

    def save_text(self, button_num):
        self.saved_texts[button_num] = {}
        for day, entry in self.text_entries.items():
            text = entry.get()
            if text:
                self.saved_texts[button_num][day] = text

    def generate_text(self):
        if not self.current_button:
            messagebox.showwarning("Warning", "Please select a section before generating text.")
            return

        self.save_text(self.current_button)  # Save current section

        generated_text = ""
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day in days_of_week:
            generated_text += f"\n-- {day} --\n"
            for section_num in self.saved_texts.keys():
                generated_text += f"{section_num}: {self.saved_texts[section_num].get(day, '')}\n"

        messagebox.showinfo("Generated Text", "Generated Text:\n\n" + generated_text)

        # Write generated text to a file
        filename = "generated_text.txt"
        with open(filename, "w") as file:
            file.write(generated_text)

        # Open file
        webbrowser.open(filename)

if __name__ == "__main__":
    root = tk.Tk()
    app = BoxApp(root)
    root.mainloop()
