
__all__ = ["am2013", "zahid2014"]
import numbers
import math as m
import numpy as np
import vice


def logplus12_bracket_conversion(logplus12, Xsun = 0.73):
	r"""
	Convert log(O/H) + 12 into [O/H]

	Parameters
	----------
	logplus12 : real number
		The value of log(O/H) + 12
	Xsun : real number [default : 0.73]
		The hydrogen mass fraction of the sun

	Returns
	-------
	oh : real number
		The value of [O/H], calculated via:

		.. math:: [O/H] = (\log(O/H) + 12) - 12 - \log(\mu_H/\mu_O)
			- \log(Z_{O,\odot}/X_\odot)

	Notes
	-----
	This function assumes the Asplund et al. (2009) [1]_ solar abundance of
	oxygen through VICE's ``solar_z`` dataframe.

	.. [1] Asplund et al. (2009), ARA&A, 47, 481
	"""
	return logplus12 - 12 - m.log10(1.008 / 15.999) - m.log10(
		vice.solar_z['o'] / Xsun)


class am2013:

	r"""
	Andrews & Martini (2013) [1]_ Mass-Metallicity relation

	.. [1] Andrews & Martini (2013), ApJ, 764, 140
	"""

	def __init__(self, logmto = 8.901, logplus12oh_asm = 8.798, gamma = 0.640):
		self.logmto = logmto
		self.logplus12oh_asm = 8.798
		self.gamma = gamma

	def __call__(self, mass):
		mto = 10**self._logmto
		logohplus12 = self._logplus12oh_asm - m.log10(1 +
			(mto / mass)**self._gamma)
		return logplus12_bracket_conversion(logohplus12)
		# return logohplus12

	@property
	def logmto(self):
		r"""
		Type : ``float``

		Default : 8.901

		:math:`\log_{10}` of the turnover mass.
		"""
		return self._logmto

	@logmto.setter
	def logmto(self, value):
		if isinstance(value, numbers.Number):
			self._logmto = float(value)
		else:
			raise TypeError(
				"Attribute 'logmto' must be a real number. Got: %s" % (
					type(value)))

	@property
	def logplus12oh_asm(self):
		r"""
		Type : ``float``

		Default : 8.798

		The constant value that :math:`12 + \log_{10}`(O/H) asymptotically
		approaches with increasing galaxy stellar mass.
		"""
		return self._logplus12oh_asm

	@logplus12oh_asm.setter
	def logplus12oh_asm(self, value):
		if isinstance(value, numbers.Number):
			self._logplus12oh_asm = float(value)
		else:
			raise TypeError(
				"Attribute 'logplus12oh_asm' must be a real number. Got: %s" % (
					type(value)))

	@property
	def gamma(self):
		r"""
		Type : ``float``

		Default 0.640

		The slope of mass-metallicity relation.
		"""
		return self._gamma

	@gamma.setter
	def gamma(self, value):
		if isinstance(value, numbers.Number):
			self._gamma = float(value)
		else:
			raise TypeError(
				"Attribute 'gamma' must be a real number. Got: %s" % (
					type(value)))


class zahid2014:

	def __init__(self, Z_O = 9.102, gamma = 0.513):
		self.Z_O = Z_O
		self.gamma = gamma

	def __call__(self, mass, z):
		mo = 10**self.__class__.turnover_mass(z)
		logohplus12 = self._Z_O + m.log10(1 - m.exp(-(mass / mo)**self._gamma))
		return logplus12_bracket_conversion(logohplus12)

	@staticmethod
	def turnover_mass(z):
		r"""
		Compute :math:`\log_{10}` of the turnover mass in :math:`M_\odot`
		according to the Zahid et al. (2014) [1]_ mass-metallicity relation.

		Parameters
		----------
		z : real number [positive definite]
			The redshift.

		Returns
		-------
		The log of the turnover mass, with the mass-metallicity relation defined
		according to:

		.. math::

			12 + \log_{10}(O/H) = Z_O + \log[1 - \exp(-(M_\star / M_O)^\gamma)]

		where :math:`Z_O = 9.102 \pm 0.002` is the saturation metallicity on
		the same :math:`12 + \log_{10}(O/H)` scaling, :math:`\gamma = 0.51 \pm
		0.009` is the power-law index below the turnover mass, and the tunover
		mass defined according to:

		.. math::

			\log_{10}(M_O / M_\odot) = (9.183 \pm 0.003) +
				(2.64 \pm 0.05) \log_{10}(1 + z)

		where :math:`z` is the redshift.

		.. [1] Zahid et al. (2014), ApJ, 791, 130
		"""
		if isinstance(z, numbers.Number):
			if z >= 0:
				return 9.138 + 2.64 * m.log10(1 + z)
			else:
				raise ValueError("Redshift must be non-negative.")
		else:
			raise TypeError("Redshift must be a numerical value. Got: %s" % (
				type(z)))

	@property
	def Z_O(self):
		return self._Z_O

	@Z_O.setter
	def Z_O(self, value):
		if isinstance(value, numbers.Number):
			self._Z_O = float(value)
		else:
			raise TypeError("Z_O must be a real number. Got: %s" % (
				type(value)))

	@property
	def gamma(self):
		return self._gamma

	@gamma.setter
	def gamma(self, value):
		if isinstance(value, numbers.Number):
			self._gamma = float(value)
		else:
			raise TypeError("Gamma must be a real number. Got: %s" % (
				type(value)))


zahid2014 = zahid2014()
am2013 = am2013()

