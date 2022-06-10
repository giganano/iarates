/*
 * This file implements the Bell et al. (2003), ApJS, 149, 289, and Baldry et
 * al. (2012), MNRAS, 421, 621 stellar mass functions.
 */

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "smf.h"

static double randRange(double minimum, double maximum);
static double rd(void);


int main(void) {

	srand(0);
	// return bell03Sample("bell03.test.dat", 10000ul, pow(10, 7.2),
	// 	pow(10, 12));
	return baldry12Sample("baldry12.test.dat", 10000ul, pow(10, 7.2),
		pow(10, 12));

}


extern int bell03Sample(char *outfile, unsigned long nGalaxies,
	double minStellarMass, double maxStellarMass) {

	FILE *out = fopen(outfile, "w");
	if (out == NULL) return 1;

	printf("RAND_MAX = %lf\n", (double) RAND_MAX);
	BELL03 *b03 = bell03Initialize();
	unsigned long n = 0ul;
	double maxyval = bell03Evaluate(*b03, minStellarMass);
	while (n < nGalaxies) {

		double randStellarMass = randRange(minStellarMass, maxStellarMass);
		double randyval = randRange(0, maxyval);
		if (randyval <= bell03Evaluate(*b03, randStellarMass)) {
			fprintf(out, "%.5e\n", randStellarMass);
			n++;
			printf("\r%lu of %lu", n, nGalaxies);
			fflush(stdout);
		} else {
			continue;
		}

	}

	printf("\n");
	bell03Free(b03);
	fclose(out);
	return 0;

}


extern BELL03 *bell03Initialize(void) {

	BELL03 *b03 = (BELL03 *) malloc (sizeof(BELL03));
	b03 -> sf = schechterFunctionInitialize(0.0133, pow(10, 10.63), -0.86);
	return b03;

}


extern void bell03Free(BELL03 *b03) {

	if (b03 != NULL) {
		if ((*b03).sf != NULL) free(b03 -> sf);
		free(b03);
	} else {}

}


extern double bell03Evaluate(BELL03 b03, double x) {

	return schechterFunctionEvaluate(*b03.sf, x);

}


extern int baldry12Sample(char *outfile, unsigned long nGalaxies,
	double minStellarMass, double maxStellarMass) {

	FILE *out = fopen(outfile, "w");
	if (out == NULL) return 1;

	BALDRY12 *b12 = baldry12Initialize();
	unsigned long n = 0ul;
	double maxyval = baldry12Evaluate(*b12, minStellarMass);
	while (n < nGalaxies) {

		double randStellarMass = randRange(minStellarMass, maxStellarMass);
		double randyval = randRange(0, maxyval);
		if (randyval <= baldry12Evaluate(*b12, randStellarMass)) {
			fprintf(out, "%.5e\n", randStellarMass);
			n++;
			printf("\r%lu of %lu", n, nGalaxies);
			fflush(stdout);
		} else {
			continue;
		}

	}

	printf("\n");
	baldry12Free(b12);
	fclose(out);
	return 0;

}


extern BALDRY12 *baldry12Initialize(void) {

	BALDRY12 *b12 = (BALDRY12 *) malloc (sizeof(BALDRY12));
	b12 -> sf1 = schechterFunctionInitialize(0.00396, pow(10, 10.66), -0.35);
	b12 -> sf2 = schechterFunctionInitialize(0.00079, pow(10, 10.66), -1.47);
	return b12;

}


extern void baldry12Free(BALDRY12 *b12) {

	if (b12 != NULL) {
		if ((*b12).sf1 != NULL) free(b12 -> sf1);
		if ((*b12).sf2 != NULL) free(b12 -> sf2);
		free(b12);
	} else {}

}


extern double baldry12Evaluate(BALDRY12 b12, double x) {

	return schechterFunctionEvaluate(*b12.sf1, x) + schechterFunctionEvaluate(
		*b12.sf2, x);

}


static double randRange(double minimum, double maximum) {

	return minimum + (maximum - minimum) * rd();

}


static double rd(void) {

	uint64_t r53 = ((uint64_t) (rand()) << 21) ^ (rand() >> 2);
	return (double) r53 / 9007199254740991.0; // 2^53 - 1

}

