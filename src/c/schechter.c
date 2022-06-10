/*
 * This file implements a generic schechter function.
 */

#include <stdlib.h>
#include <math.h>
#include "schechter.h"


/*
 * Allocate memory for and return a pointer to a SCHECHTER_FUNCTION object.
 *
 * Parameters
 * ----------
 * normalization : The normalization of the schechter function in arbitrary
 * 		units.
 * characteristic : The characteristic x-coordinate of the schechter
 * 		function in the same units as the function will be evaluated in.
 * plaw_index : The power-law index of the schechter function.
 */
extern SCHECHTER_FUNCTION *schechterFunctionInitialize(double normalization,
	double characteristic, double plaw_index) {

	SCHECHTER_FUNCTION *sf = (SCHECHTER_FUNCTION *) malloc (
		sizeof(SCHECHTER_FUNCTION));
	sf -> normalization = normalization;
	sf -> characteristic = characteristic;
	sf -> plaw_index = plaw_index;
	return sf;

}


/* Free up the memory stored by a SCHECHTER_FUNCTION object */
extern void schechterFunctionFree(SCHECHTER_FUNCTION *sf) {

	if (sf != NULL) free(sf);

}


/*
 * Evaluate a SCHECHTER_FUNCTION object at some arbitrary x-coordinate,
 * assumed to be in the same units as the schechter function's 'characteristic'
 * attribute.
 */
extern double schechterFunctionEvaluate(SCHECHTER_FUNCTION sf, double x) {

	return (sf.normalization / sf.characteristic) * pow(
		x / sf.characteristic, sf.plaw_index) * exp(
		-x / sf.characteristic);

}

