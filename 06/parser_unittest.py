import unittest
from Parser import Parser

class TestParser(unittest.TestCase):

	def setUp(self):
		assembly_filename = 'test.asm'
		self.parser = Parser(assembly_filename)

	# --------- remove_comments ------------

	def test_remove_comments_start_of_line(self):
		line = '// This is a comment'
		result = self.parser.remove_comments(line)

		self.assertEqual(result, '')

	def test_remove_comments_after_code(self):
		line = 'code code code // Comment!'
		result = self.parser.remove_comments(line)

		self.assertEqual(result, 'code code code')

	def test_remove_comments_whitespace_before_code(self):
		line = ' code code code // Comment!'
		result = self.parser.remove_comments(line)

		self.assertEqual(result, 'code code code')