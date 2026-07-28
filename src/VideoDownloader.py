import os
import sys
from pathlib import Path
# disable yt-dlp plugin discovery because we add them manually
os.environ["YTDLP_NO_PLUGINS"] = "1"
import math
from yt_dlp import YoutubeDL
from pprint import pprint
import traceback
import logging

# Get path where app was launch
if getattr(sys, "frozen", False):
    # PyInstaller executable or .app bundle
    app_dir = Path(sys.executable)
    print(1)
    print(app_dir)
    print("sys plat:")
    print(sys.platform)
    print("app_dir.parent.name:")
    print(app_dir.parent.name)
    # macOS .app bundle
    if sys.platform == "darwin":
        app_dir = app_dir.parents[3]  # folder containing MyApp.app
        print(2)
        print(app_dir)
else:
    app_dir = Path(__file__).resolve().parent
    print(3)
    print(app_dir)

print("App Dir: ")
print(app_dir)

# Configure the logger
# os.makedirs(app_dir, exist_ok=True)
log_file = os.path.join(app_dir, "soup.log")

logging.basicConfig(
    filename=log_file,
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

from YtDlpLogger import YtDlpLogger

import tkinter as tk
import tkinter.messagebox as tkMessageBox
from PIL import ImageTk

# Custom extractor. Need more research to add to offical yt-dlp repo
from custom_extractor.tvbanywhere import TVBAnywhereIE

try:
    LOGGER=logging.getLogger(__name__)

    LOGGER.info("cwd = %s", os.getcwd())
    LOGGER.info("sys.executable = %s", sys.executable)
    LOGGER.info("__file__ = %s", __file__ if "__file__" in globals() else "frozen")
    LOGGER.info("_MEIPASS = %s", getattr(sys, "_MEIPASS", None))

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

    # LOGGER.info("Done")
    # print('Some videos failed to download' if errorCode else 'All videos successfully downloaded')

    BGCOLOR= "#3d6477"
    DEFAULTFONT="TkMenuFont"
    i = 0

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
    def resource_path(relative_path):
        """
        Return absolute path to bundled resources.

        Works for:
        - Normal Python execution
        - PyInstaller one-file builds
        - PyInstaller .app bundles on macOS
        """
        if getattr(sys, "frozen", False):
            # PyInstaller bundle
            base_path = getattr(
                sys,
                "_MEIPASS",
                os.path.dirname(sys.executable)
            )
        else:
            # Running from source
            base_path = os.path.dirname(
                os.path.abspath(__file__)
            )

        return os.path.join(base_path, relative_path)

    logo_img = ImageTk.PhotoImage(
        file=resource_path("assets/RRecipe_logo_bottom.png")
    )
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

    def my_hook(d):
        if d['status'] == 'finished':
            downloadBtn.config(text="Download!", state="normal")
        elif d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')

            if total:
                downloaded = d.get('downloaded_bytes', 0)
                p = math.floor(downloaded / total * 100)
                downloadBtn.config(text=f"Wait... {p}%")
            else:
                downloadBtn.config(text="Wait...")

            downloadBtn.config(state="disabled")

        root.update()

    def downloadVideo(url):
        ydl_opts = {
            'logger': YtDlpLogger(),
            'progress_hooks': [my_hook],
            'format': 'bestvideo+bestaudio[language=vi]/best',
            'outtmpl': os.path.join(
                app_dir,
                '%(title)s [%(id)s].%(ext)s',
            ),
            # For mac when launching app from "Finder"
            'ffmpeg_location': '/opt/homebrew/bin',
        }

        ydl = YoutubeDL(ydl_opts)

        # Create and register custom extractor
        extractor = TVBAnywhereIE()
        extractor.set_downloader(ydl)

        LOGGER.info("Custom extractor: %s", extractor.ie_key())
        LOGGER.info("URL matches extractor: %s", extractor.suitable(url))

        print("Custom extractor:", extractor.ie_key())
        print("URL matches:", extractor.suitable(url))

        try:
            # Bypass yt-dlp extractor selection and call our extractor directly
            info = extractor.extract(url)

            # Let yt-dlp handle the actual download
            ydl.process_ie_result(info, download=True)
            return True

        except Exception:
            LOGGER.exception("Download failed")
            raise

    def downloadStuff():
        downloadBtn.configure(state="disabled")
        downloadBtn.config(text="Wait...")
        root.update()

        try:
            ret = downloadVideo(videoLink.get())

            if ret:
                tkMessageBox.showinfo(title="Yah!", message="download good, find file in the same folder of this program")
            else:
                tkMessageBox.showerror(title="Uh oh!", message="download fail, see log for more details")

            downloadBtn.config(text="Download!", state="normal")

        except Exception as e:
            LOGGER.exception(e)
            downloadBtn.config(text="Download!", state="normal")
            tkMessageBox.showerror(title="Uh oh!", message="Something really bad happened, see log for more details")

    # run app
    root.mainloop()
except Exception:
    LOGGER.exception("Startup failed")
    raise
