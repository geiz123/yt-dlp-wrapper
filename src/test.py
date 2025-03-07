from yt_dlp import YoutubeDL
from pprint import pprint
import traceback
import logging
# Configure the logger
logging.basicConfig(
    filename='soup.log',
    filemode='w',
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s %(name)s %(message)s')
from YtDlpLogger import YtDlpLogger

import tkinter as tk
import tkinter.messagebox as tkMessageBox
from PIL import ImageTk

LOGGER=logging.getLogger(__name__)

# ydlOpts = \
# {'logger': YtDlpLogger(),
#  'extract_flat': 'discard_in_playlist',
#  'format': 'best/bestaudio/lang=en',
#  'listformats': True,
#  'fragment_retries': 10,
#  'ignoreerrors': 'only_download',
#  'postprocessors': [{'key': 'FFmpegConcat',
#                      'only_multi_video': True,
#                      'when': 'playlist'}],
#  'retries': 10}

URLS = ['https://www.youtube.com/watch?v=CAyWN9ba9J8']
# with YoutubeDL(ydlOpts) as ydl:
#     errorCode = ydl.download(URLS)

def my_hook(d):
    # pprint(d)

    if d['status'] == 'finished':
        # print('Done downloading, now converting ...')
        pass

def downloadVideo(url):
    '''Dowload the video from the `url`

    Extended description of function.

    Args:
        url (str): URL to a video

    Returns:
        int: Return code of `yt_dlp.download()`

    Raises:
        whatever `yt_dlp.download()` throws

    '''

    ydl_opts = {
        'logger': YtDlpLogger(),
        'progress_hooks': [my_hook],
        'format': 'best/bestaudio/lang=en',
        #'listformats': True,
        }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            return ydl.download(url)
        except Exception as e:
            # LOGGER.exception(e)
            # Rethrow the exception back up
            raise

# LOGGER.info("Done")
# print('Some videos failed to download' if errorCode else 'All videos successfully downloaded')

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

# Var that store the text from input box
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
    downloadBtn.config(text="Wait...")
    root.update()

    try:
        ret = downloadVideo(videoLink.get())

        if ret:
            tkMessageBox.showerror(title="Uh oh!", message="download fail, see log for more details")
        else:
            tkMessageBox.showinfo(title="Yah!", message="download good, find file in the same folder of this program")

        downloadBtn.config(text="Download!", state="normal")

    except Exception as e:
        LOGGER.exception(e)
        downloadBtn.config(text="Download!", state="normal")
        tkMessageBox.showerror(title="Uh oh!", message="Something really bad happened, see log for more details")

# run app
root.mainloop()
