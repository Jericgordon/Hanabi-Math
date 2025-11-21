# Hanabi Math - A module by Jen Gordon
## Introduction
This repository was built to explore several questions we had around the card game of Hanabi. If you're unsure of what Hanabi is, I recommend you watch [this video](https://www.youtube.com/watch?v=o7DkGdchbDk) both for the gameplay, but also to gain an intuition for how the game is play

## Materials
In brief, There are two seperate modules in this reop.
## Buffer problem
 The first is labled "Buffer problem" and was my first attempt at simulating Hanabi. It's not a full version of the game, but because of that it's much faster. 

The buffer problem is a situation you run into in a game where you can't discard or play any card without decreasing your maximum score. It was my first attempt at establishing a maximum score. I've kept it here as an artifact of past research, but it's not flexible or useable

## Hanabi_simulations

This is a much more flexible Repository. It is a fully customizeable version of the game Hanabi, with easy access for anyone to create a "strategy" and test it over the course of many games. It isolates the work of beating Hanabi, without having to really care about building a working version of the games

## Using this repository to test strategy ideas (short version)
1. Instantiate Hanabi_Game with a number of colors in the deck (5,6)
2. Create a Strategy (see section on creating a strategy)
3. run "play game" with the class (uninstantieated as an object")
4. Play game will return the score achieved by that run


## Using this repository to test strategy ideas (Long version)
1. Instantiate this class with a number of colors in the deck (5,6)
	There's no reason that this wouldn't work with an arbitrary number of colors. You could test out 7 or 8, and to my knowlege, nothing would break technically. But, for instance, if you ran it with 1 color, you'd only have 2 turns in a game since end of game would be instantly triggered.

2. Create a Strategy. (see section on creating a strategy)




## Creating a strategy
### Encoding
One of the main challanges in Hanabi is Efficient encoding of cards into numbers. The way I accomplished this
was to do the numbers 0-25, and have each number encode both a color, and a number.

{1,2,3,4,5} are one suit
{6,7,8,9,6} are another, and so on.

The advantage of this is that \
\
**num % 5** is the number of the suite \
and **(num -1) // 5** is the color of the suite \
\
(or at least a number 1-6 representing color) These are all arranged in various places throughout this code. The purpose of the Card class
was to simplifiy some of this for the end user, but if there are tweaks here and there, it's important
to understand the underlying encoding, as it's neccessary to understand some of the infomration passed by the game

### Strategy classes template
```
class Strategy():
	def __intit__():
	"""
	A strategy class can have take no parameters on init
	"""

	def play_next_turn(self,my_hand,other_hand,discard,play_base,misfires,clue_tokens):
	"""
	Paramaters:
		my_hand : An array of Cards (see cards section). Strategies are allowed to access
			All card infomration if they'd like to cheat. We ran several emulations where this was the case.
			If you'd like to not cheat, restrict yourself to using the methods get_color and get_number for my_hand
		
		other_hand : An array of cards (see card section). The get_pretty_entire_card is provided for printing. Get value also allows you to get the entire value of the card.

		discard : A dictionary of card values (e.g. 1-25) where the key is the card value and the value is the number of that card in the discard.

		play_base : An array, in color order, where the number represents the "currently played" card. At the start of the game this array looks like [0,5,10...]. You will note that 5 also represents the first color 5,
and is the play base for the second color. This can cause bugs if you're only looking if there's a sequential match on the board.

		misfires : int, the number of misfires so far

		clue_tokens : the number of clue tokens available.

	Returns:
		One of 3 options
			-> ("play",index)
			-> ("discard",index)
			-> ("clue",clue_type ("number" or "color"), the number or color your're clueing) 
			EG. (play,0),(discard,4),("clue","number",5),("clue","color",0s
```


### Card
A card has 3 important methods which will be listed here

	def get_color(self) -> int: #returns 0-4 for a 5 color game or -1 if color not yet identified
        """Returns the color of the card if known, or -1 if not identified"""

	def get_number(self) -> int: #returns 1-5 or -1 if color not yet identified
        """Returns the number of the card if known, or -1 if not identified"""

	def get_value(self) ->int: #returns 1-26 for a 5 color game.
       """Using this method qualifies as cheating. if the card is not fully know. It returns
        The encoded value of the card. See the section on encoding"""


	 def get_pretty_entire_card(self) -> str:
        """Allows getting the entire card, ignoring whether it's been clued or not
            Returns:
                A colord version of the card for printing. Used if the card is in the other player's hand
        """



## Other
### Flamboyants
This module does not at this time provide support for flamboyants or Black Poweder.

### Results
I'll provide a copy of My personal results using this in the description.


