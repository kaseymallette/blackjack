# Blackjack Project

## Introduction

Create a blackjack program that:
`(i) allows a single user to continuously play blackjack hands from a six-deck shoe`
`(ii) uses basic strategy to run through blackjack hands for x number of six-deck shoes`
`(iii) tracks and exports hand and shoe data for all hands played`

## Objectives

* Analyze data collected from all hands dealt
* Anlayze data collected from all shoes dealt

*hand_data.csv*
column | description
------ | -----------
dealer_up | Dealer's up card (A, 2, 3, ..., 10)
player | Player's hand (5-21, soft hands, or pairs)
move | Player's first move (0 = stand, 1 = hit, 2 = double)
outcome | The outcome of the hand (win, loss, or push)
dealer_bj | Whether or not the dealer had blackjack
is_split | Whether or not the hand was split
orig_hand | If the hand was split, the original hand that was dealt. If not, 0
shuffle | The shuffle method used (1, 3, 5, 9, 15, part_1, part_2, casino)

*shoe_data.csv*
column | description
------ | -----------
player_win | The number of hands the player won
player_loss | The number of hands the player lost
push | The number of hands the player pushed (tied)
win_push | The number of hands both won and pushed
total_hands | The total number of hands dealt in the shoe
win_pct | The percentage of hands won
win_push_pct | The percentage of hands won and pushed
doubles_won | The number of hands the player doubled and won
doubles_lost | The number of hands the player doubled and lost
doubles_won_pct | The percentage of hands doubled that the player won
player_bj | The number of hands the player was dealt blackjack
dealer_bj | The number of hands the dealer was dealt blackjack
dealer_ten | The number of hands the dealer had a 10 showing
dealer_bust | The number of hands the dealer busted (hand > 21)
dealer_draw | The number of hands the dealer hit and stood on 17-21
dealer_21_draw | The number of hands the dealer hit and drew to 21
dealer_ten_pct | The percentage of total hands the dealer had a 10 showing
dealer_bust_pct | The percentage of total hands the dealer busted
dealer_draw_pct | The percentage of total hands the dealer drew to make a hand
dealer_21_draw_pct | The percentage of total hands the dealer drew to 21
dealer_avg_hand | The average hand of the dealer when hand < 21
num_of_shuffles | The number of shuffles of the same shoe
shuffle_method | The shuffle method used to shuffle the shoe 

## UML Project Diagram 

![](images/project_diagram.png)
