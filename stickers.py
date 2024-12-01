import cv2 as cv
import numpy as np

sticker_miniature_size = 64
sticker_size = 256

image_paths = [
    'stickers/blue_chill.png',
    'stickers/flustered.webp',
    'stickers/ok.png',
    'stickers/silly.webp',
    'stickers/smiley.webp'
]

class Sticker:
	def __init__(self, image, x, y):
		self.image = image
		self.x = x
		self.y = y

def load_sticker_images():
    sticker_images = []

    for path in image_paths:
        img = cv.imread(path, cv.IMREAD_UNCHANGED)
    
        if img.shape[2] == 3:
            alpha_channel = np.ones((img.shape[0], img.shape[1]), dtype=img.dtype) * 255 
            img = cv.merge((img, alpha_channel))
        
        img = cv.resize(img, (sticker_size, sticker_size))
        sticker_images.append(img)

    return sticker_images

def load_sticker_image_minuatures():
    sticker_images = load_sticker_images()
    sticker_minuatures = []

    for sticker in sticker_images:
        sticker_minuatures.append(cv.resize(sticker, (sticker_miniature_size, sticker_miniature_size)))

    return sticker_minuatures

def apply_stickers(state):	
	for sticker in state.stickers:
		state.current_image = apply_sticker(state.current_image, sticker.image, sticker.x, sticker.y)

# Baseado no exemplo de aula
def apply_sticker(background, sticker, pos_x=None, pos_y=None):
	"""
	Cola um sticker (foreground) com canal alpha em um fundo (background),
	ajustando posição pelo centro e cortando se ultrapassar as bordas.

	Parameters:
		background: numpy.ndarray
			Imagem de fundo (BGR).
		foreground: numpy.ndarray
			Imagem do sticker (RGBA, com canal alpha).
		pos_x: int
			Posição X do centro do sticker no fundo.
		pos_y: int
			Posição Y do centro do sticker no fundo.

	Returns:
		numpy.ndarray
			Imagem final com o sticker aplicado.
	"""

	# Separar canais do foreground (com alpha)
	b, g, r, a = [], [], [], []
	
	num_channels = sticker.shape[2]
	if num_channels == 4:
		b, g, r, a = cv.split(sticker)
	elif num_channels == 3:
		b, g, r = cv.split(sticker)
		a = 255 * np.ones_like(r, dtype=np.uint8)

	# Dimensões das imagens
	f_rows, f_cols, _ = sticker.shape
	b_rows, b_cols, _ = background.shape

	# Ajustar pos_x e pos_y para serem o centro background
	if pos_x is None:
		pos_x = b_cols // 2
	if pos_y is None:
		pos_y = b_rows // 2

	# Coordenadas do sticker ajustadas para o centro
	x_start = pos_x - f_cols // 2
	y_start = pos_y - f_rows // 2

	# Calcula os cortes para evitar extrapolação das bordas
	bg_x_start = max(0, x_start)
	bg_y_start = max(0, y_start)
	bg_x_end = min(b_cols, x_start + f_cols)
	bg_y_end = min(b_rows, y_start + f_rows)

	fg_x_start = max(0, -x_start)
	fg_y_start = max(0, -y_start)
	fg_x_end = fg_x_start + (bg_x_end - bg_x_start)
	fg_y_end = fg_y_start + (bg_y_end - bg_y_start)

	# Recorta as regiões de sobreposição
	sticker = sticker[fg_y_start:fg_y_end, fg_x_start:fg_x_end]
	mask = a[fg_y_start:fg_y_end, fg_x_start:fg_x_end]
	mask_inv = cv.bitwise_not(mask)
	roi = background[bg_y_start:bg_y_end, bg_x_start:bg_x_end]

	# Combinar as imagens usando máscaras
	img_bg = cv.bitwise_and(roi, roi, mask=mask_inv)
	img_fg = cv.bitwise_and(sticker, sticker, mask=mask)
	res = cv.add(img_bg, img_fg)

	# Atualizar o fundo com o resultado
	background[bg_y_start:bg_y_end, bg_x_start:bg_x_end] = res

	return background