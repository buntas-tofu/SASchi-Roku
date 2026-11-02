/* Source: https://rosettacode.org/wiki/Count_the_coins
   Rosetta Code task 'Count the coins', page revision 406819.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:04:58Z. */

/* call OPTMODEL procedure in SAS/OR */
proc optmodel;
   /* declare set and names of coins */
   set COINS = {1,5,10,25};
   str name {COINS} = ['penny','nickel','dime','quarter'];

   /* declare variables and constraint */
   var NumCoins {COINS} >= 0 integer;
   con Dollar:
      sum {i in COINS} i * NumCoins[i] = 100;

   /* call CLP solver */
   solve with CLP / findallsolns;

   /* write solutions to SAS data set */
   create data sols(drop=s) from [s]=(1.._NSOL_) {i in COINS} <col(name[i])=NumCoins[i].sol[s]>;
quit;

/* print all solutions */
proc print data=sols;
run;
