proc glm data=work.have;
  class segment;
  model outcome = segment dose;
  output out=work.predicted p=prediction;
run;
quit;
