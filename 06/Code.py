class Code():
	def __init__(self, parsed_line, output_filename='output.hack'):
		self.parsed_line 	 = parsed_line
		self.output_filename = output_filename

	def process(self):
		bits = self.translate_parsed_line_to_bits()

		if bits is None:
			return

		self.write_bits(bits)

	def translate_parsed_line_to_bits(self):
		command_type = self.parsed_line['command_type']

		if command_type == 'A_COMMAND':
			return self.get_A_command_bits()

		if command_type == 'C_COMMAND':
			return self.get_C_command_bits()

		return None

	def get_A_command_bits(self):
		base_10 = int(self.parsed_line['symbol'])
		return self.base_10_to_binary(base_10)

	def get_C_command_bits(self):
		comp_bits = self.get_comp_bits(self.parsed_line['comp'])
		dest_bits = self.get_dest_bits(self.parsed_line['dest'])
		jump_bits = self.get_jump_bits(self.parsed_line['jump'])

		return '111' + comp_bits + dest_bits + jump_bits

	def get_comp_bits(self, comp_type):
		a_bit  = self.get_comp_a_bit(comp_type)
		c_bits = self.get_comp_c_bits(comp_type)

		comp_bits = a_bit + c_bits

		return comp_bits

	def get_comp_a_bit(self, comp_type):
		if 'M' in comp_type:
			return '1'
		else:
			return '0'

	def get_comp_c_bits(self, comp_type):
		comp_type = comp_type.replace('M', 'A')

		if comp_type is None:
			return '101010'

		translation = {
			'0':   '101010',
			'1':   '111111',
			'-1':  '111010',
			'D':   '001100',
			'A':   '110000',
			'!D':  '001101',
			'!A':  '110001',
			'D+1': '011111',
			'A+1': '110111',
			'D-1': '001110',
			'A-1': '110010',
			'D+A': '000010',
			'D-A': '010011',
			'A-D': '000111',
			'D&A': '000000',
			'D|A': '010101'
		}

		return translation[comp_type]

	def get_dest_bits(self, dest_type):
		if not dest_type:
			dest_type = ''

		types = ['', 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']

		try:
			base_10 = types.index(dest_type)
		except:
			raise Exception(f'{dest_type} is not a valid dest type.')

		dest_bits = self.base_10_to_binary(base_10, word_length=3)

		return dest_bits

	def get_jump_bits(self, jump_type):
		if not jump_type:
			jump_type = ''

		types = ['', 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']

		try:
			base_10 = types.index(jump_type)
		except:
			raise Exception(f'{jump_type} is not a valid jump type.')	
		
		jump_bits = self.base_10_to_binary(base_10, word_length=3)

		return jump_bits

	def base_10_to_binary(self, base_10, word_length=16):
		return format(base_10, '0{}b'.format(word_length))

	def write_bits(self, bits):
		with open(self.output_filename, 'a') as f:
			f.write(bits + '\n')
		f.close()