import json

def parse_int(encoded_text, first_digit_index):
	next_e_index = encoded_text.index('e', first_digit_index)
	parsed_int = encoded_text[first_digit_index: next_e_index]
	return (int(parsed_int), next_e_index+1)

def parse_string(encoded_text, string_len_index):
	colon_index = encoded_text.index(':', string_len_index)
	string_len = int(encoded_text[string_len_index: colon_index])
	string = encoded_text[colon_index+1: colon_index+string_len+1]
	return string, colon_index+string_len+1

def rec_dict(encoded_text, index):
	my_dict = {}
	while encoded_text[index] != 'e':
		next_char = encoded_text[index]
		if next_char == 'i':
			key, index = parse_int(encoded_text, index+1)
		elif next_char in ['l','d']:
			raise(Exception("a dictionary or list can't be a key"))
		else:
			key, index = parse_string(encoded_text, index)

		next_char = encoded_text[index]
		if next_char == 'l':
			value, index = rec_list(encoded_text, index+1)
		elif next_char == 'd':
			value, index = rec_dict(encoded_text, index+1)
		elif next_char == 'i':
			value, index = parse_int(encoded_text, index+1)
		else:
			value, index = parse_string(encoded_text, index)

		my_dict[key] = value
		
	return my_dict, index+1

	
def rec_list(encoded_text, index):
	my_list = []
	while encoded_text[index] != 'e':
		next_char = encoded_text[index]

		if next_char == 'l':
			value, index = rec_list(encoded_text, index+1)
		elif next_char == 'd':
			value, index = rec_dict(encoded_text, index+1)
		elif next_char == 'i':
			value, index = parse_int(encoded_text, index+1)
		else:
			value, index = parse_string(encoded_text, index)

		my_list.append(value)
	
	return my_list, index+1
	
	
def decode(encoded_text):
	first_char = encoded_text[0]
	if first_char == 'd':
		decoded, index = rec_dict(encoded_text, 1)
	elif first_char == 'l':
		decoded, index = rec_list(encoded_text, decoded, 1)
	else:
		raise Exception("not a dictionary or list")
	return decoded


if __name__ == '__main__':

	examples = [
		'd4:key1li105ei20eee',
		'd4:key1d4:key2i10eee',
		'd4:key1li105el4:testi10eee4:key2d4:key3i5eee'
	]

	with open('.torrent_files\debian-12.4.0-amd64-netinst.iso.torrent', 'rb') as file:
		file_contents = file.read()

	# with open('.torrent_files/The Skin I Live In (2011) [1080p] [BluRay] [5.1] [YTS.MX].torrent', 'rb') as file:
	# 	file_contents = file.read()

	try:
		ansi_text = file_contents.decode('ansi')
	except UnicodeDecodeError:
		print("No ansi Text found.")

	decoded = decode(ansi_text)

	with open('decoded.json', 'w') as file:
		json.dump(decoded, file, indent=4)



