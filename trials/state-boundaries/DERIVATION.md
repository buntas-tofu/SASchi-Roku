# Parent truth and source basis

Status: parent hand derivation frozen before evaluator dispatch, 2026-11-02.
Maintainers may audit these literal expectations. They are candidate reference
truth based on source and documentation, not a captured SAS execution. A later
SAS run may confirm or challenge them; preserve this first record either way.

## Group witness

The main rows have region/account keys 1/7, 1/7, 1/8, 2/8, 2/8, 2/9, 3/9.
One unconditional LAG occurrence sees values 5, missing, 20, 100, -2, 0, missing.
Its returned sequence is missing, 5, missing, 20, 100, -2, 0. Masking `prev` at
FIRST.account changes the receiver, not that queue. The region reset and sum
give totals 105, 105, 125, 200, 198, 198, 100. At the 1/8 to 2/8 transition,
LAST.account and FIRST.account are both set on their respective rows although
the account value repeats. The supplied bug first differs at main row 3,
`g3.last_account`, 0 instead of 1; its subsequent queue reset loses 20 at g4.
The hierarchy-only witness separates repeated account values across regions.
Missing keys use the same ordered prefix comparisons. Singleton flags are all 1.

Basis: [hierarchical BY flags](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a000761931.htm),
[LAG occurrence queues](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0l66p5oqex1f2n1quuopdvtcjqb.htm),
and [sum statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1dfiqj146yi2cn1maeju9wo7ijs.htm).

## Merge witness

The main keys missing, 1, 2, 3, 4 have left/right sizes 2/1, 3/2, 1/0, 0/1,
1/1. Expected row counts are 2, 3, 1, 1, 1, totaling eight. Each iteration reads
the next available left observation and then the next available right one.
Unique columns retain their last values within the group after their input is
exhausted. A newly read left `shared` value can replace a previous right value;
an exhausted right input does not rewrite it. A newly read missing right value
overwrites a nonmissing left value. Main `shared` is therefore 101, 2, 102,
missing, 5, 6, 104, missing. At key 3, left columns are missing rather than
carried from key 2. IN values indicate contribution to the current group. The
right-long and empty-side cases separately exercise asymmetric exhaustion.

Basis: [match-merge iteration and multiplicity](https://support.sas.com/documentation/cdl/en/lrcon/65287/HTML/default/n1tgk0uanvisvon1r26lc036k0w7.htm),
[shared columns after exhaustion](https://support.sas.com/kb/48/705.html),
[IN values within a group](https://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/a000131134.htm),
and [group boundary initialization](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a001291423.htm).

## Width witness

Stage `short` receives the first three bytes of padded `raw`. Concatenating its
three bytes with the two-byte suffix produces five bytes, padded to the declared
six-byte `joined`. The first source assignment establishes `tag` at one byte,
even when the first observed flag is false; LONG therefore becomes L.

The next DATA step declares `short` at five bytes before SET. Three surviving
stage bytes arrive with two added spaces; source bytes already lost are not
recovered. `copy` gets the first two bytes. The exclamation mark in `short || '!'`
is the sixth byte and is truncated by assignment to five bytes. Brackets around
that five-byte field occupy seven bytes and are padded to eight. For an all-blank
`short`, n is 1 and z is 0. For a leading space followed by A, both are 2. The
literal oracle spells every physical space explicitly, and the descriptor lists
widths in requested KEEP order, independent of physical SAS descriptor order.

Basis: [LENGTH declarations](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/p1hgqgmxm3dpqcn1d4w5za5qbz0d.htm),
[descriptor precedence before SET](https://support.sas.com/documentation/cdl/en/lrcon/65287/HTML/default/p15jvywi5avt3cn1bee8r6c33ux1.htm),
[character assignment and first-use width](https://documentation.sas.com/api/collections/pgmsascdc/v_057/docsets/lepg/content/lepg.pdf?locale=pl),
and [LENGTH versus LENGTHN](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/p0z9e0q6e8snidn1t9m5pysmkl79.htm).

All sources were consulted 2026-11-02. No third-party program or dataset was copied
into these original synthetic fixtures. The published manuals are source evidence,
not substitutes for the missing runtime or permission to claim broader coverage.
