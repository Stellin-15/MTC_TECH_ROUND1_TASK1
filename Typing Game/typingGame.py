import pygame 
import random 
import copy
import nltk


pygame.init()
nltk.download('words')
from nltk.corpus import words

wordlist = words.words()
len_indexes = []
length = 1

wordlist.sort(key=len)
for i in range(len(wordlist)):
    if len(wordlist[i]) > length:
        length += 1
        len_indexes.append(i)
len_indexes.append(len(wordlist))




width = 800
height = 600
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption("MTC Typing Competition")
surafce = pygame.Surface((width,height),pygame.SRCALPHA) 
timer = pygame.time.Clock()
fps = 60




header_font = pygame.font.Font('fonts/Square.ttf',50)
pause_font = pygame.font.Font('fonts/1up.ttf',38)
banner_font = pygame.font.Font('fonts/1up.ttf',28)
font = pygame.font.Font('fonts/AldotheApache.ttf',50)





level = 0
active_string = ''
score = 0
lives = 5
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
paused = False
submit = ''
word_objects = []
choices = [False, True, False, False, False, False, False]
new_level = True

file = open('highScore.txt','r')
read = file.readlines()
highscore = int (read[0])
file.close()

class Button:
    def __init__(self,x_pos,y_pos,text,clicked,surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked 
        self.surf = surf 

    def draw(self):
        cir = pygame.draw.circle(self.surf,(115,115,115),(self.x_pos,self.y_pos),35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            button_pressed = pygame.mouse.get_pressed()
            if button_pressed[0]:
                pygame.draw.circle(self.surf,'white',(self.x_pos,self.y_pos),35)
                self.clicked = True
            else:
                pygame.draw.circle(self.surf,'black',(self.x_pos,self.y_pos),35)
        pygame.draw.circle(self.surf,'white',(self.x_pos,self.y_pos),35,3)
        self.surf.blit(pause_font.render(self.text,True,'white'),(self.x_pos - 12,self.y_pos - 30))




def generate_levels():

    word_objects = []
    include = []
    vertical_spacing = (height - 150)
    if True not in choices:
        choices[0] = True 
    
    for i in range (len(choices)):
        if choices[i]:
            include.append((len_indexes[i],len_indexes[i+1]))
    
    for i in range(level):
        speed = random.randint(3,4)
        y_pos = random.randint(10 + (i * vertical_spacing),(i+1) * vertical_spacing)
        x_pos = random.randint(width, width + 1000)
        indx_sel = random.choice(include)
        index = random.randint(indx_sel[0],indx_sel[1])
        text = wordlist[index].lower()
        new_word = word(text,speed,y_pos,x_pos)
        word_objects.append(new_word)


    return word_objects

def check_high_score():
    global high_score
    if score > high_score:
        high_score = score
        file = open('high_score.txt', 'w')
        file.write(str(int(high_score)))
        file.close()




class word:

    def __init__(self,text,speed,y_pos,x_pos):
        self.text = text
        self.speed = speed 
        self.y_pos = y_pos
        self.x_pos = x_pos

    def draw(self):
        color = 'black'
        screen.blit(font.render(self.text,True,color),(self.x_pos,self.y_pos))
        active_length = len(active_string)
        if active_string == self.text[:active_length]:
            screen.blit(font.render(active_string,True,'green'),(self.x_pos,self.y_pos))

    def update(self):
        self.x_pos -= self.speed




def draw_paused():
    choice_commits = copy.deepcopy(choices)
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [100, 100, 600, 300], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [100, 100, 600, 300], 5, 5)
    resume_button = Button(160, 200, '>', False, surface)
    resume_button.draw()
    quit_button= Button(410, 200, 'X', False, surface)
    quit_button.draw()
    surface.blit(header_font.render('MENU', True, 'white'), (110, 110))
    surface.blit(header_font.render('PLAY!', True, 'white'), (210, 175))
    surface.blit(header_font.render('QUIT', True, 'white'), (450, 175))
    


    screen.blit(surface,(0,0))
    return resume_button.clicked,quit_button.clicked,choice_commits



def draw_screen():
    pygame.draw.rect(screen,(0,164,239),[0,height-100,width,100])
    pygame.draw.rect(screen,"white",[0,0,width,height],5)
    pygame.draw.line(screen,"white",(250,height-100),(250,height),2)
    pygame.draw.line(screen,"white",(700,height-100),(700,height),2)
    pygame.draw.line(screen,"white",(0,height-100),(width,height-100),2)
    pygame.draw.rect(screen,"black",[0,0,width,height],2)

    
    screen.blit(header_font.render(f'Level : {level}',True,'white'),(10,height - 75))
    screen.blit(header_font.render(f'"{active_string}"',True,'white'),(270,height - 75))


    pause_button = Button(748, height-52, '||', False, screen)
    pause_button.draw()


    screen.blit(banner_font.render(f'SCORE: {score}',True,(242,80,34)),(170,10))
    screen.blit(banner_font.render(f'BEST SCORE: {highscore}',True,(242,80,34)),(500,10))
    screen.blit(banner_font.render(f'LIFE: {lives}',True,(242,80,34)),(10,10))

    return pause_button.clicked


def check_answer(score):
    for word in word_objects:
        if word.text == submit:
            points = word.speed * len(word.text) * 10 * (len(word.text)/3)
            score += int(points)
            word_objects.remove(word)

    return score 


run = True 
while run:
    screen.fill('gray')
    timer.tick(fps)
    paused_button_status = draw_screen()


    if paused:
        resume_button, changes, quit_button =draw_paused()
        if resume_button:
            paused = False 
        if quit_button:
            run = False
    if new_level and not paused:
        word_objects = generate_levels()
        new_level = False
    else:
        for w in word_objects:
            w.draw()
            if not paused:
                w.update()
            if w.x_pos < -200:
                word_objects.remove(w)
                lives -= 1
    
    if len(word_objects) <= 0 and not paused:
        level  +=1
        new_level = True  

    if submit != '':
        init = score
        score = check_answer(score)
        submit = ''
        if init == score:
            pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check_high_score()
            run = False
        
        if event.type == pygame.KEYDOWN:
            if not paused:
                if event.unicode.lower() in letters:
                    active_string += event.unicode.lower()
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[ :-1]
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = active_string
                    active_string = ''

            if event.key == pygame.K_ESCAPE:
                if paused:
                 paused = False
                else:
                    paused = True

        if event.type == pygame.MOUSEBUTTONUP and paused:
            if event.button == 1:
                chocies = changes


    if paused_button_status:
        paused = True


    if lives < 0:
        paused = True 
        level = 1
        level = 5
        word_objects =[]
        new_level = True
        check_high_score()
        score = 0

    pygame.display.flip()
pygame.quit()