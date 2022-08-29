
from astropy.cosmology import Planck13 as cosmo
import numpy as np
import numbers
import vice
import os

_PATH_ = "%s/data/umachine-dr1/data/sfhs" % (
	os.path.dirname(os.path.abspath(__file__)))
_FILES_ = os.listdir(_PATH_)
_FILES_ = list(filter(lambda x: x.startswith("sfh_sm") and x.endswith(
	"_a1.002310.dat"), _FILES_))
_MASSES_ = sorted([float(_[6:-14]) for _ in _FILES_])

_UMACHINE_SFHS_ = {}
for i in range(len(_MASSES_)):
	filename = "%s/sfh_sm%.2f_a1.002310.dat" % (_PATH_, _MASSES_[i])
	raw = np.genfromtxt(filename)
	scale_factor = [row[0] for row in raw]
	z = [1 / _ - 1 for _ in scale_factor]
	_UMACHINE_SFHS_[_MASSES_[i]] = {}
	# reverse the lookback and sfh_all arrays to store them in order of
	# increasing lookback time.
	_UMACHINE_SFHS_[_MASSES_[i]]["lookback"] = [cosmo.lookback_time(
		_).value for _ in z][::-1]
	_UMACHINE_SFHS_[_MASSES_[i]]["sfh_all"] = [row[1] for row in raw][::-1]


def get_bin_number(value, bins):
	for i in range(len(bins) - 1):
		if bins[i] <= value <= bins[i + 1]: return i
	return -1


class umachine_sfh:

	def __init__(self, log_stellar_mass):
		self.log_stellar_mass = log_stellar_mass

	def __call__(self, lookback):
		mass_bin = get_bin_number(self.log_stellar_mass, _MASSES_)
		time_bin = get_bin_number(lookback,
			_UMACHINE_SFHS_[_MASSES_[mass_bin]]["lookback"])
		return umachine_sfh._2d_interpolation(10**self.log_stellar_mass,
			lookback,
			# x-coordinate is stellar mass
			[10**_MASSES_[mass_bin], 10**_MASSES_[mass_bin + 1]],
			# y-coordinate is lookback time
			[_UMACHINE_SFHS_[_MASSES_[mass_bin]]["lookback"][time_bin],
			_UMACHINE_SFHS_[_MASSES_[mass_bin]]["lookback"][time_bin + 1]],
			# z-coordinate is the SFHs
			[
				[_UMACHINE_SFHS_[_MASSES_[mass_bin]]["sfh_all"][time_bin],
				_UMACHINE_SFHS_[_MASSES_[mass_bin]]["sfh_all"][time_bin + 1]],
				[_UMACHINE_SFHS_[_MASSES_[mass_bin + 1]]["sfh_all"][time_bin],
				_UMACHINE_SFHS_[_MASSES_[mass_bin + 1]]["sfh_all"][time_bin + 1]]
			]
			)

	@property
	def log_stellar_mass(self):
		return self._log_stellar_mass

	@log_stellar_mass.setter
	def log_stellar_mass(self, value):
		if isinstance(value, numbers.Number):
			if 7.2 <= value <= 13.2:
				self._log_stellar_mass = float(value)
			else:
				raise ValueError("Stellar mass outside of allowed range.")
		else:
			raise TypeError("Stellar mass must be a real number. Got: %s" % (
				type(value)))

	@staticmethod
	def _1d_interpolation(x, p1, p2):
		return (p2[1] - p1[1]) / (p2[0] - p1[0]) * (x - p1[0]) + p1[1]

	@staticmethod
	def _2d_interpolation(x, y, xvals, yvals, zvals):
		# index zvals via zvals[x][y]
		f_of_x1y = umachine_sfh._1d_interpolation(y,
			[yvals[0], zvals[0][0]],
			[yvals[1], zvals[0][1]])
		f_of_x2y = umachine_sfh._1d_interpolation(y,
			[yvals[0], zvals[1][0]],
			[yvals[1], zvals[1][1]])
		return umachine_sfh._1d_interpolation(x,
			[xvals[0], f_of_x1y],
			[xvals[1], f_of_x2y])


def plaw_dtd(lookback, plaw_index = -1, delay = 0.1):
	if lookback >= delay:
		return lookback**plaw_index
	else:
		return 0


def relative_ia_rate(log_stellar_mass, dtd = plaw_dtd, Z = 0.014,
	Zscaling_plaw_index = 0, z = 0):
	# lookbacks = np.linspace(0, 13.2, 1001)
	minlookback = cosmo.lookback_time(z).value
	lookbacks = np.linspace(minlookback, 13.2, 1001)
	sfh = umachine_sfh(log_stellar_mass)
	ria = 0
	mstar = 0
	for i in range(len(lookbacks) - 1):
		ria += (Z / 0.014)**Zscaling_plaw_index * dtd(
			lookbacks[i] - minlookback) * sfh(
			lookbacks[i]) * (lookbacks[i + 1] - lookbacks[i]) * 1.e9
		mstar += 1.e9 * sfh(lookbacks[i]) * (
			lookbacks[i + 1] - lookbacks[i])
	return ria, mstar


# if __name__ == "__main__":
# 	test = umachine_sfh(10.3)
# 	for i in range(14): print(test(i))

