import pygame
from pygame.locals import *
import time
import random


SIZE = 40
WIN_HEIGHT = 1000
WIN_WIDTH = 800
BACKGROUND_COLOR = (51,119,255)

class Apple:
    def __init__(self, partent_screen):
        self.apple = pygame.image.load("img/apple1.png").convert()
        self.partent_screen = partent_screen
        self.x = SIZE*3
        self.y = SIZE*3



    def move_x(self):
        if self.x <= 0 and self.x >= WIN_WIDTH:
            self.x = 0
        else:
            self.x = random.randint(0,20)*SIZE
    
    def move_y(self):
        if self.y <= 0 and self.y >= WIN_HEIGHT:
            self.x = 0
        else:
            self.y = random.randint(0,12)*SIZE
    
    
    def move(self):
        # self.y = random.randint(0,25)*SIZE
        self.move_x()
        self.move_y()


    def draw(self):
        # self.parent_screen.fill((134,101,102))
        self.partent_screen.blit(self.apple, (self.x,self.y))
        pygame.display.flip()
        
 

class snake:
    def __init__(self, partent_screen, length):
        self.length = length
        self.parent_screen = partent_screen
        self.block = pygame.image.load("img/block1.png").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = "right"

    def incr_len(self):
        self.length +=1
        self.x.append(-1)
        self.y.append(-1)
        

    def move_up(self):
        self.direction = 'up'
        self.draw()
    def move_down(self):
        self.direction = 'down'
        self.draw()
    def move_left(self):
        self.direction = 'left'
        self.draw()
    def move_right(self):
        self.direction = 'right'
        self.draw()



    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE 


        self.draw()


    def draw(self):
        self.parent_screen.fill((0,0,0))

        for i in range (self.length):
            self.parent_screen.blit(self.block, (self.x[i],self.y[i]))

        pygame.display.flip()



class game:
    runing = True
    pause = False


    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode((WIN_HEIGHT,WIN_WIDTH))
        self.surface.fill((255,255,255))

        pygame.display.set_caption("Codewithyoha")
        
        pygame.mixer.init()


        # logo
        logo = pygame.image.load("img/apple1.png").convert()

        # set logo
        pygame.display.set_icon(logo)

        self.snake = snake(self.surface, 1)
        self.Apple = Apple(self.surface)
        self.snake.draw()
        self.Apple.draw()


    def in_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 <= y2 + SIZE:
                return True
            
        return False



    # def play(self):
    def player(self):
        self.snake.walk()
        self.Apple.draw()
        self.score()

        # Snake collsion eith apple
        if self.in_collision(self.snake.x[0], self.snake.y[0], self.Apple.x, self.Apple.y):
            sound = pygame.mixer.Sound("SFX/3.wav")
            pygame.mixer.Sound.play(sound)
            self.snake.incr_len()
            self.Apple.move()

        # snake colltision with its self
        for i in range(3, self.snake.length):
            if self.in_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound("SFX/2.wav")
                pygame.mixer.Sound.play(sound)
                time.sleep(.9)
                self.Apple.move()
                raise "Game Over"
            

    def score(self):
        font = pygame.font.SysFont("arial", 40)
        score = font.render(f"Score: {self.snake.length - 1}", True , (255,255,255))
        self.surface.blit(score, (800,20))
        pygame.display.flip()

    def show_gane_o(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        Message = font.render(f"Game is over! Your score is {self.snake.length}", True , (255,255,255))
        self.surface.blit(Message, (200, 200))
        
        Message1 = font.render(f"To play again press Enter, To exit press Escape!", True , (255,255,255))
        self.surface.blit(Message1, (200, 300))

        pygame.display.flip()
        self.snake.length = 1


    def run(self):
            

            
            while self.runing:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.runing = False
                        
                        if event.key == K_RETURN:
                            if self.pause:
                                self.pause = False
                            else:
                                self.pause = True

                        if event.key == K_UP:
                            self.snake.move_up()
                            

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()




                    elif event.type == QUIT:
                        self.runing = False

                try:
                    if self.pause != True:
                        self.player()
                except Exception as e:
                    self.show_gane_o()
                    self.pause = True
                    


                time.sleep(0.1)


        

if __name__ == "__main__":
    game = game()
    game.run()
    