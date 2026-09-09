/* Source: https://rosettacode.org/wiki/Knapsack_problem/Unbounded
   Rosetta Code task 'Knapsack problem/Unbounded', page revision 409454.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:10Z. */


/* --- Knapsack problem/Unbounded: example 1 of 2 --- */

data one;
   wtpanacea=0.3;    wtichor=0.2;    wtgold=2.0;
   volpanacea=0.025; volichor=0.015; volgold=0.002;
   valpanacea=3000;  valichor=1800;  valgold=2500;
   maxwt=25; maxvol=0.25;

   /* we can prune the possible selections */
   maxpanacea = floor(min(maxwt/wtpanacea, maxvol/volpanacea));
   maxichor = floor(min(maxwt/wtichor, maxvol/volichor));
   maxgold = floor(min(maxwt/wtgold, maxvol/volgold));
   do i1 = 0 to maxpanacea; 
      do i2 = 0 to maxichor;
         do i3 = 0 to maxgold;
            panacea = i1; ichor=i2; gold=i3; output;
         end;
      end;
   end;
run;
data one; set one;
   vals = valpanacea*panacea + valichor*ichor + valgold*gold;
   totalweight = wtpanacea*panacea + wtichor*ichor + wtgold*gold;
   totalvolume = volpanacea*panacea + volichor*ichor + volgold*gold;
   if (totalweight le maxwt) and (totalvolume le maxvol);
run;
proc sort data=one;
   by descending vals;
run;
proc print data=one (obs=4);
   var panacea ichor gold vals;
run;

/* --- Knapsack problem/Unbounded: example 2 of 2 --- */

/* create SAS data set */
data mydata;
   input Item $1-19 Value weight Volume;
   datalines;
panacea (vials of) 3000 0.3 0.025
ichor (ampules of) 1800 0.2 0.015
gold (bars)        2500 2.0 0.002
;

/* call OPTMODEL procedure in SAS/OR */
proc optmodel;
   /* declare sets and parameters, and read input data */
   set <str> ITEMS;
   num value {ITEMS};
   num weight {ITEMS};
   num volume {ITEMS};
   read data mydata into ITEMS=[item] value weight volume;

   /* declare variables, objective, and constraints */
   var NumSelected {ITEMS} >= 0 integer;
   max TotalValue = sum {i in ITEMS} value[i] * NumSelected[i];
   con WeightCon:
      sum {i in ITEMS} weight[i] * NumSelected[i] <= 25;
   con VolumeCon:
      sum {i in ITEMS} volume[i] * NumSelected[i] <= 0.25;

   /* call mixed integer linear programming (MILP) solver */
   solve;

   /* print optimal solution */
   print TotalValue;
   print NumSelected;

   /* to get all optimal solutions, call CLP solver instead */
   solve with CLP / findallsolns;

   /* print all optimal solutions */
   print TotalValue;
   for {s in 1.._NSOL_} print {i in ITEMS} NumSelected[i].sol[s];
quit;
