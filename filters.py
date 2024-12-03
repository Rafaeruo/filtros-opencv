import cv2 as cv
import numpy as np

def apply_filter(image, filter_name):
	if filter_name == "Grayscale":
		return grayscale(image)
	elif filter_name == "Sepia":
		return sepia(image)
	elif filter_name == "Invert":
		return inverted(image)
	elif filter_name == "Blur":
		return blur(image)
	elif filter_name == "Edge Detection":
		return edge_detection(image)
	elif filter_name == "Emboss":
		return emboss(image)
	elif filter_name == "Increase Brightness":
		return increase_brightness(image)
	elif filter_name == "Increase Contrast":
		return increase_contrast(image)
	elif filter_name == "Blue Tint":
		return blue_tint(image)
	elif filter_name == "Red Tint":
		return red_tint(image)
	
	return image

def grayscale(img):
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
	return cv.cvtColor(gray, cv.COLOR_GRAY2BGRA)

def sepia(img):
	# separar os canais de cor e o canal alpha
	rgb = img[:, :, :3]
	alpha = img[:, :, 3]

	# Matriz de filtro sepia aos canais RGB
	sepia_filter = np.array([[0.393, 0.769, 0.189],
							 [0.349, 0.686, 0.168],
							 [0.272, 0.534, 0.131]])
	img_sepia = cv.transform(rgb, sepia_filter)
	img_sepia = np.clip(img_sepia, 0, 255).astype(np.uint8)

	# Adicionar o canal alpha de volta
	img_sepia = cv.merge([img_sepia[:, :, 0], img_sepia[:, :, 1], img_sepia[:, :, 2], alpha])

	return img_sepia

def inverted(img):
	img = 255 - img # Operação vetorizada equivalente a ^ 255
	return img

def blur(img):
	img_blur = cv.GaussianBlur(img, (15, 15), 0)
	return img_blur

def edge_detection(img):
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	edges = cv.Canny(gray, 100, 200)
	
	edges_bgr = cv.cvtColor(edges, cv.COLOR_GRAY2BGRA)
	return edges_bgr

def emboss(img):
	emboss_kernel = np.array([[-2, -1, 0], 
							  [-1, 1, 1], 
							  [0, 1, 2]])
	
	img_emboss = cv.filter2D(img, -1, emboss_kernel)
	return img_emboss

def increase_brightness(img, value=50):
	img_bright = cv.convertScaleAbs(img, alpha=1, beta=value)
	return img_bright

def increase_contrast(img, alpha=2.0):
	img_contrast = cv.convertScaleAbs(img, alpha=alpha, beta=0)
	return img_contrast

def blue_tint(img):
	# Aumenta o canal azul e diminui os outros
	img_blue_tint = img.copy()
	img_blue_tint[:, :, 0] = cv.add(img_blue_tint[:, :, 0], 50)  # Blue channel
	img_blue_tint[:, :, 1] = cv.subtract(img_blue_tint[:, :, 1], 50)  # Green channel
	img_blue_tint[:, :, 2] = cv.subtract(img_blue_tint[:, :, 2], 50)  # Red channel
	return img_blue_tint

def red_tint(img):
	# Aumenta o canal vermelho e diminui os outros
	img_red_tint = img.copy()
	img_red_tint[:, :, 0] = cv.subtract(img_red_tint[:, :, 0], 50)  # Blue channel
	img_red_tint[:, :, 1] = cv.subtract(img_red_tint[:, :, 1], 50)  # Green channel
	img_red_tint[:, :, 2] = cv.add(img_red_tint[:, :, 2], 50)  # Red channel
	return img_red_tint
