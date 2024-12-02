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

main_frame = tk.Frame(window)
main_frame.pack(padx=10, pady=10)

canvas = tk.Canvas(main_frame, width=640, height=480, bg="gray")
canvas.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
canvas.bind("<Button-1>", lambda event: on_canvas_click_callback(event, state))
state.canvas = canvas

button_frame = tk.Frame(main_frame)
button_frame.grid(row=1, column=0, columnspan=4, pady=10)

btn_abrir = tk.Button(button_frame, text="Open Image", command=lambda: on_open_image_callback(state), width=20)
btn_abrir.grid(row=0, column=0, padx=5)

btn_salvar = tk.Button(button_frame, text="Save Image", command=lambda: on_save_image_callback(state.current_image), width=20)
btn_salvar.grid(row=0, column=1, padx=5)

btn_iniciar = tk.Button(button_frame, text="Start Camera", command=lambda: on_start_camera_callback(state, window), width=20)
btn_iniciar.grid(row=0, column=2, padx=5)

btn_parar = tk.Button(button_frame, text="Stop Camera", command=on_stop_camera_callback, width=20)
btn_parar.grid(row=0, column=3, padx=5)

filtros_frame = tk.Frame(main_frame)
filtros_frame.grid(row=2, column=0, columnspan=4, pady=10)

filters_label = tk.Label(filtros_frame, text="Filters and stickers:", font=('Arial', 10, 'bold'))
filters_label.grid(row=0, column=0, padx=5, sticky="w")

filtros = ttk.Combobox(filtros_frame, values=[
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
], state="readonly", width=35)
filtros.set("None")
filtros.grid(row=1, column=0, padx=5)
filtros.bind("<<ComboboxSelected>>", lambda e: on_select_filter_callback(state, e.widget.get()))

sticker_frame = tk.Frame(main_frame)
sticker_frame.grid(row=3, column=0, columnspan=4, pady=10)

sticker_miniatures = load_sticker_image_minuatures()
for i, miniature in enumerate(sticker_miniatures):
	sticker = tk.PhotoImage(data=cv2.imencode('.png', miniature)[1].tobytes())
	sticker = sticker.subsample(2)

	def set_sticker(i):
		state.current_sticker = i

	sticker_button = tk.Button(sticker_frame, image=sticker, command=lambda i=i: set_sticker(i))
	sticker_button.image = sticker
	sticker_button.grid(row=1, column=i, padx=5)

window.mainloop()
