from stickers import Sticker
from helpers import update_canvas, open_image, save_image, ask_for_save_path
from filters import apply_filter
from video import capture_camera_video
import threading

def on_canvas_click_callback(event, state):
	if state.current_image is None:
		return
	
	if state.current_sticker is None:
		return
	
	# Get the canvas dimensions and the image dimensions
	canvas_width = state.canvas.winfo_width()
	canvas_height = state.canvas.winfo_height()
	img_height, img_width, _ = state.current_image.shape

	# Calculate offsets for centered image
	x_offset = (canvas_width - img_width) // 2
	y_offset = (canvas_height - img_height) // 2

	# Get the click position relative to the canvas
	click_x, click_y = event.x, event.y
	print(f"Mouse clicked at: ({click_x}, {click_y})")

	# Adjust click coordinates for the image's position on the canvas
	img_x = click_x - x_offset
	img_y = click_y - y_offset

	# Check if the click is within the bounds of the image
	if 0 <= img_x < img_width and 0 <= img_y < img_height:
		print(f"Click mapped to image coordinates: ({img_x}, {img_y})")
	else:
		print("Click was outside the image bounds.")
		# return

	current_sticker_image = state.sticker_images[state.current_sticker]
	sticker = Sticker(current_sticker_image, img_x, img_y)
	state.stickers.append(sticker)
	update_canvas(state)

def on_select_filter_callback(state, filter_name):
	if state.current_image is None:
		return
	
	state.current_filter = filter_name
	state.current_image = apply_filter(state.unmodified_image, filter_name)
	update_canvas(state)

def on_open_image_callback(state):
	state.current_image = open_image()
	if state.current_image is None:
		return

	state.unmodified_image = state.current_image.copy()
	state.stickers = []
	update_canvas(state)

def on_save_image_callback(image):
	path = ask_for_save_path()
	if not path:
		return
	
	save_image(image, path)

def on_start_camera_callback(state, window):
	state.stickers = []
	threading.Thread(target=lambda: capture_camera_video(state, window)).start()

def on_stop_camera_callback(state):
	state.read_camera = False