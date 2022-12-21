import contextlib
import tkinter
import tkinter.messagebox
import customtkinter
import pyautogui
import tkinter.filedialog as fd
import tkinter.messagebox as showinfo
from PIL import Image

# Modes: 'System' (standard), 'Dark', 'Light'
customtkinter.set_appearance_mode('System')
# Themes: 'blue' (standard), 'green', 'dark-blue'
customtkinter.set_default_color_theme('dark-blue')


class App(customtkinter.CTk):

    WIDTH = 1400
    HEIGHT = 750
    MINWIDTH = 800
    MINHEIGHT = 500

    def __init__(self):
        super().__init__()

        self.iconbitmap(default='images\main_icon.ico')
        self.title('Text Editor')
        self.geometry(f'{App.WIDTH}x{App.HEIGHT}')
        self.minsize(App.MINWIDTH, App.MINHEIGHT)
        # call .on_closing() when app gets closed
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        self.file_path = None
        self.menu_font = ('Arial', -16)
        self.textbox_fontstyle = 'Roboto'
        self.textbox_fontsize = 13
        self.filetypes = (
            ('All files', '*.*'),
            ('File di testo', '*.txt'),
            ('Python', '*.py'),
            ('Javascript', '*.js'),
            ('CSV', '*.csv')
        )
        self.list_default_fontsize = [
            '8', '9', '10', '11', '12', '13', '14', '18', '24', '30', '36', '48', '72', '96']

        open_file_icon = customtkinter.CTkImage(
            dark_image=Image.open('images/open_file.png'), size=(20, 20))
        new_file_icon = customtkinter.CTkImage(
            dark_image=Image.open('images/new_file.png'), size=(20, 20))
        undo_icon = customtkinter.CTkImage(
            dark_image=Image.open('images/undo.png'), size=(20, 20))
        redo_icon = customtkinter.CTkImage(
            dark_image=Image.open('images/redo.png'), size=(20, 20))
        save_icon = customtkinter.CTkImage(
            dark_image=Image.open('images/save.png'), size=(20, 20))
        plus_icon = customtkinter.CTkImage(
            dark_image=Image.open('images/plus.png'), size=(12, 12))
        minus_icon = customtkinter.CTkImage(
            dark_image=Image.open('images/minus.png'), size=(12, 12))

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ============ create two frames ============

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky='nswe')

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky='nswe', padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (9x19) deifining the empty spaces
        self.frame_left.grid_rowconfigure(0, weight=1)
        self.frame_left.grid_rowconfigure(2, weight=1)
        self.frame_left.grid_rowconfigure(4, weight=1)
        self.frame_left.grid_rowconfigure(6, weight=1)
        self.frame_left.grid_rowconfigure(8, weight=1)
        self.frame_left.grid_rowconfigure(10, weight=1)
        self.frame_left.grid_rowconfigure(12, weight=1)
        self.frame_left.grid_rowconfigure(14, weight=1)
        self.frame_left.grid_rowconfigure(16, weight=10)
        self.frame_left.grid_rowconfigure(18, weight=1)

        self.frame_left.grid_columnconfigure(0, weight=1)
        self.frame_left.grid_columnconfigure(4, weight=1)
        self.frame_left.grid_columnconfigure(8, weight=1)

        # row 1
        self.title_label = customtkinter.CTkLabel(master=self.frame_left,
                                                  text='TEXT EDITOR',
                                                  font=('Roboto Medium', -16))
        self.title_label.grid(row=1, column=1, columnspan=7, padx=10)

        # row 3
        self.font_optionmenu = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                           values=[
                                                               'Roboto', 'Arial', 'Calibri', 'Comic Sans MS', 'Lucida Console'],
                                                           command=self.update_font_style)
        self.font_optionmenu.grid(row=3, column=1, columnspan=7, padx=10)

        # row 5
        self.fontsize_var = customtkinter.StringVar(value='13')

        self.fontsize_combobox = customtkinter.CTkComboBox(
            master=self.frame_left, values=self.list_default_fontsize, command=self.update_font_size, variable=self.fontsize_var, justify='center', width=60)
        self.fontsize_combobox.bind('<Return>', self.update_font_size)
        self.fontsize_combobox.grid(
            row=5, column=3, columnspan=3)

        self.decrease_fontsize_button = customtkinter.CTkButton(
            master=self.frame_left, text='', image=minus_icon, command=self.decrease_font_size, width=30)
        self.decrease_fontsize_button.grid(
            row=5, column=1, columnspan=2, padx=10)

        self.increase_fontsize_button = customtkinter.CTkButton(
            master=self.frame_left, text='', image=plus_icon, command=self.increase_font_size, width=30)
        self.increase_fontsize_button.grid(
            row=5, column=6, columnspan=2, padx=10)

        # row 7
        self.openfile_button = customtkinter.CTkButton(master=self.frame_left,
                                                       text='Apri File',
                                                       command=self.open_file,
                                                       image=open_file_icon,
                                                       anchor='w')
        self.openfile_button.grid(row=7, column=1, columnspan=7, padx=10)

        # row 9
        self.newfile_button = customtkinter.CTkButton(master=self.frame_left,
                                                      text='Nuovo File',
                                                      command=self.ask_save_file,
                                                      image=new_file_icon,
                                                      anchor='w')
        self.newfile_button.grid(row=9, column=1, columnspan=7, padx=10)

        # row 11
        self.undo_button = customtkinter.CTkButton(master=self.frame_left,
                                                   text='',
                                                   image=undo_icon,
                                                   command=self.undo,
                                                   width=60)
        self.undo_button.grid(
            row=11, column=1, columnspan=4, padx=10, sticky='w')

        self.redo_button = customtkinter.CTkButton(master=self.frame_left,
                                                   text='',
                                                   image=redo_icon,
                                                   command=self.redo,
                                                   width=60)
        self.redo_button.grid(
            row=11, column=4, columnspan=4, padx=10, sticky='e')

        # row 13
        self.save_button = customtkinter.CTkButton(master=self.frame_left,
                                                   text='Salva',
                                                   image=save_icon,
                                                   command=self.save_file,
                                                   anchor='w')
        self.save_button.grid(row=13, column=1, columnspan=7, padx=10)

        # row 15
        self.autosave_var = customtkinter.StringVar(value='off')
        self.autosave_switch = customtkinter.CTkSwitch(
            master=self.frame_left, text='Auto Save', variable=self.autosave_var, onvalue='on', offvalue='off')
        self.autosave_switch.grid(row=15, column=1, columnspan=7, padx=10)

        # row 17
        self.theme_optionmenu = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                            values=[
                                                                'Light', 'Dark', 'System'],
                                                            command=self.change_appearance_mode)
        self.theme_optionmenu.grid(row=17, column=1, columnspan=7, padx=10)

        # ============ frame_right ============

        # configure grid layout (1x1)
        self.frame_right.rowconfigure(1, weight=1)
        self.frame_right.columnconfigure(1, weight=1)

        # configure the text box
        self.main_textbox = customtkinter.CTkTextbox(
            master=self.frame_right, undo=True, activate_scrollbars=False)
        # bind commands to the text box
        self.main_textbox.bind('<Any-KeyRelease>', self.auto_save)
        self.main_textbox.bind('<Control-KeyRelease-s>', self.save_file)
        self.main_textbox.bind('<Control-KeyRelease-o>', self.open_file)
        self.main_textbox.bind('<Control-KeyRelease-n>', self.ask_save_file)
        # place the text box in the grid
        self.main_textbox.grid(row=0, column=0, columnspan=2,
                               rowspan=8, pady=20, padx=20, sticky='nsew')

        # configure the scrollbars
        self.ctk_textbox_yscrollbar = customtkinter.CTkScrollbar(
            master=self.frame_right, command=self.main_textbox.yview)
        self.ctk_textbox_yscrollbar.grid(
            row=0, column=1, rowspan=2, pady=20, sticky='nse')
        self.main_textbox.configure(
            yscrollcommand=self.ctk_textbox_yscrollbar.set)

        self.ctk_textbox_xscrollbar = customtkinter.CTkScrollbar(
            master=self.frame_right, command=self.main_textbox.xview, orientation='horizontal')
        self.ctk_textbox_xscrollbar.grid(
            row=0, column=1, rowspan=2, padx=20, sticky='sew')
        self.main_textbox.configure(
            xscrollcommand=self.ctk_textbox_xscrollbar.set, wrap='none')

        # set default values
        self.font_optionmenu.set('Font')
        self.theme_optionmenu.set('Tema')

    # ============ file functions ============
    # update the font style of the text box when the font option menu is changed
    def update_font_style(self, new_font_style: str) -> None:
        self.textbox_fontstyle = new_font_style
        self.main_textbox.configure(
            font=(self.textbox_fontstyle, self.textbox_fontsize))

    # update the font size of the text box when the font size combo box is changed
    def update_font_size(self, *args) -> None:
        self.textbox_fontsize = int(self.fontsize_var.get())
        self.main_textbox.configure(
            font=(self.textbox_fontstyle, self.textbox_fontsize))

    # increase the font size of the text box of 1 when the + button is pressed
    def increase_font_size(self, *args) -> None:
        self.fontsize_var.set(str(self.textbox_fontsize + 1))
        self.update_font_size()

    # decrease the font size of the text box of 1 when the - button is pressed
    def decrease_font_size(self, *args) -> None:
        self.fontsize_var.set(str(self.textbox_fontsize - 1))
        self.update_font_size()

    # read the text from a file
    def read_text_from_file(self, percorso: str) -> str:
        with open(percorso, 'r') as file:
            txt = file.read()
        return txt

    # auto save the file when a key is pressed
    def auto_save(self, pressed_key) -> None:
        # check if pressed_key is a character
        if pressed_key.char != '':
            if self.file_path != None and self.autosave_var.get() == 'on':
                self.save_file()
                return
            self.title(f'*{self.file_path} - Text Editor')

    # saves the file
    def save_file(self, *args) -> None:
        self.title(f'{self.file_path} - Text Editor')
        if self.file_path != None:
            with open(self.file_path, 'w') as file:
                file.truncate(0)
                file.write(self.main_textbox.get(0.0, 'end'))
            return
        f = fd.asksaveasfile(mode='w',
                             title='Save file',
                             initialdir='/',
                             filetypes=self.filetypes,
                             defaultextension=self.filetypes)
        if f != None:  # asksaveasfile return "None" if dialog closed with "cancel".
            f.write(self.main_textbox.get(0.0, 'end'))
            f.close()

    # ask if the user wants to save the file before opening a new one
    def ask_save_file(self, *args) -> None:
        if self.file_path is None:
            return
        with open(self.file_path, 'r') as file:
            txt = file.read()
        if txt.strip() != self.main_textbox.get(0.0, 'end').strip():
            current_text = self.main_textbox.get(0.0, 'end')
            current_text = ''.join(current_text.split())
            if current_text != '' and tkinter.messagebox.askyesno('Text Editor', 'Salvare le modifiche del file?'):
                self.save_file()
            self.main_textbox.delete('0.0', 'end')
            self.file_path = None

    # open a file and put its text in the text box
    def open_file(self, *args) -> None:
        self.ask_save_file()
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=self.filetypes)
        if filename != '':
            self.file_path = filename
            self.main_textbox.delete('0.0', 'end')
            self.main_textbox.insert(
                '0.0', self.read_text_from_file(self.file_path))
        self.title(f'{self.file_path} - Text Editor')

    # ============ edit functions ============
    # redo the last action
    def redo(self, *args) -> None:
        pyautogui.hotkey('ctrl', 'y')

    # undo the last action
    def undo(self, *args) -> None:
        pyautogui.hotkey('ctrl', 'z')

    # ============ view functions ============
    # change the appearance mode of the app (dark or light)
    def change_appearance_mode(self, new_appearance_mode) -> None:
        customtkinter.set_appearance_mode(new_appearance_mode)

    # close the app when the window is closed
    def on_closing(self, event=0) -> None:
        self.ask_save_file()
        self.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()
