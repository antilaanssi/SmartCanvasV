import numpy as np
import cv2
import torch
from torchvision.transforms.functional import to_tensor, to_pil_image
from PIL import Image

from smart_canvas.filters.model import Generator


class AnimeFilter:

	def __init__(self):

		self.device = "cpu" # change to to cuda if available
		self.model="./smart_canvas/filters/weights/face_paint_512_v2.pt"
		self.net = Generator()
		self.net.load_state_dict(torch.load(self.model, map_location="cpu"))
		self.net.to(self.device).eval()
		print(f"model loaded: {self.model}")


	def filter(self, original_img):
		
		PIL_img = self.convert_openCV_to_PIL(original_img)

		with torch.no_grad():
			image = to_tensor(PIL_img).unsqueeze(0) * 2 - 1
			out_img = self.net(image.to(self.device), False).cpu()
			out_img = out_img.squeeze(0).clip(-1, 1) * 0.5 + 0.5
			out_img = to_pil_image(out_img)

		opencv_img = self.convert_PIL_to_openCV(out_img)

		return opencv_img


	@staticmethod
	def convert_openCV_to_PIL(opencv_img):
		RGB_img = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2RGB)
		PIL_img = Image.fromarray(RGB_img)
		return PIL_img

	@staticmethod
	def convert_PIL_to_openCV(PIL_img):
		numpy_img = np.array(PIL_img)
		opencv_img = cv2.cvtColor(numpy_img, cv2.COLOR_RGB2BGR) 
		return opencv_img

