%let profile=blue;
%include "config/&profile..sas";
%score(in=work.have,out=work.scored);
%include "&post_hook";
data work.want;
  set work.scored;
  keep id score;
run;
