from Code import Code

class Parser():
	def __init__(self, assembly_filename):
		self.assembly_filename = assembly_filename
		self.ROM_address = -1
		self.initialize_symbol_table()

	def initialize_symbol_table(self):
		self.symbol_table = {
			'SP': 0,
			'LCL': 1,
			'ARG': 2,
			'THIS': 3,
			'THAT': 4,
			'SCREEN': 16384,
			'KBD': 24576
		}

		for i in range(16):
			self.symbol_table[f'R{i}'] = i

	def parse(self):
		self.first_pass()
		self.second_pass()

	def first_pass(self):
		self.f = open(self.assembly_filename, 'r')

		for i, line in enumerate(self.f):

			line = self.remove_comments(line)

			if len(line) == 0:
				continue

			self.current_line = line

			command_type = self.command_type()
			symbol = self.symbol()

			self.update_ROM_address(command_type)
			self.update_symbol_table(command_type, symbol)

		self.f.close()

	def second_pass(self):
		self.ROM_address = 0
		self.RAM_address = 16

		self.f = open(self.assembly_filename, 'r')

		for i, line in enumerate(self.f):
			line = self.remove_comments(line)

			if len(line) == 0:
				continue

			self.current_line = line

			command_type = self.command_type()
			symbol = self.symbol()

			if command_type == 'A_COMMAND' and not symbol.isdigit():
				if symbol in self.symbol_table.keys():
					symbol = self.symbol_table[symbol]
				else:
					self.symbol_table[symbol] = self.RAM_address
					symbol = self.RAM_address
					self.RAM_address += 1

			parsed_data = {
				'command_type': command_type,
				'symbol': symbol,
				'dest': self.dest(),
				'comp': self.comp(),
				'jump': self.jump(),
			}

			output_filename   = self.get_output_fileame()

			code_generator = Code(parsed_data, output_filename=output_filename)
			code_generator.process()

		self.f.close()

	def remove_comments(self, line):
		line = line.strip()
		comment_position = line.find('//')

		if comment_position < 0:
			return line

		line = line[:comment_position].strip()

		return line

	# Increment the ROM address if we have either an A or C command.
	def update_ROM_address(self, command_type):
		if command_type == 'L_COMMAND':
			return

		self.ROM_address += 1

	def update_symbol_table(self, command_type, symbol):
		if command_type != 'L_COMMAND':
			return

		self.symbol_table[symbol] = self.ROM_address+1

	def command_type(self):

		if self.current_line[0] == '@':
			return 'A_COMMAND'

		if self.current_line[0] == '(':
			return 'L_COMMAND'

		return 'C_COMMAND'

	def is_c_command(self):
		if self.command_type() == 'C_COMMAND':
			return True
		else:
			return False

	def symbol(self):
		command_type = self.command_type()

		if command_type == 'A_COMMAND':
			return self.current_line[1:]

		elif command_type == 'L_COMMAND':
			return self.current_line[1:-1]
		else:
			return None

	def dest(self):
		if not self.is_c_command():
			return None

		# Dest value appears before equals sign.
		equals_position = self.current_line.find('=')

		# No dest value if '=' is omitted.
		if equals_position < 0:
			return None

		dest = self.current_line[:equals_position]

		return dest

	def comp(self):
		if not self.is_c_command():
			return None

		start_of_comp_position = self.current_line.find('=')+1
		end_of_comp_position = self.current_line.find(';')

		if end_of_comp_position < 0:
			return self.current_line[start_of_comp_position:]
		else:
			return self.current_line[start_of_comp_position:end_of_comp_position]

	def jump(self):
		if not self.is_c_command():
			return None

		semicolon_position = self.current_line.find(';')

		if semicolon_position < 0:
			return None
		else:
			return self.current_line[semicolon_position+1:]

	def get_output_fileame(self):
		return self.assembly_filename.split('.')[0] + '.hack'

	# Empty the output file if it already exists.
	def create_output_file(self):
		output_filename = self.get_output_fileame()
		open(output_filename, 'w').close()