from PIL import Image
import pytesseract
import time
import keyboard
import random

IMAGE_INPUT_NAME = 'input.jpg'
FILE_OUTPUT_NAME = 'result.txt'
ACCEPTED_ASCII_LIST = [x for x in range(32, 127)]
RANDOM_ASCII_RANGE = 5
INITIAL_TYPO_CHANCE = 0.01
INCREMENT_TYPO_CHANCE = 0.004
DELAY_TIME_AFTER_TYPO = 0.4
DELAY_BETWEEN_CHAR = 0.04

def extract_text_from_image() -> None:
	PIPE_ASCII = 124
	
	time_start = time.perf_counter()
	text = pytesseract.image_to_string(Image.open(IMAGE_INPUT_NAME))
	with open(FILE_OUTPUT_NAME, 'w') as f_out:
		for c in text:
			ascii = ord(c)
			if ascii == PIPE_ASCII:
				f_out.write('I')
			elif ascii in ACCEPTED_ASCII_LIST:
				f_out.write(c)
			else:
				f_out.write(' ')
	time_end = time.perf_counter()
	print('\nDone! Executed in: {:.2f} seconds'.format(time_end - time_start))

def type_text() -> None:
	SPACE_ASCII = 32
	
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
				random_char = get_nearby_random_char(c)
				keyboard.write(random_char)
				time.sleep(DELAY_TIME_AFTER_TYPO)
				keyboard.press('backspace')
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
	
def get_nearby_random_char(char: chr) -> chr:
	LOWERCASE_A_ASCII = 97
	LOWERCASE_Z_ASCII = 122

	random_char_ascii = random.randint(ord(char) - RANDOM_ASCII_RANGE, ord(char) + RANDOM_ASCII_RANGE)
	return chr(clamp_int(random_char_ascii, LOWERCASE_A_ASCII, LOWERCASE_Z_ASCII))
	
def clamp_int(value: int, min: int, max: int) -> int:
	result = value
	if value < min:
		result = min
	elif value > max:
		result = max
	return result
			
if __name__ == '__main__':
	while(True):
		print('Type \'s\' to start reading, \'e\' to exit...')
		inp = input()
		if (inp == 'e'): break
		extract_text_from_image()
		print('Press esc to start typing..')
		keyboard.wait('esc')
		type_text()