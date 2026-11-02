libname source "/inputs";
libname results "/outputs";
data results.summary;
  set source.measurements;
  keep id amount;
run;
