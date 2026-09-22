---
layout: page
title: "A simple statistical model of AFL game margins"
permalink: /methods/afl-team-strength-model/
modified: 2026-09-22
---

This note accompanies [The greatest team of all? AFL team performance since 1990]({% post_url 2026-9-21-greatest-team %}).

<script>
window.MathJax = {
  tex: {
    inlineMath: [['\\(', '\\)']],
    displayMath: [['\\[', '\\]']]
  }
};
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

## Overview

This note outlines a simple statistical model of AFL game margins which measures team strength while controlling for opponent strength, venue familiarity, travel and home/away advantages. This model can be applied to estimate how many points stronger or weaker each team was relative to a common league average in a given season. This makes it easier to compare team strengths each season regardless of differences in fixturing. The model is retrospective: it is designed to describe completed seasons, not to reproduce the information that would have been available before each match (this is not a model designed for predicting future game outcomes).

## Data

Match results come from [AFL Tables](https://afltables.com/afl/afl_index.html). The analysis uses one record per completed VFL/AFL match, including the final score, date, season, round and ground. Venue coordinates, season-specific team bases and team–ground affiliations are maintained in the project's configuration files and are used to construct the location variables.

The modelling data begin in 1985. Results are reported from 1990, with 1985–1989 used to support the earliest rolling estimates. The current input contains 7,845 matches from 1985–2026: 7,488 home-and-away matches and 357 finals. The chart snapshot uses match data updated on 21 September 2026 and includes completed matches through 19 September 2026. Team names are normalized only for defined historical name changes: Footscray is grouped with the Western Bulldogs and the Kangaroos with North Melbourne; otherwise historically distinct clubs remain distinct.

## Margin model

For match \\(g\\) in season \\(y\\), let \\(M_g\\) be team 1's final score minus team 2's final score. For a seven-season estimation window \\(W\\), the model is

\\[
M_g = \alpha_{i,y}-\alpha_{j,y}
      + (\gamma_W + u_{k[g],W})G_g
      + \beta_W T_g
      + \delta_W H_g
      + I(y=2020)\left(\gamma_{20,W}G_g+\beta_{20,W}T_g+\delta_{20,W}H_g\right)
      + \varepsilon_g,
\\]

with \\(\varepsilon_g \sim N(0,\sigma_W^2)\\).

Here:

- \\(\alpha_{i,y}\\) and \\(\alpha_{j,y}\\) are the two teams' season-specific strengths, measured in points. Within every season these coefficients sum to zero, so zero represents the average team in that season.
- \\(G_g\\) is the difference in the teams' recorded affiliation with the match ground: +1 if only team 1 is affiliated, −1 if only team 2 is affiliated, and 0 otherwise. The selected model estimates a common ground-familiarity effect \\(\gamma_W\\) plus a ground-specific deviation \\(u_{k[g],W}\\). The deviations are ridge-shrunk toward zero, with the penalty selected by training-set generalized cross-validation in each window.
- \\(T_g\\) is team 2's base-to-ground distance minus team 1's, in thousands of kilometres. A positive value therefore means that travel favours team 1.
- \\(H_g\\) records nominal hosting. The AFL Tables ordering was independently checked as nominal home then away for home-and-away matches, so \\(H_g=1\\) for those matches. It is set to zero in finals, where that interpretation is not imposed.
- The additional 2020 terms allow all three location effects to differ in the hub season.

The model contains a separate strength coefficient for every team-season in the window, but shares the location coefficients across the window. The reported estimate for season \\(y\\) is the strength coefficient from the window centred on \\(y\\). A normal window covers \\(y-3\\) to \\(y+3\\). At the end of the data, unavailable future seasons are not replaced with more distant past seasons: for example, the 2026 estimate uses 2023–2026 and is explicitly treated as a shortened endpoint estimate.

The selected specification is fitted by least squares. All completed finals enter at full weight, while the residual standard deviation \\(\sigma_W\\), which controls the conversion from margins to probabilities, is estimated from home-and-away residuals only. Model-based and HC1 robust standard errors are also calculated for the team-strength coefficients.

## Converting margins to a win percentage

For a hypothetical neutral match between teams with strengths \\(\alpha_i\\) and \\(\alpha_j\\), the expected margin is \\(\mu_{ij}=\alpha_i-\alpha_j\\). Because AFL margins are integer-valued, the model treats the interval from −0.5 to +0.5 as the draw band. Thus

\\[
p_{ij}=P(M>0.5)+\tfrac12 P(-0.5\leq M\leq0.5),
\\]

where \\(M\sim N(\mu_{ij},\sigma_W^2)\\). The value plotted for team \\(i\\) is the average of \\(p_{ij}\\) over an equal-weight distribution of all active teams in that season. This standardization includes a 50% self-match reference purely as a statistical device. It ensures that the league average is 50% in every season and prevents changes in schedule composition from mechanically shifting the scale.

## Model selection and checks

Specifications were compared using deterministic five-fold cross-validation. Entire rounds, rather than individual matches, were assigned cyclically to folds within each centre season. The common comparison sample comprised 6,141 held-out home-and-away matches across the fully centred 1990–2023 windows. Mean log loss was the primary selection criterion; Brier score and margin root mean squared error (RMSE) were retained as supporting diagnostics. This is retrospective blocked cross-validation, not a real-time forecasting exercise, because matches from surrounding seasons remain in the training window.

In the comparison matching the final article setup—full-weight finals in training and home-and-away round blocks held out—the selected seven-season partially pooled model had a mean log loss of 0.5816, Brier score of 0.1969 and margin RMSE of 37.0 points over 6,141 held-out matches from the fully centred 1990–2023 windows. The earlier regular-season-only comparison also showed that the Normal-margin probability predictions were materially better than the corresponding Bradley–Terry win/loss model.

Several sensitivity tests informed the final specification:

- One-, three-, five- and seven-season windows were compared. The seven-season window produced the lowest mean log loss among the common-ground baseline models, although the difference from five seasons was small.
- A partially pooled, ground-specific model had a slightly lower mean log loss than the common-ground article model (difference −0.00038), although its season-clustered 95% interval (−0.00108 to 0.00033) included no improvement. Partial pooling was reinstated because it was the raw predictive winner and provides shrinkage rather than unrestricted ground estimates. A fully unpooled model performed worse.
- Lagged travel was defined as team 2's previous-match travel minus team 1's, in thousands of kilometres; relative rest was team 1's capped days of rest minus team 2's. Tested separately on top of partial ground pooling, lagged travel worsened mean log loss by 0.00027 and rest by 0.00043. Their unrestricted coefficients frequently had the opposite sign to the fatigue hypothesis. Constraining each coefficient to be non-negative mostly set it to zero and still worsened log loss, by 0.00024 for lagged travel and 0.00018 for rest. Neither term is included in the article model.
- Finals weights of 0, 0.25, 0.5 and 1 were tested while always scoring the same held-out home-and-away matches. Full-weight finals improved mean log loss from 0.5840 to 0.5820; the paired difference was −0.00203 (season-clustered 95% interval −0.00292 to −0.00115). Finals were therefore included at full weight in the chart model.

Across the 37 fitted reporting windows, the home-and-away residual standard error ranged from 30.9 to 39.2 points (mean 34.8). These values indicate substantial match-to-match variation even after adjustment, so small differences between teams or seasons should not be over-interpreted.

## Interpretation and limitations

The model-adjusted retrospective strength estimates are not a causal estimate of coaching, player quality or travel effects, and not a pre-match forecast. Centred windows deliberately borrow information from nearby seasons to estimate relatively stable location effects; consequently, most historical estimates use both earlier and later seasons. Team strength itself remains season-specific and is not smoothed across years.

The location controls depend on recorded team bases and ground affiliations and cannot capture every circumstance, particularly the unusual 2020 hub season. Dedicated 2020 interaction terms reduce that risk but do not make the season directly comparable in every respect. The most recent estimates also use shortened windows and may change when further matches or later seasons become available.
