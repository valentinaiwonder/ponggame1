import pygame
import sys
import random
import math

# Inicializar o Pygame
pygame.init()

# Configurações da janela do jogo (16:9)
screen_width = 853
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Definir cores
WHITE = (255, 255, 255)
DARK_PURPLE = (75, 0, 130)  # Roxo mais escuro
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FIRE_COLOR = (255, 69, 0)  # Cor da bola de fogo

# Configurações de velocidade do jogo
clock = pygame.time.Clock()
fps = 30  # Reduzido para diminuir a velocidade

# Configurações das raquetes e bola
paddle_width = 10
paddle_height = 100
paddle_speed = 8  # Reduzi a velocidade das raquetes

ball_size = 20
initial_ball_speed = 6  # Velocidade inicial da bola
ball_speed_x = initial_ball_speed
ball_speed_y = initial_ball_speed
ball_acceleration = 1.02  # Aceleração da bola em cada colisão
max_ball_speed = 12  # Velocidade máxima da bola

# Posições iniciais
player1_x = 50
player1_y = screen_height // 2 - paddle_height // 2

player2_x = screen_width - 50 - paddle_width
player2_y = screen_height // 2 - paddle_height // 2

ball_x = screen_width // 2 - ball_size // 2
ball_y = screen_height // 2 - ball_size // 2

# Pontuação dos jogadores
player1_score = 0
player2_score = 0

# Nomes dos jogadores
player1_name = "Player 1"
player2_name = "Player 2"

# Carregar sons
hit_sound = pygame.mixer.Sound('pong_hit.wav')
score_sound = pygame.mixer.Sound('score_point.wav')
win_sound = pygame.mixer.Sound('game_win.wav')
climax_sound = pygame.mixer.Sound('climax.wav')

# Carregar imagens
galaxy_bg = pygame.image.load('galaxy_background.png').convert_alpha()  # Troquei para PNG
galaxy_bg = pygame.transform.scale(galaxy_bg, (screen_width, screen_height))

ping_pong_table_bg = pygame.image.load('ping_pong_table.jpg').convert()
ping_pong_table_bg = pygame.transform.scale(ping_pong_table_bg, (screen_width, screen_height))


# Função para desenhar o texto na tela
def draw_text(text, font_size, color, surface, position):
    font = pygame.font.Font(None, font_size)
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = position
    surface.blit(textobj, textrect)


# Função para desenhar uma bola de fogo
def draw_fireball(x, y, size):
    # Desenhar a parte interna da bola (núcleo de fogo)
    pygame.draw.circle(screen, FIRE_COLOR, (x + size // 2, y + size // 2), size // 2)

    # Desenhar o rastro de fogo com partículas aleatórias
    for _ in range(15):  # Aumentar o número de partículas para um efeito mais visível
        particle_x = x + random.randint(-size, size)
        particle_y = y + random.randint(-size, size)
        particle_size = random.randint(1, size // 4)
        particle_color = (255, random.randint(50, 150), 0)  # Variantes de laranja
        pygame.draw.circle(screen, particle_color, (particle_x, particle_y), particle_size)


# Função para desenhar um efeito de glitch
def draw_glitch(offset_x, offset_y):
    # Desenha linhas horizontais e verticais que se movem aleatoriamente para criar um efeito de glitch
    for _ in range(20):
        start_pos = (random.randint(0, screen_width), random.randint(0, screen_height))
        end_pos = (start_pos[0] + random.randint(-10, 10), start_pos[1] + random.randint(-10, 10))
        pygame.draw.line(screen, WHITE, (start_pos[0] + offset_x, start_pos[1] + offset_y),
                         (end_pos[0] + offset_x, end_pos[1] + offset_y), random.randint(1, 3))


# Função de tela de início
def start_screen():
    global start_button  # Declarar a variável global
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_x, mouse_y):
                    return  # Iniciar o jogo principal

        # Desenhar a tela de início
        screen.blit(galaxy_bg, (0, 0))  # Desenhar o fundo da galáxia
        draw_text("Pong", 100, WHITE, screen, (screen_width // 2, screen_height // 3))

        # Desenhar botão "Play"
        start_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2 - 25, 100, 50)
        pygame.draw.rect(screen, BLUE, start_button)
        draw_text("Play", 50, WHITE, screen, (screen_width // 2, screen_height // 2))

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(fps)


# Função de tela de entrada dos nomes
def name_input_screen():
    global player1_name, player2_name
    input_box1 = pygame.Rect(screen_width // 4 - 100, screen_height // 2 - 50, 200, 50)
    input_box2 = pygame.Rect(screen_width * 3 // 4 - 100, screen_height // 2 - 50, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color1 = color_inactive
    color2 = color_inactive
    text1 = ''
    text2 = ''
    active1 = False
    active2 = False
    font = pygame.font.Font(None, 74)
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active1 = not active1
                else:
                    active1 = False
                if input_box2.collidepoint(event.pos):
                    active2 = not active2
                else:
                    active2 = False
                color1 = color_active if active1 else color_inactive
                color2 = color_active if active2 else color_inactive
            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_RETURN:
                        player1_name = text1
                        text1 = ''
                        active1 = False
                        color1 = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                if active2:
                    if event.key == pygame.K_RETURN:
                        player2_name = text2
                        text2 = ''
                        active2 = False
                        color2 = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode

        screen.fill(BLACK)
        # Desenhar a tela de entrada dos nomes
        draw_text("Enter Player 1 Name:", 50, WHITE, screen, (screen_width // 4, screen_height // 3 - 50))
        draw_text("Enter Player 2 Name:", 50, WHITE, screen, (screen_width * 3 // 4, screen_height // 3 - 50))

        txt_surface1 = font.render(text1, True, color1)
        screen.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 5))
        pygame.draw.rect(screen, color1, input_box1, 2)

        txt_surface2 = font.render(text2, True, color2)
        screen.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 5))
        pygame.draw.rect(screen, color2, input_box2, 2)

        pygame.display.flip()
        clock.tick(fps)

        if not active1 and not active2 and text1 and text2:
            done = True


# Função de tela de vitória
def victory_screen(winner):
    global restart_button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_x, mouse_y):
                    return  # Reiniciar o jogo

        # Desenhar a tela de vitória com imagem de fundo
        screen.blit(ping_pong_table_bg, (0, 0))
        draw_text(f"{winner} Wins!", 100, WHITE, screen, (screen_width // 2, screen_height // 3))

        # Desenhar botão "Recomeço"
        restart_button = pygame.Rect(screen_width // 2 - 75, screen_height // 2 - 25, 150, 50)  # Ajuste a posição
        pygame.draw.rect(screen, BLUE, restart_button)
        draw_text("Recomeço", 40, WHITE, screen, (screen_width // 2, screen_height // 2))

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(fps)


# Função principal do jogo
def main_game():
    global player1_y, player2_y, ball_x, ball_y, ball_speed_x, ball_speed_y, player1_score, player2_score, climax_triggered
    climax_triggered = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimentar as raquetes com as teclas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1_y > 0:
            player1_y -= paddle_speed
        if keys[pygame.K_s] and player1_y < screen_height - paddle_height:
            player1_y += paddle_speed
        if keys[pygame.K_UP] and player2_y > 0:
            player2_y -= paddle_speed
        if keys[pygame.K_DOWN] and player2_y < screen_height - paddle_height:
            player2_y += paddle_speed

        # Movimentar a bola
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Colisão com as paredes superiores e inferiores
        if ball_y <= 0 or ball_y >= screen_height - ball_size:
            ball_speed_y = -ball_speed_y

        # Colisão com as raquetes
        if (player1_x < ball_x < player1_x + paddle_width and
            player1_y < ball_y < player1_y + paddle_height) or \
                (player2_x < ball_x + ball_size < player2_x + paddle_width and
                 player2_y < ball_y < player2_y + paddle_height):
            ball_speed_x = -ball_speed_x * ball_acceleration
            ball_speed_y *= ball_acceleration
            ball_speed_x = min(ball_speed_x, max_ball_speed)
            ball_speed_y = min(ball_speed_y, max_ball_speed)
            hit_sound.play()

        # Pontuação
        if ball_x <= 0:
            player2_score += 1
            score_sound.play()
            ball_x = screen_width // 2 - ball_size // 2
            ball_y = screen_height // 2 - ball_size // 2
            ball_speed_x = initial_ball_speed  # Bola vai em direção ao Player 2
        if ball_x >= screen_width:
            player1_score += 1
            score_sound.play()
            ball_x = screen_width // 2 - ball_size // 2
            ball_y = screen_height // 2 - ball_size // 2
            ball_speed_x = -initial_ball_speed  # Bola vai em direção ao Player 1

        # Verificar vitória
        if player1_score == 10:
            win_sound.play()
            victory_screen(player1_name)
            player1_score = 0
            player2_score = 0
        if player2_score == 10:
            win_sound.play()
            victory_screen(player2_name)
            player1_score = 0
            player2_score = 0

        # Ativar música de clímax quando um jogador alcançar 7 pontos
        if player1_score >= 7 or player2_score >= 7:
            if not climax_triggered:
                climax_sound.play(-1)  # Tocar som de clímax em loop
                climax_triggered = True
                ball_speed_x = 10
                ball_speed_y = 10
        else:
            climax_sound.stop()
            climax_triggered = False

        # Desenhar fundo do jogo
        screen.blit(ping_pong_table_bg, (0, 0))

        # Desenhar as raquetes
        pygame.draw.rect(screen, WHITE, (player1_x, player1_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, WHITE, (player2_x, player2_y, paddle_width, paddle_height))

        # Desenhar a bola com efeito de fogo
        draw_fireball(ball_x, ball_y, ball_size)

        # Desenhar a pontuação dos jogadores
        draw_text(f"{player1_name}: {player1_score}", 40, DARK_PURPLE, screen, (screen_width // 4, 20))
        draw_text(f"{player2_name}: {player2_score}", 40, DARK_PURPLE, screen, (screen_width * 3 // 4, 20))

        # Desenhar efeitos de glitch se o clímax estiver ativado
        if climax_triggered:
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            draw_glitch(offset_x, offset_y)

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(fps)


# Início do jogo
start_screen()
name_input_screen()
main_game()