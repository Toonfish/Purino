import tkinter as tk
import tkinter.ttk as ttk
import settings
from PIL import Image, ImageTk


class Toplevel(tk.Toplevel):
    def __init__(self, title="", *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.config(bg=settings.gui_bg_color)
        if title != "":
            self.title(title)


class Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.config(bg=settings.gui_bg_color)


class Button(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.config(bg=settings.gui_button_color, activebackground=settings.gui_abg_color, borderwidth=1,
                    fg=settings.gui_text_color, activeforeground=settings.gui_text_color)
        self.bind('<Next>', lambda e: self.tk_focusNext().focus())
        self.bind('<Return>', lambda e: self.tk_focusNext().focus())
        self.bind('<Prior>', lambda e: self.tk_focusPrev().focus())


class Label(tk.Label):
    def __init__(self, *args, **kwargs):
        tk.Label.__init__(self, *args, **kwargs)
        self.config(bg=settings.gui_bg_color, fg=settings.gui_text_color)


class Text(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.bind('<Next>', lambda e: self.tk_focusNext().focus())
        self.bind('<Return>', lambda e: self.tk_focusNext().focus())
        self.bind('<Prior>', lambda e: self.tk_focusPrev().focus())
        self.bind('<FocusOut>', lambda e: self.strip_self())

    def strip_self(self):
        to_insert = self.get(1.0, tk.END).strip()
        self.delete(1.0, tk.END)
        self.insert(1.0, to_insert)

    def read(self):
        return self.get(1.0, tk.END).strip()

    def clear(self):
        self.delete(1.0, tk.END)


class TextFrame(Frame):
    def __init__(self, master, name, width=20, height=1, *args, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.label = Label(self, text=name)
        self.text = Text(self, width=width, height=height)
        self.label.grid(row=0, column=0, **kwargs)
        self.text.grid(row=1, column=0, **kwargs)
        self.config(bg=settings.gui_bg_color)

    def strip_self(self):
        self.text.strip_self()

    def read(self):
        return self.text.read()

    def clear(self):
        self.text.clear()


class CheckButton(tk.Checkbutton):
    def __init__(self, *args, **kwargs):
        tk.Checkbutton.__init__(self, *args, **kwargs)
        self.state = tk.IntVar()
        self.config(bg=settings.gui_bg_color, fg=settings.gui_text_color, variable=self.state)
        self.bind('<Next>', lambda e: self.tk_focusNext().focus())
        self.bind('<Return>', lambda e: self.tk_focusNext().focus())
        self.bind('<Prior>', lambda e: self.tk_focusPrev().focus())

    def strip_self(self):
        self.deselect()

    def read(self):
        return self.state.get()


class CheckButtonFrame(Frame):
    def __init__(self, master, name, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.label = Label(self, text=name, *args, **kwargs)
        self.check = CheckButton(self, *args, **kwargs)
        self.label.grid(row=0, column=1, **kwargs)
        self.check.grid(row=0, column=0, **kwargs)
        self.config(bg=settings.gui_bg_color)

    def strip_self(self):
        self.check.strip_self()

    def read(self):
        return self.check.read()

    def clear(self):
        self.check.deselect()


class AutocompleteCombobox(tk.ttk.Combobox):
    def __init__(self, master, completion_list, **kwargs):
        tk.ttk.Combobox.__init__(self, master, **kwargs)
        self._init_completion_list = completion_list
        self._completion_list = []
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self.bind('<Next>', lambda e: self.tk_focusNext().focus())
        self.bind('<Return>', lambda e: self.tk_focusNext().focus())
        self.bind('<Prior>', lambda e: self.tk_focusPrev().focus())
        self['values'] = self._completion_list  # Setup our popup menu

    def set_completion_list(self, completion_list):
        """Use our completion list as our drop down selection menu, arrows move through menu."""
        self._completion_list = sorted(completion_list, key=str.lower)  # Work with a sorted list
        self['values'] = self._completion_list  # update the popup menu

    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tk.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get_non_selection())
        # collect hits
        _hits = []
        for element in self._init_completion_list:
            if element.lower().startswith(self.get_non_selection().lower()):  # Match case insensitively
                _hits.append(element)
        self.set_completion_list(_hits)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def get_non_selection(self):  # stop an unwanted autocomplete when typing too quickly
        """use this to only limit the completion list to the non-selected part of the entry"""
        result = self.get()
        if self.selection_present() != 0:
            result = result[0:-len(self.selection_get())]
        return result

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(tk.INSERT), tk.END)
            self.position = self.index(tk.END)
        if event.keysym == "Left":
            if self.position < self.index(tk.END):  # delete the selection
                self.delete(self.position, tk.END)
            else:
                self.position -= 1  # delete one character
                self.delete(self.position, tk.END)
        if event.keysym == "Right":
            self.position = self.index(tk.END)  # go to end (no selection)
        if len(event.keysym) == 1:
            self.autocomplete()
            # No need for up/down, we'll jump to the popup
            # list at the position of the autocompletion

    def clear(self):
        self.delete(0, tk.END)

    def strip_self(self):
        to_insert = self.read()
        self.delete(0, tk.END)
        self.insert(0, to_insert)

    def read(self):
        return self.get().strip()


class ComboboxFrame(Frame):
    def __init__(self, master, name, completion_list, width=20, height=1, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.label = Label(self, text=name, **kwargs)
        self.ac_box = AutocompleteCombobox(self, completion_list, width=width, height=height, **kwargs)
        self.label.grid(row=0, column=0, **kwargs)
        self.ac_box.grid(row=1, column=0, **kwargs)
        self.config(bg=settings.gui_bg_color)

    def strip_self(self):
        self.ac_box.strip_self()

    def read(self):
        return self.ac_box.read()

    def clear(self):
        self.ac_box.clear()


class MultiImageCanvas(tk.Frame):
    """
    Returns a tk.Frame object containing a scrollable canvas showing all items from a list of images.
    The Canvas also automatically resizes itself upon changing the parent window size.
    """
    def __init__(self, gui_master, *args, **kwargs):
        tk.Frame.__init__(self, gui_master, *args, **kwargs)
        self.gui_master = gui_master
        self.image_path_list = []
        self.current_index = 0
        self.current_image = None  # needs to be saved so the GC doesn't delete it

        # region gui
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.canvas = tk.Canvas(self, bg=settings.gui_bg_color)
        self.canvas.grid(row=0, column=0, rowspan=4, columnspan=2)
        Button(self, text="Vorherige Seite", borderwidth=1, width=12, command=self.prev_page).grid(row=0, column=0)
        self.page_info = Label(self, text="Seite ? von ?", width=12)
        self.page_info.grid(row=1, column=0, )
        Button(self, text="Nächste Seite", borderwidth=1, width=12, command=self.next_page).grid(row=2, column=0)
        # endregion

        self.canvas.addtag_all("all")
        self.gui_master.bind("<Configure>", self.on_resize)
        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)

    def on_resize(self, event):
        self.canvas.config(width=self.gui_master.gui_master.winfo_width(), height=self.gui_master.gui_master.winfo_height())

    def new_image_list(self, image_paths):
        self.image_path_list = image_paths
        self.current_index = 0
        self.load_image()

    def load_image(self):
        self.canvas.delete("all")
        image_path = self.image_path_list[self.current_index]
        tmp_image = Image.open(image_path)
        tmp_image.thumbnail(settings.invoice_size, Image.BILINEAR)
        self.current_image = ImageTk.PhotoImage(tmp_image)
        self.canvas.create_image((self.current_image.width() / 2, self.current_image.height() / 2),
                                 image=self.current_image, tags="all", state=tk.NORMAL)
        self.page_info.config(
            text="Seite {} von {}".format(str(self.current_index + 1), str(len(self.image_path_list))))
        self.gui_master.title(image_path.split("/")[-1])

    def prev_page(self):
        if len(self.image_path_list) != 0:
            if self.current_index - 1 < 0:
                self.current_index = len(self.image_path_list) - 1
            else:
                self.current_index -= 1
            self.load_image()

    def next_page(self):
        if len(self.image_path_list) != 0:
            if self.current_index + 1 >= len(self.image_path_list):
                self.current_index = 0
            else:
                self.current_index += 1
            self.load_image()

    def get_current_page_path(self):
        return self.image_path_list[self.current_index]

    def scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)