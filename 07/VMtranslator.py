import sys
import os
import glob

from Parser import Parser
from CodeWriter import CodeWriter

class VMtranslator():
	def __init__(self, target_path):

		self.output_path = self.get_output_path(target_path)
		self.initialize_output_file()
		self.code_writer = CodeWriter(self.output_path)

		self.handle_target_path(target_path)


	def get_output_path(self, target_path):
		cwd = os.path.abspath(os.getcwd())
		target_path = target_path.rstrip('/')
		filename = target_path.split('/')[-1] + '.asm'

		return f'{cwd}/{target_path}/{filename}'


	def initialize_output_file(self):
		open(self.output_path, 'w').close()


	def handle_target_path(self, target_path):
		if os.path.isdir(target_path):
			os.chdir(target_path)

			for filename in glob.glob("*.vm"):
				Parser(filename, self.code_writer)
		else:
			if target_path.endswith('.vm'):
				Parser(filename, self.code_writer)
			else:
				raise Exception(f'{target_path} contains no vm files.')

		self.completion_message()

	def completion_message(self):
		print(f'Assembly code written to {self.output_path}')




VMtranslator(sys.argv[1])