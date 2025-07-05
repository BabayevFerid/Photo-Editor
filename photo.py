import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter

class PhotoFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Filter Application")
        self.root.geometry("800x600")
        
        # Image variables
        self.original_image = None
        self.filtered_image = None
        self.display_image = None
        
        # Create interface
        self.create_widgets()
    
    def create_widgets(self):
        # Control panel
        control_frame = tk.Frame(self.root)
        control_frame.pack(side="top", fill="x", padx=5, pady=5)
        
        # Buttons
        self.btn_open = tk.Button(control_frame, text="Open Image", command=self.open_image)
        self.btn_open.pack(side="left", padx=5)
        
        self.btn_save = tk.Button(control_frame, text="Save", command=self.save_image)
        self.btn_save.pack(side="left", padx=5)
        
        # Filter selection
        filter_frame = tk.LabelFrame(self.root, text="Filters")
        filter_frame.pack(side="left", fill="y", padx=5, pady=5)
        
        self.filter_var = tk.StringVar(value="Normal")
        
        filters = [
            ("Normal", "Normal"),
            ("Grayscale", "Grayscale"),
            ("Sepia", "Sepia"),
            ("Cartoon", "Cartoon"),
            ("Sketch", "Sketch"),
            ("Blur", "Blur"),
            ("Sharpen", "Sharpen"),
            ("Edge Detection", "Edge")
        ]
        
        for text, mode in filters:
            rb = tk.Radiobutton(filter_frame, text=text, variable=self.filter_var,
                              value=mode, command=self.apply_filter)
            rb.pack(anchor="w")
        
        # Image display area
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(side="right", expand=True, fill="both")
        
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(expand=True)
    
    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.filtered_image = self.original_image.copy()
            self.display_image()
    
    def save_image(self):
        if self.filtered_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
            if file_path:
                cv2.imwrite(file_path, cv2.cvtColor(self.filtered_image, cv2.COLOR_RGB2BGR))
    
    def apply_filter(self):
        if self.original_image is None:
            return
            
        filter_type = self.filter_var.get()
        image = self.original_image.copy()
        
        if filter_type == "Grayscale":
            filtered = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            self.filtered_image = cv2.cvtColor(filtered, cv2.COLOR_GRAY2RGB)
        elif filter_type == "Sepia":
            kernel = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
            self.filtered_image = cv2.transform(image, kernel)
        elif filter_type == "Sketch":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            inverted = cv2.bitwise_not(gray)
            blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
            inverted_blur = cv2.bitwise_not(blurred)
            self.filtered_image = cv2.divide(gray, inverted_blur, scale=256.0)
            self.filtered_image = cv2.cvtColor(self.filtered_image, cv2.COLOR_GRAY2RGB)
        elif filter_type == "Cartoon":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(image, 9, 300, 300)
            self.filtered_image = cv2.bitwise_and(color, color, mask=edges)
        elif filter_type == "Blur":
            self.filtered_image = cv2.GaussianBlur(image, (15, 15), 0)
        elif filter_type == "Sharpen":
            kernel = np.array([[-1, -1, -1],
                             [-1, 9, -1],
                             [-1, -1, -1]])
            self.filtered_image = cv2.filter2D(image, -1, kernel)
        elif filter_type == "Edge":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            self.filtered_image = cv2.Canny(gray, 100, 200)
            self.filtered_image = cv2.cvtColor(self.filtered_image, cv2.COLOR_GRAY2RGB)
        else:  # "Normal"
            self.filtered_image = image.copy()
        
        self.display_image()
    
    def display_image(self):
        if self.filtered_image is not None:
            # Convert OpenCV image to PIL format
            image = cv2.cvtColor(self.filtered_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            
            # Resize if needed
            width, height = image.size
            max_width = self.image_frame.winfo_width() - 20
            max_height = self.image_frame.winfo_height() - 20
            
            if width > max_width or height > max_height:
                ratio = min(max_width/width, max_height/height)
                image = image.resize((int(width*ratio), int(height*ratio)), Image.LANCZOS)
            
            # Display image
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoFilterApp(root)
    root.mainloop()
