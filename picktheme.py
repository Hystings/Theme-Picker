import tkinter as tk
from PIL import Image, ImageTk
import os


current=0
background=[]
image_ids = [[],[]]
current_loaded=["",""]
resolutions=((344,144),(192,108))
# The centerpoint of these resolutions
centers=((172,72),(96,54))
directorypath="/home/hyst/themes"
themes=[]
paths=[]


def read_themes():
    global themes, paths
    dirs=os.listdir(directorypath)
    paths=dirs
    for directory in dirs:
        title=directory.replace("-", " ").title()
        images = []
        images.append(directorypath+"/"+directory+"/backgrounds/DP-1.jpg")
        images.append(directorypath+"/"+directory+"/backgrounds/DP-2.jpg")
        themes.append((title, images))
    








    
def main():
    def update_images(title, images):
        label.config(text=title)
        delete_last(0)
        draw_image(images[0], 0)
        delete_last(1)
        draw_image(images[1], 1)
        root.update()

    def delete_last(display):
        if image_ids[display]:
            last_id=image_ids[display].pop()
            background[display].delete(last_id)

    def draw_image(image, display):
        global current_loaded
        global background
        
        try:
            originalimage = Image.open(image)
        except FileNotFoundError:
            originalimage = Image.open("/home/hyst/Documents/default-DP2.png")
 
        resizedimage=originalimage.resize(resolutions[display],Image.Resampling.LANCZOS)
        img_ref=ImageTk.PhotoImage(resizedimage)
        img_id = background[display].create_image(centers[display],image=img_ref,anchor="center")
        current_loaded[display]=img_ref
        image_ids[display].append(img_id)

        
    def decrease(event):
        global current
        if current == 0:
            current = len(themes)-1
        else:
            current = current - 1
        update_images(*themes[current])
        root.update()
        
    def increase(event):
        global current
        if current == len(themes)-1:
            current = 0
        else:
            current = current + 1
        update_images(*themes[current])
        root.update()
    def close(event):
        root.destroy()
    def confirm(event):
        os.system(f'cp -f /home/hyst/themes/{paths[current]}/waybar/* ~/.config/waybar')
        os.system(f'cp -f /home/hyst/themes/{paths[current]}+/wofi/* ~/.config/wofi')
        os.system(f'cp -f /home/hyst/themes/{paths[current]}/backgrounds/* ~/backgrounds')
        os.system('swaymsg reload')
        os.system(f'notify-send "Theme Swapped" "Theme Swapped to {themes[current][0]}."')

    global background
    root=tk.Tk(className="transparent tk")
    root.config(bg="white")
    root.title("Theme Picker")
    read_themes()

    label=tk.Label(master=root,text="")
    
    for entry in resolutions:
        background.append(tk.Canvas(root, width=entry[0], height=entry[1]))
    for monitor in background:
        monitor.config(bg='lightgray')
        monitor.pack()
    label.pack()

    buttons=tk.Frame(root)
    

    root.bind("<Left>", decrease)
    root.bind("<Right>", increase)
    root.bind("<Escape>", close)
    root.bind("<Return>", confirm)

    update_images(*themes[0])
    label.config(text=themes[0][0])

    root.update()
    
    root.mainloop()



main()
