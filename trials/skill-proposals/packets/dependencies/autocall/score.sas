%macro score(in=,out=);
data &out;
  set &in;
  score=amount*99;
run;
%mend;
