import json
from pathlib import Path
import hashlib
import binascii

examples = [
		'd4:key1li105ei20eee',
		'd4:key1d4:key2i10eee',
		'd4:key1li105el4:testi10eee4:key2d4:key3i5eee'
	]

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
		decoded, index = rec_list(encoded_text, 1)
	else:
		raise Exception("not a dictionary or list")
	return decoded

def validate_hash(downloaded_file_path, decoded, ):
	with open(downloaded_file_path, 'rb') as f:
			piece_len = decoded['info']['piece length']
			pieces_string = decoded['info']['pieces']
			index = 0
			SHA1_HASH_LEN = 20
			for piece in read_in_chunks(f, piece_len):
				check_hash(index, piece, pieces_string, SHA1_HASH_LEN)
				index+=SHA1_HASH_LEN

def check_hash(index, piece, pieces_string, SHA1_HASH_LEN):
	sha1_func = hashlib.sha1()
	sha1_torrent_file = pieces_string[index:index+SHA1_HASH_LEN]
	sha1_torrent_file = sha1_torrent_file.encode('ANSI')

	sha1_func.update(piece)
	sha1_downloaded_file = sha1_func.digest()
	if sha1_torrent_file != sha1_downloaded_file:
		raise Exception(f"piece: {index/20} hashes don't match")
	
	print(binascii.hexlify(sha1_downloaded_file).decode())
	print(binascii.hexlify(sha1_torrent_file).decode())
	print("")

def read_in_chunks(file_object, chunk_size):
	while True:
		data = file_object.read(chunk_size)
		if not data:
			break
		yield data

if __name__ == '__main__':
	input_file_path = Path(r'.torrent_files\debian-12.4.0-amd64-netinst.iso.torrent').resolve()
	downloaded_file_path = Path(r'downloaded_files\debian-12.4.0-amd64-netinst.iso').resolve()
	output_file_path = Path(f'{input_file_path.name}_decoded.json')

	with open(input_file_path, 'rb') as file:
		file_contents = file.read()

	try:
		ansi_text = file_contents.decode('ansi')
	except UnicodeDecodeError:
		print("No ansi Text found.")

	decoded = decode(ansi_text)
	validate_hash(downloaded_file_path, decoded)
	
	with open(output_file_path, 'w') as file:
		json.dump(decoded, file, indent=4)



