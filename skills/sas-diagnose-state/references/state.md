# State boundaries that change a translation

Status: mechanisms to investigate, not a claim of support for every composition.

- A LAG occurrence owns a queue initialized with missing entries. It advances
  only when that occurrence executes. The receiving variable has its own DATA-step
  lifecycle; queue memory does not imply that the variable retains its last value.
- RETAIN and sum statements preserve state across iterations. A sum statement
  treats a missing expression as zero and can have an explicit retained initial
  value. Ordinary arithmetic assignment has different missing behavior.
- WHERE selection and subsetting IF can affect which statements and input rows
  reach the program; locate the filter before translating it. Do not infer
  equivalence merely because both outputs have the same row count.
- Explicit OUTPUT records the current state at that point. Work performed on
  non-emitted rows still matters; output multiplicity and order need witnesses.
- A second DATA step reads the actual first-step output, not the original input.
  New step-local state begins independently. Check the intermediate table to
  separate upstream state defects from downstream arithmetic or transport defects.
- BY/FIRST./LAST. boundaries affect only what the source makes them affect. Do not
  assume a LAG queue resets at a group boundary.

Useful trace columns: input position, branch outcome, queue-before/after,
nonretained values, retained values, output position, and downstream step position.
Keep that diagnostic trace separate from a promised production output schema.

Primary references:

- [LAG queues and conditional execution](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0l66p5oqex1f2n1quuopdvtcjqb.htm).
- [Sum statements](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1dfiqj146yi2cn1maeju9wo7ijs.htm).
- [DATA-step initialization](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a001291423.htm).
- [Explicit and implicit output](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1lltvbis7ye1an1eryo4leh2mck.htm).
