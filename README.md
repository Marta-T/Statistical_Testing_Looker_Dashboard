# DS.v3.2.2.5
Note: there were 2 datasets analysed.
# 1. Mobile Games A/B Testing - Cookie Cats
## Introduction
### Overview
This dataset includes A/B test results of Cookie Cats mobile game to examine what happens when the first gate in the game was moved from level 30 to level 40. When a player installed the game, he or she was randomly assigned to either gate_30 or gate_40.

Dataset includes:
- userid: A unique number that identifies each player.
- version: Whether the player was put in the control group (gate_30 - a gate at level 30) or the group with the moved gate (gate_40 - a gate at level 40).
- sum_gamerounds: the number of game rounds played by the player during the first 14 days after install.
- retention_1: Did the player come back and play 1 day after installing?
- retention_7: Did the player come back and play 7 days after installing?
### Goal of the analysis
The goal of this analysis is to decide if the placement of the progression gate (at level 30 comparing to level 40) significantly impacts player retention and engagement.

Questions to analyse:
1. Does gate placement at level 40 (gate_40) lead to higher 1-day and 7-day retention rates compared to level 30 (gate_30)?
2. Does gate placement affect the total number of game rounds (sum_gamerounds) played in the first 14 days?
### Target metrics
1-day and 7-day retention rate (True or False, measuring days after installation):
- this measures if the users stayed and continued to play the game

Number of game rounds played by a player within the first 14 days after installation:
- this measures how much user was engaged - how many times he/she played the game
### Analysis methods
- Proportions z-test was used for retention data, since it is binary and the sample size is large.
- Welch's t-test was used for game rounds data, since the sample size in each group is large (above 45 000 samples per group). This is used instead of Student's t-test because even though the variances are homogenous, Welch's t-test is more robust, at high sample size gives the same results as Student's t-test and is a standard practice.
### Conclusions
Dataset about a mobile game Cookie Cats was analyzed. This dataset included:
- 90189 users
- 2 game versions (first gate either at level 30 or level 40)
- retention rate after 1 day
- retention rate after 7 days
- game rounds played
There were no significant differences in retention rates or the game rounds played when the gate is put on 30th level comparing to 40th.
### Decision
There is no significant difference in gamerounds played or retention rates when comparing gate 30 and gate 40 game versions.
# 2. Fast Food Marketing Campaign A\B Test
## Introduction
### Overview
This dataset includes A/B test results of a new fast food item sales to examine which marketing campaign was the most successful. The new item was introduced at different locations in several randomly selected markets.

Dataset includes:
- MarketID - a number for a randomly selected market (10 in total)
- MarketSize - size of market area by sales (small, medium, large)
- LocationID - store location unique ID (137 in total)
- AgeOfStore - age of store in years
- Promotion - promotion tested (3 in total)
- week - week when the promotions were run (4 in total)
- SalesInThousands - sales amount for a specific LocationID, Promotion, and week

Overview of the dataset also can be found in this [Looker Studio dashboard](https://lookerstudio.google.com/reporting/9e70f9ee-7e18-4d86-9014-0a0aaa7e78e7).
### Goal of the analysis
The goal of this analysis is to decide which marketing campaign was the most successful and lead to the most sales of the new item.

Questions to analyse:
1. Is there a statistically significant difference in mean sales across three promotions?
2. How can the promotions can be ranked from the most to the least successful?
### Target metric
SalesInThousands: sales in the first 4 weeks of introducing the new item (by a specific promotion in a specific location) in thousands. The more sales there were, the more successful the campaign was in promoting the new product.
### Analysis methods
- Kruskal Wallis t-test was used to compare the average sales accross the promotions, since the distribution was not normal, there were 3 groups to compare and the sample size was small (43-47 per group)
- CIs were computed analytically (using SciPy package) and using bootstrap.
- For post-hoc analysis to determine the rank the campaigns, Bonferroni correction was used (due to multiple testing) and Mann-Whitney U test was used to compare the pairs, because the Kruskal Wallis t-test was used previously.
### Conclusions
Dataset about a new fast food item sales was analysed. This dataset included:
- 10 randomly selected markets
- 137 store locations
- 3 tested campaigns
- 4 weeks of sales
- sales amount
There were statistically significant differences in sales across the campaigns, with campaign 1 and 2 performing the best. 
### Decision
For the best results, either campaign 1 or 2 can be chosen, the choice can also depend on the costs of these campaigns, which were not included in the dataset analyzed.
