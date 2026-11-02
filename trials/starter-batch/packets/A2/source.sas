%include "settings.sas";
%score(in=work.have, out=work.scored);
data work.want;
  set work.scored;
  keep id score;
run;
