%macro score(in=,out=);
data &out;
  set &in;
  score=amount*2;
run;
%mend;
