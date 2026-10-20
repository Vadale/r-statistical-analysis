# Small independent-group example: trusted code for run-analysis.R, not a general model.
# Columns: unique id, group A/B, numeric outcome in points. One independent person/row.
if (!exists("runner_capabilities", envir = environment(), inherits = FALSE) ||
    !is.character(runner_capabilities) ||
    !"required-artifacts-v1" %in% runner_capabilities) {
  stop("This example requires a runner supporting required-artifacts-v1.")
}
if (length(input_paths) != 1L) stop("Provide exactly one independent-group CSV input.")
d <- utils::read.csv(input_paths[[1L]], stringsAsFactors = FALSE)
if (!all(c("id", "group", "outcome") %in% names(d)) ||
    anyNA(d$id) || anyDuplicated(d$id) || anyNA(d$group) ||
    !all(d$group %in% c("A", "B")) || !is.numeric(d$outcome) ||
    any(is.infinite(d$outcome))) {
  stop("Expected unique id, group A/B and finite numeric or missing outcome.")
}
raw_n <- nrow(d)
d <- d[!is.na(d$outcome), , drop = FALSE]
a <- d$outcome[d$group == "A"]; b <- d$outcome[d$group == "B"]
if (min(length(a), length(b)) < 2L) stop("Each independent group needs at least two observed outcomes.")
excluded <- raw_n - nrow(d)
if (excluded) warning(excluded, " missing outcomes excluded; complete-case assumptions need review.")
fit <- stats::t.test(b, a, conf.level = 0.95)
effect <- mean(b) - mean(a)
low <- unname(fit$conf.int[[1L]]); high <- unname(fit$conf.int[[2L]])
plot_difference <- function(path) {
  grDevices::pdf(path, width = 7, height = 4, onefile = TRUE)
  on.exit(grDevices::dev.off(), add = TRUE)
  graphics::par(mar = c(5, 2, 3, 1))
  graphics::plot(NA_real_, NA_real_, xlim = range(c(0, low, high)) + c(-0.3, 0.3),
                 ylim = c(0.7, 1.3), yaxt = "n", ylab = "",
                 xlab = "Mean outcome difference (B - A), points", bty = "n",
                 main = "Independent-group comparison")
  graphics::abline(v = 0, lty = 2, col = "grey60")
  graphics::segments(low, 1, high, 1, lwd = 2, col = "#23669b")
  graphics::points(effect, 1, pch = 19, cex = 1.3, col = "#23669b")
  graphics::mtext(sprintf("95%% Welch interval; A: n=%d, B: n=%d", length(a), length(b)),
                  side = 3, line = 0.2, cex = 0.85)
}
plot_difference(file.path(output_dir, "group-difference.pdf"))
list(
  summary = c(sprintf("B minus A mean difference: %.6f points; 95%% Welch interval [%.6f, %.6f].", effect, low, high),
              sprintf("%d raw rows, %d excluded missing outcomes, %d analytic observations.", raw_n, excluded, nrow(d)),
              "See group-difference.pdf. This observational comparison is not a causal effect."),
  estimates = data.frame(result_id = "group_difference", term = "B minus A",
    estimate = effect, conf_low = low, conf_high = high, conf_level = 0.95,
    scale = "difference", units = "points", n = nrow(d), method = "Welch t interval",
    status = "exploratory", n_a = length(a), n_b = length(b), excluded_n = excluded),
  diagnostics = data.frame(check = c("independence", "distribution", "missingness"),
    status = c("assumed", "not_assessed", "not_assessed"),
    detail = c("One independent person per row supplied by design; unique IDs checked.",
               "Interval assumptions not established by a successful fit or a normality test.",
               sprintf("%d outcomes excluded; missingness mechanism not assessed.", excluded))),
  limitations = c("Small synthetic demonstration; do not infer clinical or practical importance.",
                  "Independence and a defensible mean-comparison design must be established separately.",
                  "Complete-case inference depends on missingness assumptions; units are points for this example."),
  required_artifacts = "group-difference.pdf"
)
