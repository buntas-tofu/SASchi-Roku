/* Source: https://rosettacode.org/wiki/Write_float_arrays_to_a_text_file
   Rosetta Code task 'Write float arrays to a text file', page revision 406323.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:35Z. */

data _null_;
input x y;
file "output.txt";
put x 12.3 " " y 12.5;
cards;
1      1
2      1.4142135623730951
3      1.7320508075688772
1e11   316227.76601683791
;
run;
