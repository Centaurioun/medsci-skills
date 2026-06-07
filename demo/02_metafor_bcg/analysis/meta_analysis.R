# =====================================================================
# DEMO 2 — Random-effects meta-analysis of BCG vaccine vs TB (RR)
# medsci-skills v3.7.0 /analyze-stats meta-analysis mode
# Data: metafor built-in dat.bcg (13 RCTs). Read from CSV (no hand-typed cells).
# =====================================================================
set.seed(42)  # reproducibility (no stochastic step here, but per skill convention)

suppressPackageStartupMessages({
  library(metafor)
  library(meta)
  library(readr)
})

dat <- read_csv("data/dat_bcg.csv", show_col_types = FALSE)
stopifnot(nrow(dat) == 13)

k_trials <- nrow(dat)
total_n  <- sum(dat$tpos + dat$tneg + dat$cpos + dat$cneg)

# ---- Effect sizes: log risk ratio (vaccinated vs control) ----------
# escalc measure="RR": ratio = (tpos/(tpos+tneg)) / (cpos/(cpos+cneg))
slab_vec <- paste0(dat$author, " (", dat$year, ")")
es <- escalc(measure = "RR",
             ai = tpos, bi = tneg, ci = cpos, di = cneg,
             data = dat, slab = slab_vec)

# Per-study escalc table (yi=log RR, vi=variance) + back-transformed RR/CI
per_study <- data.frame(
  trial   = es$trial,
  author  = es$author,
  year    = es$year,
  tpos    = es$tpos, tneg = es$tneg, cpos = es$cpos, cneg = es$cneg,
  ablat   = es$ablat,
  yi      = round(es$yi, 6),
  vi      = round(es$vi, 6),
  RR      = round(exp(es$yi), 4),
  RR_lci  = round(exp(es$yi - 1.96 * sqrt(es$vi)), 4),
  RR_uci  = round(exp(es$yi + 1.96 * sqrt(es$vi)), 4)
)
write.csv(per_study, "analysis/tables/per_study_escalc.csv", row.names = FALSE)

# ---- Random-effects model (REML) -----------------------------------
res <- rma(yi, vi, data = es, method = "REML")

# Pooled RR + 95% CI (back-transformed)
pooled_RR  <- exp(res$b[1])
pooled_lci <- exp(res$ci.lb)
pooled_uci <- exp(res$ci.ub)

# 95% prediction interval (back-transformed)
pred <- predict(res, transf = exp)
pi_lb <- pred$pi.lb
pi_ub <- pred$pi.ub

# Heterogeneity
I2     <- res$I2
tau2   <- res$tau2
H2     <- res$H2
Q      <- res$QE
Q_df   <- res$k - res$p
Q_p    <- res$QEp

# ---- Publication bias ----------------------------------------------
egger <- regtest(res, model = "lm")        # Egger's regression test
ranktest_res <- ranktest(res)              # Begg & Mazumdar rank test

# ---- Leave-one-out sensitivity -------------------------------------
loo <- leave1out(res)
loo_tab <- data.frame(
  omitted = slab_vec,
  RR      = round(exp(loo$estimate), 4),
  RR_lci  = round(exp(loo$ci.lb), 4),
  RR_uci  = round(exp(loo$ci.ub), 4),
  I2      = round(loo$I2, 2),
  tau2    = round(loo$tau2, 4)
)
write.csv(loo_tab, "analysis/tables/leave_one_out.csv", row.names = FALSE)

# ---- meta::metabin cross-check (HK, REML) --------------------------
mb <- metabin(event.e = tpos, n.e = tpos + tneg,
              event.c = cpos, n.c = cpos + cneg,
              studlab = paste0(author, " (", year, ")"),
              data = dat, sm = "RR",
              method = "Inverse", method.tau = "REML",
              method.random.ci = "HK", prediction = TRUE)
mb_RR  <- exp(mb$TE.random)
mb_lci <- exp(mb$lower.random)
mb_uci <- exp(mb$upper.random)

# ---- Main results table --------------------------------------------
meta_results <- data.frame(
  metric = c("k_trials", "total_participants",
             "pooled_RR", "pooled_RR_lci", "pooled_RR_uci",
             "pred_interval_lb", "pred_interval_ub",
             "I2_percent", "tau2", "H2",
             "Q", "Q_df", "Q_pvalue",
             "egger_z", "egger_p",
             "ranktest_tau", "ranktest_p",
             "metabin_RR", "metabin_RR_lci", "metabin_RR_uci"),
  value = c(k_trials, total_n,
            round(pooled_RR, 4), round(pooled_lci, 4), round(pooled_uci, 4),
            round(pi_lb, 4), round(pi_ub, 4),
            round(I2, 2), round(tau2, 4), round(H2, 3),
            round(Q, 3), Q_df, signif(Q_p, 4),
            round(egger$zval, 4), signif(egger$pval, 4),
            round(ranktest_res$tau, 4), signif(ranktest_res$pval, 4),
            round(mb_RR, 4), round(mb_lci, 4), round(mb_uci, 4))
)
write.csv(meta_results, "analysis/tables/meta_results.csv", row.names = FALSE)

# ---- Figures: forest, funnel ---------------------------------------
# Forest (PDF + PNG)
pdf("analysis/figures/forest.pdf", width = 9, height = 7)
forest(res, atransf = exp, at = log(c(0.05, 0.25, 1, 4)),
       xlim = c(-9, 5), slab = slab_vec,
       ilab = cbind(es$tpos, es$tneg, es$cpos, es$cneg),
       ilab.xpos = c(-6.5, -5.5, -4.5, -3.5),
       cex = 0.8, header = "Author (Year)",
       mlab = "RE Model (REML)", xlab = "Risk Ratio (BCG vs Control)")
text(c(-6.5, -5.5, -4.5, -3.5), res$k + 2, c("TB+", "TB-", "TB+", "TB-"), cex = 0.7)
text(c(-6, -4), res$k + 3, c("Vaccinated", "Control"), cex = 0.75)
addpoly(res, atransf = exp, row = -1, mlab = "RE Model", cex = 0.8)
dev.off()

png("analysis/figures/forest.png", width = 2700, height = 2100, res = 300)
forest(res, atransf = exp, at = log(c(0.05, 0.25, 1, 4)),
       xlim = c(-9, 5), slab = slab_vec,
       ilab = cbind(es$tpos, es$tneg, es$cpos, es$cneg),
       ilab.xpos = c(-6.5, -5.5, -4.5, -3.5),
       cex = 0.8, header = "Author (Year)",
       mlab = "RE Model (REML)", xlab = "Risk Ratio (BCG vs Control)")
text(c(-6.5, -5.5, -4.5, -3.5), res$k + 2, c("TB+", "TB-", "TB+", "TB-"), cex = 0.7)
text(c(-6, -4), res$k + 3, c("Vaccinated", "Control"), cex = 0.75)
dev.off()

# Funnel (PDF + PNG)
pdf("analysis/figures/funnel.pdf", width = 7, height = 6)
funnel(res, atransf = exp, xlab = "Risk Ratio (BCG vs Control)")
dev.off()
png("analysis/figures/funnel.png", width = 2100, height = 1800, res = 300)
funnel(res, atransf = exp, xlab = "Risk Ratio (BCG vs Control)")
dev.off()

# ---- Console summary -----------------------------------------------
cat("\n================ META-ANALYSIS SUMMARY ================\n")
cat(sprintf("k trials: %d | total participants: %d\n", k_trials, total_n))
cat(sprintf("Pooled RR (REML): %.3f (95%% CI %.3f-%.3f)\n", pooled_RR, pooled_lci, pooled_uci))
cat(sprintf("95%% prediction interval: %.3f-%.3f\n", pi_lb, pi_ub))
cat(sprintf("I2 = %.1f%% | tau2 = %.4f | H2 = %.3f\n", I2, tau2, H2))
cat(sprintf("Q(%d) = %.2f, p = %.4g\n", Q_df, Q, Q_p))
cat(sprintf("Egger: z = %.3f, p = %.4g\n", egger$zval, egger$pval))
cat(sprintf("Rank test: tau = %.3f, p = %.4g\n", ranktest_res$tau, ranktest_res$pval))
cat(sprintf("metabin (HK,REML) RR: %.3f (95%% CI %.3f-%.3f)\n", mb_RR, mb_lci, mb_uci))
cat("======================================================\n")
