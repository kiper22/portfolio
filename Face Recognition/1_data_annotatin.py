import os
import shutil
from PIL import Image, ImageTk
import tkinter as tk

# path to folder with all images and with annotated images
images_from_folder = r'C:\Projekty\PracaInz\Data\Datasets\CFPW_dataset_RAW'
images_to_folder = r'C:\Projekty\PracaInz\Data\Datasets\CFPW_dataset_manual'

def f_images_dataset(path):
    '''
    the function recursively searches the folder and returns a list of paths files *.png
    '''
    data_list = []
    
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith('png'):
                data_list.append(file_path)
    
    return data_list

# based on the file name, a list of images that have not been annotated is created
images = f_images_dataset(images_from_folder)
images_used = f_images_dataset(images_to_folder)

images_names = [os.path.basename(image) for image in images]
images_used_names = [os.path.basename(image) for image in images_used]
images = [image for image in images if os.path.basename(image) not in images_used_names]


print(len(images))

# main program
def main():
    def display_image():
        '''
        Draws and display a picture on canvas. The canvas size is adjusted to the original image size
        '''
        nonlocal index
        
        with Image.open(images[index]) as img_pil:
            width, height = img_pil.size
        
        canvas.config(width=width, height=height)

        if 0 <= index < len(images):
            image_path = images[index]
            img_pil = Image.open(image_path)
            img_pil = img_pil.resize((width, height))

            img_tk = ImageTk.PhotoImage(img_pil)
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            canvas.img_tk = img_tk

    def draw_crosshair(event):
        '''
        Draws crossed lines to the cursor location
        '''
        x, y = event.x, event.y
        canvas.delete("crosshair")
        canvas.create_line(x, 0, x, canvas.winfo_height(), fill="red", tags="crosshair")
        canvas.create_line(0, y, canvas.winfo_width(), y, fill="red", tags="crosshair")

    def previous_image(event):
        '''
        Change the image to the previous one
        '''
        nonlocal index, annotation_text
        index = max(0, index - 1)
        annotation_text = ''
        display_image()

    def next_image(event):
        '''
        Change the image to the next one
        '''
        nonlocal index, annotation_text
        index = min(len(images) - 1, index + 1)
        print(images[index])
        annotation_text = ''
        display_image()

    def make_annotation():
        '''
        Makes annotation ith variable annotation_text
        This function calculates the normalized coordinates and dimensions of a bounding box
        based on the annotation_coords and the dimensions of the currently displayed image.
        '''
        nonlocal index
        nonlocal annotation_text
        
        with Image.open(images[index]) as img_pil:
            w, h = img_pil.size
            print(f'Width: {w}, height: {h}')
            
        if annotation_coords:
            x1, y1, x2, y2 = annotation_coords
            x1 = float(x1/w)
            x2 = min(float(x2/w), 1)
            y1 = float(y1/h)
            y2 = min(float(y2/h),1)
            if x2 < 0:
                x2 = 0
            if y2 < 0:
                y2 = 0
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            annotation_text += f'0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f} \n'
            print(annotation_text)
    
    def start_annotation(event):
        '''
        Initiates the annotation process by capturing the starting coordinates of the bounding box
        '''
        nonlocal annotation_start
        annotation_start = (event.x, event.y)

    def end_annotation(event):
        '''
        Completes the annotation process by capturing the ending coordinates of the bounding box,
        making the annotation, and drawing the annotation rectangle on the canvas
        '''
        nonlocal annotation_start, annotation_coords
        if annotation_start:
            x1, y1 = annotation_start
            x2, y2 = event.x, event.y
            annotation_coords = (x1, y1, x2, y2)
            annotation_start = None
            make_annotation()
            draw_annotation_rect()

    def draw_annotation_rect():
        '''
        Draws the annotation rectangle on the canvas based on the current annotation_coords
        '''
        nonlocal annotation_rect
        if annotation_rect:
            canvas.delete(annotation_rect)
        x1, y1, x2, y2 = annotation_coords
        annotation_rect = canvas.create_rectangle(x1, y1, x2, y2, outline="red")
    
    def save_annotation_without_annotation():
        '''
        Saves an annotation without specifying the bounding box
        '''
        nonlocal annotation_text
        # <id_class> <x_center_boundingbox> <y_center_boundingbox> <width_boundingbox> <height_boundingbox>
        annotation_text = '0 0.5 0.5 1 1'
        save_annotation()
    
    def save_annotation():
        '''
        Saves the current annotation to a text file, copies the annotated image,
        and updates the image list.
        '''
        nonlocal index, annotation_text
        global images_used_folder
        
        image_path = images[index]
        image_name = os.path.basename(image_path)
        image_name = image_name.split('.')[0]
        annotation_file_path = os.path.join(images_used_folder, image_name + ".txt")
        with open(annotation_file_path, 'w') as f:
            f.write(annotation_text)
        
        shutil.copy(images[index], images_used_folder)
        
        del images[index]
        index = min(len(images) - 1, index)
        annotation_text = ''
        display_image()
        pass

    window = tk.Tk()
    index = 0
    annotation_start = None
    annotation_coords = None
    annotation_rect = None
    annotation_text =''
    
    with Image.open(images[index]) as img_pil:
        width, height = img_pil.size
    
    canvas = tk.Canvas(window, width=width, height=height)
    canvas.pack()
        
    display_image()
    
    window.bind("<Left>", previous_image)
    window.bind("<Right>", next_image)
    canvas.bind("<Button-1>", start_annotation)
    canvas.bind("<ButtonRelease-1>", end_annotation)
    canvas.bind("<Motion>", draw_crosshair)
    window.bind("s", lambda event: save_annotation())
    window.bind("<space>", lambda event: save_annotation_without_annotation())
    window.bind("x", lambda event: print(len(images)))
    
    window.mainloop()

if __name__ == '__main__':
    main()
