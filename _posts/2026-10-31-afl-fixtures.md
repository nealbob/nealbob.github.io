---
layout: post
title: "Who gets the best fixture in the AFL? (No, it's not Collingwood)"
date: 2026-10-31 00:00:00 +1000
excerpt: "Let's take a closer look at fixture winners and losers since 1990."
modified: 2026-10-31
tags: [AFL, data analysis, sport]
comments: true
image: /images/afl-fixtures/fixture-advantage-1990-2026.png
---

The 2027 AFL fixture came out this week, and within a few hours media outlets were telling us who had the best and worst draws, with Fox Sports' [assessment](https://www.foxsports.com.au/afl/afl-fixture-2027-winners-and-losers-from-afl-draw-fixture-difficulty-analysis-as-every-teams-doubleups-revealed-hardest-and-easiest-2027-draws/news-story/71836847d925e02a410d663528a3c371) (based on the 2026 percentages of double-up opponents) creating some rage bait by suggesting Collingwood had one of the best draws.

But that analysis was rather basic. A more careful assessment has to look beyond double-ups and consider the full fixture, including travel and venue. This should be obvious, and it was to many people on [Reddit](https://www.reddit.com/r/AFL/comments/1xi90w8/2027_fixture_difficulty/). (For what it's worth, this [assessment](https://x.com/sportpunter/status/2115633344365109656) from [SportPunter](https://www.sportpunter.com/) came out a few hours later and was more accurate).

## Fixture advantage 1990 to 2026

Before getting into 2027, let's look at the AFL from 1990 to 2026 and see which teams have had the best fixtures on average. This analysis is based on a statistical model of AFL team strength that accounts for opponent, venue, travel and hosting status ([details are here]({{ '/methods/afl-team-strength-model/' | relative_url }})). The figure shows the effect of the fixture on an average team's expected win percentage:

![Long-run AFL fixture advantage, 1990 to 2026]({{ '/images/afl-fixtures/fixture-advantage-1990-2026.png' | relative_url }})

Here Gold Coast have the most favourable draw on average and the Bulldogs the hardest (the results are based on each club's active seasons, so Gold Coast's and GWS's results cover a shorter period than the others).

Since 2014 the AFL has explicitly taken previous-season performance into account for fixturing, giving weaker teams easier draws. Since Gold Coast have spent most of this time in the bottom third of the ladder, it's not too surprising they've had an easier fixture. Geelong, despite being the most consistent team of the period, are reasonably high on this list, due to their unique position as the only Victorian team with a dedicated home venue ([more on that here]({% post_url 2026-9-21-greatest-team %})).

This assessment also accounts for things beyond AFL control, including teams selling home games interstate, which has led to some self-inflicted fixture disadvantage for clubs like the Bulldogs, Melbourne and St Kilda. There are some judgements in the model here about whether grounds are considered "familiar": for example, it treats Ballarat as a second home ground for the Bulldogs, but not their occasional venues in Darwin and Cairns. Although to be fair, [the Bulldogs have done better than Melbourne and St Kilda](https://www.afl.com.au/news/1532714/melbourne-demons-woes-north-melbourne-kangaroos-big-tests-how-have-clubs-who-sold-home-games-interstate-fared) in their interstate "home" games in recent years.

## Collingwood has a harder draw than people think

OK, so now the most surprising result: contrary to public opinion, Collingwood do not get the easiest draw. According to this model, they have had the second-hardest fixture on average. Yes, Collingwood play a lot of games at the MCG and travel less than some other teams. But many of their games at the MCG are against other MCG-based teams (where the model assumes no ground-familiarity advantage, unlike, say, Geelong at Kardinia Park; it also doesn't account for crowd size / bias).

Collingwood also play some nominal home games at Docklands, which the model treats as a neutral venue for them. Overall, Collingwood have done OK there, partly because they have tended to play weaker teams. In 2027, though, Collingwood will play both St Kilda and the Bulldogs at Docklands, more or less converting those two home games to away games.

Lastly, there is the "opponent mix" (i.e., double-up) component. In the long run, Collingwood have had the hardest opponent mix in the AFL. My guess is that, in addition to being a consistently strong team over the period, financial incentives to put Collingwood in blockbuster games against quality opponents may play a part. Presumably, it is in no one's interests for Collingwood to play lots of games against Gold Coast or North Melbourne. That's speculation of course; some of this might be bad luck (fixtures are based on previous years' rankings, so it doesn't always work out as intended).

So while there might be a few things to quibble about in this model (the effect of the Collingwood "army", or whether Docklands should be considered "home" for Collingwood), it still looks like Collingwood's draw is not as easy as people think.

## What about the travel burden for non-Victorian clubs?

The results above include relative travel distance for each game, but these effects largely cancel out over a season for non-Victorian teams: a disadvantage away, an advantage at home. Many would argue that teams like West Coast and Fremantle also face a burden from accumulating more travel over a season. Below are results from a model that adds cumulative season travel. It pushes Fremantle and West Coast down in the rankings, and some Victorian teams, including Collingwood, up.

![Long-run AFL fixture advantage with cumulative season travel]({{ '/images/afl-fixtures/fixture-advantage-cumulative-travel.png' | relative_url }})

The evidence for cumulative travel in the historical data is pretty limited (which is why it is excluded from the main model). That may be for purely statistical reasons though, so for now, we can leave that as an open question.

## Now on to 2027

Below is what the model says about fixture advantage or disadvantage for 2027, using 2026 team strengths. As most reporting has suggested, Brisbane have by far the hardest draw (as they should!), while Essendon, Richmond, West Coast and North Melbourne have some of the easiest (as you would expect).

![AFL 2027 fixture advantage]({{ '/images/afl-fixtures/fixture-advantage-2027-simple.png' | relative_url }})

That said, these results differ quite a bit from many in the media, particularly Fox Footy. Melbourne have a much harder draw here, partly because they play a home game in Alice Springs. Meanwhile, Collingwood's fixture is close to neutral. Although the Pies play Essendon and Richmond twice, for their two home games at Docklands they've drawn St Kilda and the Bulldogs: the worst possible result for these games.

Fremantle also do better in this list. While they have a tough set of double-up opponents (as you would expect for a grand finalist), they get 13 games in Perth, including away games against West Coast and North Melbourne (this 2027 calculation does not include cumulative season travel burden though).

Of course, this analysis assumes teams perform in 2027 like they did in 2026, which they won't. But for now, at least, fixture difficulty looks broadly as you would expect based on 2026 performance, with a few oddities due to where teams choose to play their home games.
