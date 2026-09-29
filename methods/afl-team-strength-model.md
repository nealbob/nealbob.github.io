---
layout: page
title: "Estimating AFL team strength and competitive balance"
permalink: /methods/afl-team-strength-model/
modified: 2026-09-29
---

This note provides methodological detail for two articles: [*The greatest team of all? AFL team performance since 1990*]({% post_url 2026-9-21-greatest-team %}) and [*More even than ever? Competitive balance in the AFL*]({% post_url 2026-9-28-afl-balance %}).

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

This note outlines a statistical model of AFL game margins which measures team strength while controlling for opponent strength, venue familiarity, travel and home/away advantages. The model estimates how many points stronger or weaker each team was relative to the league average in a given season. It also converts those estimates to a model-adjusted win rate against a common set of opponents, making comparisons less sensitive to differences in fixturing.

The competitive-balance analysis uses these adjusted win rates in three ways: to measure the spread between teams within a season, to estimate movement between strength groups across seasons, and to calculate the persistence of team strength over time. Premierships and Grand Final appearances are analysed separately as observed binary outcomes.

The model is retrospective. It is designed to describe completed seasons, not to reproduce the information that would have been available before each match, and it is not intended as a forecasting model.

## Data

Match results come from [AFL Tables](https://afltables.com/afl/afl_index.html). The analysis uses one record per completed VFL/AFL match, including the final score, date, season, round and ground. Venue coordinates, season-specific team bases and team–ground affiliations are maintained in the project's configuration files and are used to construct the location variables.

The modelling data begin in 1985. Results are reported from 1990, with 1985–1989 used to support the earliest rolling estimates. The current input contains 7,846 matches from 1985–2026: 7,488 home-and-away matches and 358 finals. The chart snapshot uses match data updated on 28 September 2026 and includes the complete 2026 season through the Grand Final on 26 September 2026. Team names are normalized only for defined historical name changes: Footscray is grouped with the Western Bulldogs and the Kangaroos with North Melbourne; otherwise historically distinct clubs remain distinct.

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

## Converting margins to a model-adjusted win percentage

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

Across the 37 fitted reporting windows, the home-and-away residual standard error ranged from 30.9 to 39.2 points (mean 34.8). The residual standard error declined over time, averaging 37.0 points in 1990–2007 and 32.8 points in 2008–2026. This is consistent with less unexplained match-to-match variation in recent seasons, although the comparison is descriptive: the windows overlap, the most recent estimates use shortened endpoint windows, and dispersion measured in raw points may also reflect changes in scoring levels. Match-to-match variation remains substantial even after adjustment, so small differences between teams or seasons should not be over-interpreted.

## Competitive balance measures

The competitive-balance analysis starts from the model-adjusted win rate described above, rather than each club's raw win percentage. This matters because clubs do not play identical schedules and because venue and travel advantages are unevenly distributed. Unless otherwise stated, comparisons begin in 1990 and include only clubs observed in the seasons being compared. The main era comparison divides the series into 1990–2007 and 2008–2026; a cross-season observation is assigned to the era of its later season.

### The spread of team strength within a season

Within-season competitive balance is described using the distribution of model-adjusted win rates across the active teams. The charts report selected percentiles, the gaps between the strongest and weakest parts of the distribution, and the cross-team standard deviation. Because the win rates are standardized against the same equal-weight opponent pool, their league mean is 50% in every season. A smaller percentile gap or standard deviation therefore indicates a more even season; a larger value indicates a wider separation between strong and weak teams.

### Transitions between strength groups

For the transition analysis, teams are ranked by model-adjusted win rate within each season, with rank 1 denoting the strongest team. The rankings are divided into either thirds or quarters using mid-rank cut points. For \(K\) groups, the group number for a team with rank \(r\) in a league of \(N\) teams is

\[
q(r;K,N)=1+\left\lfloor\frac{(r-0.5)K}{N}\right\rfloor,
\]

capped at \(K\). This convention keeps the strongest and weakest groups as symmetric as possible when the number of teams is not divisible by \(K\). With 18 teams, for example, the terciles contain six teams each and the quartiles contain 5, 4, 4 and 5 teams.

For each lag \(k\), a club's group in season \(t\) is paired with its group in season \(t+k\). The analysis uses lags of one, two and three seasons and includes only clubs active at both endpoints. The estimated transition probability from starting group \(a\) to ending group \(b\) is the corresponding cell count divided by all transitions that began in group \(a\):

\[
\widehat P_{ab}^{(k)}=
\frac{\#\{i:q_{i,t}=a,\ q_{i,t+k}=b\}}
     {\#\{i:q_{i,t}=a\}}.
\]

Each row of a transition matrix therefore sums to 100%. Retention rates are diagonal probabilities: for example, top-tercile retention is the proportion of clubs starting in the top third that are still in the top third after \(k\) seasons.

For charts over time, annual successes and trials are pooled within a centred seven-transition window. The smoothed probability is the sum of successes divided by the sum of trials, rather than an unweighted average of annual percentages. At the ends of the series, four to six transition years are used. Era comparisons assign a transition to the later season in the pair.

### Auto-correlation of team strength across seasons

For each later season and lag, clubs appearing in both seasons are paired and the Spearman rank correlation between their model-adjusted win rates is calculated. A high positive correlation means the ordering of clubs changed relatively little; a value near zero means the earlier ordering provides little information about the later one.

Exact team names are used to form the strength-transition and correlation pairs after the stated historical name normalizations. No value is imputed for a club that is absent from either endpoint, and the Brisbane Bears and Brisbane Lions are not joined in these particular calculations.

## Premiership and Grand Final measures

Premiership and Grand Final statistics are constructed directly from Grand Final results, not from the margin model. For each active club and season, `grand_finalist` equals one for the two participating clubs and `premiership` equals one for the winner. A drawn Grand Final and its replay count as one season-level Grand Final event: the two clubs each receive one appearance and the replay winner receives the premiership.

The outcome charts compare three similarly sized eras: 1970–1989, 1990–2007 and 2008–2026. Grand Final results from 1968 and 1969 are retained only to provide a complete two-season lookback for outcomes at the start of the first era.

For these long-run outcome comparisons, name changes representing a continuing club are combined: Footscray with the Western Bulldogs, the Kangaroos with North Melbourne, South Melbourne with Sydney, and the Brisbane Bears with the Brisbane Lions. This broader continuity rule is stated separately because it differs from the exact-name pairing used for the team-strength transitions.

### Repeat percentage

Among the premierships or Grand Final appearances in an era, this is the proportion achieved by a club that recorded the same outcome at least once in the preceding \(k\) seasons. This is a lookback measure: for a two-season window, success in either of the previous two seasons counts as a repeat.

Raw repeat percentages are affected by the number of clubs in the league. We therefore compare them with a random-allocation benchmark that preserves the clubs active in every season, assigns one premiership and two distinct Grand Final places per season, and treats seasons as independent. For a club active in the relevant prior seasons, the chance of at least one occurrence within a \(k\)-season lookback is based on

\[
1-\prod_{h=1}^{k}\left(1-\frac{s}{N_{t-h}}\right),
\]

where \(s=1\) for a premiership, \(s=2\) for a Grand Final appearance, and \(N_{t-h}\) is the number of active clubs in the prior season. Terms for seasons before a club entered the competition are omitted. These club- and season-specific probabilities are aggregated over the outcomes in each era. The reported relative-repeat statistic is the observed repeat percentage divided by this expectation, so 1 means no more repetition than random allocation after allowing for league size and club entry or exit.

### Outcome concentration

Outcome concentration is measured with the Herfindahl index, \(HHI=\sum_c s_c^2\), where \(s_c\) is club \(c\)'s share of the premierships or Grand Final places in an era. The article reports the observed HHI relative to its analytical expectation under the same season-specific random-allocation benchmark. Values above 1 indicate that outcomes are more concentrated among a small number of clubs than chance alone would imply. The reciprocal, \(1/HHI\), can also be read as the effective number of clubs sharing those outcomes.

## Interpretation and limitations

The model-adjusted retrospective strength estimates are not a causal estimate of coaching, player quality or travel effects, and not a pre-match forecast. Centred windows deliberately borrow information from nearby seasons to estimate relatively stable location effects; consequently, most historical estimates use both earlier and later seasons. Team strength itself remains season-specific and is not smoothed across years.

The transition groups and persistence statistics treat the estimated win rates as observed inputs. They do not propagate the uncertainty in each team's strength coefficient. Sampling noise can move teams near a tercile or quartile boundary from one group to another, and measurement error will generally weaken observed correlations. Successive transition pairs and centred moving averages also overlap, so they should not be read as independent observations.

Premiership and Grand Final persistence is descriptive rather than causal. The random benchmark answers a deliberately narrow question—how much repetition would be expected if the available outcome places were allocated independently among the clubs active in each season. It does not model differences in club quality, list cycles, finals systems or other mechanisms that may generate persistence.

The location controls depend on recorded team bases and ground affiliations and cannot capture every circumstance, particularly the unusual 2020 hub season. Dedicated 2020 interaction terms reduce that risk but do not make the season directly comparable in every respect. The most recent estimates also use shortened windows and may change when further matches or later seasons become available.
