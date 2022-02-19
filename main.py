import os, random, re, webbrowser, sys
from os import path
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame, soundfile

from datetime import datetime
# colours. BRITISH
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

pygame.init()
width = 800
height = 800
space = 400
barpoint1x = width - 107
outline_rect = [pygame.Rect(barpoint1x, 5, 100, 15), pygame.Rect(barpoint1x, 25, 100, 15)]
fillingALT = [pygame.Rect(barpoint1x, 5, 100, 15), pygame.Rect(barpoint1x, 25, 100, 15)]
#guardians above
screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
pygame.display.set_icon(pygame.image.load(path.join('.mainfiles', 'icon.jpg')))

singing = True
searching = False
# Default Chronological Loop All
fonds = [pygame.font.SysFont('Verdana', 15), pygame.font.SysFont('Verdana', 30), pygame.font.SysFont('Verdana', 15), '']
#fonds 3 isn't useless, I'm not the most certain on the side panel font size
fondsfr = [fonds[0].render('Volume', False, WHITE), fonds[0].render('Song #', False, WHITE),
           fonds[0].render('Song %', False, WHITE)]
clock = pygame.time.Clock()

def newsong(increment, skipto):
    global nowsong, nowsongprint
    global wywyquestion
    global length, songtotal
    if state != 'Loop' or (state == 'Loop' and skipto != no and searching == True):
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
        nowsongprint = currentprint[wywyquestion]
        if current == everysong:
            length = soundfile.SoundFile(nowsong)
            nowsongprint = nowsong[nowsong.find('\\', 8) + 1: -4]
            pygame.mixer.music.load(nowsong)
        else:
            length = soundfile.SoundFile(path.join(wywydir, nowsong))
        songtotal = length.frames / length.samplerate
        pygame.display.set_caption(nowsongprint)
        logit(no, 'Now playing ' + nowsongprint)
    if current != everysong:
        pygame.mixer.music.load(path.join(wywydir, nowsong))
    pygame.mixer.music.play(loops=0)
    if pause == True:
        pygame.mixer.music.pause()
    repastetext()


def switchtrack(direction):
    global wywymusic, wywymusicprint, current, currentprint
    global pathnamealt, pathname, tracksend
    global trainindex
    global wywydir
    global longest
    if direction == 'All':
        current = everysong
        currentprint = everyprint
        longest = 0
        for x in everysong:
            if len(x) - 4 > longest:
                longest = len(x) - 4
        tracksend = fonds[2].render('All', False, BLACK)
    else:
        if direction == 'LEFT':
            trainindex += 1
        if direction == 'RIGHT':
            trainindex -= 1
        if trainindex > len(tracks) - 1:
            trainindex = 0
        elif trainindex < 0:
            trainindex = len(tracks) - 1
        pathnamealt = tracks[trainindex]
        pathname = path.join('.tracks', pathnamealt)
        logit(no, 'Track: ' + pathname[8:])
        wywymusic = os.listdir(pathname)
        wywymusicprint = []
        for x in wywymusic:
            wywymusicprint.append(x[:-4])
        current = wywymusic
        currentprint = wywymusicprint
        wywydir = path.join(path.dirname(__file__), pathname)
        logit(wywydir + ' ' + pathname, no)
        tracksend = fonds[2].render(pathnamealt, False, BLACK)
        longest = 0
        for x in wywymusic:
            if len(x) - 4 > longest:
                longest = len(x) - 4
    newsong(0, no)

def repastetext():
    screen.blit(rainbowbk.image, rainbowbk, rainbowbk.rect)

    if width / longest < height / len(current):
        fonds[3] = pygame.font.SysFont('Verdana', int(width * 1.6 / longest))
    else:
        fonds[3] = pygame.font.SysFont('Verdana', int(height / 3 * 4 / len(current)))

    for x in range(len(current)):
        sending = fonds[3].render(currentprint[x], False, WHITE)
        screen.blit(sending, (0, x * (int(height / len(current)))))

    screen.blit(fondsfr[2], (width - 170, 45))
    pygame.draw.rect(screen, BLACK, pygame.Rect(barpoint1x, 45, 100, 15))
    pygame.draw.rect(screen, WHITE, pygame.Rect(barpoint1x, 45, 100, 15), 2)
    pygame.draw.rect(screen, WHITE, pygame.Rect(barpoint1x, 45, int(pygame.mixer.music.get_pos() / 1000 / songtotal * 100), 15))

    trackingnowsong = int((current.index(nowsong) + 1) / len(current) * 100)

    filling = [pygame.Rect(barpoint1x, 5, volume * 100, 15),
               pygame.Rect(barpoint1x, 25, trackingnowsong, 15)]

    screen.blit(fondsfr[0], (width - 170, 5))
    pygame.draw.rect(screen, BLACK, fillingALT[0])
    if volume == 1:
        pygame.draw.rect(screen, GREEN, filling[0])
    elif volume == 0.5:
        pygame.draw.rect(screen, YELLOW, filling[0])
    else:
        pygame.draw.rect(screen, WHITE, filling[0])

    if volume <= 0:
        pygame.draw.rect(screen, RED, outline_rect[0], 2)
    else:
        pygame.draw.rect(screen, WHITE, outline_rect[0], 2)
    # space so i don't go crawy
    screen.blit(fondsfr[1], (width - 170, 25))
    pygame.draw.rect(screen, BLACK, fillingALT[1])
    pygame.draw.rect(screen, WHITE, filling[1])
    pygame.draw.rect(screen, WHITE, outline_rect[1], 2)
    screen.blit(tracksend, (width - 170, 65))
    screen.blit(statesend, (width - 170, 85))
    screen.blit(pausesend, (width - 170, 105))
    if searching == True:
        searchsend = fonds[2].render(search1, False, BLACK)
        screen.blit(searchsend, (width - 170, 145))
    if configs[7] == '24hrs':
        screen.blit(fonds[2].render(datetime.now().strftime("%H:%M"), False, BLACK), (width - 170, 125))
    else:
        screen.blit(fonds[2].render(datetime.now().strftime("%I:%M %p"), False, BLACK), (width - 170, 125))

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
    global pause, pausesend
    if pause == True:
        pause = False
        pygame.mixer.music.unpause()
        if searching == False:
            logit(no, 'Playing')
        pausesend = fonds[2].render('Playing', False, BLACK)
    else:
        pause = True
        pygame.mixer.music.pause()
        if searching == False:
            logit(no, 'Paused')
        pausesend = fonds[2].render('Paused', False, BLACK)
    repastetext()


class rainbows(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def switchstate(newstate):
    global state, current, currentprint, wywymusic, wywymusicprint, statemsg, statesend
    if newstate == 'Loop':
        if state == 'Loop':
            state = 'Default'
            statemsg = state
            statesend = fonds[2].render(statemsg, False, BLACK)
            print('Loop toggled, falling back to Default state.')
        else:
            state = 'Loop'
            statemsg = state
            statesend = fonds[2].render(statemsg, False, BLACK)
            print('Started looping', nowsongprint)
        repastetext()
    else:
        state = newstate
        statemsg = state
        statesend = fonds[2].render(statemsg, False, BLACK)
        print('Playing in', newstate, 'order')
        repastetext()
    logit(state + ' order', no)


def searchit(what):
    global searching, search1, current, statemsg, statesend
    if what == 'toggle':
        if searching == False:
            searching = True
            statemsg += '(Searching)'
            statesend = fonds[2].render(statemsg, False, BLACK)
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
            statemsg = statemsg[:-11]
            statesend = fonds[2].render(statemsg, False, BLACK)
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
    global wywymusic, wywymusicprint, wywydir, wywyquestion, everysong, everyprint, current, currentprint
    global volume, pause, pausesend, info
    global allrainbow, refreshing
    global rainbow, rainbow1, allrainbow
    global no, nowsong, nowsongprint, state, statemsg, statesend, configs, search1, searching
    allrainbow = os.listdir(path.join('.mainfiles', 'animations'))
    allrainbow.sort()
    global rainbowbk
    rainbow = rainbow1 = 0
    rainbowbk = rainbows(path.join('.mainfiles', 'animations', allrainbow[rainbow1]), [0, 0])
    # another one bc rainbowbk not defined blah blah
    info = open(path.join('.mainfiles', 'readwywy.txt'), "r")
    info.seek(0)
    info = info.read()
    config = open(path.join('.mainfiles', 'config.txt'), "r")
    configs = re.findall('= ([^/]+?)\n', config.read())
    config.close()
    volume = float(configs[5])
    state = configs[1]
    statemsg = state
    statesend = fonds[2].render(statemsg, False, BLACK)
    pause = 'True' == configs[2]
    if pause == True:
        pausesend = fonds[2].render('Playing', False, BLACK)
    else:
        pausesend = fonds[2].render('Playing', False, BLACK)
    pygame.mixer.music.set_volume(volume)
    no = nowsong = nowsongprint = bruh = configs[8]
    logit(configs, no)
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
    wywymusicprint = []
    for x in wywymusic:
        wywymusicprint.append(x[:-4])
    everysong = []
    everycheck = []
    everyprint = []
    searching = False
    search1 = ''
    for x in os.listdir('.tracks'):
        for y in os.listdir(path.join('.tracks', x)):
            try:
                everycheck.index(y)
            except:
                everysong.append(path.join('.tracks', x, y))
                everyprint.append(y[y.find('\\', 8) + 1: -4])
                everycheck.append(y)
    everysong.sort()
    wywydir = path.join(path.dirname(__file__), pathname)
    currentprint = []
    longest = 0
    global tracksend
    if configs[4] == 'All':
        current = everysong
        currentprint = everyprint
        tracksend = fonds[2].render('All', False, BLACK)
        for x in current:
            if len(x) - 4 > longest:
                longest = len(x) - 4
        try:
            bruh = int(configs[3])
            newsong(0, bruh)
        except:
            newsong(0, no)
            logit("Invalid start song - reverted to random start song. (Note, this is not necessarily an error)", no)
    else:
        switchtrack('RESET')
    logit('setup is done', no)


# Start newsong

setup()

while singing:
    clock.tick(24)
    rainbow += 1
    if rainbow == refreshing:
        rainbow = 0
        #check dimensions later
        if width != screen.get_width() or height != screen.get_height():
            width = screen.get_width()
            space = width / 2
            height = screen.get_height()
            barpoint1x = width - 107
            outline_rect = [pygame.Rect(barpoint1x, 5, 100, 15), pygame.Rect(barpoint1x, 25, 100, 15)]
            fillingALT = [pygame.Rect(barpoint1x, 5, 100, 15), pygame.Rect(barpoint1x, 25, 100, 15)]
        if pause == False:
            rainbow1 += 1
            if rainbow1 > len(os.listdir(path.join('.mainfiles', 'animations'))) - 1:
                rainbow1 = 0
            rainbowbk = rainbows(path.join('.mainfiles', 'animations', allrainbow[rainbow1]), [0, 0])
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
                    if current == everysong:
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
            elif state == 'Loop':
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
                    if current == everysong:
                        switchtrack('RESET')
                    else:
                        switchtrack('All')
pygame.quit()
