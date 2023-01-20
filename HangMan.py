import pygame, random, time

# Setting up
pygame.init()
WIDTH, HEIGHT = 990, 600 # space pixels = 15
# WIDTH, HEIGHT = 1130, 600 # space pixels = 25
win = pygame.display.set_mode((WIDTH, HEIGHT))
# Color
BISQUE = (255,228,196)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 200)
WHITE = (255, 255, 255)
GREY = (140, 140, 140)
LIGHT_GREY = (224, 224, 209)
WOOD_COLOR = (216, 163, 84)
DARK_WOOD = (130, 62, 29)

# Image
body_parts = []
for i in range(1, 9):
    image = pygame.image.load(f'data/hanging parts/{i}.png')
    body_parts.append(pygame.transform.scale(image, (216, 369)))
correct = pygame.transform.scale(pygame.image.load('data/Assets/correct answer.png').convert(), (WIDTH, HEIGHT))
incorrect = pygame.transform.scale(pygame.image.load('data/Assets/incorrect answer.png').convert(), (WIDTH, HEIGHT))
# Icon
icon = pygame.image.load('data/hanging parts/8.png')
pygame.display.set_icon(icon)
# Caption
pygame.display.set_caption('Hang Man')
# Sound Effect
right = pygame.mixer.Sound('data/Assets/win.wav')
wrong = pygame.mixer.Sound('data/Assets/wrong.wav')

        
class Button:
    # Buttons for letters
    def __init__(self, text, x):
        self.text = text
        self.x = x
        index = alphabet.index(text)
        if index <=12:
            self.y = row1
        else:
            self.y = row2
        self.width = 50
        self.height = 60
        self.color = WHITE

    def draw(self):
        # Display Circle
        pygame.draw.circle(win, self.color, (self.x + 20, self.y + 35), 30)
        # Letter
        font = pygame.font.Font('data/Fonts/Roboto/Roboto-Regular.ttf', 60)
        out_text = self.text.upper()
        text = font.render(out_text, 1, BLACK)
        win.blit(text, (self.x, self.y))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False
        

class Menu:
    def __init__(self, text, x, y):
        self.clicked = False
        self.font = pygame.font.Font('data/Fonts/Arial/Arial.ttf', 50)
        self.text = self.font.render(text, 1, BLACK)
        self.x = x - self.text.get_width()//2
        self.y = y
        self.color = LIGHT_GREY # Selected button color

    def draw(self, bg=False):
        if bg:
            # Background
            image = pygame.image.load('data/Assets/forest.png')
            background = pygame.transform.scale(image, (WIDTH, HEIGHT))
            win.blit(background, (0, 0))
        # Square
        pygame.draw.rect(win, True, (self.x-3,self.y-3,self.text.get_width()+6,self.text.get_height()+6),0)
        rect = pygame.Rect(self.x, self.y, self.text.get_width(), self.text.get_height())
        pygame.draw.rect(win, self.color, rect)
        # Button Text
        win.blit(self.text, (self.x, self.y))
        if not menu.clicked:
            # Name
            image1 = pygame.image.load('data/Assets/title (black).png')
            title = pygame.transform.scale(image1, (945, 237))
            win.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT*0.05))
        else:
            # Title
            font2 = pygame.font.Font('data/Fonts/Arial/Arial.ttf', 60)
            title1 = font2.render('GAME OPTION', 1, BLACK)
            win.blit(title1, [WIDTH//2 - title1.get_width()//2, HEIGHT*0.3])
        # Display Update
        pygame.display.flip()
        
    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.text.get_width():
            if self.y < pos[1] < self.y + self.text.get_height():
                return True
        return False


class Quesion:
    def __init__(self):
        self.lst = []
        self.answers = []
        self.count = 0

    def ques_list(self):
        # File
        if self.count <= 0:
            if option2.clicked:
                self.file = open('data/questions.txt', 'r') 
                self.questions = []
                self.count += 1
            else:
                self.file = open('data/topic words.txt', 'r')
                self.count += 1
        # Shuffle Words
        for each_line in self.file:
            self.lst.append(each_line)
            random.shuffle(self.lst)
        # Return Lists
        for each in self.lst:
            if option2.clicked:
                question, answer = each.split('-')
                self.questions.append(question)
            else:
                answer = each
            answer = answer.replace('\n', '')
            self.answers.append(answer)
        if option2.clicked:
            return self.questions, self.answers
        else:
            return self.answers


class Interlude:
    def __init__(self):
        # Continue Button
        font = pygame.font.Font('data/Fonts/Arial/Arial.ttf', 25)
        self.text = font.render('continue', 1, BLACK)
        self.x = WIDTH*0.835
        self.y = HEIGHT*0.6
        self.width = self.text.get_width()
        self.height = self.text.get_height()
        self.color = WOOD_COLOR
        self.font = pygame.font.Font('data/Fonts/Arial/Arial.ttf', 28)
    
    def transition(self):
        if game.count == 8:
            # Screen
            win.blit(incorrect, (0, 0))
            # Surfaces
            self.cont()
        if game.output.isalpha():
            # Screen
            win.blit(correct, (0, 0))
            # Surfacess
            self.cont()

    def cont(self):
        # Square
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, self.color, rect)
        # Continue Button
        win.blit(self.text, (self.x, self.y))
        # Mystery Word
        mys_word = self.font.render(game.answers[game.ques_num], 1, WHITE)
        win.blit(mys_word, (WIDTH*0.51, HEIGHT*0.48))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


class Outro:
    def __init__(self):
        self.initial = 0
    
    def final(self):
        # Screen
        ending = pygame.image.load('data/Assets/ending.png')
        win.blit(ending, (0,0))
        # Final Score
        font = pygame.font.Font('data/Fonts/Roboto/Roboto-Bold.ttf', 50)
        final_score = font.render(f'Your Score: {game.score}', 1, BLACK)
        win.blit(final_score, (WIDTH*0.1, HEIGHT*0.8))
        # Music
        wrong.stop()
        right.stop()
        game.music.stop()
        if self.initial <= 0:
            pygame.mixer.music.load('data/Assets/Ending Music.mp3')
            pygame.mixer.music.play(-1)
        self.initial += 1
        # Update
        pygame.display.flip()


# Variable
FPS =  60
letters_space = 780
space = (WIDTH - letters_space)//14
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
row1 = HEIGHT - 200
row2 = row1 + 100
letters = [Button('a', space), Button('b', space*2 + 60), Button('c', space*3 + 60*2), Button('d', space*4 + 60*3),
           Button('e', space*5 + 60*4), Button('f', space*6 + 60*5), Button('g', space*7 + 60*6), Button('h', space*8 + 60*7),
           Button('i', space*9 + 60*8), Button('j', space*10 + 60*9), Button('k', space*11 + 60*10), Button('l', space*12 + 60*11),
           Button('m', space*13 + 60*12), Button('n', space), Button('o', space*2 + 60), Button('p', space*3 + 60*2),
           Button('q', space*4 + 60*3), Button('r', space*5 + 60*4), Button('s', space*6 + 60*5), Button('t', space*7 + 60*6),
           Button('u', space*8 + 60*7), Button('v', space*9 + 60*8), Button('w', space*10 + 60*9), Button('x', space*11 + 60*10),
           Button('y', space*12 + 60*11), Button('z', space*13 + 60*12)] 
menu = Menu('PLAY', WIDTH//2, HEIGHT//2)
option1 = Menu('RANDOM  WORD', WIDTH//2, HEIGHT//2)
option2 = Menu('WITH  QUESTIONS', WIDTH//2, HEIGHT//2 + 100)
ques = Quesion()
interlude = Interlude()
outro = Outro()


class Game:
    def __init__(self):
        self.passing = False
        self.count = 0
        self.ques_num = 0
        self.menu_clicked = False
        self.lst_count = 0
        self.output = '_'
        # Score
        self.score = 0
        # Endgame
        self.endgame = False
        # Music
        self.music = pygame.mixer.Sound('data/Assets/bg_music 1.mp3')
        self.music.play(-1)

    def game_loop(self):
        # Main Game
        clock = pygame.time.Clock()
        clock.tick(FPS)
        run = True
        # Can not put while loop in a try, except
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                if not self.endgame:
                    # Drawing 
                    if not option1.clicked and not option2.clicked:
                        if not menu.clicked:
                            menu.draw(True)
                        else:
                            option1.draw(True)
                            option2.draw()
                    else:
                        self.drawing()
                    pos = pygame.mouse.get_pos()
                    if not self.passing:
                        # Sound Effect
                        right.stop()
                        wrong.stop()
                        if not option1.clicked and not option2.clicked:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if not menu.clicked:
                                    if menu.isOver(pos):
                                        menu.clicked = True
                                        # The 'break' keeps the buttons from overlapping
                                        break
                                else:
                                    if option1.isOver(pos):
                                        option1.clicked = True
                                        break
                                    elif option2.isOver(pos):
                                        option2.clicked = True
                                        break
                        else:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                for i in range(26):
                                    if letters[i].isOver(pos):
                                        # Putting a letter which is no longer in self.word_left will raise ValueError
                                        try:
                                            self.word_algorithm(letters[i].text)
                                        except ValueError:
                                            pass
                        if event.type == pygame.MOUSEMOTION:
                            if not menu.clicked:
                                if menu.isOver(pos):
                                    menu.color = GREY
                                else:
                                    menu.color = LIGHT_GREY
                            else:
                                if option1.isOver(pos):
                                    option1.color = GREY
                                else:
                                    option1.color = LIGHT_GREY
                                if option2.isOver(pos):
                                    option2.color = GREY
                                else:
                                    option2.color = LIGHT_GREY
                    else:
                        # This color assigment keeps the 'continue' button its wood color after self.passing
                        interlude.color = WOOD_COLOR
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # The action happens once here (frames)
                            if interlude.isOver(pos):
                                # Score
                                if self.output.isalpha():
                                    game.score += 10
                                # Update the game
                                self.ques_num += 1
                                if self.ques_num == 10:
                                    self.endgame = True
                                    break
                                self.reset()
                        if event.type == pygame.MOUSEMOTION:
                            if interlude.isOver(pos):
                                interlude.color = DARK_WOOD
                            else:
                                interlude.color = WOOD_COLOR
                else:
                    outro.final()
        # Escape Pygame
        pygame.quit()

    def drawing(self):
        if self.lst_count <= 1:
            if self.count <=7:
                if self.lst_count <= 0:
                    if option2.clicked:
                        # Questions List
                        self.questions, self.answers = ques.ques_list()
                    elif option1.clicked:
                        # Answers List
                        self.answers = ques.ques_list()
                if self.lst_count <= 0:
                    # Word
                    self.word = self.answers[self.ques_num]
                    self.word_underscore = '_' * len(self.word)
                    self.word_left = list(self.word)
                    self.found_word = list(self.word_underscore)
                    self.output = "".join(self.found_word)
                    self.lst_count += 1
                # Background
                win.fill(BISQUE)
                # The letters
                for i in range(26):
                    letters[i].draw()
                # Mystery Word
                font = pygame.font.Font('data/Fonts/Arial/Arial.ttf', 50)
                text = font.render(self.output, 1, BLACK)
                text_pos = (WIDTH*0.4, HEIGHT*0.4)
                win.blit(text, text_pos)
                # Word length
                font1 = pygame.font.Font('data/Fonts/Arial/Arial.ttf', 40)
                word_length = font1.render(f'({len(self.word)} letters)', 1, BLACK)
                win.blit(word_length, (text_pos[0] + text.get_width() + space*4, text_pos[1]+5))
                if option2.clicked:
                    # Questions
                    font2 = pygame.font.Font('data/Fonts/Didact Gothic/DidactGothic-Regular.ttf', 25)
                    ques_text = font2.render(self.questions[self.ques_num], 1, BLACK)
                    ques_pos = (WIDTH*0.3, HEIGHT*0.2)
                    win.blit(ques_text, ques_pos)
                    font3 = pygame.font.Font('data/Fonts/Didact Gothic/DidactGothic-Regular.ttf', 30)
                    num = font3.render(str(self.ques_num + 1) + '.', 1, BLACK)
                    win.blit(num, (ques_pos[0] - 40, ques_pos[1]-5))
                # Score
                font4 = pygame.font.Font('data/Fonts/Roboto/Roboto-Black.ttf', 50)
                score = font4.render(f'Score: {str(self.score)}', 1, BLACK)
                win.blit(score, (WIDTH - score.get_width() - 10, 0))
                # Hangman
                win.blit(body_parts[self.count], (0, 0))
                # Display Update
                pygame.display.flip()
                if self.count == 7:
                    self.count += 1
                    self.lst_count += 1
                if self.output.isalpha():
                    self.lst_count += 1
        else:
            # Interlude
            if self.lst_count <= 2:
                # Time delayed for animation
                time.sleep(0.7) 
                self.lst_count += 1
                # Sound Effect
                if self.count == 8:
                    wrong.play()
                else:
                    right.play()
            self.passing = True
            interlude.transition()
            # Display Update
            pygame.display.flip()
    
    def word_algorithm(self, letter):
        letter_pos = alphabet.index(letter)
        if letter in self.word:
            letters[letter_pos].color = GREEN
            index = self.word_left.index(letter)
            self.word_left[index] = '_'
            self.found_word[index] = letter
            if letter in self.word_left:
                return self.word_algorithm(letter)
            self.output = ''.join(self.found_word)
        else:
            if not letters[letter_pos].color == RED:
                self.count += 1
            letters[letter_pos].color = RED

    def reset(self):
        self.passing = False
        self.count = 0     #Mistake
        self.lst_count = 1 #SoundEffect
        # Word
        self.word = self.answers[self.ques_num]
        self.word_underscore = '_' * len(self.word)
        self.word_left = list(self.word)
        self.found_word = list(self.word_underscore)
        self.output = "".join(self.found_word)
        # Buttons
        for i in range(26):
            letters[i].color = WHITE


# Initialization
game = Game()
game.game_loop()