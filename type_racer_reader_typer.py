from PIL import Image
import pytesseract
import time
import keyboard

ACCEPTED_CHAR_RANGE = [x for x in range(32, 128)]
IMAGE_INPUT_NAME = 'input.jpg'
FILE_OUTPUT_NAME = 'result.txt'

def extract_text_from_image():
	time_start = time.perf_counter()
	text = pytesseract.image_to_string(Image.open(IMAGE_INPUT_NAME))
	with open(FILE_OUTPUT_NAME, 'w') as f_out:
		for c in text:
			ascii = ord(c)
			if ascii == 124:
				f_out.write('I')
			elif ascii in ACCEPTED_CHAR_RANGE:
				f_out.write(c)
			else:
				f_out.write(' ')
	time_end = time.perf_counter()
	print('\nDone! Executed in: {} seconds'.format(time_end - time_start))

def type_text():
	with open(FILE_OUTPUT_NAME, 'r') as f_in:
		c = f_in.read(1)
		while c:
			if(ord(c) == 32):
				print('Press F9 to continue typing the next word..')
				keyboard.wait('f9')
			keyboard.write(c)
			c = f_in.read(1)
			time.sleep(0.03)
				
if __name__ == '__main__':
	extract_text_from_image()
	while(True):
		print('Press esc to start typing..')
		keyboard.wait('esc')
		type_text()