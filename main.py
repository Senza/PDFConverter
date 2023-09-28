from ui import uiPdf as pdfUI
import os
import mimetypes
import sqlite3

from tkinter import PhotoImage, filedialog
from tkinter.messagebox import *
from PIL import Image




class App: 
    def __init__(self):
#-------------Constants----------
        self.TEMP_FILE = "src\\ImageToPDF.pdf"
        self.DATABASEFILEPATH = "src\\_DB.db"
        self.COLOR_MODE = 'RGB'

#----------Variables--------------
        self.images_link = []
        self.built_pdf_images_header = None
        self.built_pdf_images = []
        self.num_pages = 0
        self.images = []

#----------initialize app--------------
        self.IMAGE = tuple(self.get_extension_for_type("image"))
        self.initialize()


#----------------------------------------------------
    def set_ui(self, ui):
        self.ui = ui


#----------------------------------------------------
    def add_items(self):
        errors = 0
        files = filedialog.askopenfilenames(title="Select files to be converted",
                                            defaultextension="*png",
                                            file=[("Images", self.IMAGE)])
        
        if(files == None):
            return
        
        for file in files:  
            try:  
                img = PhotoImage(file=file)
                x = int(img.width() / 2)
                y = int(img.height() / 2)
                img = self.resizeImage(img, x, y)
                self.images.append(img)
                self.ui.create_images_links(file,self.images[self.num_pages],self.num_pages,y)
                self.images_link.append(file)
                self.num_pages += 1
                self.ui.update_progress_bar(len(files), self.num_pages)
                self.ui.update_pages_count(self.num_pages)
            except Exception as ex:
                errors += 1

        if errors > 0:
            showwarning("Warning", "An error occured while loading images")
            return
        total_files = len(files)
        if total_files == 0:
            return
        
        is_plural = "s" if total_files > 1 or total_files  == 0 else ""
        showinfo("Success!", "{} image{} added successfully".format(total_files, is_plural))



#----------------------------------------------------
    def convert_images(self):
        if(len(self.images) <= 0):
            showerror("Error!", "Please use the 'add images button' to add images......\n \
                        Add images and try again?")
            return;

        for index in range(0, len(self.images_link)):
            img = Image.open(self.images_link[index])

            if(index == 0):
                # global built_pdf_images_header
                self.built_pdf_images_header = img.convert(self.COLOR_MODE)
                continue
            
            other_img = img.convert(self.COLOR_MODE)
            self.built_pdf_images.append(other_img)

        self.built_pdf_images_header.save(self.TEMP_FILE, save_all=True, append_images = self.built_pdf_images)

        self.ui.display_created_pdf(self.TEMP_FILE)



#----------------------------------------------------
    def pdf_to_img(self, page, mat):
        pix = page.get_pixmap(matrix=mat)
        return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)



#----------------------------------------------------
    def initialize(self):
        if os.path.isfile(self.DATABASEFILEPATH) is False:
            open(self.DATABASEFILEPATH, 'w')

        con = sqlite3.connect(self.DATABASEFILEPATH)
        cur = con.cursor()


        cur.execute("CREATE TABLE IF NOT EXISTS IMGToPDF_Table ( id INTEGER PRIMARY KEY, photo BLOB NOT NULL, name TEXT NOT NULL,  location TEXT NOT NULL)")



#----------------------------------------------------
    def resizeImage(self, img, newWidth, newHeight):
        oldWidth = img.width()
        oldHeight = img.height()
        newPhotoImage = PhotoImage(width=newWidth, height=newHeight)
        for x in range(newWidth):
            for y in range(newHeight):
                xOld = int(x*oldWidth/newWidth)
                yOld = int(y*oldHeight/newHeight)
                rgb = '#%02x%02x%02x' % img.get(xOld, yOld)
                newPhotoImage.put(rgb, (x, y))
        return newPhotoImage


#----------------------------------------------------
    def get_extension_for_type(self, general_types):
        for ext in mimetypes.types_map:
            if mimetypes.types_map[ext].split('/')[0] == general_types:
                yield ext
        mimetypes.init()








if __name__ == '__main__':
    WINDOW_HEIGHT = 720
    WINDOW_WIDTH = 1240

    
    main = App()
    
    ui = pdfUI(window_width=WINDOW_WIDTH, 
                window_height= WINDOW_HEIGHT, 
                func_add_items= main.add_items, 
                func_convert_images=main.convert_images)
    
    main.set_ui(ui)
    ui.initialize_ui()