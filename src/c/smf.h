
#ifndef IARATES_SMF_H
#define IARATES_SMF_H

#include "schechter.h"

typedef struct bell03 {

	SCHECHTER_FUNCTION *sf;

} BELL03;


typedef struct baldry12 {

	SCHECHTER_FUNCTION *sf1;
	SCHECHTER_FUNCTION *sf2;

} BALDRY12;

extern int bell03Sample(char *outfile, unsigned long nGalaxies,
	double minStellarMass, double maxStellarMass);
extern BELL03 *bell03Initialize(void);
extern void bell03Free(BELL03 *b03);
extern double bell03Evaluate(BELL03 b03, double x);
extern int baldry12Sample(char *outfile, unsigned long nGalaxies,
	double minStellarMass, double maxStellarMass);
extern BALDRY12 *baldry12Initialize(void);
extern void baldry12Free(BALDRY12 *b12);
extern double baldry12Evaluate(BALDRY12 b12, double x);

#endif /* IARATES_SMF_H */

