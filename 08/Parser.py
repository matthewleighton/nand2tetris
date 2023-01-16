class Parser():
	def __init__(self, input_filename, code_writer):
		self.code_writer = code_writer
		self.input_filename = input_filename

		self.parse_file()


	def parse_file(self):
		with open(self.input_filename, 'r') as f:
			for line in f:
				self.parse_line(line)


	def parse_line(self, line):
		line = self.remove_comments(line)

		if len(line) == 0:
			return

		command_type = self.get_command_type(line)
		arg1 = self.get_arg1(line, command_type)
		arg2 = self.get_arg2(line, command_type)

		self.code_writer.process_command(command_type, arg1, arg2)



	def remove_comments(self, line):
		line = line.strip()
		comment_position = line.find('//')

		if comment_position < 0:
			return line

		line = line[:comment_position].strip()

		return line


	def get_command_type(self, line):
		command = line.split(' ')[0]

		arithmetic_commands = ['add', 'sub', 'neg', 'eq', 
							   'gt', 'lt', 'and', 'or', 'not']

		if command == 'push':
			return 'C_PUSH'

		if command == 'pop':
			return 'C_POP'

		if command in arithmetic_commands:
			return 'C_ARITHMETIC'


	def get_arg1(self, line, command_type):
		sections = line.split(' ')
		if command_type == 'C_ARITHMETIC':
			return sections[0]

		if command_type == 'C_RETURN':
			return None

		return sections[1]

	def get_arg2(self, line, command_type):
		arg2_command_types = ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']

		if command_type not in arg2_command_types:
			return None

		return line.split(' ')[2]