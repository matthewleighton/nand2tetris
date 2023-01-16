import unittest
from Code import Code

class TestCode(unittest.TestCase):

	def setUp(self):
		self.parsed_line = self.get_arbitrary_parsed_line()
		self.code_generator = Code(self.parsed_line)


	def get_parsed_line(self, command_type, comp, dest=None, jump=None, symbol=None):
		return {
			'commmand_type': command_type,
			'symbol': symbol,
			'dest': dest,
			'comp': comp,
			'jump': jump
		}

	def get_arbitrary_parsed_line(self):
		return self.get_parsed_line('C_COMMAND', 'D')

	# --------- base_10_to_binary ------------

	def test_base_10_to_binary_0_word_length_16(self):
		result = self.code_generator.base_10_to_binary(0, word_length=16)
		self.assertEqual(result, '0000000000000000')

	def test_base_10_to_binary_0_word_length_3(self):
		result = self.code_generator.base_10_to_binary(0, word_length=3)
		self.assertEqual(result, '000')

	def test_base_10_to_binary_123_word_length_16(self):
		result = self.code_generator.base_10_to_binary(123, word_length=16)
		self.assertEqual(result, '0000000001111011')

	# --------- get_jump_bits ------------

	def test_get_jump_bits_empty(self):
		result = self.code_generator.get_jump_bits('')
		self.assertEqual(result, '000')

	def test_get_jump_bits_JEQ(self):
		result = self.code_generator.get_jump_bits('JEQ')
		self.assertEqual(result, '010')

	def test_get_jump_bits_JMP(self):
		result = self.code_generator.get_jump_bits('JMP')
		self.assertEqual(result, '111')

	def test_get_jump_bits_invalid(self):
		jump_type = 'JJJ'

		with self.assertRaises(Exception) as exception_context:
			self.code_generator.get_jump_bits(jump_type)
		self.assertEqual(
			str(exception_context.exception),
			f'{jump_type} is not a valid jump type.'
		)


	# --------- get_dest_bits ------------

	def test_get_dest_bits_empty(self):
		result = self.code_generator.get_dest_bits('')
		self.assertEqual(result, '000')

	def test_get_dest_bits_AM(self):
		result = self.code_generator.get_dest_bits('AM')
		self.assertEqual(result, '101')

	def test_get_dest_bits_AMD(self):
		result = self.code_generator.get_dest_bits('AMD')
		self.assertEqual(result, '111')

	def test_get_dest_bits_invalid(self):
		dest_type = 'AAA'

		with self.assertRaises(Exception) as exception_context:
			self.code_generator.get_dest_bits(dest_type)
		self.assertEqual(
			str(exception_context.exception),
			f'{dest_type} is not a valid dest type.'
		)

	# --------- get_comp_a_bit ------------

	def test_get_comp_a_bit_yes_M(self):
		result = self.code_generator.get_comp_a_bit('AMB')
		self.assertEqual(result, '1')

	def test_get_comp_a_bit_no_M(self):
		result = self.code_generator.get_comp_a_bit('ABC')
		self.assertEqual(result, '0')



