import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import check_legality as cl
import threading
class AppWindow:
    def __init__(self, master):
        self.master = master

        #   basic window settings
        self.master.title("Deck Legality Checker")
        self.master.resizable(False, False)
        self.master.geometry("500x450")

        #   set all GUI elements
        self.set_txtbox()
        self.set_dropdown() 
        self.set_checkbox()
        self.set_open_button()

    #   applies set textbox settings for the window application
    def set_txtbox(self):
        self.txtbox = tk.Text(self.master, width=50, height=20)
        self.txtbox.pack(pady=20)
        self.set_colours()

    #   assign colours to the legality types
    def set_colours(self):
        self.txtbox.tag_config('Legal', foreground='green')
        self.txtbox.tag_config('NotLegal', foreground='gray40')
        self.txtbox.tag_config('Banned', foreground='red')
        self.txtbox.tag_config('Restricted', foreground='DarkOrange1')

    #   applies the set checkbox parameters for the ignore-sidezone element
    def set_checkbox(self):
        self.ignore_side = tk.BooleanVar()
        self.checkbox_1 = tk.Checkbutton(
            self.master, 
            text='Ignore Sideboard', 
            variable=self.ignore_side, 
            onvalue=True, 
            offvalue=False
        )
        self.checkbox_1.pack()

    #   applies the set parameters for the button-element responsible- 
    #   for opening a .COD file 
    def set_open_button(self):
        self.button = ttk.Button(
            self.master, 
            text='Open .COD file containing deck info',
            command=self.get_file
        )
        self.button.pack(expand=True)

    #   applies the set parameters for the dropdown list of game formats
    def set_dropdown(self):
        self.dropdown = tk.StringVar(self.master)

        #   the game formats available for checking
        self.drop_options = ["Standard", "Commander", "Legacy", "Modern", "Vintage"]

        self.dropdown.set(self.drop_options[0]) #   set the default format to Standard
        
        self.w = tk.OptionMenu(self.master, self.dropdown, *self.drop_options)
        self.w.pack()

    def get_file(self):
        file_types = {
            ('text files', '*.txt'),
            ('COD file ', '*.COD')
        }

        self.file = filedialog.askopenfilename()

        if self.file != "":  #   assuming the user has provided a file
            thread = threading.Thread(target=self.get_format_legality_pairs)
            thread.start()

    #   uses the check_legality and mtgsdk library to-
    #   retrieve information regarding the cards
    def get_format_legality_pairs(self):
        self.write_output({'Loading': 'Loading'})
        output = cl.main(self.file, self.dropdown.get(), self.ignore_side.get())
        self.write_output(output)

    #   writes the results of the check from check_legality into the AppWindow textbox
    def write_output(self, format_legality_pairs):

        self.txtbox.delete('1.0', tk.END)   #   clear the textbox

        for pair in format_legality_pairs:
            self.txtbox.insert(tk.END, pair + ": ") #   first write the name of the card
            self.txtbox.insert(
                tk.END, 
                format_legality_pairs[pair] + "\n", #   write the legality of the card with colour code
                format_legality_pairs[pair].replace(" ", "")
            )

if __name__ == '__main__':
    root = tk.Tk()
    main_application = AppWindow(root)
    root.mainloop()