import tkinter as tk
from tkinter import ttk
from stickers import load_sticker_image_minuatures, load_sticker_images
from callbacks import on_canvas_click_callback, on_select_filter_callback, on_open_image_callback, on_save_image_callback, on_start_camera_callback, on_stop_camera_callback
import cv2

class State:
	def __init__(self):
		self.unmodified_image = None
		self.current_image = None
		self.canvas_image = None
		self.current_filter = None
		self.current_sticker = None
		self.sticker_images = load_sticker_images()
		self.stickers = []
		self.canvas = None

state = State()

window = tk.Tk()
window.title("OpenCV Image Editor")

canvas = tk.Canvas(window, width=640, height=480, bg="gray")
canvas.grid(row=0, column=0, columnspan=4)
canvas.bind("<Button-1>", lambda event: on_canvas_click_callback(event, state))
state.canvas = canvas

btn_abrir = tk.Button(window, text="Open image", command= lambda: on_open_image_callback(state))
btn_abrir.grid(row=1, column=0, padx=5, pady=5)

btn_salvar = tk.Button(window, text="Save image", command= lambda: on_save_image_callback(state.current_image))
btn_salvar.grid(row=1, column=1, padx=5, pady=5)

btn_iniciar = tk.Button(window, text="Start camera", command=lambda: on_start_camera_callback(state, window))
btn_iniciar.grid(row=1, column=2, padx=5, pady=5)

btn_parar = tk.Button(window, text="Stop camera", command=on_stop_camera_callback)
btn_parar.grid(row=1, column=3, padx=5, pady=5)

filtros = ttk.Combobox(window, values=[
	"None", 
	"Grayscale", 
	"Sepia", 
	"Invert", 
	"Blur", 
	"Edge Detection", 
	"Emboss", 
	"Increase Brightness", 
	"Increase Contrast", 
	"Blue Tint", 
	"Red Tint"
], state="readonly")
filtros.set("None")

filtros.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
filtros.bind("<<ComboboxSelected>>", lambda e: on_select_filter_callback(state, e.widget.get()))

# Criar botões de miniaturas dos stickers
sticker_miniatures = load_sticker_image_minuatures()
for i in range(len(sticker_miniatures)):
	miniature = sticker_miniatures[i]
	sticker = tk.PhotoImage(data=cv2.imencode('.png', miniature)[1].tobytes())
	sticker = sticker.subsample(2)

	def set_sticker(i):
		state.current_sticker = i

	sticker_button = tk.Button(window, image=sticker, command=lambda i=i: set_sticker(i))
	sticker_button.image = sticker
	sticker_button.grid(row=3, column=i)

window.mainloop()