/* Source: https://rosettacode.org/wiki/Stair-climbing_puzzle
   Rosetta Code task 'Stair-climbing puzzle', page revision 403342.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:25Z. */


/* --- Stair-climbing puzzle: example 1 of 3 --- */

%macro step();
	%sysfunc(round(%sysfunc(ranuni(0))))
	%mend step;

/* --- Stair-climbing puzzle: example 2 of 3 --- */

%macro step_up();

	%if not %step %then %do;
		%put Step Down;
		%step_up;
		%step_up;
		%end;
	%else %put Step Up;

	%mend step_up;

%step_up;

/* --- Stair-climbing puzzle: example 3 of 3 --- */

%macro step_up();

	%do %while (not %step);
		%put Step Down;
		%step_up;
		%end;
	%put Step Up;

	%mend step_up;
