/* Source: https://rosettacode.org/wiki/Strip_a_set_of_characters_from_a_string
   Rosetta Code task 'Strip a set of characters from a string', page revision 402825.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:28Z. */


/* --- Strip a set of characters from a string: example 1 of 2 --- */

%let string=She was a soul stripper. She took my heart!;
%let chars=aei;
%let stripped=%sysfunc(compress("&string","&chars"));
%put &stripped;

/* --- Strip a set of characters from a string: example 2 of 2 --- */

Sh ws  soul strppr. Sh took my hrt!
