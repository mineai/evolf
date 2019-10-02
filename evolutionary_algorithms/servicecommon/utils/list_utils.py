class ListUtils():
	"""
	This class contains list utility functions.
	"""

	@staticmethod
	def to_string(target):
		"""
		This string converts a list dna to
		a string.
		:param target: A list which represents the list
		:returns target_str: String representation of
		the dna
		"""
		target_str = ''.join(target)
		return target_str

	@staticmethod
	def copy_elements(elements, copies):
		"""
		This function makes multiple copies of
		elements in a list.
		:param elements: List containing the information to be copied
		:copies: List specifying number of copies of each element in elements
		list
		:returns final_list: List containing each element copied number of times
		specified by the copies list.
		"""
		import math
		final_list = []
		for idx, element in enumerate(elements):
		    [final_list.append(element) for times in range(math.floor(copies[idx]))]

		return final_list

	@staticmethod
	def sort_lists(x, y):
		"""
		This function sorts list x, based on list y values and returns
		the sorted values of x in desc order.
		"""
		z = [x for _,x in sorted(zip(y,x))][::-1]
		return z

	@staticmethod
	def block_list(target, max_chunk_length):
		"""
		This function takes it in a list and
		breaks it into smaller lists.
		"""
		bits_of_strings = []

		length_of_list = len(target)
		number_of_bits = int(length_of_list / max_chunk_length)
		start_idx = 0
		for bit in range(number_of_bits+1):
			end_idx = start_idx + max_chunk_length
			if end_idx > length_of_list:
				end_idx = length_of_list

			bit = target[start_idx:end_idx]
			if len(bit):
				bits_of_strings.append(bit)
			start_idx = end_idx

		return bits_of_strings

	@staticmethod
	def read_file(target_path):
		"""
		This function takes in a file path and reads
		it and returns as a list
		"""
		with open (target_path, "r") as target_string:
			target = target_string.readlines()[0]
			if isinstance(target, str):
				target = list(target)
		return target
