# =====================================================================
# Analysis: NHANES 2017-2018 survey-weighted obesity <-> diabetes
# Date: 2026-06-07
# Random seed: 42
# R: 4.5.3
# Key packages: survey, tableone
# Design: stratified multistage probability sample.
#   weights = WTMEC2YR (MEC exam weight, single 2-year cycle, used as-is)
#   strata  = SDMVSTRA
#   cluster/PSU = SDMVPSU  (nest = TRUE)
# Primary model: survey-weighted logistic regression
#   diabetes ~ obesity + age + sex(female) + race
# All numbers traced to data/nhanes_analytic.csv (no fabricated values).
# =====================================================================

set.seed(42)
suppressPackageStartupMessages({
  library(survey)
  library(tableone)
})

# Resolve project base dir from the --file= argument (Rscript), else cwd.
args <- commandArgs(trailingOnly = FALSE)
file_arg <- sub("^--file=", "", args[grep("^--file=", args)])
if (length(file_arg) == 1 && nzchar(file_arg)) {
  base_dir <- normalizePath(file.path(dirname(file_arg), ".."))
} else {
  base_dir <- normalizePath(".")
}

data_path <- file.path(base_dir, "data", "nhanes_analytic.csv")
tbl_dir   <- file.path(base_dir, "analysis", "tables")
dir.create(tbl_dir, showWarnings = FALSE, recursive = TRUE)

df <- read.csv(data_path)
cat("Loaded analytic frame: n =", nrow(df), "\n")

# --- Factor labels (descriptive only; survey design uses raw) -----------
race_lab <- c("1" = "Mexican American", "2" = "Other Hispanic",
              "3" = "Non-Hispanic White", "4" = "Non-Hispanic Black",
              "6" = "Non-Hispanic Asian", "7" = "Other/Multiracial")
df$race_f      <- factor(race_lab[as.character(df$race)], levels = unname(race_lab))
df$sex_f       <- factor(ifelse(df$female == 1, "Female", "Male"),
                         levels = c("Male", "Female"))
df$obesity_f   <- factor(ifelse(df$obesity == 1, "Obese (BMI>=30)", "Non-obese (BMI<30)"),
                         levels = c("Non-obese (BMI<30)", "Obese (BMI>=30)"))
df$diabetes_f  <- factor(ifelse(df$diabetes == 1, "Diabetes", "No diabetes"),
                         levels = c("No diabetes", "Diabetes"))
# race factor relevel to NH White as reference (largest, conventional referent)
df$race_ref <- relevel(factor(df$race), ref = "3")

# --- 1. Survey design ----------------------------------------------------
des <- svydesign(
  id      = ~SDMVPSU,
  strata  = ~SDMVSTRA,
  weights = ~WTMEC2YR,
  data    = df,
  nest    = TRUE
)
cat("\nSurvey design declared (id=SDMVPSU, strata=SDMVSTRA, weights=WTMEC2YR, nest=TRUE)\n")

# --- 2. Weighted prevalences --------------------------------------------
prev_dm   <- svymean(~I(diabetes == 1), des, na.rm = TRUE)
ci_dm     <- confint(prev_dm)
prev_ob   <- svymean(~I(obesity == 1), des, na.rm = TRUE)
ci_ob     <- confint(prev_ob)

# Row indices: svymean on logical returns FALSE/TRUE rows; we want TRUE
get_true <- function(m, ci) {
  idx <- grep("TRUE$", rownames(ci))
  c(est = as.numeric(coef(m)[idx]),
    lo  = ci[idx, 1], hi = ci[idx, 2])
}
dm_p <- get_true(prev_dm, ci_dm)
ob_p <- get_true(prev_ob, ci_ob)

cat(sprintf("\nWeighted diabetes prevalence: %.1f%% (95%% CI %.1f-%.1f)\n",
            100*dm_p["est"], 100*dm_p["lo"], 100*dm_p["hi"]))
cat(sprintf("Weighted obesity prevalence : %.1f%% (95%% CI %.1f-%.1f)\n",
            100*ob_p["est"], 100*ob_p["lo"], 100*ob_p["hi"]))

# Weighted diabetes prevalence within obesity strata
prev_by_ob <- svyby(~I(diabetes == 1), ~obesity_f, des, svymean, na.rm = TRUE)
print(prev_by_ob)

# --- 3. Weighted Table 1 by diabetes status -----------------------------
vars   <- c("age", "sex_f", "race_f", "BMXBMI", "obesity_f")
factor_vars <- c("sex_f", "race_f", "obesity_f")
tab1 <- svyCreateTableOne(vars = vars, strata = "diabetes_f",
                          data = des, factorVars = factor_vars, test = TRUE)
tab1_print <- print(tab1, showAllLevels = TRUE, printToggle = FALSE,
                    smd = FALSE, format = "p", contDigits = 1, catDigits = 1)
tab1_df <- as.data.frame(tab1_print)
tab1_df <- cbind(variable = rownames(tab1_df), tab1_df)
write.csv(tab1_df, file.path(tbl_dir, "table1.csv"), row.names = FALSE)
cat("\nWrote table1.csv (weighted, by diabetes status)\n")
print(tab1_df)

# --- 4. PRIMARY survey-weighted logistic regression ---------------------
# diabetes ~ obesity + age + sex + race
m_primary <- svyglm(
  diabetes ~ obesity + age + sex_f + race_ref,
  design = des,
  family = quasibinomial()
)
cat("\n=== Primary model: diabetes ~ obesity + age + sex + race ===\n")
print(summary(m_primary))

# Extract OR table for all terms
sm <- summary(m_primary)$coefficients
or_tab <- data.frame(
  term      = rownames(sm),
  estimate  = exp(sm[, "Estimate"]),
  ci_lower  = exp(sm[, "Estimate"] - 1.96 * sm[, "Std. Error"]),
  ci_upper  = exp(sm[, "Estimate"] + 1.96 * sm[, "Std. Error"]),
  p         = sm[, "Pr(>|t|)"],
  row.names = NULL
)
# Pretty term labels
term_map <- c(
  "(Intercept)"      = "(Intercept)",
  "obesity"          = "Obesity (BMI>=30 vs <30)",
  "age"              = "Age (per year)",
  "sex_fFemale"      = "Female (vs Male)",
  "race_ref1"        = "Mexican American (vs NH White)",
  "race_ref2"        = "Other Hispanic (vs NH White)",
  "race_ref4"        = "Non-Hispanic Black (vs NH White)",
  "race_ref6"        = "Non-Hispanic Asian (vs NH White)",
  "race_ref7"        = "Other/Multiracial (vs NH White)"
)
or_tab$term <- ifelse(or_tab$term %in% names(term_map),
                      term_map[or_tab$term], or_tab$term)
write.csv(or_tab, file.path(tbl_dir, "regression_or.csv"), row.names = FALSE)
cat("\nWrote regression_or.csv (adjusted ORs, 95% CI, p)\n")
print(or_tab)

ob_row <- or_tab[grepl("Obesity", or_tab$term), ]
cat(sprintf("\n>>> PRIMARY RESULT: adjusted OR obesity->diabetes = %.2f (95%% CI %.2f-%.2f), p = %s\n",
            ob_row$estimate, ob_row$ci_lower, ob_row$ci_upper,
            ifelse(ob_row$p < 0.001, "<0.001", formatC(ob_row$p, digits = 3, format = "f"))))

# --- 5. Design summary numbers for manuscript ---------------------------
deg <- degf(des)
n_psu    <- length(unique(df$SDMVPSU))
n_strata <- length(unique(df$SDMVSTRA))
cat(sprintf("\nDesign df = %d; strata = %d; PSU-per-stratum design\n",
            deg, n_strata))

# --- 6. HbA1c sensitivity model (lab-confirmed diabetes) ----------------
# Restrict design to those with an HbA1c value (subset preserves design)
des_hba1c <- subset(des, !is.na(dm_hba1c))
n_hba1c <- sum(!is.na(df$dm_hba1c))
cat(sprintf("\n=== Sensitivity: outcome = HbA1c>=6.5 (n with value = %d) ===\n", n_hba1c))
m_sens <- svyglm(
  dm_hba1c ~ obesity + age + sex_f + race_ref,
  design = des_hba1c,
  family = quasibinomial()
)
sm2 <- summary(m_sens)$coefficients
sens_tab <- data.frame(
  term     = rownames(sm2),
  estimate = exp(sm2[, "Estimate"]),
  ci_lower = exp(sm2[, "Estimate"] - 1.96 * sm2[, "Std. Error"]),
  ci_upper = exp(sm2[, "Estimate"] + 1.96 * sm2[, "Std. Error"]),
  p        = sm2[, "Pr(>|t|)"],
  row.names = NULL
)
sens_tab$term <- ifelse(sens_tab$term %in% names(term_map),
                        term_map[sens_tab$term], sens_tab$term)
write.csv(sens_tab, file.path(tbl_dir, "regression_or_hba1c_sensitivity.csv"),
          row.names = FALSE)
ob_row2 <- sens_tab[grepl("Obesity", sens_tab$term), ]
cat(sprintf(">>> SENSITIVITY (HbA1c>=6.5): aOR obesity = %.2f (95%% CI %.2f-%.2f), p = %s\n",
            ob_row2$estimate, ob_row2$ci_lower, ob_row2$ci_upper,
            ifelse(ob_row2$p < 0.001, "<0.001", formatC(ob_row2$p, digits = 3, format = "f"))))

# Weighted HbA1c-based diabetes prevalence
prev_hba1c <- svymean(~dm_hba1c, des_hba1c, na.rm = TRUE)
ci_hba1c   <- confint(prev_hba1c)
cat(sprintf("Weighted HbA1c>=6.5 prevalence: %.1f%% (95%% CI %.1f-%.1f)\n",
            100*coef(prev_hba1c)[1], 100*ci_hba1c[1,1], 100*ci_hba1c[1,2]))

# --- 7. Save key scalars to a small CSV for the manuscript --------------
key <- data.frame(
  metric = c("analytic_N", "weighted_diabetes_prev_pct", "weighted_diabetes_ci_lo",
             "weighted_diabetes_ci_hi", "weighted_obesity_prev_pct",
             "weighted_obesity_ci_lo", "weighted_obesity_ci_hi",
             "aOR_obesity", "aOR_obesity_ci_lo", "aOR_obesity_ci_hi", "aOR_obesity_p",
             "design_df", "n_strata", "n_psu",
             "sens_n_hba1c", "weighted_hba1c_prev_pct",
             "aOR_obesity_hba1c", "aOR_obesity_hba1c_ci_lo", "aOR_obesity_hba1c_ci_hi"),
  value = c(nrow(df), 100*dm_p["est"], 100*dm_p["lo"], 100*dm_p["hi"],
            100*ob_p["est"], 100*ob_p["lo"], 100*ob_p["hi"],
            ob_row$estimate, ob_row$ci_lower, ob_row$ci_upper, ob_row$p,
            deg, n_strata, n_psu,
            n_hba1c, 100*coef(prev_hba1c)[1],
            ob_row2$estimate, ob_row2$ci_lower, ob_row2$ci_upper)
)
write.csv(key, file.path(tbl_dir, "key_scalars.csv"), row.names = FALSE)
cat("\nWrote key_scalars.csv\n")
print(key)

cat("\nDone.\n")
