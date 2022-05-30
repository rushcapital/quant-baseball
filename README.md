# quant-baseball

i found a passion for building things related to quantitative sports betting such as fair odds calculators, winner/loser probabilities, daily matchups, etc. and wanted a nice frontend to visualize some of these metrics, so i built this dashboard template. i really like real-time ticker widgets so i included one here, i do not like how (because its someone elses widget) that i am unable to change the background transparency and text of the widget so the dark mode background looks more streamlined (right now, im happy with light mode; dark mode needs to fix the widget color). work in progress though.

![rush capital](https://user-images.githubusercontent.com/100492617/171062830-c44d0586-aa1e-427f-88c5-674261518ab6.gif)

# alpha 1: inning run unders
for sports betting, theres this major annoyance of mine when it comes to real-time baseball updates; nowhere on the internet can i find the game state that keeps track of the current batting order STATE as you go from inning to inning (i.e. the 1st inning ends, what are BOTH of the "due up" lineups). you can interpret this from looking at the live box scores between innings and finding the index of the first minimum PA (plate appearance), which i have done. anyways, why is this important? because i believe there is a trend if you sum the order number of both "due up" lineups (i.e. 5,6,7 away hitters + 7,8,9 home hitters) > 45, you have a high probability of hitting the inning under assuming the starting pitchers whip < a certain threshold. i'll make this public as soon as i can find a nice looking html table format i like because the reason theres a box in the middele of my dashboard is because i have not found a tutorial/guide to display tables in a visually appelaing way (they look so bad).

