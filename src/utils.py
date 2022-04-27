
import math as m
import numbers

class schechter_function:

	def __init__(self, normalization, characteristic, plaw_index):
		self.normalization = normalization
		self.characteristic = characteristic
		self.plaw_index = plaw_index

	def __call__(self, x):
		return self._normalization / self._characteristic * (
			x / self._characteristic)**self._plaw_index * m.exp(
			-x / self._characteristic)

	@property
	def normalization(self):
		r"""
		Type : ``float``

		The normalization of the schechter function.
		"""
		return self._normalization

	@normalization.setter
	def normalization(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				self._normalization = float(value)
			else:
				raise ValueError("Attribute 'normalization' must be positive.")
		else:
			raise TypeError(
				"Attribute 'normalization' must be a real number. Got: %s" % (
					type(value)))

	@property
	def characteristic(self):
		r"""
		Type : ``float``

		The "characteristic" quantity described the schechter function.
		Colloquially referred to as "M-star" or "L-star" for mass and
		luminosity functions, respectively.
		"""
		return self._characteristic

	@characteristic.setter
	def characteristic(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				self._characteristic = float(value)
			else:
				raise ValueError("Attribute 'characteristic' must be positive.")
		else:
			raise TypeError(
				"Attribute 'characteristic' must be a real number. Got: %s" % (
					type(value)))

	@property
	def plaw_index(self):
		r"""
		Type : ``float``

		The power-law index of the schechter function.
		"""
		return self._plaw_index

	@plaw_index.setter
	def plaw_index(self, value):
		if isinstance(value, numbers.Number):
			self._plaw_index = float(value)
		else:
			raise TypeError(
				"Attribute 'plaw_index' must be a real number. Got: %s" % (
					type(value)))


