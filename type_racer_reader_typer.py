from PIL import Image
import pytesseract
import time
import keyboard
import random

ACCEPTED_CHAR_RANGE = [x for x in range(32, 128)]
IMAGE_INPUT_NAME = 'input.jpg'
FILE_OUTPUT_NAME = 'result.txt'
INITIAL_TYPO_CHANCE = 0.01
INCREMENT_TYPO_CHANCE = 0.005
DELAY_TIME_AFTER_TYPO = 0.5
DELAY_BETWEEN_CHAR = 0.03
PIPE_ASCII = 124
SPACE_ASCII = 32

def extract_text_from_image() -> None:
	time_start = time.perf_counter()
	text = pytesseract.image_to_string(Image.open(IMAGE_INPUT_NAME))
	with open(FILE_OUTPUT_NAME, 'w') as f_out:
		for c in text:
			ascii = ord(c)
			if ascii == PIPE_ASCII:
				f_out.write('I')
			elif ascii in ACCEPTED_CHAR_RANGE:
				f_out.write(c)
			else:
				f_out.write(' ')
	time_end = time.perf_counter()
	print('\nDone! Executed in: {:.2f} seconds'.format(time_end - time_start))

def type_text() -> None:
	total_char = 0
	total_word = 1
	total_typo = 0
	time_start = time.perf_counter()
	
	with open(FILE_OUTPUT_NAME, 'r') as f_in:
		c = f_in.read(1)
		typo_chance = 0.02
		print('Press F9 to type the next word..')
		while c:
			if(ord(c) == SPACE_ASCII):
				typo_chance = INITIAL_TYPO_CHANCE
				total_char -= 1
				total_word += 1
				keyboard.wait('f9')
			if randomize_typo(typo_chance):
				# random_char = randrange(33, 128)
				random_char = '^'
				keyboard.write(random_char)
				time.sleep(DELAY_TIME_AFTER_TYPO)
				keyboard.write('*')
				total_typo += 1
			else:
				typo_chance += INCREMENT_TYPO_CHANCE
			keyboard.write(c)
			c = f_in.read(1)
			total_char += 1
			time.sleep(DELAY_BETWEEN_CHAR)
			
	time_end = time.perf_counter()
	delta_time = time_end - time_start
	wpm = int(total_word / (delta_time) * 60)
	accuracy = (total_char - total_typo) / total_char * 100
	print('Typing finish. Randomized {} typo(s) from {} character(s)'.format(total_typo, total_char))
	print('Typed {} word(s) in {:.2f} seconds'.format(total_word, delta_time))
	print('WPM:{}'.format(wpm))
	print('Accuracy:{:.2f}%'.format(accuracy))

def randomize_typo(chance: float) -> bool:
	return random.uniform(0, 1) <= chance
			
if __name__ == '__main__':
	extract_text_from_image()
	while(True):
		print('Press esc to start typing..')
		keyboard.wait('esc')
		type_text()