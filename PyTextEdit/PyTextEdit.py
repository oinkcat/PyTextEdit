# coding: utf-8

from Tkinter import *
import tkFileDialog as dialogs
import tkMessageBox as msgs
import os.path as path

class SimpleTextEditorApp:
    ''' Simple text editor application '''

    WINDOW_TITLE = u'Text editor'

    def __init__(self):
        ''' Initialize data and create UI '''

        self.wnd = None
        self.modified = False
        self.txt = None
        self.create_ui()

    def run(self):
        ''' Start application's event loop '''

        mainloop()

    def create_ui(self):
        ''' Create application GUI '''

        self.wnd = Tk()
        self.wnd.title(SimpleTextEditorApp.WINDOW_TITLE)
        # Subscribe to window close message
        self.wnd.protocol('WM_DELETE_WINDOW', self.exit)

        # Create menu
        main_menu = Menu(self.wnd)
        file_menu=Menu(main_menu,tearoff=0)
        file_menu.add_command(label=u'New', command=self.new_file)
        file_menu.add_command(label=u'Open...', command=self.open_file)
        file_menu.add_command(label=u'Save as...', command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label=u'Exit', command=self.exit)
        main_menu.add_cascade(label=u'File', menu=file_menu)
        self.wnd.config(menu=main_menu)

        # Create text editing box with scrollbar and put into layout
        self.txt = Text(self.wnd, width=100, height=40)
        yscrollbar = Scrollbar(self.wnd, orient=VERTICAL, command=self.txt.yview)
        yscrollbar.pack(side=RIGHT, fill=Y)
        self.txt['yscrollcommand'] = yscrollbar.set
        self.txt.bind('<<Modified>>', self.set_modified)
        self.txt.pack(fill=BOTH, anchor=S, expand=YES)

    def exit(self):
        ''' Exit application '''

        if self.ask_save_if_modified():
            self.wnd.destroy()

    def ask_save_if_modified(self):
        ''' Ask user to save modified file '''

        can_continue = True
        if self.modified:
            answer = msgs.askyesnocancel(u'Text has been modified', 
                                         u'Text has been modified. Save changes?')
            if answer == True:
                can_continue = self.save_file()
            else:
                can_continue = answer is not None
        return can_continue

    def clear(self):
        ''' Clear all text in textbox '''

        self.txt.delete('1.0', END)
        self.clear_modified()

    def new_file(self):
        ''' Initialize new text file '''

        if self.ask_save_if_modified():
            self.clear()

    def open_file(self):
        ''' Open existing text file '''

        if self.ask_save_if_modified():
            file_name = dialogs.askopenfilename(
                title=u'Open text file',
                filetypes=[(u'Plain text files', '*.txt')]
                )
            if path.exists(file_name):
                self.clear()
                with open(file_name) as file_to_read:
                    text = file_to_read.read()
                self.txt.insert('1.0', text)
                self.txt.mark_set('insert', '1.0')
                # Clear modified flag
                self.clear_modified()

    def save_file(self):
        ''' Save file to file system '''

        saved = False
        if self.modified:
            file_name = dialogs.asksaveasfilename(
                title=u'Save text file',
                filetypes=[(u'Plain text files', '*.txt')],
                defaultextension='.txt'
                )

            # Save all text from editing box to file
            text = self.txt.get('1.0', END)
            with open(file_name, 'w') as file_to_write:
                file_to_write.write(text)
            saved = True
            self.clear_modified()
        return saved

    def clear_modified(self):
        ''' Clear text modification flag '''

        self.txt.edit_modified(False)
        self.modified = False

    def set_modified(self, event):
        ''' Set text modification flag '''

        self.modified = True

# Entry point
if __name__ == '__main__':
    SimpleTextEditorApp().run()