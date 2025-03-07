import tkinter as tk
import YtDlpLogger
from PIL import ImageTk

import logging
logging.basicConfig(
    filename='soup.log',
    filemode='w',
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s %(name)s %(message)s')

LOGGER=logging.getLogger(__name__)

BGCOLOR= "#3d6477"
DEFAULTFONT="TkMenuFont"

# initiallize app
root = tk.Tk()
root.title('ASDF')

# Tcl (Tool Command Language) https://www.tcl-lang.org/
root.eval("tk::PlaceWindow . center")

# Frame 1
frame1 = tk.Frame(root, width=500, height=600, bg=BGCOLOR)
frame1.grid(row=0, column=0, sticky="nesw")
# Prevent child from modifing parent settings
frame1.pack_propagate(False)

# frame1 widgets
logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo_bottom.png")
logo_widget = tk.Label(frame1, image=logo_img, bg=BGCOLOR)
logo_widget.image = logo_img
logo_widget.grid(row=1, column=1)

tk.Label(
    frame1, 
    text="Link here:",
    bg=BGCOLOR,
    fg="white",
    font=(DEFAULTFONT, 13)
    ).grid(row=2, column=1, pady=23)

videoLink = tk.StringVar(None)
textBox = tk.Entry(
    frame1, 
    textvariable=videoLink, 
    width=79,
    font=(DEFAULTFONT, 13)
    )
textBox.grid(row=2, column=2, padx=23)

# create button widget
downloadBtn = tk.Button(
    frame1,
    text="Download!",
    font=(DEFAULTFONT, 20),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    width=17,
    command=lambda:downloadStuff()
    )
downloadBtn.grid(row=3, columnspan=5, pady=20)

def downloadStuff():
    downloadBtn.configure(state="disabled")
    downloadBtn.config(text="yah")

# run app
root.mainloop()

print("Done")

