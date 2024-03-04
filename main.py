import pygame
import math
import random
import time
import os
pygame.init()

pygame.mouse.set_cursor(pygame.cursors.broken_x)
# cursor_image = pygame.image.load("C:\\Users\\Ahmad\\Desktop\\python_project\\download.png")
# pygame.mouse.set_cursor((24, 24), (0, 0), *cursor_image.get_masks())

WIDTH , HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("aim trainer for MASH")

TARGET_INCREMENT = 400

TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 60

BG_COLOR = (0, 25, 40)

LIVES = 3

TOP_BAR_HEIGHT = 50

game_music_path = os.path.join("C:\\Users\\Ahmad\\Desktop\\python_project\\gamemusic.mp3")  # adjust the path to your MP3 sound file
game_music = pygame.mixer.Sound(game_music_path)

sound_path2 = os.path.join("sounds", "C:\\Users\\Ahmad\\Desktop\\python_project\\gameover.wav")  # adjust the path to your MP3 sound file
sound2 = pygame.mixer.Sound(sound_path2)


LABEL_FONT = pygame.font.SysFont("cursive", 24) ## comicsans

sound_path = os.path.join("sounds", "C:\\Users\\Ahmad\\Desktop\\python_project\\pistol.mp3")  # adjust the path to your MP3 sound file
sound = pygame.mixer.Sound(sound_path)

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"
    #target(circle) constructor
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True # can grow is is still TRUE

    #this function is for update current target on every RENDER
    def update(self):
        if self.size + self.grow >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE

        else:
            self.size -= self.GROWTH_RATE    

    #the circle is composed of 4 sub-circle like a real target
    def draw(self,win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)  
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)  
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)  

    #this method called with mouse position event, if the click position is inside the area of circle , will rertuen TRUE, else FALSE
    def collide(self, x, y):
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size

# a function to draw all circle object that stored in targets LIST, and also to re-colore the background on every render
def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win) 

      

#fromat the time to be understand for user
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minuts = int(secs // 60)

    return f"{minuts:02d}:{seconds:02d}.{milli}"                     

# a top bar that show to the user the statistque of his game
def draw_top_bar(win, elapsed_time, target_pressed, misses):
    pygame.draw.rect(win, "gray",(0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}",1,"black")
    
    speed = round(target_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")

    hits_label = LABEL_FONT.render(f"Hits: {target_pressed}", 1, "black")

    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))

#a function called when user lose game, will be refill the screen color(like a reset), and show the user the final game statistics 
def end_screen(win, elapsed_time, target_pressed, clicks):
    game_music.stop()
    sound2.play()
    win.fill(BG_COLOR)
    pygame.mouse.set_cursor(pygame.cursors.diamond)
    

    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}",1,"white")
    
    speed = round(target_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")

    hits_label = LABEL_FONT.render(f"Hits: {target_pressed}", 1, "white")

    accuracy = round(target_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy} %", 1, "white")
    finish_label = LABEL_FONT.render("GAME OVER -_-", 1,"red")

    win.blit(finish_label, (get_middle(finish_label), 50))
    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()
 
# a function used to positioning the last statistics on the middle of screen
def get_middle(surface):
    return WIDTH / 2 - surface.get_width()/2

#MAIN FUNCTION
def main():
    game_music.play()
    run = True
    targets = []
    clock = pygame.time.Clock()

    target_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT) # send pygame user event every 400 ms

    while run:
        clock.tick(60) # to slow the cpu work, or like an FPS adjustment

        click = False
        mouse_pos = pygame.mouse.get_pos() # return a  tuple that contain mouse click position x and y
        elapsed_time = time.time() - start_time ## in second

        for event in pygame.event.get(): # if user press window close button
            if event.type == pygame.QUIT:
                run = False
                break
            
            # recive the signal sended by line 141 , and create a virtual random target every 400 ms (on every signal received) 
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, WIDTH - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                sound.play() #when user click , recive that event and count it 
                click = True
                clicks += 1    

        for target in targets:# update the growth of every target on the screen
            target.update()

            if target.size <= 0:# remove the missed target
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos): # handle when user click on a target => remove that target , increment the score 
                targets.remove(target)
                target_pressed += 1

        if misses >= LIVES: # if the nissed target number more than live number 
            end_screen(WIN, elapsed_time,target_pressed,clicks) # show the end screen that contain a final statistics


        draw(WIN, targets) # on every loop, draw the target LIST
        draw_top_bar(WIN, elapsed_time, target_pressed, misses) # on evrery render , update the top bar (live statistics)
        pygame.display.update()   # update the screen       

    pygame.quit()

if __name__ == "__main__":
    main()