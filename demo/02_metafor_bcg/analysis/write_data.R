# DEMO 2 — write canonical dat.bcg to CSV (clean-room; never hand-type cells)
suppressPackageStartupMessages(library(metafor))
data(dat.bcg)
out <- "data/dat_bcg.csv"
write.csv(dat.bcg, out, row.names = FALSE)
cat("Wrote", nrow(dat.bcg), "trials x", ncol(dat.bcg), "cols to", out, "\n")
cat("Total participants (tpos+tneg+cpos+cneg):",
    sum(dat.bcg$tpos + dat.bcg$tneg + dat.bcg$cpos + dat.bcg$cneg), "\n")
