import pygame
import sys
import random
from time import sleep

padWidth = 480  # 화면 가로크기
padHeight = 640 # 화면 세로크기
botImage = ['./img/bot1.png', './img/bot2.png', './img/bot3.png', './img/bot4.png', './img/bot5.png', './img/bot6.png'] # 봇 이미지들

highScore = 0  # 하이스코어 변수
shotCount = 0 # 점수 변수
lives = 3  # 목숨 개수
paused = False  # 게임 일시정지 상태 변수

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def initGame():
    global gamePad, clock, background, fighter, missile, explosion, tiny5_font, fighter_boom, heart, highScore, lives
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('Shooting Game')                # 게임 이름
    background = pygame.image.load('./img/background.png')     # 배경 그림
    fighter = pygame.image.load('./img/fighter.png')           # 전투기 그림
    fighter_boom = pygame.image.load('./img/fighter_boom.png') # 전투기 폭발 그림
    missile = pygame.image.load('./img/missile.png')           # 미사일 그림
    explosion = pygame.image.load('./img/explosion.png')       # 폭발 그림
    heart = pygame.image.load('./img/heart.png')               # 목숨 하트 그림
    tiny5_font = pygame.font.Font('./fonts/Tiny5.ttf', 20)     # Tiny5 폰트
    clock = pygame.time.Clock()
    lives = 3  # 목숨 개수 초기화
    
    # 게임 아이콘 설정
    icon = pygame.image.load('./img/icon.bmp')
    pygame.display.set_icon(icon)

# 점수 표기
def writeScore(count):
    global gamePad
    score_font = pygame.font.Font('./fonts/Tiny5.ttf', 30)  
    text = score_font.render('SCORE: ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

# 최고점수 표기
def writeHighScore(highScore):
    global gamePad, padWidth
    score_font = pygame.font.Font('./fonts/Tiny5.ttf', 30)
    text = score_font.render('HIGH SCORE: ' + str(highScore), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.topright = (padWidth - 10, 0) 
    gamePad.blit(text, text_rect)

# 목숨 표기
def drawLives(lives):
    global gamePad, heart
    for i in range(lives):
        drawObject(heart, 8 + (i * 30), padHeight - 50)

# 메시지 표기(표기내용, 크기, 색깔, x좌표, y좌표)
def writeMessage(text, size, color, center_x, center_y):
    global gamePad, tiny5_font
    textfont = pygame.font.Font('./fonts/Tiny5.ttf', size)
    message = textfont.render(text, True, color)
    textpos = message.get_rect()
    textpos.center = (center_x, center_y)
    gamePad.blit(message, textpos)
    pygame.display.update()

def showRetryPopup(): # 다시시작?
    global gamePad, tiny5_font
    textfont = pygame.font.Font('./fonts/Tiny5.ttf', 40)
    message = textfont.render('RETRY?', True, (255, 255, 255))
    
    def render_text(text, color, alpha):
        text_surface = textfont.render(text, True, color)
        text_surface.set_alpha(alpha)
        return text_surface

    selected_option = 'YES'  # 초기 선택은 YES로 설정
    while True:
        gamePad.fill((0, 0, 0))
        gamePad.blit(message, (padWidth / 2 - 60, padHeight / 2 - 60))

        if selected_option == 'YES':
            yes_surface = render_text('YES', (0, 255, 0), 255)
            no_surface = render_text('NO', (255, 0, 0), 128)
        else:
            yes_surface = render_text('YES', (0, 255, 0), 128)
            no_surface = render_text('NO', (255, 0, 0), 255)
        
        gamePad.blit(yes_surface, (padWidth / 2 - 60, padHeight / 2))
        gamePad.blit(no_surface, (padWidth / 2 + 20, padHeight / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_option = 'YES'
                elif event.key == pygame.K_RIGHT:
                    selected_option = 'NO'
                elif event.key == pygame.K_RETURN: # 엔터키를 눌러 선택
                    return selected_option  # 선택된 옵션 반환

def crash(): # 봇에 맞거나 봇이 바닥에 닿았을 때
    global gamePad, x, y, shotCount, highScore, lives, bot, botX, botY, botSpeed
    
    # 목숨 감소
    lives -= 1

    ###### 실습할 부분 ######
    # lives가 줄어들고 0이 되면 게임오버하는 동작
    
    # lives가 남아 있을 경우 봇을 초기화하는 동작만 실행
    if lives == lives: # 조건문을 통해 분기 결정 실습
        # 봇 초기화
        bot = pygame.image.load(random.choice(botImage))
        botSize = bot.get_rect().size
        botWidth = botSize[0]
        botX = random.randrange(0, padWidth - botWidth)
        botY = 0
        botSpeed = 4 # 봇에 맞았을 경우 속도 설정
    # lives가 없을 경우 전투기 폭발 및 게임오버 메시지 표출
    else:
        # 전투기 폭발 후 아래로 떨어지기
        for i in range(20):
            drawObject(background, 0, 0)
            y += 5
            drawObject(fighter_boom, x, y)
            pygame.display.update()
            sleep(0.04)

        # 0.8초 대기 후 게임 오버 메시지
        sleep(0.8)
        writeMessage('GAME OVER...', 80, (255, 0, 0), padWidth / 2, padHeight / 2)

        # 현재 점수가 최고점수보다 높으면 업데이트
        if shotCount > highScore:
            highScore = shotCount

        # 1초 대기 후 YOUR SCORE 메시지
        sleep(1)
        writeMessage('YOUR SCORE: ' + str(shotCount), 50, (255, 255, 255), padWidth / 2, padHeight / 2 + 60)

        # 2초 대기 후 RETRY 메시지
        sleep(2)
        if showRetryPopup() == 'YES':
            initGame()  # 게임 환경 초기화
            runGame()
        else:
            gamePad.fill((0, 0, 0))
            writeMessage('HIGH SCORE: ' + str(highScore), 50, (255, 0, 0), padWidth / 2, padHeight / 2)
            pygame.display.update()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        pygame.quit()
                        sys.exit()
    ######/ 실습할 부분 ######

def runGame():
    global gamePad, clock, background, fighter, missile, explosion, x, y, shotCount, lives, bot, botX, botY, botSpeed, paused

    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    x = padWidth * 0.45
    y = padHeight * 0.85
    fighterX = 0

    missileXY = []

    bot = pygame.image.load(random.choice(botImage))
    botSize = bot.get_rect().size
    botWidth = botSize[0]
    botHeight = botSize[1]

    botX = random.randrange(0, padWidth - botWidth)
    botY = 0
    botSpeed = 3 # 봇이 내려오는 기본 속도

    isShot = False
    shotCount = 0

    # 게임 시작 시 3, 2, 1 카운트다운
    for count in range(3, 0, -1):
        drawObject(background, 0, 0)
        writeMessage(str(count), 100, (255, 255, 255), padWidth / 2, padHeight / 2)
        sleep(1)
    
    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:  # 게임 프로그램 종료
                pygame.quit()
                sys.exit()
                
            ###### 실습할 부분 ######

            # 왼쪽 오른쪽 방향키로 이동, 스페이스 키로 미사일 발사,
            # + esc키로 게임 일시정지 기능 구현

            ######/ 실습할 부분 ######

        if not paused: 
            drawObject(background, 0, 0)    # 배경 화면 그리기

            x += fighterX
            if x < 0:
                x = 0
            elif x > padWidth - fighterWidth:
                x = padWidth - fighterWidth

            drawObject(fighter, x, y)  # 전투기 그리기

            if len(missileXY) != 0:
                for i, bxy in enumerate(missileXY):
                    bxy[1] -= 10
                    missileXY[i][1] = bxy[1]

                    if bxy[1] <= 0:
                        try:
                            missileXY.remove(bxy)
                        except:
                            pass

            if len(missileXY) != 0:
                for bx, by in missileXY:
                    drawObject(missile, bx-8, by) # 미사일 그리기

            botY += botSpeed

            if botY > padHeight:
                crash()  # 바닥에 닿으면 생명 감소
                bot = pygame.image.load(random.choice(botImage))
                botSize = bot.get_rect().size
                botWidth = botSize[0]
                botHeight = botSize[1]
                botX = random.randrange(0, padWidth - botWidth)
                botY = 0
                botSpeed += 0.2
                if botSpeed >= 6:
                    botSpeed = 6 # 최고 속도 설정

            if y < botY + botHeight:
                if (botX > x and botX < x + fighterWidth) or \
                   (botX + botWidth > x and botX + botWidth < x + fighterWidth):
                    crash()

            drawObject(bot, botX, botY)  # 봇 그리기

            if len(missileXY) != 0:
                for i, bxy in enumerate(missileXY):
                    if bxy[1] < botY:
                        if bxy[0] > botX and bxy[0] < botX + botWidth:
                            missileXY.remove(bxy)
                            isShot = True
                            shotCount += 100 # 획득 점수 설정

            if isShot:
                drawObject(explosion, botX, botY)
                bot = pygame.image.load(random.choice(botImage))
                botSize = bot.get_rect().size
                botWidth = botSize[0]
                botHeight = botSize[1]
                botX = random.randrange(0, padWidth - botWidth)
                botY = 0
                isShot = False

                botSpeed += 0.2
                if botSpeed >= 6:
                    botSpeed = 6 # 최고 속도 설정

            writeScore(shotCount)  # 점수 표시
            writeHighScore(highScore)  # 최고 점수 표시
            drawLives(lives)  # 남은 목숨 표시

        else: # 일시정지
            writeMessage('PAUSED', 100, (255, 255, 255), padWidth / 2, padHeight / 2)

        pygame.display.update()
        clock.tick(70) # 높을수록 속도 빨라짐

initGame()
runGame()
