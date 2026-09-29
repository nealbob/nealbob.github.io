---
layout: post
title: "More even than ever? Competitive balance in the AFL"
date: 2026-09-28 00:00:00 +1000
excerpt: "What can the data tell us about the evenness and mobility of team strength in the Australian Football League?"
modified: 2026-09-28
tags: [AFL, data analysis, sport]
comments: true
image: /images/afl-competitive-balance/team-strength-spread.png
---

Sport can be cruel. On Saturday, Fremantle were a few minutes away from their first premiership since joining the AFL in 1995. Unfortunately for them (and many neutral supporters), Brisbane kicked ahead to claim their third premiership in a row and their sixth since 2001.

Even before Saturday's game was over, though, the issue of competitive balance had been rearing its head. Seven teams have won 23 of the 26 AFL premierships since 2001 and, more importantly, many of those same teams remain among the competition's best (particularly Brisbane, Hawthorn, Sydney, Geelong and, to a lesser extent, Collingwood).

So are the AFL's equalisation policies working as intended, or is the competition becoming less balanced over time? And, if so, how do we reconcile this with frequent comments from AFL coaches suggesting [the competition is more even than ever](https://www.geelongcats.com.au/news/1636756/round-24-chris-scott-press-conference-takeaways)?

## How should we measure competitive balance?

Measuring competitive balance in the AFL is complicated for a number of reasons. For one, ladder position is an imperfect measure of team strength given the inherent unevenness of the draw, while finals offer a limited sample and can be rather noisy (just ask Fremantle). On top of that, the AFL has undergone frequent structural changes, including a gradual increase in the number of teams from 12 in the VFL era to 18 today.

We can attempt to address some of this noise with a bit of statistical modelling. In short, we combine game data from the home-and-away season and finals to estimate a [model of team strength]({{ '/methods/afl-team-strength-model/' | relative_url }}) that controls for the vagaries of the draw, including the effects of venue, travel and opposition strength. This model can then be used to produce a model-adjusted win rate for each season: notionally, the percentage of games each team would be likely to win that year with a hypothetically even draw.

Once we have this measure of team strength, we can look at competitive balance from two distinct perspectives. First, the distribution or spread of team strength within each season: how big is the gap between the top-, middle- and bottom-ranked teams? Second, team mobility across seasons: how hard is it for bottom-ranked teams to catch up to and eventually displace top-ranked teams?

## More even at the top, less even at the bottom

The chart below shows the spread of team strength for every AFL season between 1990 and 2026.

![AFL team-strength spread based on model-adjusted win rates]({{ '/images/afl-competitive-balance/team-strength-spread.png' | relative_url }})

While the results are noisy, some trends are apparent. First, the AFL became more even (with less distance between the top and bottom teams) during the 1990s, likely in response to equalisation policies such as the salary cap and draft introduced in the late 1980s. However, from the mid-to-late 2000s, the spread in team strength seems to have opened up again.

This second chart provides a clearer picture by comparing the top- and bottom-performing teams with the effective middle (median) team on a rolling five-year basis. Here we see that, over recent decades, the gap between the middle and bottom teams has widened, while the gap between the top and the middle has closed.

![Model-adjusted win-rate gaps between the best, worst and median AFL teams]({{ '/images/afl-competitive-balance/top-bottom-strength-gaps.png' | relative_url }})

This offers some explanation for why coaches might view the competition as "more even than ever" despite a wider total spread. From 2000 to 2010, it was more common to see one or two teams well ahead of the pack. Now, competition among the top eight teams appears very tight, with many close and unpredictable games (even for teams as successful as Brisbane). At the same time, a larger gap appears to have opened at the bottom, with some teams well behind the pack.

### What about mobility?

This next chart shows the correlation in team strength across seasons: to what extent is a team's strength this year related to its strength last year, the year before that and so on? Dividing the period since 1990 into two eras, we can see a clear increase in the persistence, or stickiness, of team strength (i.e., a reduction in mobility) in the latter period from 2008 to 2026.

![Correlation in team strength over one to three previous seasons by era]({{ '/images/afl-competitive-balance/team-strength-persistence.png' | relative_url }})

We can get a more tangible picture of mobility by looking at "transition probabilities": specifically, the likelihood of a team moving between the top, middle and bottom thirds of the competition over a one-, two- or three-year period.

![Team-strength movement between top, middle and bottom terciles over one to three seasons]({{ '/images/afl-competitive-balance/team-strength-tercile-transitions.png' | relative_url }})

These numbers suggest that, between 1990 and 2007, there was a 61% chance that a team in the bottom group would remain there one year later. In the later era, from 2008 to 2026, the chance of a bottom team remaining in the bottom group the following season increased to 65%. The results are more striking over three years, with the chance of a bottom team remaining in the bottom group increasing from 35% to 44%.

Looking at the data more closely, we can see a trend towards reduced mobility emerging from around 2000 at both the top and bottom of the competition: good teams staying up for longer and bottom teams staying down for longer.

![The AFL's top and bottom strength tiers have become stickier]({{ '/images/afl-competitive-balance/team-strength-retention.png' | relative_url }})

## How does the AFL compare with the VFL of the 1970s and 1980s?

During the 1970s and 1980s, the VFL was dominated by a small number of clubs, with five clubs claiming all 20 premierships and two (Hawthorn and Carlton) claiming 13 of them. The chart below compares the concentration of premierships and Grand Final appearances in the VFL from 1970 to 1989 with what would be expected in a perfectly even competition. This comparison controls for the size of the competition and the entry of new teams over time (see the [methods paper]({{ '/methods/afl-team-strength-model/' | relative_url }}) for details).

![Premiership and Grand Final concentration relative to random allocation]({{ '/images/afl-competitive-balance/premiership-grand-final-concentration.png' | relative_url }})

The beginning of the AFL era saw a big drop in the concentration of premierships and Grand Final appearances, with the competition becoming about as close to even as possible. The latter half of the AFL era, from 2008 onwards, has been decidedly less even, though still a long way from the former VFL days.

While not a perfect benchmark, a simple analysis of end-of-year ladder positions (below) shows a similar pattern: a big improvement in team mobility at the start of the AFL era, followed by a step backwards from 2008 onwards.

![Ladder-position movement between top, middle and bottom terciles over one to three seasons]({{ '/images/afl-competitive-balance/ladder-tercile-transitions.png' | relative_url }})

One distinctive feature of the recent AFL period has been the frequency of repeat premierships. While premierships have generally been less concentrated in the AFL era, repeat premierships have become more common, particularly in the 2008–2026 period.

![One-year repeat premiership and Grand Final appearance rates relative to random allocation]({{ '/images/afl-competitive-balance/repeat-premierships-grand-finals.png' | relative_url }})

## Is it free agency?

Many will rush to blame the introduction of free agency in 2012, which gave players more freedom to pursue offers from rival AFL clubs. There are, of course, examples of high-profile players leaving lower-ranked clubs to join higher-ranked clubs, including Oscar Allen, a former West Coast captain and now a premiership player for Brisbane. Perhaps more concerning is the apparent willingness of some players to trade off income for team success, such that top teams might acquire players at a discount.

But a full assessment of free agency would need to take a long-term perspective and consider the compensation picks and players received in these exchanges. There are always counterexamples, such as Fremantle losing Chris Mayne in 2016 and eventually ending up with Caleb Serong. And, while it predates the free-agency era, I have to mention Leigh Colbert, the Geelong captain, leaving for reigning premier North Melbourne in 1999. It felt like a gut punch at the time, but by 2007 Cameron Mooney (received as part of that deal, along with the pick used for Corey Enright) was standing on the MCG fence holding Geelong's first cup in 44 years.

## ... or something else?

It also seems unlikely that free agency is the only factor at play. It's possible, for example, that increasing investment in off-field systems—sports science, training, nutrition, coaching, etc.—has contributed to differences between teams. There is no doubt that AFL football has become an expensive pursuit, and that clubs are much more complex than a group of players and a coach. While the "soft cap" (introduced in 2015) is designed to prevent an arms race in these areas, it seems plausible that differences could emerge given how long these investments take to implement and filter through to a playing group.

Over time we might expect off-field systems to converge on a frontier, constrained by a combination of the soft cap and natural athletic limits. While this could lead to greater evenness (particularly at the top), it might also reduce mobility to some extent by reducing randomness. If all teams are maximising their performance on all dimensions all the time, maybe a 1% better team will just win each time. The data seems to support this idea, with statistical models showing [reduced noise in game results in more recent seasons]({{ '/methods/afl-team-strength-model/' | relative_url }}).

Another underappreciated factor is longevity. People in general are living longer, and AFL playing careers are extending with improvements in nutrition, sports science and related areas. Patrick Dangerfield, at 36, was one of Geelong's best players in this finals series, while Dayne Zorko, at 37, was one of Brisbane's best. Scott Pendlebury broke the games record this year at 38. All will play on next year. The way things are heading, players like Harry Sheezel and Nick Daicos might play into their 40s. It seems plausible that longer playing careers could widen the "premiership window" of top teams, making it harder for young, up-and-coming teams to displace them and increasing the likelihood of repeat premierships.

## Does it matter?

It's hard for this topic not to become partisan. Supporters of struggling clubs are likely to be concerned by these trends and in favour of rule changes to increase mobility. The incumbent teams, not so much.

But it's important to keep some perspective. The AFL era and its equalisation policies have been effective overall: the competition has become more even since 1990. Most of the non-Victorian entrants have won premierships since joining; Fremantle came agonisingly close this year; GWS have been competitive in their short history; and, while Gold Coast were disappointing this year, expectations for their current playing list remain high. Several Victorian teams that couldn't get a look-in during the 1970s and 1980s (Melbourne, the Bulldogs and Geelong) have broken long premiership droughts. Although Brisbane have had two very dominant teams since 1990, they have spent extended periods near the bottom in between. Richmond and West Coast are currently languishing, but their glory days were not that long ago.

It's also not clear exactly what an ideal competition would look like. A perfectly even distribution in which each team wins a premiership once every 18 years would be rather dull. Adversity is part of the attraction of sport. When teams like Fremantle and St Kilda break their droughts, it will be all the sweeter because of it.

That said, it seems like there are some trends here that deserve attention. Setting up the rules for a balanced professional sporting competition is not easy. Clubs will do everything in their power to seek out a competitive edge and exploit loopholes wherever possible. Competitive pressures and broader technological changes mean that the rules need to adapt constantly to keep up.
