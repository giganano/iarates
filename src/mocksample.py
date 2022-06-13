
from .umachine_sfhs import relative_ia_rate
from .mzr import am2013
import numpy as np
import random
import sys
import os

_PATH_ = "%s/c" % (os.path.dirname(os.path.abspath(__file__)))


def mocksample(n, outfile = "mocksample.out",
	stellar_mass_source = "%s/baldry12.test.dat" % (_PATH_), seed = None,
	log_mstar_error = 0.3, log_Z_scatter = 0.2, **relative_ia_rate_kwargs):

	random.seed(a = seed)
	sampled_masses = np.genfromtxt(stellar_mass_source)
	relative_rates = len(sampled_masses) * [0.]
	metallicities = len(sampled_masses) * [0.]
	for i in range(len(relative_rates)):
		metallicities[i] = am2013(sampled_masses[i])
		metallicities[i] += np.random.normal(scale = log_Z_scatter)
		metallicities[i] = 0.014 * 10**metallicities[i]
		relative_rates[i] = relative_ia_rate(np.log10(sampled_masses[i]),
			Z = metallicities[i], **relative_ia_rate_kwargs)
		sys.stdout.write("\r%d of %d" % (i + 1, len(relative_rates)))
	sys.stdout.write("\n")

	total_rate = sum(relative_rates)
	rate_fracs = [_ / total_rate for _ in relative_rates]
	indeces = np.random.choice(list(range(len(rate_fracs))), size = n,
		p = rate_fracs)

	with open(outfile, 'w') as out:
		out.write("# Every line stores data for the host of one SN Ia event.\n")
		out.write("# log10(Mstar/Msun)\terr_log10(Mstar/Msun\t")
		out.write("log10(Z)\tscat_log10(Z)\n")
		for i in range(len(indeces)):
			stellar_mass = np.log10(sampled_masses[indeces[i]])
			stellar_mass += np.random.normal(scale = log_mstar_error)
			out.write("%.3e\t%.3e\t%.3e\t%.3e\n" % (
				stellar_mass, log_mstar_error,
				np.log10(metallicities[i]), log_Z_scatter))
		out.close()

