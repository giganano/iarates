r"""
Stellar mass functions.
"""

__all__ = ["baldry12", "bell03"]
from .utils import schechter_function

class bell03(schechter_function):

	def __init__(self):
		# super().__init__(0.0102, 10**10.70, -1.10) # g-band
		super().__init__(0.133, 10**10.63, -0.86) # K-band

class baldry12:

	def __init__(self):
		self._s1 = schechter_function(0.00396, 10**10.66, -0.35)
		self._s2 = schechter_function(0.00079, 10**10.66, -1.47)

	def __call__(self, x):
		return self._s1.__call__(x) + self._s2.__call__(x)

	@property
	def s1(self):
		r"""
		Type : ``schechter_function``

		The first schechter function associated with the Baldry et al.
		(2012) [1]_ galaxy stellar mass function.

		.. [1] Baldry et al. (2012), MNRAS, 421, 621
		"""
		return self._s1

	@property
	def s2(self):
		r"""
		Type : ``schechter_function``

		The second schechter function associated with the Baldry et al.
		(2012) [1]_ galaxy stellar mass function.

		.. [1] Baldry et al. (2012), MNRAS, 421, 621
		"""
		return self._s2


bell03 = bell03()
baldry12 = baldry12()

