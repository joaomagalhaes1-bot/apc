import pygame
import pickle
from sys import exit

pygame.init()
pygame.mixer.init()

tela = pygame.display.set_mode((800, 500))
relogio = pygame.time.Clock()
pygame.display.set_caption('PyngPong')
FPS = 60

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

LARGURA_RAQUETE, ALTURA_RAQUETE = 10, 100
VELOCIDADE_RAQUETE = 6
TAMANHO_BOLA = 16
VELOCIDADE_BOLA_X = 7
VELOCIDADE_BOLA_Y = 8

fonte = pygame.font.SysFont(None, 48)
fonte_pequena = pygame.font.SysFont(None, 28)

raquete_esquerda = pygame.Rect(20, (500 - ALTURA_RAQUETE)//2, LARGURA_RAQUETE, ALTURA_RAQUETE)
raquete_direita = pygame.Rect(800 - 20 - LARGURA_RAQUETE, (500 - ALTURA_RAQUETE)//2, LARGURA_RAQUETE, ALTURA_RAQUETE)
bola = pygame.Rect((800 - TAMANHO_BOLA)//2, (500 - TAMANHO_BOLA)//2, TAMANHO_BOLA, TAMANHO_BOLA)

velocidade_bola_x = VELOCIDADE_BOLA_X
velocidade_bola_y = VELOCIDADE_BOLA_Y

placar_esquerda = 0
placar_direita = 0
recorde = 0

som_toque = pygame.mixer.Sound("sons/bounce.mp3")
som_ponto = pygame.mixer.Sound("sons/point.mp3")
som_ponto.set_volume(0.5)

def salvar_recorde(recorde):
    with open("recorde.pkl", "wb") as arquivo:
        pickle.dump(recorde, arquivo)

def carregar_recorde():
    try:
        with open("recorde.pkl", "rb") as arquivo:
            return pickle.load(arquivo)
    except FileNotFoundError:
        return 0

recorde = carregar_recorde()

def reiniciar_bola(direcao=1):
    global bola, velocidade_bola_x, velocidade_bola_y
    bola.x = (800 - TAMANHO_BOLA)//2
    bola.y = (500 - TAMANHO_BOLA)//2
    velocidade_bola_x = VELOCIDADE_BOLA_X * direcao
    velocidade_bola_y = VELOCIDADE_BOLA_Y if pygame.time.get_ticks() % 2 == 0 else -VELOCIDADE_BOLA_Y

jogando = True
while jogando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_w] and raquete_esquerda.top > 0:
        raquete_esquerda.y -= VELOCIDADE_RAQUETE
    if teclas[pygame.K_s] and raquete_esquerda.bottom < 500:
        raquete_esquerda.y += VELOCIDADE_RAQUETE
    if teclas[pygame.K_UP] and raquete_direita.top > 0:
        raquete_direita.y -= VELOCIDADE_RAQUETE
    if teclas[pygame.K_DOWN] and raquete_direita.bottom < 500:
        raquete_direita.y += VELOCIDADE_RAQUETE
    if teclas[pygame.K_ESCAPE]:
        jogando = False

    bola.x += velocidade_bola_x
    bola.y += velocidade_bola_y

    if bola.top <= 0 or bola.bottom >= 500:
        velocidade_bola_y = -velocidade_bola_y

    if bola.colliderect(raquete_esquerda):
        bola.left = raquete_esquerda.right
        velocidade_bola_x = -velocidade_bola_x
        offset = (bola.centery - raquete_esquerda.centery) / (ALTURA_RAQUETE / 2)
        velocidade_bola_y = VELOCIDADE_BOLA_Y * offset
        som_toque.play()

    if bola.colliderect(raquete_direita):
        bola.right = raquete_direita.left
        velocidade_bola_x = -velocidade_bola_x
        offset = (bola.centery - raquete_direita.centery) / (ALTURA_RAQUETE / 2)
        velocidade_bola_y = VELOCIDADE_BOLA_Y * offset
        som_toque.play()

    if bola.left <= 0:
        placar_direita += 1
        reiniciar_bola(direcao=-1)
        som_ponto.play()
    if bola.right >= 800:
        placar_esquerda += 1
        reiniciar_bola(direcao=1)
        som_ponto.play()

    maior_atual = max(placar_esquerda, placar_direita)
    if maior_atual > recorde:
        recorde = maior_atual
        salvar_recorde(recorde)

    tela.fill(PRETO)

    for y in range(0, 500, 10):
        pygame.draw.rect(tela, BRANCO, (400 - 2, y, 4, 4))

    for i in range(0, ALTURA_RAQUETE, 4):
        pygame.draw.rect(tela, BRANCO, (raquete_esquerda.x, raquete_esquerda.y + i, LARGURA_RAQUETE, 4))
        pygame.draw.rect(tela, BRANCO, (raquete_direita.x, raquete_direita.y + i, LARGURA_RAQUETE, 4))

    for i in range(0, TAMANHO_BOLA, 4):
        for j in range(0, TAMANHO_BOLA, 4):
            pygame.draw.rect(tela, BRANCO, (bola.x + i, bola.y + j, 4, 4))

    texto_placar = fonte.render(f"{placar_esquerda}   {placar_direita}", True, BRANCO)
    tela.blit(texto_placar, ((800 - texto_placar.get_width())//2, 10))

    texto_recorde = fonte_pequena.render(f"Recorde: {recorde}", True, BRANCO)
    tela.blit(texto_recorde, (10, 10))

    instrucoes = fonte_pequena.render('Esc - Sair', False, BRANCO)
    tela.blit(instrucoes, ((800 - instrucoes.get_width())//2, 470))

    pygame.display.flip()
    relogio.tick(FPS)

pygame.quit()
exit()
