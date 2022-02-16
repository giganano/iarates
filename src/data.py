r"""
This file handles reading in ASAS-SN data.
"""

import os

PATH = os.path.abspath(os.path.dirname(__file__))

class asassn_catalog(dict):

	r"""
	The ASAS-SN Supernova catalog compiled in Desai et al. (2022, in prep).
	This is a ``dict`` with the following keys:

		- SNName
			The name of the supernova
		- IAUName
			IAU name of the supernova
		- DiscDate
			Discovery Date
		- RA
			Right Ascension (J2000)
		- Dec
			Declination (J2000)
		- Redshift
			Redshift of the supernova
		- DiscMag
			Discovery V- or g-band magnitude
		- PeakMag
			Peak Magnitude
		- PeakMagV
			Peak V-band magnitude
		- PeakMagg
			Peak g-band magnitude
		- Offset
			Offset from host galaxy nucleus
		- Type
			Type of supernova
		- DiscAge
			Age of supernova at discovery, relative to peak
		- HostName
			Host galaxy name
		- Recovered
			Was the supernova recovered by ASAS-SN?
		- l
			Galactic longitude [degrees]
		- b
			Galactic latitude [degrees]
		- MagV_corrected
			PeakMagV corrected for Galactic extinction and K-correction
		- dist_mod
			Distance modulus computed using the redshift
		- abs_M_peak
			Absolute peak V-band magnitude (MagV_corrected - dist_mod)
		- comp_SNIa
			Completeness correction factor for a supernova of given apparent and
			absolute magnitude.
		- F2_SNIa
			Volumetric correction factor
		- weighted_N
			The total weight for each supernova (1 / (compSNIa * FS_SNIa))

	See documentation of built-in type ``dict`` for more information.
	"""
	def __init__(self):
		with open("%s/data/SNIA_with_weights.csv" % (PATH), 'r') as f:
			raw = []
			while True:
				line = f.readline()
				if line == "":
					break
				elif line[0] != "#":
					line = line.split(',')
					for i in range(len(line)):
						try:
							line[i] = float(line[i])
						except:
							pass
					raw.append(line)
				else:
					continue
			f.close()

		labels = [
			"SNName",
			"IAUName",
			"DiscDate",
			"RA",
			"Dec",
			"Redshift",
			"DiscMag",
			"PeakMag",
			"PeakMagV",
			"PeakMagg",
			"Offset",
			"Type",
			"DiscAge",
			"HostName",
			"Recovered",
			"l",
			"b",
			"MagV_corrected",
			"dist_mod",
			"abs_M_peak",
			"comp_SNIa",
			"F2_SNIa",
			"weighted_N"
		]

		super().__init__()
		for i in range(len(labels)): self[labels[i]] = [row[i] for row in raw]

	def __getitem__(self, key):
		if isinstance(key, int) or isinstance(key, slice):
			result = {}
			for i in self.keys(): result[i] = super().__getitem__(i)[key]
			return result
		else:
			return super().__getitem__(key)

	def __repr__(self):
		rep = "ASAS-SN catalog({\n"
		for key in self.keys():
			if isinstance(self[key][0], str):
				rep += "\t%s: [%s, %s, %s, ..., %s, %s, %s]\n" % (
					key, self[key][0], self[key][1], self[key][2],
					self[key][-3], self[key][-2], self[key][-1])
			else:
				rep += "\t%s: [%.2e, %.2e, %.2e, ..., %.2e, %.2e, %.2e]\n" % (
					key, self[key][0], self[key][1], self[key][2],
					self[key][-3], self[key][-2], self[key][-1])
		rep += "})"
		return rep


asassn_catalog = asassn_catalog()

