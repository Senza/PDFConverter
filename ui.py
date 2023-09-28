from tkinter import *
from tkinter import ttk, font
from tkinter import filedialog, colorchooser
from tkinter.messagebox import *
import webview



class uiPdf:

    def __init__(self, window_width, window_height, func_add_items, func_convert_images):
        self.window_width = window_width
        self.window_height = window_height

        self.MAINCOLOR = '#26242f'
        self.SECONDARY_COLOR = '#292b2c'
        self.ACCENT_COLOR = '#eac025'
        self.TEXT_COLOR = '#f8f8f8'
        self.PROGRESS_COLOR = '#7FFFE8'

        self.func_add_items = func_add_items
        self.func_convert_images = func_convert_images

        print(type(self.func_add_items))




    def initialize_ui(self):

        window = Tk()

        window.title("PDF Converter")
        window_icon = PhotoImage(file="src/ICON.png")

        window.iconphoto(True,window_icon)

        screen_width = window.winfo_screenwidth();
        screen_height = window.winfo_screenheight();

        x = int((screen_width/2) - (self.window_width/2))
        y = int((screen_height/2) - (self.window_height/2))

        self.app_font = font.Font(family='Segoe UI Black', name='App font', size=12)

        window.geometry('{}x{}+{}+{}'.format(self.window_width, self.window_height, x, y))

        selection_frame = Frame(window, bg=self.SECONDARY_COLOR, height=50)
        center_canvas= Canvas(window)

        self.scrollbar = Scrollbar(center_canvas, orient='vertical', command=center_canvas.yview)
        self.scrollable_frame = Frame(center_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: center_canvas.configure(
                scrollregion=center_canvas.bbox("all")
            )
        )

        center_canvas.create_window((0,0), window=self.scrollable_frame, anchor='nw')
        center_canvas.configure(yscrollcommand=self.scrollbar.set, bg=self.MAINCOLOR)

        selection_frame.pack(side='top', fill='x')
        center_canvas.pack(side='left',  expand=True, fill='both')

        self.scrollbar.pack(side='right', fill='y')

        self.add_items_button = Button(selection_frame, 
                                    text='Add images', 
                                    borderwidth=0, 
                                    bg=self.ACCENT_COLOR, 
                                    fg=self.SECONDARY_COLOR,
                                    padx=20, 
                                    font=self.app_font,
                                    command=self.func_add_items)
        
        self.add_items_button.grid(row=0, column=0)

        self.convert_images_button = Button(selection_frame, 
                                            text='convert images', 
                                            borderwidth=0,
                                            bg=self.ACCENT_COLOR, 
                                            fg=self.SECONDARY_COLOR,
                                            padx=20, 
                                            font=self.app_font,
                                            command=self.func_convert_images)
        self.convert_images_button.grid(row=0, column=1)


        self.pages = Label(selection_frame, 
                            text='0 pages',
                            font=self.app_font,
                            bg=self.SECONDARY_COLOR,
                            fg=self.TEXT_COLOR,
                            width=10
                            )
        self.pages.grid(row=0, column=2)

        s = ttk.Style()
        s.theme_use('clam')
        s.configure("r.Horizontal.TProgressbar",  background=self.PROGRESS_COLOR,)
        self.progress_indicator = ttk.Progressbar(selection_frame, style="r.Horizontal.TProgressbar", orient="horizontal",
                        length=600, mode="determinate", maximum=100, value= 1)
        self.progress_indicator.grid(row=0, column=3, sticky= W + E)

        #----------Menu items----------------
        menu_bar = Menu(window)
        window.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label= "File", menu=file_menu)
        file_menu.add_command(label="New process", command=None)
        file_menu.add_command(label="Main window")

        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=None)

        window.mainloop()


    def update_progress_bar(self, total_task_completed, current_task_count):
        self.progress_indicator['value'] += 100/total_task_completed * current_task_count
        self.progress_indicator.update()

    def create_images_links(self, file, button_image, page_index, y):
        btn_links = Button(self.scrollable_frame, 
                    text= "page {}".format(page_index + 1), 
                    image=button_image, 
                    height= y,
                    padx=10,
                    pady=10, 
                    compound='left')
        btn_links.config(
            borderwidth=0,
            border=0,
            fg=self.TEXT_COLOR,
            bg=self.MAINCOLOR,
            font=self.app_font,
            command= lambda : self.modify_links(page_index, page_index, btn_links),
        )
        
        btn_links.grid(row=page_index, columnspan=3, sticky= N + S + W + E)


        
    
    def display_created_pdf(self, temp_file):
        webview.create_window('untitled.pdf', temp_file)
        webview.start()




    def update_pages_count(self, total_pages):
        is_plural = "s" if total_pages > 1 or total_pages == 0 else ""
        self.pages.config(text="{} page{}".format(total_pages, is_plural))



    
    def modify_links(self, page_index:int, link:str, button:Button):

        pop_action = Toplevel()

        pop_action.resizable(False, False)
        
        screen_width = pop_action.winfo_screenwidth();
        screen_height = pop_action.winfo_screenheight();

        x = int((screen_width/2) - (200))
        y = int((screen_height/2) - (120))

        pop_action.geometry('{}x{}+{}+{}'.format(400, 240, x, y))
        pop_action.config(bg=self.MAINCOLOR)
        pop_action.grab_set()



        Label(pop_action, 
                text="move page {} to".format(page_index + 1),
                font=self.app_font,
                fg=self.TEXT_COLOR,
                bg=self.MAINCOLOR,
                border=0,
                borderwidth=0,
                pady=10
                ).pack()

        entry_text = StringVar(pop_action)
        entry_text.set(value=str(page_index + 1))

        change_index_entry = Entry(pop_action, 
                                    borderwidth=0, 
                                    bg=self.SECONDARY_COLOR,
                                    fg=self.ACCENT_COLOR,
                                    font=self.app_font,
                                    textvariable=entry_text,
                                    justify='center'
                                    )
        
        change_index_entry.pack()

        move_index_button = Button(pop_action, text="Move page")
        move_index_button.config(
                    height=1,
                    width=10,
                    font=self.app_font,
                    bg=self.ACCENT_COLOR,
                    fg=self.TEXT_COLOR,
                    border=0,
                    borderwidth=0,
                )
        
        move_index_button.pack()

        Label(pop_action, 
        text="OR",
        pady=5,
        font=self.app_font,
        fg=self.TEXT_COLOR,
        bg=self.MAINCOLOR,
        border=0,
        borderwidth=0
        ).pack()

        delete_button = Button(pop_action, text="Delete page")
        delete_button.config(
                height=1,
                width=15,
                pady=10, 
                font=self.app_font,
                bg=self.SECONDARY_COLOR,
                fg=self.TEXT_COLOR,
                border=0,
                borderwidth=0,
                command= lambda : self.destory_button(button, pop_action, page_index)
            )
        delete_button.pack()
    
    def destory_button(self, button:Button, pop_action:Toplevel, page_index:int ):
        pop_action.destroy()
        button.destroy()
        self.scrollable_frame.update_idletasks()