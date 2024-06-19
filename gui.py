import tkinter as tk
from tkinter import filedialog
from tkinter import Label, Button
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model

# Loading the Model
model = load_model('Age_Sex_Detection.h5')

# Initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Age & Gender Detector')
top.configure(background='#CDCDCD')

# Initializing the Labels (1 for age and 1 for Sex)
label1 = Label(top, background="#CDCDCD", font=('arial', 15, "bold"))
label2 = Label(top, background="#CDCDCD", font=('arial', 15, 'bold'))
sign_image = Label(top)

# Defining Detect function which detects the age and gender of the person in the image using the model
def Detect(file_path):
    global label_packed
    image = Image.open(file_path)
    image = image.resize((48, 48))
    image = np.array(image)

    # Check if the image has an alpha channel and remove it if necessary
    if image.shape[-1] == 4:
        image = image[..., :3]

    # Normalize the image
    image = image / 255.0

    # Expand dimensions to match the model input
    image = np.expand_dims(image, axis=0)

    # Predict the age and gender
    pred = model.predict(image)
    
    # Assuming the model outputs age as a scalar and gender as a binary class
    age = int(np.round(pred[1][0]))
    sex = int(np.round(pred[0][0]))
    
    sex_f = ["Male", "Female"]
    
    print("Predicted Age is " + str(age))
    print("Predicted Gender is " + sex_f[sex])
    
    label1.configure(foreground="#011638", text=f"Age: {age}")
    label2.configure(foreground="#011638", text=f"Gender: {sex_f[sex]}")

# Defining Show_detect button function
def show_Detect_button(file_path):
    Detect_b = Button(top, text="Detect Image", command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
    Detect_b.place(relx=0.79, rely=0.46)

# Defining Upload Image Function
def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image = im
        label1.configure(text='')
        label2.configure(text='')
        show_Detect_button(file_path)
    except Exception as e:
        print(f"Error: {e}")

upload = Button(top, text="Upload an Image", command=upload_image, padx=10, pady=5)
upload.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
upload.pack(side='bottom', pady=50)
sign_image.pack(side='bottom', expand=True)
label1.pack(side="bottom", expand=True)
label2.pack(side="bottom", expand=True)
heading = Label(top, text="Age and Gender Detector", pady=20, font=('arial', 20, "bold"))
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()
top.mainloop()
