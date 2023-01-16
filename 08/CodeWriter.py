class CodeWriter():

	STACK_BASE_ADDRESS = 256
	SEGMENT_CODES = {
		'local': 'LCL',
		'argument': 'ARG',
		'this': 'THIS',
		'that': 'THAT',
		'pointer': '3',
		'temp': '5',
		'static': '16'
	}

	def __init__(self, output_path):
		self.output_path = output_path
		# self.initialize_stack_pointer()
		
		self.bool_count = 0
		
	def initialize_stack_pointer(self):
		self.write_line(f'@{self.STACK_BASE_ADDRESS}')
		self.write_line('D=A')
		self.write_line('@SP')
		self.write_line('M=D')

	def process_command(self, command_type, arg1, arg2):
		if command_type == 'C_PUSH':
			self.push(arg1, arg2)

		if command_type == 'C_POP':
			self.pop(arg1, arg2)

		if command_type == 'C_ARITHMETIC':
			self.arithmetic(arg1, arg2)

		return 'process_command'

	def write_line(self, line):
		with open(self.output_path, 'a') as f:
			f.write(line + '\n')
		f.close()

	def push(self, segment, index):
		index = int(index)

		if segment == 'constant':
			# Value to push comes from specified constant
			self.write_line(f'@{index}')
			self.write_line('D=A')
		else:
			# Value to push comes from specified segment/index.
			self.point_A_cache_to_segment_base(segment)
			self.increment_A_cache(index)
			self.write_line('D=M')

		# We've put the value in the D cache. Now push it to the stack.
		self.point_A_cache_to_stack_top()
		self.write_line('M=D')
		self.increment_stack_pointer()

	def pop(self, segment, index):
		index = int(index)

		self.decrement_stack_pointer()
		self.point_A_cache_to_stack_top()
		self.write_line('D=M')
		self.point_A_cache_to_segment_base(segment)
		self.increment_A_cache(index)
		self.write_line('M=D')


	def arithmetic(self, arg1, arg2):
		if arg1 in ['lt', 'eq', 'gt']:
			self.compare(arg1)
		elif arg1 in ['add', 'sub']:
			self.add_sub(arg1)
		elif arg1 in ['and', 'or']:
			self.and_or(arg1)
		elif arg1 == 'neg':
			self.neg()
		elif arg1 == 'not':
			self.not_command()

		self.increment_stack_pointer()

	def add_sub(self, function):
		symbol = {'add': '+', 'sub': '-'}[function]

		self.load_top_two_stack_values_to_D_and_M_caches()
		self.write_line(f'M=M{symbol}D')


	def compare(self, vm_command):
		self.add_sub('sub')

		# Load the resulting sub value itno the D cache.
		self.point_A_cache_to_stack_top()
		self.write_line('D=M')
		self.write_line(f'@TRUE_{self.bool_count}')
		self.write_line(f'D;J{vm_command.upper()}')

		# Case when comparison is False. (Jump does not happen)
		self.point_A_cache_to_stack_top()
		self.write_line('M=0')
		self.write_line(f'@END_BOOL_{self.bool_count}')
		self.write_line('0;JMP')

		# Case when comparison is True.
		self.write_line(f'(TRUE_{self.bool_count})')
		self.point_A_cache_to_stack_top()
		self.write_line('M=-1')
		
		# Comparison finished. Continuing with code.
		self.write_line(f'(END_BOOL_{self.bool_count})')

		self.bool_count += 1

	def and_or(self, function):
		symbol = {'and': '&', 'or': '|'}[function]

		self.load_top_two_stack_values_to_D_and_M_caches()
		self.write_line(f'M=D{symbol}M')

	def neg(self):
		self.decrement_stack_pointer()
		self.point_A_cache_to_stack_top()
		self.write_line('D=0')
		self.write_line('M=D-M')


	def not_command(self):
		self.decrement_stack_pointer()
		self.write_line('A=M')
		self.write_line('M=!M')

	# The top stack value will be loaded to the D cache.
	# The second value in the stack will be loaded to the M cache (i.e. its address loaded to A)
	def load_top_two_stack_values_to_D_and_M_caches(self):
		self.decrement_stack_pointer()
		self.point_A_cache_to_stack_top()
		self.write_line('D=M')
		self.decrement_stack_pointer()
		self.point_A_cache_to_stack_top()

	def increment_stack_pointer(self):
		self.write_line('@SP')
		self.write_line('M=M+1')

	def decrement_stack_pointer(self):
		self.write_line('@SP')
		self.write_line('M=M-1')

	def point_A_cache_to_stack_top(self):
		self.write_line('@SP')
		self.write_line('A=M')

	def point_A_cache_to_segment_base(self, segment):
		segment_code = self.SEGMENT_CODES[segment]

		self.write_line(f'@{segment_code}')

		if segment not in ['pointer', 'temp', 'static']:
			self.write_line('A=M')

	def increment_A_cache(self, index):
		for i in range(index):
			self.write_line('A=A+1')