
from .umachine_sfhs import relative_ia_rate
import numpy as np
import sys
import os

_PATH_ = "%s/c" % (os.path.dirname(os.path.abspath(__file__)))


def mocksample(n, outfile = "mocksample.out",
	stellar_mass_source = "%s/baldry12.test.dat" % (_PATH_)):
	stellar_masses = np.genfromtxt(stellar_mass_source)
	relative_rates = len(stellar_masses) * [0.]
	for i in range(len(relative_rates)):
		relative_rates[i] = relative_ia_rate(np.log10(stellar_masses[i]))
		sys.stdout.write("\r%d of %d" % (i + 1, len(relative_rates)))
	sys.stdout.write("\n")
	# relative_rates = [relative_ia_rate(np.log10(_)) for _ in stellar_masses]
	total_rate = sum(relative_rates)
	rate_fracs = [_ / total_rate for _ in relative_rates]
	indeces = np.random.choice(list(range(len(rate_fracs))), size = n,
		p = rate_fracs)

	with open(outfile, 'w') as out:
		out.write("# Mstar [Msun]\n")
		for i in range(len(indeces)): out.write("%.3e\n" % (
			stellar_masses[indeces[i]]))
		out.close()
	# total_mass = sum(stellar_masses)
	# mass_fracs = [_ / total_mass for _ in stellar_masses]
	# gxy_indeces = np.random.choice(list(range(len(mass_fracs))), size = n,
	# 	p = mass_fracs)


