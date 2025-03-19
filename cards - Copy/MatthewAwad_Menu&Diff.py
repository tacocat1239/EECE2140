import pygame
import random
import sys
# Matthew Awad Iteration #04: Initial Implementation and Testing, working menu and difficulty screen. This code when ran on pygames
# will display a menu screen with a start and exit button. When the start button is clicked, the difficulty screen will be displayed
# with three options: Undergrad, Masters, and PhD. 
# Code won't work without the file because it's still in development. (Visual Studios)

class Game:
    width, height = 800, 600
    green = (0, 128, 0)
    dark_green = (0, 100, 0)
    white = (255, 255, 255)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game Menu")
        self.running = True
        self.menu = Menu(self)
        self.difficulty_menu = Difficulty(self)
        self.current_screen = self.menu

    def run(self):
        while self.running:
            self.screen.fill(self.green)
            self.current_screen.draw()
            self.quit()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

    def quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.current_screen.clicker(event.pos)

class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Comic Sans MS", 25)
        
        start_x = game.width // 2 - 60
        start_y = game.height // 2 - 30
        exit_y = game.height // 2 + 20

        self.start_button = pygame.Rect(start_x, start_y, 120, 30)
        self.exit_button = pygame.Rect(start_x, exit_y, 120, 30)
        self.cards = CardManager(game)

    def draw(self):
        self.cards.draw()

        pygame.draw.rect(self.game.screen, self.game.dark_green, self.start_button)
        pygame.draw.rect(self.game.screen, self.game.dark_green, self.exit_button)

        start_text = self.font.render("Start", True, (0, 0, 0))
        exit_text = self.font.render("Exit", True, (0, 0, 0))

        startborderx = self.start_button.x + 30
        startbordery = self.start_button.y - 3
        endborderx = self.exit_button.x + 30
        endbordery = self.exit_button.y - 3

        self.game.screen.blit(start_text, (startborderx, startbordery))
        self.game.screen.blit(exit_text, (endborderx, endbordery ))

    def clicker(self, pos):  

        if self.start_button.collidepoint(pos):
            self.game.current_screen = self.game.difficulty_menu
            
        elif self.exit_button.collidepoint(pos):
            pygame.quit()
            sys.exit()

class Difficulty:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Comic Sans MS", 40)
        self.difficulties = ["Undergrad", "Masters", "PhD"]
        self.positions = [200, 300, 400]
    
    def draw(self):

        for i in range(3):
            text = self.font.render(self.difficulties[i], True, self.game.white)
        
            self.game.screen.blit(text, (self.game.width // 2 - 100, self.positions[i]))


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
                card_image = pygame.image.load(card_path)
                card_image = pygame.transform.scale(card_image, (50, 75))
                cards.append(card_image)

            except pygame.error:
                pass 

        
        return cards
    
    def CardPositions(self):
        positions = []
        while len(positions) < 40:  
            x = random.randint(0, self.game.width - 50)
            y = random.randint(0, self.game.height - 75)
            
            overlapping = False
            for px, py in positions: 

                xO = abs(x - px) < 55  
                yO = abs(y - py) < 80  

                if xO and yO:
                    overlapping = True
                    break  
            
            if not overlapping:
                positions.append((x, y))
        return positions

    def draw(self):

        for idx, (x, y) in enumerate(self.card_positions): 
            number_of_cards = len(self.cards)  
            index = idx % number_of_cards 
            display_cards = self.cards[index]  
            self.game.screen.blit(display_cards, (x, y))  




if __name__ == "__main__":
    game = Game()
    game.run()
