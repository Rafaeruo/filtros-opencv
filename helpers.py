import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2 as cv
from stickers import apply_stickers
import numpy as np

def open_image():
	path = filedialog.askopenfilename()
	if not path:
		return
		
	img  = cv.imread(path, cv.IMREAD_UNCHANGED)

	if img is None:
		return None
	
	img = to_rgba(img)
	return img

def opencv_to_pillow(opencv_image):
	opencv_image = cv.cvtColor(opencv_image, cv.COLOR_BGR2RGB)  # Convert BGR to RGB
	return Image.fromarray(opencv_image)

def resize_image_to_canvas(image, canvas):
	canvas_width = canvas.winfo_width()
	canvas_height = canvas.winfo_height()
	if canvas_width > 1 and canvas_height > 1:
		image.thumbnail((canvas_width, canvas_height))

def update_canvas(state):
	apply_stickers(state)
	state.canvas_image = opencv_to_pillow(state.current_image)
	resize_image_to_canvas(state.canvas_image, state.canvas)

	canvas_width = state.canvas.winfo_width()
	canvas_height = state.canvas.winfo_height()
	img_width, img_height = state.canvas_image.size

	x_offset = (canvas_width - img_width) // 2
	y_offset = (canvas_height - img_height) // 2

	state.canvas_photoimage = ImageTk.PhotoImage(state.canvas_image)
	state.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=state.canvas_photoimage)

def save_image(image, path):
	cv.imwrite(path, image)

def ask_for_save_path():
	return tk.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])

def to_rgba(image):
	if image.shape[2] == 3:
		alpha_channel = np.ones((image.shape[0], image.shape[1]), dtype=image.dtype) * 255
		return cv.merge((image, alpha_channel))
	return image