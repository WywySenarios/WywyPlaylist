import os, random, soundfile, re, webbrowser
from os import path

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from datetime import datetime

# colours. BRITISH
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
pygame.display.set_icon(pygame.image.load(path.join('.mainfiles', 'icon.jpg')))

singing = True
searching = False
# Default Chronological Loop All
fonds = [pygame.font.SysFont('Verdana', 15), pygame.font.SysFont('Verdana', 30), pygame.font.SysFont('Verdana', 15), '']
fondsfr = [fonds[0].render('Volume', False, WHITE), fonds[0].render('Song #', False, WHITE),
           fonds[2].render('Song %', False, WHITE)]
clock = pygame.time.Clock()


def newsong(increment, skipto):
    global nowsong, nowsongprint
    global wywyquestion
    global length, songtotal
    global everysong, wywymusic, current
    if state == 'All':
        current = everysong
    else:
        current = wywymusic
    if loop != True or (loop == True and skipto != no and searching == True):
        if increment != 0 and increment != no:
            wywyquestion += int(increment)
        #I need to repeat as in regular, but the above same statement is to fix search.
        elif skipto != no:
            wywyquestion = int(skipto) - 1
        elif state == 'Chronological':
            wywyquestion += 1
        else:
            wywyquestion = random.randint(1, len(current)) - 1
        if wywyquestion > len(current) - 1:
            wywyquestion = 0
        elif wywyquestion < 0:
            wywyquestion = len(current) - 1
        nowsong = current[wywyquestion]
        nowsongprint = nowsong[:-4]
        if state == 'All':
            length = soundfile.SoundFile(nowsong)
            nowsongprint = nowsong[nowsong.find('\\', 8) + 1: -4]
            pygame.mixer.music.load(nowsong)
        else:
            length = soundfile.SoundFile(path.join(wywydir, nowsong))
        songtotal = length.frames / length.samplerate
        pygame.display.set_caption(nowsongprint)
        logit(no, 'Now playing ' + nowsongprint)
    if state != 'All':
        pygame.mixer.music.load(path.join(wywydir, nowsong))
    pygame.mixer.music.play(loops=0)
    if pause == True:
        pygame.mixer.music.pause()
    repastetext()


def switchtrack(direction):
    global wywymusic
    global pathnamealt
    global pathname
    global trainindex
    global wywydir
    global longest
    if state == 'All':
        print('Dude, switch from all mode to something else!')
    if direction == 'LEFT':
        trainindex += 1
    else:
        trainindex -= 1
    if trainindex > len(tracks) - 1:
        trainindex = 0
    elif trainindex < 0:
        trainindex = len(tracks) - 1
    pathnamealt = tracks[trainindex]
    pathname = path.join('.tracks', pathnamealt)
    logit(no, 'Track: ' + pathname[8:])
    wywymusic = os.listdir(pathname)
    wywydir = path.join(path.dirname(__file__), pathname)
    logit(wywydir + ' ' + pathname, no)
    longest = 0
    for x in wywymusic:
        if len(x) - 4 > longest:
            longest = len(x) - 4
    newsong(0, no)


def repastetext():
    space = screen.get_width() / 2
    rainbowbk = rainbows(path.join('.mainfiles', 'animations', allrainbow[rainbow1]), [0, 0])
    screen.blit(rainbowbk.image, rainbowbk, rainbowbk.rect)

    if screen.get_width() / longest < screen.get_height() / len(current):
        fonds[3] = pygame.font.SysFont('Verdana', int(screen.get_width() * 1.6 / longest))
    else:
        fonds[3] = pygame.font.SysFont('Verdana', int(screen.get_height() / len(current)))

    for x in range(len(current)):
        texting = current[x][:-4]
        sending = fonds[3].render(texting, False, WHITE)
        screen.blit(sending, (0, x * (int(screen.get_height() / len(current)))))

    seconds = int(pygame.mixer.music.get_pos() / 1000)
    screen.blit(fondsfr[2], (screen.get_width() - 170, 45))
    pygame.draw.rect(screen, BLACK, pygame.Rect(screen.get_width() - 107 + int(seconds / songtotal * 100), 45, 100 - int(seconds / songtotal * 100), 15))
    pygame.draw.rect(screen, WHITE, pygame.Rect(screen.get_width() - 107, 45, 100, 15), 2)
    pygame.draw.rect(screen, WHITE, pygame.Rect(screen.get_width() - 107, 45, int(seconds / songtotal * 100), 15))

    trackingnowsong = int((current.index(nowsong) + 1) / len(current) * 100)

    outline_rect = [pygame.Rect(screen.get_width() - 107, 5, 100, 15),
                    pygame.Rect(screen.get_width() - 107, 25, 100, 15)]
    filling = [pygame.Rect(screen.get_width() - 107, 5, volume * 100, 15),
               pygame.Rect(screen.get_width() - 107, 25, trackingnowsong, 15)]
    fillingALT = [pygame.Rect(screen.get_width() - 107 + volume * 100, 5, 100 - volume * 100, 15),
                  pygame.Rect(screen.get_width() - 107 + trackingnowsong, 25, 100 - trackingnowsong, 15)]

    screen.blit(fondsfr[0], (screen.get_width() - 170, 5))
    if volume == 1:
        pygame.draw.rect(screen, GREEN, filling[0])
    elif volume == 0.5:
        pygame.draw.rect(screen, YELLOW, filling[0])
    else:
        pygame.draw.rect(screen, WHITE, filling[0])
    pygame.draw.rect(screen, BLACK, fillingALT[0])
    if int(volume * 100) <= 0:
        pygame.draw.rect(screen, RED, outline_rect[0], 2)
    else:
        pygame.draw.rect(screen, WHITE, outline_rect[0], 2)
    # space so i don't go crawy
    screen.blit(fondsfr[1], (screen.get_width() - 170, 25))
    if trackingnowsong == 100:
        pygame.draw.rect(screen, GREEN, filling[1])
    elif trackingnowsong == 50:
        pygame.draw.rect(screen, YELLOW, filling[1])
    else:
        pygame.draw.rect(screen, WHITE, filling[1])
    pygame.draw.rect(screen, BLACK, fillingALT[1])
    if trackingnowsong <= 0:
        pygame.draw.rect(screen, RED, outline_rect[1], 2)
    else:
        pygame.draw.rect(screen, WHITE, outline_rect[1], 2)
    statemsg = state
    if loop == True:
        statemsg += ' Looping'
    if searching == True:
        statemsg += '(Searching)'
        searchsend = fonds[1].render(search1, False, BLACK)
        screen.blit(searchsend, (space, 100))
    statesend = fonds[1].render(statemsg, False, BLACK)
    screen.blit(statesend, (space, 10))
    if pause == True:
        pausesend = fonds[1].render('Paused', False, BLACK)
    else:
        pausesend = fonds[1].render('Playing', False, BLACK)
    screen.blit(pausesend, (space, 40))
    timesend = fonds[1].render(datetime.now().strftime("%H:%M"), False, BLACK)
    screen.blit(timesend, (space, 70))

    pygame.display.flip()

def loudness(increment, set):
    global volume
    if volume * 100 < 100 and increment > 0:
        volume += increment
    elif volume > 0 and increment < 0:
        volume += increment
    if set != no: volume = set
    pygame.mixer.music.set_volume(volume)
    logit(no, 'Volume: ' + str(int(volume * 100)))
    repastetext()


def endit():
    global singing
    pygame.mixer.music.unload()
    pygame.mixer.music.load(path.join('.mainfiles', 'done.wav'))
    pygame.mixer.music.play(loops=0)
    logit(no, configs[9])
    while True:
        if pygame.mixer.music.get_busy() != 1: break
    singing = False


def paused():
    global pause
    if pause == True:
        pause = False
        pygame.mixer.music.unpause()
        if searching == False:
            logit(no, 'Playing')
    else:
        pause = True
        pygame.mixer.music.pause()
        if searching == False:
            logit(no, 'Paused')
    repastetext()


class rainbows(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (screen.get_width(), screen.get_height()))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def switchstate(newstate):
    global state, current, wywymusic, loop
    if newstate == 'Loop':
        if True == loop:
            loop = False
        else:
            loop = True
            print('Started looping', nowsongprint)
        repastetext()
    elif newstate == 'All':
        state = newstate
        print('Playing All')
        current = everysong
        newsong(0, no)
    else:
        if state == 'All':
            state = newstate
            newsong(0, no)
        state = newstate
        print('Playing in', newstate, 'order')
        repastetext()
        current = wywymusic
    if state == 'All':
        current = everysong
    else:
        current = wywymusic
    logit(state + ' order', no)


def searchit(what):
    global searching, search1, current
    if what == 'toggle':
        if searching == False:
            searching = True
            search1 = ''
            if pause == False:
                paused()
        elif searching == True:
            if search1 == '':
                logit(no, configs[10])
            else:
                search = int(search1)
                if len(current) < int(search1):
                    logit(no, "Error, You searched a number larger than the playlist size. (" + search1 + ")")
                else:
                    newsong(0, search)
                    if search1[-1] == '1':
                        searchname = 'You searched for the ' + search1 + 'st Song'
                    elif search1[-1] == '2':
                        searchname = 'You searched for the ' + search1 + 'nd Song'
                    elif search1[-1] == '3':
                        searchname = 'You searched for the ' + search1 + 'rd Song'
                    else:
                        searchname = 'You searched for the ' + search1 + 'th Song'
                    logit(no, searchname)
            search1 = ''
            paused()
            searching = False
    elif searching == True:
        search1 = search1 + str(what)
        repastetext()


def logit(logme, printme):
    global no
    log = open(".mainfiles\\log.txt", "a")
    time = str(datetime.now().strftime("%H:%M:%S")) + ' - '
    if printme == no:
        log.write(time + str(logme) + '\n')
    else:
        print(printme)
        log.write(time + str(printme) + '\n')
    log.close()


def setup():
    global tracks, trainindex, longest
    global pathname, pathnamealt
    global wywymusic, wywydir, wywyquestion, everysong, current
    global volume, pause, info
    global allrainbow, refreshing
    global rainbow, rainbow1, allrainbow
    global no, nowsong, nowsongprint, state, configs, search1, searching, loop
    allrainbow = os.listdir(path.join('.mainfiles', 'animations'))
    allrainbow.sort()
    info = open(path.join('.mainfiles', 'readwywy.txt'), "r")
    info.seek(0)
    info = info.read()
    config = open(path.join('.mainfiles', 'config.txt'), "r")
    configs = re.findall('= ([^/]+?)\n', config.read())
    config.close()
    volume = float(configs[5])
    state = configs[1]
    pause = 'True' == configs[2]
    pygame.mixer.music.set_volume(volume)
    no = nowsong = nowsongprint = configs[8]
    logit(configs, no)
    rainbow = rainbow1 = 0
    refreshing = int(configs[6])
    print(datetime.now().strftime("%H:%M:%S"))
    logit(datetime.now().strftime("%A %d. %B %Y"), no)
    tracks = os.listdir('.tracks')
    tracks.sort()
    try:
        pathnamealt = tracks[int(configs[4]) - 1]
    except:
        pathnamealt = tracks[0]
    pathname = path.join('.tracks', pathnamealt)
    trainindex = tracks.index(pathnamealt)
    wywymusic = os.listdir(pathname)
    wywymusic.sort()
    everysong = []
    everycheck = []
    searching = False
    search1 = ''
    for x in os.listdir('.tracks'):
        for y in os.listdir(path.join('.tracks', x)):
            try:
                everycheck.index(y)
            except:
                everysong.append(path.join('.tracks', x, y))
                everycheck.append(y)
    everysong.sort()
    wywydir = path.join(path.dirname(__file__), pathname)
    if state == 'All':
        current = everysong
    else:
        current = wywymusic
    longest = 0
    for x in current:
        if len(x) - 4 > longest:
            longest = len(x) - 4
    logit(no, 'Track: ' + pathname[8:])
    wywyquestion = random.randint(1, len(current)) - 1
    loop = False
    #this one is part of a guardian-first we generate the song and then we turn on loop so we don't get an ERROR for nowsong
    #If this isn't False at the start there will be trackback loop isn't defined
    try:
        bruh = int(configs[3])
        newsong(0, bruh)
    except:
        newsong(0, no)
        logit("Invalid start song - reverted to random start song. (Note, this is not necessarily an error)", no)
    if configs[7] == 'True':
        loop = True
    else:
        loop = False
    logit('setup is done', no)


# Start newsong

setup()

while singing:
    clock.tick(60)

    rainbow += 1
    if rainbow == refreshing:
        rainbow = 0
        if pause == False:
            rainbow1 += 1
            if rainbow1 > len(os.listdir(path.join('.mainfiles', 'animations'))) - 1:
                rainbow1 = 0
        repastetext()

    if pygame.mixer.music.get_busy() != 1 and pause == False:
        newsong(0, no)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            endit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS:
                loudness(0.05, no)
            elif event.key == pygame.K_EQUALS:
                loudness(0.05, no)
            elif event.key == pygame.K_MINUS:
                loudness(-0.05, no)
            elif event.key == pygame.K_v:
                loudness(0, 0.5)
            elif event.key == pygame.K_m:
                loudness(0, 1)
            elif event.key == pygame.K_SEMICOLON:
                searchit('toggle')
            elif event.key == pygame.K_ESCAPE:
                endit()
            elif event.key == pygame.K_i:
                logit(no, info)
            elif event.key == pygame.K_y:
                webbrowser.open_new_tab("https://loader.to/en58/youtube-wav-converter.html")
            elif event.key == pygame.K_g:
                webbrowser.open_new_tab("https://ezgif.com/split")
            elif event.key == pygame.K_r:
                logit(no, '\nRefreshing!\n')
                setup()
            elif event.key == pygame.K_QUOTE:
                for x in range(len(current)):
                    y = current[x][:-4]
                    if state == 'All':
                        y = y[y.find('\\', 8) + 1:]
                    print(str(x + 1) + ' - ' + y)
            elif searching == True:
                if event.key == pygame.K_SEMICOLON:
                    searchit('toggle')
                elif event.key == pygame.K_1:
                    searchit(1)
                elif event.key == pygame.K_2:
                    searchit(2)
                elif event.key == pygame.K_3:
                    searchit(3)
                elif event.key == pygame.K_4:
                    searchit(4)
                elif event.key == pygame.K_5:
                    searchit(5)
                elif event.key == pygame.K_6:
                    searchit(6)
                elif event.key == pygame.K_7:
                    searchit(7)
                elif event.key == pygame.K_8:
                    searchit(8)
                elif event.key == pygame.K_9:
                    searchit(9)
                elif event.key == pygame.K_0:
                    searchit(0)
                else:
                    logit(no, configs[11])
            elif loop == True:
                if event.key == pygame.K_l:
                    switchstate('Loop')
                elif event.key == pygame.K_p:
                    paused()
                elif event.key == pygame.K_RETURN:
                    paused()
                elif event.key == pygame.K_KP_ENTER:
                    paused()
                else:
                    logit(no, configs[12])
            else:
                if event.key == pygame.K_SEMICOLON:
                    searchit('toggle')
                elif event.key == pygame.K_1:
                    newsong(0, int(len(current) / 10 * 1))
                elif event.key == pygame.K_2:
                    newsong(0, int(len(current) / 10 * 2))
                elif event.key == pygame.K_3:
                    newsong(0, int(len(current) / 10 * 3))
                elif event.key == pygame.K_4:
                    newsong(0, int(len(current) / 10 * 4))
                elif event.key == pygame.K_5:
                    newsong(0, int(len(current) / 10 * 5))
                elif event.key == pygame.K_6:
                    newsong(0, int(len(current) / 10 * 6))
                elif event.key == pygame.K_7:
                    newsong(0, int(len(current) / 10 * 7))
                elif event.key == pygame.K_8:
                    newsong(0, int(len(current) / 10 * 8))
                elif event.key == pygame.K_9:
                    newsong(0, int(len(current) / 10 * 9))
                elif event.key == pygame.K_0:
                    newsong(0, 1)
                elif event.key == pygame.K_SPACE:
                    newsong(0, no)
                elif event.key == pygame.K_PAGEDOWN:
                    switchtrack('RIGHT')
                elif event.key == pygame.K_PAGEUP:
                    switchtrack('LEFT')
                elif event.key == pygame.K_w:
                    newsong(1, no)
                elif event.key == pygame.K_s:
                    newsong(-1, no)
                elif event.key == pygame.K_UP:
                    newsong(1, no)
                elif event.key == pygame.K_DOWN:
                    newsong(-1, no)
                elif event.key == pygame.K_p:
                    paused()
                elif event.key == pygame.K_RETURN:
                    paused()
                elif event.key == pygame.K_KP_ENTER:
                    paused()
                elif event.key == pygame.K_l:
                    switchstate('Loop')
                elif event.key == pygame.K_d:
                    switchstate('Default')
                elif event.key == pygame.K_c:
                    switchstate('Chronological')
                elif event.key == pygame.K_a:
                    switchstate('All')
pygame.quit()
