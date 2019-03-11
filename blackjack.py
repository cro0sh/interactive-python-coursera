# Blackjack
# Cam Simmons for Interactive Programming With Python Pt 2
# Run at http://www.codeskulptor.org/#user43_y9hKDBTQoC_1.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

card_back_new = simplegui.load_image("https://i.imgur.com/HhDUv0J.png")    

# initialize some useful global variables
in_play = False
outcome = ""
player_score = 0
dealer_score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):        
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = [] # create Hand object        

    def __str__(self):
        self.string = ''
        for card in self.cards:
            self.string += card.__str__()
        return 'Hand contains ' + self.string	# return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        global hand_value
        hand_value = 0                
        for card in self.cards:
            for item in str(card):
                hand_value += VALUES.get(item, 0)

                if item == 'A':
                    if hand_value + 10 <= 21:
                        hand_value = hand_value + 10
                        if len(self.cards) > 2:
                            hand_value = hand_value - 10
                                      
                    else:
                        hand_value = hand_value
              
                else:
                    hand_value = hand_value
        return hand_value
   
    def draw(self, canvas, pos): 
        
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] = pos[0] + 50 
        
# define deck class

class Deck:
    def __init__(self):
        self.cards = []	# create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit,rank))
        
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)    # use random.shuffle()

    def deal_card(self):
        return self.cards[random.randint(0,51)]	# deal a card object from the deck
    
    def __str__(self):
        s = ''
        for card in self.cards:
            s = s + 'Deck contains ' + card.__str__()
        return s


#define event handlers for buttons
def deal():
    global outcome, in_play, ph, dh, hand_value, dealer_score
     
    if in_play: 
        outcome = 'Dealer wins!'
        dealer_score += 1
        in_play = False
    else:
        d = Deck()
        d.shuffle()

        ph = Hand()
        dh = Hand() 

        ph.add_card(d.deal_card())
        ph.add_card(d.deal_card())

        dh.add_card(d.deal_card())
        dh.add_card(d.deal_card())

        print 'Player ',  ph
        print 'Dealer ', dh  

        print 'ph.get_value()', ph.get_value()

        outcome = 'Hit or stand?'
        in_play = True    


def hit():
    global in_play, outcome, dealer_score, player_score
    d = Deck()    
    
    if in_play:
        if ph.get_value() <= 21: # if the hand is in play, hit the player
            ph.add_card(d.deal_card())
            print 'hitting', ph.__str__()
            print 'ph.get_value() once hit', ph.get_value()
            
            if ph.get_value() > 21:
                outcome = 'Player busted, dealer wins!'
                dealer_score += 1
                in_play = False
                   
        else:
            outcome = 'Dealer wins!'
            in_play = False
            dealer_score += 1  
            
    
   
       
def stand():
    global outcome, in_play, player_score, dealer_score
    d = Deck()     
    
    while in_play:    
        
        if dh.get_value() <= 17 or 17 < dh.get_value() <= 21 and dh.get_value() < ph.get_value():
            dh.add_card(d.deal_card())
            
            print 'dh', dh.__str__()
            print 'dh.get_value()', dh.get_value()
           
            if dh.get_value() > 21:
                outcome = 'Dealer busted, player wins!'                               
                in_play = False
                player_score += 1                
                
                
            if ph.get_value() <= dh.get_value() and 17 < dh.get_value() <= 21:
                outcome =  'Dealer wins!'                               
                in_play = False
                dealer_score += 1
                
                
            if ph.get_value() > dh.get_value() and dh.get_value() >= 17:
                outcome = 'Player wins!'                              
                in_play = False
                player_score += 1
                
        elif ph.get_value() <= dh.get_value() and 17 < dh.get_value() <= 21:
            
            outcome = 'Dealer wins!'                      
            in_play = False
            dealer_score += 1   
            
def reset_scores():
    global player_score, dealer_score
    player_score = 0
    dealer_score = 0
    outcome = 'Hit or stand?'
    
# draw handler    
def draw(canvas):   
     
    canvas.draw_text("Blackjack", (20, 40), 30, 'White')
    canvas.draw_text(outcome, (250, 100), 30, 'White')
    
    canvas.draw_text(str(player_score), (500, 200), 30, 'White')
    canvas.draw_text(str(dealer_score), (500, 450), 30, 'White')
    
    ph.draw(canvas, [150,150])    
    dh.draw(canvas, [150, 400])    
       
    if in_play:
        canvas.draw_image(card_back_new, (68/2, 100/2), (68,100), [165,448], CARD_SIZE)
    else:
        canvas.draw_text('New deal?', (335, 50), 30, 'White')    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Reset Scores", reset_scores, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
