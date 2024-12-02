from stickers import Sticker
from helpers import update_canvas, open_image, save_image, ask_for_save_path
from filters import apply_filter
from video import capture_camera_video
import threading

def on_canvas_click_callback(event, state):
	if state.canvas_image is None:
		return
	
	if state.current_sticker is None:
		return
	
	# Ajustar posição do sticker pelo offset de centralização
	canvas_width = state.canvas.winfo_width()
	canvas_height = state.canvas.winfo_height()
	canvas_image_width, canvas_image_height = state.canvas_image.size

	x_offset = (canvas_width - canvas_image_width) // 2
	y_offset = (canvas_height - canvas_image_height) // 2

	click_x, click_y = event.x, event.y
	sticker_x = click_x - x_offset
	sticker_y = click_y - y_offset

	# Desfazer escala da imagem do canvas para obter posição do sticker na imagem original
	original_height, original_width, _ = state.unmodified_image.shape
	sticker_x = int(sticker_x * (original_width/canvas_image_width))
	sticker_y = int(sticker_y * (original_height/canvas_image_height))

	within_bounds = 0 <= sticker_x < original_width and 0 <= sticker_y < original_height
	if not within_bounds:
		return
	
	current_sticker_image = state.sticker_images[state.current_sticker]
	sticker = Sticker(current_sticker_image, sticker_x, sticker_y)
	state.stickers.append(sticker)
	update_canvas(state)

def on_select_filter_callback(state, filter_name):
	if state.current_image is None:
		return
	
	state.current_filter = filter_name
	state.current_image = apply_filter(state.unmodified_image, filter_name)
	update_canvas(state)

def on_open_image_callback(state):
	on_stop_camera_callback(state)
	state.current_image = open_image()
	if state.current_image is None:
		return

	state.unmodified_image = state.current_image.copy()
	state.stickers = []
	update_canvas(state)

def on_save_image_callback(image):
	if image is None:
		return

	path = ask_for_save_path()
	if not path:
		return
	
	save_image(image, path)

def on_start_camera_callback(state, window):
	state.stickers = []
	threading.Thread(target=lambda: capture_camera_video(state, window)).start()

def on_stop_camera_callback(state):
	state.read_camera = False