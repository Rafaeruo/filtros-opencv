import cv2
from filters import apply_filter
from helpers import update_canvas, to_rgba

def capture_camera_video(state, window):
	state.read_camera = True
	captura = cv2.VideoCapture(0)

	def process_frame():
		if not state.read_camera:
			captura.release()
			return
		 
		ret, state.current_image = captura.read()
		if ret:
			state.current_image = to_rgba(state.current_image)
			state.unmodified_image = state.current_image.copy()
			state.current_image = apply_filter(state.unmodified_image, state.current_filter)
			update_canvas(state)

		window.after(10, process_frame)
	process_frame()