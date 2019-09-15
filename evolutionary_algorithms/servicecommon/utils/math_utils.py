import numpy as np

class MathUtils():
	"""
	This class contains the mathematics
	utilities. 
	"""

	@staticmethod
	def softmax(x):
		"""
		Converts a list of elements into probability values
		using softmax
		
		:param x: List containing values
		:returns softmax_x: Softmax(x)
		"""
		e_x = np.exp(x - np.max(x))
		softmax_x = e_x / e_x.sum()
		return softmax_x

