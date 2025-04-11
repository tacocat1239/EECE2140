"""
Blackjack and Blackjack Free for All
Author: Matthew Awad
Date: 1/6/2025 - 4/11/2025

"""
import pygame
import random
import sys

#calculate_hand_value and create_deck_console are used in both the undergrad and both difficulty modes. Literally calculates hand

def calculate_hand_value(hand):
    # Compute blackjack total for hand; adjust for aces.
    value = 0
    aces = 0
    for card in hand:
        rank = card[0]
        if rank.isdigit():
            value += int(rank)
        elif rank in ["Jack", "Queen", "King"]:
            value += 10
        else:  # Ace
            value += 11
            aces += 1
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def create_deck_console():
    # Create a standard 52-card deck as (rank, suit) tuples. 
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    deck = []
    # Create the deck with all combinations of ranks and suits.
    for suit in suits:
        for rank in ranks:
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck

# Creates the NPCS
class ComputerPlayer:
    def __init__(self, name, difficulty="undergrad"):
        self.name = name                # NPC name
        self.hand = []                  # NPC's hand
        self.money = 1000               # Starting money
        self.difficulty = difficulty    # 'undergrad', 'masters', or 'phd'
        self.bet = 0                    # NPC bet for the round
        self.busted = False             # Bust flag

    def place_bet(self, min_bet, max_bet):
        if self.difficulty == "undergrad":
            self.bet = min_bet
        elif self.difficulty == "masters":
            self.bet = min(max_bet // 2, self.money // 3, min_bet * 2) or min_bet
        else:  # phd
            self.bet = min(max_bet, self.money // 2, min_bet * 3) or min_bet
        self.money -= self.bet
        return self.bet

    def make_action(self, dealer_up_value):
        
        hand_value = calculate_hand_value(self.hand)
        if hand_value >= 18 and self.money >= 50 and random.random() < 0.5:
            return "raise"
        if self.difficulty == "undergrad":
            return "hit" if hand_value < 17 else "stand"
        elif self.difficulty in ["masters", "phd"]:
            if hand_value <= 11:
                return "hit"
            elif hand_value == 12 and 4 <= dealer_up_value <= 6: #NPCs technically cheating but if I didn't put it here they would always bust and it was annoying
                return "stand"
            elif 13 <= hand_value <= 16 and 2 <= dealer_up_value <= 6:
                return "stand"
            else:
                return "hit"

#CardManager loads the cards and draws them on the screen literally just for the menu
class CardManager:
    def __init__(self, game):
        self.game = game
        self.cards = self.loadCards()
        self.card_positions = self.CardPositions()
    def loadCards(self):
        cards = []
        for i in range(1, 55):
            card_path = f'cards/{i}.png'
            try:
                img = pygame.image.load(card_path)
                img = pygame.transform.scale(img, (50,75))
                cards.append(img)
            except pygame.error:
                pass
        return cards
    # CardPositions generates 40 random positions for the cards to be drawn on the screen, just for menu
    def CardPositions(self):
        positions = []
        while len(positions) < 40:
            x = random.randint(0, self.game.width - 50)
            y = random.randint(0, self.game.height - 75)
            overlapping = False
            for px,py in positions:
                if abs(x-px) < 55 and abs(y-py) < 80:
                    overlapping = True
                    break
            if not overlapping:
                positions.append((x,y))
        return positions
    #draw pretty much just draws the cards on the screen 
    def draw(self):
        for idx, (x,y) in enumerate(self.card_positions):
            index = idx % len(self.cards)
            self.game.screen.blit(self.cards[index], (x,y))

    def validate_card_position(self, x, y, width, height):
        return (0 <= x <= self.game.width - width and
                0 <= y <= self.game.height - height)

#Main game menu.
class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Comic Sans MS", 25)
        
        start_x = game.width//2 - 60
        start_y = game.height//2 - 60
        rules_y =  start_y+40
        exit_y = start_y+80
    

        self.start_button = pygame.Rect(start_x, start_y, 120, 30)
        self.rules_button = pygame.Rect(start_x, rules_y , 120, 30)
        self.exit_button = pygame.Rect(start_x, exit_y, 120, 30)
    def draw(self):
      
        self.game.card_manager.draw()
        green_1 = self.game.dark_green
        game_screen = self.game.screen

        buttons = [ (self.start_button, "Start"), (self.rules_button, "Rules"), (self.exit_button, "Exit")]

        for button, text in buttons:
    
            button_width = button.width
            button_height = button.height
            button_x = button.x
            button_y = button.y

            text_surface = self.font.render(text, True, (0, 0, 0))
            text_width = text_surface.get_width()
            text_height = text_surface.get_height()
            text_x = button_x + (button_width - text_width) // 2
            text_y = button_y + (button_height - text_height) // 2

            pygame.draw.rect(game_screen, green_1, button)
            game_screen.blit(text_surface, (text_x, text_y))

    def clicker(self, pos):
        if self.start_button.collidepoint(pos):
            self.game.current_screen = DifficultyMenu(self.game)
        elif self.rules_button.collidepoint(pos):
            self.game.current_screen = RulesScreen(self.game)
        elif self.exit_button.collidepoint(pos):
            pygame.quit()
            sys.exit()

class DifficultyMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Comic Sans MS", 40)
        self.difficulties = ["Undergrad", "Masters", "PhD"]
        self.buttons = []

        center_x = game.width // 2
        base_y = 200
        button_width = 100
        button_height = 50
        for i, diff in enumerate(self.difficulties):
            text = self.font.render(diff, True, (0, 0, 0))
            rect = text.get_rect()
            rect.topleft = (center_x - button_width, base_y + i * 100)
            button_rect = rect.inflate(20, 10)
            self.buttons.append((diff.lower(), button_rect))
    #  Draws the buttons for the difficulties           
    def draw(self):
        self.game.card_manager.draw()
        for diff, rect in self.buttons:
            pygame.draw.rect(self.game.screen, self.game.dark_green, rect)
            text = self.font.render(diff.capitalize(), True, (0,0,0))
            self.game.screen.blit(text, rect.topleft)
    def clicker(self, pos):
        for diff, rect in self.buttons:
            if rect.collidepoint(pos):
                self.game.current_screen = BlackjackGame(self.game, diff)
                break

class RulesScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Times New Roman", 18)
        self.text_lines = [
            "Three difficulties: Undergrad, Masters, PhD.",
            "Undergrad: Standard blackjack (player vs. dealer). Player and dealer are dealt one card. ",
            "Then the player may double down or stand. One more card is then dealt to both.",
            " The player may hit repeatedly; the dealer reveals their hidden card ",
            "and draws until reaching 17. Outcome is determined by comparing totals.",
            "Masters: 'Blackjack Free For All' with 1 NPC. Dealer and NPC each receive one upcard",
            "and one hidden card. After dealing, the NPC acts (drawing extra cards and possibly raising $50).",
            "-If the NPC raises, a message is shown and the player's ",
            "buttons change to 'Match Bet' and 'Fold'. Then the player acts.",
            "PhD: 'Blackjack Free For All' with 2 NPCs.",
            "Similar to Masters but with 2 NPCs.",
            "Special rules:",
            "If the dealer busts, every winning player doubles their initial bet.",
            "If any player (NPC or human) gets exactly 21, they receive a bonus equal to their initial bet.",
            "The session ends when either you or all NPCs run out of money."
        ]
        self.back_button = pygame.Rect(50, game.height - 70, 120, 30)
    #
    def draw(self):
        self.game.screen.fill(self.game.green)
        y = 50
        # Draw the text lines
        rendered_lines = [self.font.render(line, True, self.game.white) for line in self.text_lines]
        for rendered in rendered_lines:
            self.game.screen.blit(rendered, (50, y))
            y += 35
        self._draw_button(self.back_button, "Back")

    def clicker(self, pos):
        if self.back_button.collidepoint(pos):
            self.game.current_screen = Menu(self.game)
    # Draws the button for the back button
    def _draw_button(self, button, text):
        pygame.draw.rect(self.game.screen, self.game.dark_green, button)
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_x = button.x + (button.width - text_surface.get_width()) // 2
        text_y = button.y + (button.height - text_surface.get_height()) // 2
        self.game.screen.blit(text_surface, (text_x, text_y))


class BlackjackGame:
    def __init__(self, game, difficulty):
        self.game = game
        self.difficulty = difficulty.lower()   # 'undergrad', 'masters', or 'phd'
        self.font = pygame.font.SysFont("Comic Sans MS", 25)
        self.large_font = pygame.font.SysFont("Comic Sans MS", 35)
        ## Set up the game state. Sets up the min and max bets for npcs, initial pot, round results, and money.
        self.player_money = 1000
        self.player_bet = 100
        self.min_bet = 5
        self.max_bet = 100
        self.pot = 0
        self.round_result = ""

        # Undergrad is different, its just generic blackjack so this is the code for it.
                #  Set up the game state
        if self.difficulty == "undergrad":
            self.state = "initial_deal"
        else:
            self.state = "double_down_decision"
    # Load card images
        self.card_images = {}
        for i in range(1, 55):
            try:
                img = pygame.image.load(f'cards/{i}.png')
                img = pygame.transform.scale(img, (75,105))
                self.card_images[i] = img
            except pygame.error:
                pass

        #back is jokers 
        self.card_back = self.card_images.get(53, None)
        self.buttons = {}

        # Create NPCs for masters.
        if self.difficulty == "undergrad":
            self.npc_players = []
            self.reset_round_undergrad()
        else:
            if self.difficulty == "masters":
                self.npc_players = [ComputerPlayer("NPC", difficulty=self.difficulty)]
            else:  # phd
                self.npc_players = [ComputerPlayer("NPC 1", difficulty=self.difficulty),
                                    ComputerPlayer("NPC 2", difficulty=self.difficulty)]
            self.reset_round_multidiff()

   #undergrad
    def reset_round_undergrad(self):
        ## Reset the round for undergrad mode
        self.deck = create_deck_console()
        self.player_hand, self.dealer_hand = [], []
        self.player_bet = 100
        self.player_money -= self.player_bet
        self.pot = self.player_bet
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)
        self.state, self.round_result = "initial_deal", ""

    def _draw_undergrad_screen(self):
        # Draw the screen for undergrad mode
        self.game.screen.fill(self.game.green)
        self.draw_hand_undergrad(self.dealer_hand, "dealer")
        self.draw_hand_undergrad(self.player_hand, "player")
        # Draw NPC hands if any
        money = self.font.render(f"Money: ${self.player_money}", True, self.game.white)
        bet   = self.font.render(f"Bet:   ${self.player_bet}", True, self.game.white)
        self.game.screen.blit(money, (20, self.game.height-120))
        self.game.screen.blit(bet,   (20, self.game.height-90))
        if self.round_result:
            # Draw the round result message
            txt = self.large_font.render(self.round_result, True, self.game.white)
            self.game.screen.blit(txt, (self.game.width//2 - txt.get_width()//2,
                                        self.game.height//2 + 40))
            
        self.draw_buttons_undergrad()

    def draw_hand_undergrad(self, hand, position="player"):
        cardw, cardh, space = 75, 105, 10           
        dealerstate = {"initial_deal", "player_turn"} #

    #  layout 
        y_lookup = {
         "dealer": 50,
            "player": self.game.height - 150,
    }
        y = y_lookup.get(position, 0)
        #  card positions
        n = len(hand)
        total_w = n * cardw + (n - 1) * space
        start_x = (self.game.width - total_w) // 2 if position in y_lookup else 0

        #  draw cards 
        hide_second = (position == "dealer" and self.state in dealerstate and n > 1)

        for i, card in enumerate(hand):
            x = start_x + i * (cardw + space)
            should_hide = hide_second and i == 1

            if should_hide:
                # draw card back (or placeholder)
                if self.card_back:
                    self.game.screen.blit(self.card_back, (x, y))
                else:
                    pygame.draw.rect(self.game.screen, self.game.white, (x, y, cardw, cardh))
            else:
                img = self.get_card_image(card)
                if img:
                    self.game.screen.blit(img, (x, y))
                else:
                    pygame.draw.rect(self.game.screen, self.game.white, (x, y, cardw, cardh))

    # value label 
        visible_hand = [hand[0]] if hide_second else hand
        value = calculate_hand_value(visible_hand) if hand else 0

        label = self.font.render(f"Value: {value}", True, self.game.white)
        self.game.screen.blit(label, (start_x, y - 30))


    def draw_buttons_undergrad(self):

        button_height=50
        column_x=self.game.width-200
        first_y=self.game.height-150
        second_y=self.game.height-90
        dark_green=self.game.dark_green
        black=(0,0,0)

        ##  button specs
        if self.state=="initial_deal": 
            specs=[("Double Down",160,"Double Down"),("Stand",150,"Stand")]
        elif self.state=="player_turn": 
            specs=[("Hit",160,"Hit"),("Stand",150,"Stand")]
        elif self.state=="round_over": 
            specs=[("Next Round",160,"Next Round"),("Back to Menu",150,"Menu")]
        else: 
            self.buttons={}
            return
        ##  draw buttons
        self.buttons={}
        for ((key,width,caption),y) in zip(specs,(first_y,second_y)):
            rect = pygame.Rect(column_x,y,width,button_height)
            self.buttons[key]=rect

            pygame.draw.rect(self.game.screen,dark_green,rect)
            txt=self.font.render(caption,True,black)
            self.game.screen.blit(txt,txt.get_rect(center=rect.center))

    #Clicker 
    def clicker_undergrad(self, pos):
        for label, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self.handle_button_undergrad(label)
                break
    # Handle button clicks for undergrad mode
    def handle_button_undergrad(self, label):
        if self.state == "initial_deal":
            if label == "Double Down":
                if self.player_money >= self.player_bet:
                    self.player_money -= self.player_bet
                    self.player_bet *= 2

                else:
                    self.round_result = "Insufficient funds to double down."
                    self.state = "round_over"
                    return
                
            self.deal_card(self.player_hand)
            self.deal_card(self.dealer_hand)
            self.state = "player_turn"

        elif self.state == "player_turn":
            if label == "Hit":
                self.deal_card(self.player_hand)

                if calculate_hand_value(self.player_hand) > 21:
                    self.round_result = "Bust!"
                    self.state = "round_over"

            elif label == "Stand":
                self.state = "dealer_turn"
                self.dealer_play_undergrad()

        elif self.state == "round_over":
            if label == "Next Round":
                if self.player_money > 0:
                    self.reset_round_undergrad()

                else:
                    self.round_result = "You are out of money. Game over."

            elif label == "Back to Menu":
                self.game.current_screen = Menu(self.game)

    def resolve_round_undergrad(self):
        self.state = "round_over"
        dealer_total = calculate_hand_value(self.dealer_hand)
        player_total = calculate_hand_value(self.player_hand)

        if player_total > 21:
            self.round_result = "Bust!"
            # Money is already deducted when placing bet
        elif dealer_total > 21 or player_total > dealer_total:
            self.player_money += self.player_bet * 2  # Win pays 2x bet
            self.round_result = "Dealer busted! You win!" if dealer_total > 21 else "You win!"
        elif dealer_total == player_total:
            self.player_money += self.player_bet     # Push returns bet
            self.round_result = "Push!"
        else:
            self.round_result = "Dealer wins!"       #  Loss keeps deducted bet


    def dealer_play_undergrad(self):
        self.state = "dealer_turn"
        while self.dealer_should_hit_undergrad():
            self.deal_card(self.dealer_hand)
            if calculate_hand_value(self.dealer_hand) > 21:
                break
        self.resolve_round_undergrad()

    def dealer_should_hit_undergrad(self):
        return calculate_hand_value(self.dealer_hand) < 17
    
    def reset_round_multidiff(self):
        self.deck = create_deck_console()
        self.player_hand, self.dealer_hand = [], []
        self.player_money -= self.player_bet
        self.pot = self.player_bet

        for npc in self.npc_players:
            self.pot += npc.place_bet(self.min_bet, self.max_bet)

        for _ in range(2):
            self.deal_card(self.player_hand)
            self.deal_card(self.dealer_hand)

        for npc in self.npc_players:
            npc.hand, npc.busted = [], False
            for _ in range(2):
                self.deal_card(npc.hand)

        self.npc_phase()
        self.round_result = ""

    
    def draw_hand(self, hand, position="player", label="", money=0, busted=False):

        card_width = 75
        spacing = 10
        n = len(hand)
        # For dealer and player, layout is standard.
        if position == "dealer":
            y = 50
            total_width = n * card_width + (n - 1) * spacing
            start_x = (self.game.width - total_width) // 2
        elif position == "player":
            y = self.game.height - 150
            total_width = n * card_width + (n - 1) * spacing
            start_x = (self.game.width - total_width) // 2
        # For NPCs:
        elif position in ["npc_left", "npc_right"]:
            y = 200
            # For PHd, arrange in two rows if more than 3 cards.
            if self.difficulty == "phd" and n > 3:
                row1_count = 3
                row2_count = n - 3
                total_width_row1 = row1_count * card_width + (row1_count - 1) * spacing
                if position == "npc_left":
                    start_x = 20
                else:
                    start_x = self.game.width - total_width_row1 - 20
                # Draw first row:
                for i in range(row1_count):
                    x = start_x + i * (card_width + spacing)
                    # For NPCs, only show upcard (first card) when round not over.
                    if (self.state != "round_over" and not busted) and i > 0:
                        if self.card_back:
                            self.game.screen.blit(self.card_back, (x, y))
                        else:
                            pygame.draw.rect(self.game.screen, self.game.white, (x, y, card_width, 105))
                    else:
                        card_img = self.get_card_image(hand[i])
                        if card_img:
                            self.game.screen.blit(card_img, (x,y))
                        else:
                            pygame.draw.rect(self.game.screen, self.game.white, (x,y,card_width,105))
                # Draw second row:
                row2_y = y + card_width + 10
                total_width_row2 = row2_count * card_width + (row2_count - 1) * spacing
                start_x_row2 = start_x + (total_width_row1 - total_width_row2) // 2
                for i in range(row2_count):
                    x = start_x_row2 + i * (card_width + spacing)
                    if self.state != "round_over":
                        if self.card_back:
                            self.game.screen.blit(self.card_back, (x, row2_y))
                        else:
                            pygame.draw.rect(self.game.screen, self.game.white, (x, row2_y, card_width, 105))
                    else:
                        card_img = self.get_card_image(hand[row1_count + i])
                        if card_img:
                            self.game.screen.blit(card_img, (x, row2_y))
                        else:
                            pygame.draw.rect(self.game.screen, self.game.white, (x, row2_y, card_width, 105))
            
                if self.state != "round_over":
                    value = calculate_hand_value([hand[0]]) if hand else 0
                else:
                    value = calculate_hand_value(hand)
                value_text = self.font.render(f"Value: {value}", True, self.game.white)
                self.game.screen.blit(value_text, (start_x, y-30))
                label_text = self.font.render(f"{label} (${money})", True, self.game.white)
                self.game.screen.blit(label_text, (start_x, y-60))
                return
            else:
                total_width = n * card_width + (n - 1) * spacing
                if position == "npc_left":
                    start_x = 20
                else:
                    start_x = self.game.width - total_width - 20
                y = 200
        else:
            y = 0
            start_x = 0
        
        for i, card in enumerate(hand):
            x = start_x + i * (card_width + spacing)
            if position=="dealer" and i==0 and self.state in ["double_down_decision", "npc_raise_decision", "player_turn"]:
                if self.card_back:
                    self.game.screen.blit(self.card_back, (x,y))
                else:
                    pygame.draw.rect(self.game.screen, self.game.white, (x,y,card_width,105))
            elif (position=="npc_left" or position=="npc_right") and i > 0 and (self.state != "round_over" and not busted):
                 if self.card_back:
                    self.game.screen.blit(self.card_back, (x,y))
                 else:
                    pygame.draw.rect(self.game.screen, self.game.white, (x,y,card_width,105))
            else:
                card_img = self.get_card_image(card)
                if card_img:
                    self.game.screen.blit(card_img, (x,y))
                else:
                    pygame.draw.rect(self.game.screen, self.game.white, (x,y,card_width,105))
        if position=="dealer" and self.state in ["double_down_decision", "npc_raise_decision", "player_turn"]:
            value = calculate_hand_value([hand[1]]) if len(hand)>1 else 0
        elif (position=="npc_left" or position=="npc_right") and (self.state != "round_over" and not busted):
            value = calculate_hand_value([hand[0]]) if hand else 0
        else:
            value = calculate_hand_value(hand)
        value_text = self.font.render(f"Value: {value}", True, self.game.white)
        self.game.screen.blit(value_text, (start_x, y-30))

        if position in ["npc_left", "npc_right"]:
            label_text = self.font.render(f"{label} (${money})", True, self.game.white)
            self.game.screen.blit(label_text, (start_x, y-60))

    def get_card_image(self, card):
        rank, suit = card
        rank_order = ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
        suit_order = ["Clubs", "Spades", "Hearts", "Diamonds"]
        try:
            index = rank_order.index(rank)*4 + suit_order.index(suit) + 1
        except ValueError:
            index = 53
        return self.card_images.get(index, None)

    def npc_phase(self):
        for npc in self.npc_players:
            if npc.busted:
                continue
            dealer_up = calculate_hand_value([self.dealer_hand[1]]) if len(self.dealer_hand) > 1 else 0
            while calculate_hand_value(npc.hand) < 17:
                self.deal_card(npc.hand)
          
                if calculate_hand_value(npc.hand) > 21:
                    npc.busted = True
                    break
        
            if not npc.busted and calculate_hand_value(npc.hand) >= 18 and npc.money >= 50:
                npc.money -= 50
                npc.bet += 50
                self.pot += 50
                self.npc_raise_amount = 50
                self.round_result = f"{npc.name} raised pot by $50."
                self.state = "npc_raise_decision"
                return
        self.state = "player_turn"

    def draw_buttons(self):
        x=self.game.width-200
        h=50
        dg=self.game.dark_green
        black=(0,0,0)
        self.buttons={}
        
        if self.state=="double_down_decision" :
            specs=[("Double Down",160,"Double Down",self.game.height-150), ("Stand",150,"Stand",self.game.height-90)]
        elif self.state=="npc_raise_decision" :
            specs=[("Match Bet",160,"Match Bet",self.game.height-150), ("Fold",150,"Fold",self.game.height-90)]
        elif self.state=="player_turn":
            if self.difficulty=="masters":
                specs=[("Hit",160,"Hit",self.game.height-150), ("Stand",150,"Stand",self.game.height-90)]
            else: 
                specs=[("Hit",160,"Hit",self.game.height-180), ("Raise $100",160,"Raise $100",self.game.height-120), ("Stand",150,"Stand",self.game.height-60)]
        elif self.state=="round_over":
            specs=[("Next Round",160,"Next Round",self.game.height-150), ("Back to Menu",150,"Menu",self.game.height-90)]
        else:
            return
        

        for key,w,cap,y in specs:
            rect   =  pygame.Rect(x,y,w,h)
            self.buttons[key] = rect
            pygame.draw.rect(self.game.screen,dg,rect)

            txt=self.font.render(cap,True,black)

            self.game.screen.blit(txt,txt.get_rect(center=rect.center))

    def clicker_multidiff(self, pos):
        for label, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self.handle_button(label)
                break

    def handle_button(self, label):
        if self.state == "double_down_decision":
            if label == "Double Down":
                if self.player_money >= self.player_bet:
                    self.player_money -= self.player_bet
                    self.player_bet *= 2
                    self.pot += self.player_bet
                self.deal_card(self.player_hand)
                self.deal_card(self.dealer_hand)

            elif label == "Stand":
                self.deal_card(self.player_hand)
                self.deal_card(self.dealer_hand)

            if self.difficulty in ["masters", "phd"]:
                self.npc_phase()

            if self.state != "npc_raise_decision":
                self.state = "player_turn"

        elif self.state == "npc_raise_decision":
            if label == "Match Bet":
                self.player_bet += self.npc_raise_amount
                self.pot += self.npc_raise_amount
                self.round_result = "Player matched the raise."
                self.state = "player_turn"
            elif label == "Fold":
                self.round_result = "Player folded! Round over."
                self.state = "round_over"
        elif self.state == "player_turn":
            if label == "Hit":
                self.deal_card(self.player_hand)
                if calculate_hand_value(self.player_hand) > 21:
                    self.round_result = "You busted!"
                    self.state = "round_over"
            elif label == "Stand":
                self.state = "dealer_turn"
                self.dealer_play()
            elif label == "Raise $100":
                if self.player_money >= 100:
                    self.player_money -= 100
                    self.player_bet += 100
                    self.pot += 100
                    self.round_result = "Player raised $100."
                else:
                    self.round_result = "Player is all-in."
        elif self.state == "round_over":
            if label == "Next Round":
                if ((self.player_money > 0 and any(npc.money > 0 for npc in self.npc_players))
                      or self.difficulty=="undergrad"):
                    if self.difficulty=="undergrad":
                        self.reset_round_undergrad()
                    else:
                        self.reset_round_multidiff()
                else:
                    if self.player_money > 0:
                        self.round_result = "congrats, you win!"
                    else:
                        self.round_result = "game over! You lose."
            elif label == "Back to Menu":
                self.game.current_screen = Menu(self.game)
                
    def dealer_play(self):
        while self.dealer_should_hit():
            self.deal_card(self.dealer_hand)
        if self.difficulty=="phd" and len(self.npc_players)==2:
            npc2 = self.npc_players[1]
            if not npc2.busted:
                while calculate_hand_value(npc2.hand) < 17:
                    self.deal_card(npc2.hand)
                    if calculate_hand_value(npc2.hand) > 21:
                        npc2.busted = True
                        break
        self.resolve_round()

    def dealer_should_hit(self):
        return calculate_hand_value(self.dealer_hand) < 17
    def resolve_round(self):
        
        self.state = "round_over"
        dealer_total = calculate_hand_value(self.dealer_hand)
        player_total = calculate_hand_value(self.player_hand)
     
        npc_totals = []
        for npc in self.npc_players:
            total = calculate_hand_value(npc.hand)
            if total > 21:
                total = -1  # busted NPC
                npc.busted = True
            npc_totals.append(total)
        
        outcome = ""
        
       
        if self.difficulty == "undergrad":
            if player_total > 21:
                outcome = "you busted! dealer wins."
                self.player_money -= self.player_bet
            elif dealer_total > 21:
                outcome = "dealer busted! You win!"
                self.player_money += self.player_bet
            elif player_total > dealer_total:
                outcome = "you win!"
                self.player_money += self.player_bet
            elif dealer_total > player_total:
                outcome = "dealer wins!"
                self.player_money -= self.player_bet
            else:
                outcome = "push! Bet returned."
                self.player_money += self.player_bet

        elif self.difficulty == "masters":
            npc_total = npc_totals[0] if npc_totals else -1
            if player_total > 21:
                outcome = "You busted! dealer wins."
                self.player_money -= self.player_bet
            elif dealer_total > 21 and npc_total < 0:
                outcome = "dealer & npc busted! You win!"
                self.player_money += self.player_bet
            elif dealer_total > 21:
                outcome = "dealer busted! You win!"
                self.player_money += self.player_bet * 2  
            elif npc_total < 0:
               
                if player_total > dealer_total:
                    outcome = "you win!"
                    self.player_money += self.player_bet
                elif dealer_total > player_total:
                    outcome = "dealer wins!"
                    self.player_money -= self.player_bet
                else:
                    outcome = "push! Bet returned."
                    self.player_money += self.player_bet
            else:
              
                if (player_total > dealer_total) and (player_total > npc_total):
                    outcome = "you win!"
                    self.player_money += self.player_bet
                elif (dealer_total > player_total) and (dealer_total > npc_total):
                    outcome = "dealer wins!"
                    self.player_money -= self.player_bet
                elif (npc_total > player_total) and (npc_total > dealer_total):
                    outcome = "npc wins!"
                    self.player_money -= self.player_bet
                else:
                    outcome = "push! Bet returned."
                    self.player_money += self.player_bet


        elif self.difficulty == "phd":
           
            if len(npc_totals) < 2:
              
                npc_totals = npc_totals + [-1]*(2-len(npc_totals))
         
            values = {
                "player": player_total,
                "dealer": dealer_total,
                "npc1": npc_totals[0],
                "npc2": npc_totals[1]
            }
            # If the dealer busts, treat its total as -1.
            if dealer_total > 21:
                values["dealer"] = -1
            # Determine the highest total.
            max_total = max(values.values())
            # Find all entities that have the maximum total.
            winners = [name for name, total in values.items() if total == max_total]
            if len(winners) == 1:
                winner = winners[0]
                if winner == "player":
                    outcome = "You win!"
                    self.player_money += self.player_bet
                elif winner == "dealer":
                    outcome = "Dealer wins!"
                    self.player_money -= self.player_bet
                elif winner.startswith("npc"):
                    outcome = f"{winner.upper()} wins!"
                    self.player_money -= self.player_bet
                else:
                    outcome = "Push! Bet returned."
                    self.player_money += self.player_bet
            else:
                outcome = "Push! Bet returned."
                self.player_money += self.player_bet

       
        if player_total == 21:
            outcome += " Blackjack bonus!"
            self.player_money += self.player_bet
        
        for idx, npc in enumerate(self.npc_players):
            total = calculate_hand_value(npc.hand)
            if total > 21:
                npc.busted = True
            if total == 21:
                npc.money += npc.bet  
            if dealer_total > 21 and total > 0: 
                npc.money += npc.bet * 2
            elif total > dealer_total and total > 0:
                npc.money += npc.bet
            elif dealer_total > total:
                pass
            else:
                npc.money += npc.bet
        self.round_result = outcome


    def draw(self):
        if self.difficulty == "undergrad":
            self._draw_undergrad_screen()    #  <<< FIX 2
        else:
            self.draw_multidiff()

    def draw_multidiff(self):
        self.game.screen.fill(self.game.green)
        self.draw_hand(self.dealer_hand, position="dealer")
        if self.npc_players:
            if len(self.npc_players)==1:
                self.draw_hand(self.npc_players[0].hand, position="npc_left",
                               label=self.npc_players[0].name, money=self.npc_players[0].money)
            elif len(self.npc_players)==2:
                self.draw_hand(self.npc_players[0].hand, position="npc_left",
                               label=self.npc_players[0].name, money=self.npc_players[0].money)
                self.draw_hand(self.npc_players[1].hand, position="npc_right",
                               label=self.npc_players[1].name, money=self.npc_players[1].money)
        self.draw_hand(self.player_hand, position="player")
        money_text = self.font.render(f"Money: ${self.player_money}", True, self.game.white)
        bet_text = self.font.render(f"Bet: ${self.player_bet}", True, self.game.white)
        self.game.screen.blit(money_text, (20, self.game.height-120))
        self.game.screen.blit(bet_text, (20, self.game.height-90))
        if self.round_result:
            result_text = self.large_font.render(self.round_result, True, self.game.white)
            self.game.screen.blit(result_text, (self.game.width//2 - result_text.get_width()//2, self.game.height//2 + 40))
        self.draw_buttons()

    def deal_card(self, hand):
        if self.deck:
            card = self.deck.pop()
            hand.append(card)
            return card
        return None

    def clicker(self, pos):
        if self.difficulty == "undergrad":
            self.clicker_undergrad(pos)
        else:
            self.clicker_multidiff(pos)

    def clicker_undergrad(self, pos):
        for label, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self.handle_button_undergrad(label)
                break

    def handle_button_undergrad(self, label):
        if self.state=="initial_deal":
            if label=="Double Down":
                if self.player_money >= self.player_bet:
                    self.player_money -= self.player_bet
                    self.player_bet *= 2
                else:
                    self.round_result = "Insufficient funds to double down."
                    self.state = "round_over"
                    return
            self.deal_card(self.player_hand)
            self.deal_card(self.dealer_hand)
            self.state = "player_turn"
        elif self.state=="player_turn":
            if label=="Hit":
                self.deal_card(self.player_hand)
                if calculate_hand_value(self.player_hand) > 21:
                    self.round_result = "You busted!"
                    self.state = "round_over"
            elif label=="Stand":
                self.state = "dealer_turn"
                self.dealer_play_undergrad()
        elif self.state=="round_over":
            if label=="Next Round":
                if self.player_money>0:
                    self.reset_round_undergrad()
                else:
                    self.round_result = "You are out of money. Game over."
            elif label=="Back to Menu":
                self.game.current_screen = Menu(self.game)

    def dealer_play_undergrad(self):
        self.state = "dealer_turn"
        while self.dealer_should_hit_undergrad():
            self.deal_card(self.dealer_hand)
            if calculate_hand_value(self.dealer_hand)>21:
                break
        self.resolve_round_undergrad()

    def dealer_should_hit_undergrad(self):
        return calculate_hand_value(self.dealer_hand) < 17

    def validate_bet(self, amount):
        return (amount > 0 and 
                amount <= self.player_money and
                self.min_bet <= amount <= self.max_bet)

    def check_deck_status(self):
        if len(self.deck) < 10:  # Minimum cards needed
            self.deck = create_deck_console()
            return True
        return False

    def validate_game_state(self, new_state):
        valid_transitions = {
            "initial_deal": ["player_turn", "round_over"],
            "player_turn": ["dealer_turn", "round_over"],
            # etc.
        }
        return new_state in valid_transitions.get(self.state, [])

class Game:
    # Define game screen dimensions and common colors
    width, height = 800, 600
    green = (0,128,0)
    dark_green = (0,100,0)
    white = (255,255,255)

    def __init__(self):
        # Initialize pygame and create the game window


        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Blackjack Free For All")
        self.running = True
        # Initialize CardManager and set the starting screen to Menu
        self.card_manager = CardManager(self)
        self.current_screen = Menu(self)

    def run(self):
        # Main game loop begins; fills the screen and draws the current screen
        while self.running:
            self.screen.fill(self.green)
            self.current_screen.draw()
            self.check_events()
            pygame.display.flip()
        # Quit pygame and exit system when loop ends
        pygame.quit()
        sys.exit()

    def check_events(self):
        # Process event queue for quitting or mouse button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # If the event is a mouse click and current screen has clicker, call its clicker method
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hasattr(self.current_screen, "clicker"):
                    self.current_screen.clicker(event.pos)


if __name__ == "__main__":
    game = Game()
    game.run()