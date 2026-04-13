import pygame
import random
import math
import sys

pygame.init()

# =========================
# CONFIGURAÇÕES GERAIS
# =========================
LARGURA = 1000
ALTURA = 650
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Space Galaxy")

RELOGIO = pygame.time.Clock()
FPS = 60

META_ESTRELAS = 15  # condição de vitória

# Cores
PRETO = (10, 10, 20)
BRANCO = (255, 255, 255)
AZUL = (70, 140, 255)
AZUL_CLARO = (120, 200, 255)
VERMELHO = (220, 70, 70)
AMARELO = (255, 220, 70)
CINZA = (130, 130, 130)
CINZA_ESCURO = (80, 80, 80)
ROXO = (170, 90, 220)
VERDE = (80, 220, 120)

fonte = pygame.font.SysFont("arial", 30)
fonte_pequena = pygame.font.SysFont("arial", 20)

# =========================
# FUNÇÕES AUXILIARES
# =========================
def desenhar_texto(texto, fnt, cor, x, y):
    img = fnt.render(texto, True, cor)
    TELA.blit(img, (x, y))

def criar_estrelas_fundo(qtd=90):
    estrelas = []
    for _ in range(qtd):
        estrelas.append([
            random.randint(0, LARGURA),
            random.randint(0, ALTURA),
            random.randint(1, 3)
        ])
    return estrelas

def desenhar_fundo(estrelas):
    TELA.fill(PRETO)
    for e in estrelas:
        pygame.draw.circle(TELA, BRANCO, (int(e[0]), int(e[1])), e[2])

def atualizar_fundo(estrelas, velocidade=2):
    for e in estrelas:
        e[1] += velocidade
        if e[1] > ALTURA:
            e[0] = random.randint(0, LARGURA)
            e[1] = random.randint(-50, -10)

def colisao_precisa(obj1, obj2):
    offset_x = obj2.rect.left - obj1.rect.left
    offset_y = obj2.rect.top - obj1.rect.top
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

def criar_superficie_nave():
    surf = pygame.Surface((80, 100), pygame.SRCALPHA)

    pygame.draw.polygon(
        surf,
        AZUL,
        [(40, 0), (70, 70), (55, 90), (25, 90), (10, 70)]
    )

    pygame.draw.polygon(
        surf,
        AZUL_CLARO,
        [(40, 15), (58, 65), (48, 82), (32, 82), (22, 65)]
    )

    pygame.draw.ellipse(surf, BRANCO, (28, 30, 24, 18))
    pygame.draw.polygon(surf, VERMELHO, [(10, 70), (0, 92), (24, 85)])
    pygame.draw.polygon(surf, VERMELHO, [(70, 70), (80, 92), (56, 85)])
    pygame.draw.polygon(surf, AMARELO, [(33, 90), (40, 100), (47, 90)])

    return surf

def criar_superficie_asteroide():
    surf = pygame.Surface((70, 70), pygame.SRCALPHA)
    pygame.draw.circle(surf, CINZA, (35, 35), 28)
    pygame.draw.circle(surf, CINZA_ESCURO, (24, 26), 7)
    pygame.draw.circle(surf, CINZA_ESCURO, (45, 22), 5)
    pygame.draw.circle(surf, CINZA_ESCURO, (42, 46), 8)
    pygame.draw.circle(surf, CINZA_ESCURO, (22, 48), 4)
    return surf

def criar_superficie_estrela():
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pontos = [
        (20, 0), (24, 13), (39, 14), (27, 22), (31, 38),
        (20, 29), (9, 38), (13, 22), (1, 14), (16, 13)
    ]
    pygame.draw.polygon(surf, AMARELO, pontos)
    return surf

def criar_superficie_bonus():
    surf = pygame.Surface((38, 38), pygame.SRCALPHA)
    pygame.draw.circle(surf, ROXO, (19, 19), 15)
    pygame.draw.circle(surf, BRANCO, (19, 19), 6)
    return surf

# =========================
# CLASSES
# =========================
class Nave:
    def __init__(self):
        self.x = LARGURA // 2
        self.y = ALTURA - 130

        self.imagem_original = criar_superficie_nave()

        self.angulo = 0
        self.escala = 1.0
        self.velocidade = 6

        self.tempo_bonus_reducao = 0
        self.escala_reduzida = 0.65

        self.imagem_atual = None
        self.rect = None
        self.mask = None
        self.atualizar_transformacao()

    def atualizar_transformacao(self):
        imagem = self.imagem_original

        largura = int(imagem.get_width() * self.escala)
        altura = int(imagem.get_height() * self.escala)
        imagem = pygame.transform.smoothscale(imagem, (largura, altura))

        imagem = pygame.transform.rotate(imagem, self.angulo)

        self.imagem_atual = imagem
        self.rect = self.imagem_atual.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.imagem_atual)

    def ativar_bonus(self):
        self.escala = self.escala_reduzida
        self.tempo_bonus_reducao = FPS * 2

    def atualizar(self, teclas):
        movendo = False

        # TRANSLAÇÃO
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.velocidade
            self.angulo = 18
            movendo = True

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.velocidade
            self.angulo = -18
            movendo = True

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.y -= self.velocidade
            movendo = True

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.y += self.velocidade
            movendo = True

        if not movendo:
            self.angulo = 0

        if self.x < 60:
            self.x = 60
        if self.x > LARGURA - 60:
            self.x = LARGURA - 60
        if self.y < 60:
            self.y = 60
        if self.y > ALTURA - 60:
            self.y = ALTURA - 60

        if self.tempo_bonus_reducao > 0:
            self.tempo_bonus_reducao -= 1
        else:
            self.escala = 1.0

        self.atualizar_transformacao()

    def desenhar(self, tela):
        tela.blit(self.imagem_atual, self.rect)


class NaveReflexo:
    def __init__(self, nave_principal):
        self.nave_principal = nave_principal

    def desenhar(self, tela):
        nave = self.nave_principal

        imagem = nave.imagem_original.copy()
        imagem = pygame.transform.flip(imagem, True, False)

        largura = int(imagem.get_width() * nave.escala)
        altura = int(imagem.get_height() * nave.escala)
        imagem = pygame.transform.smoothscale(imagem, (largura, altura))

        imagem = pygame.transform.rotate(imagem, -nave.angulo)
        imagem.set_alpha(110)

        x_reflexo = LARGURA - nave.x
        y_reflexo = nave.y

        rect = imagem.get_rect(center=(x_reflexo, y_reflexo))
        tela.blit(imagem, rect)


class Asteroide:
    def __init__(self):
        self.imagem_base = criar_superficie_asteroide()
        self.x = random.randint(70, LARGURA - 70)
        self.y = random.randint(-700, -60)
        self.velocidade = random.randint(4, 8)
        self.angulo = random.randint(0, 359)
        self.rotacao_vel = random.choice([-4, -3, -2, 2, 3, 4])

        self.imagem_atual = None
        self.rect = None
        self.mask = None
        self.atualizar_transformacao()

    def atualizar_transformacao(self):
        self.imagem_atual = pygame.transform.rotate(self.imagem_base, self.angulo)
        self.rect = self.imagem_atual.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.imagem_atual)

    def atualizar(self):
        self.y += self.velocidade
        self.angulo = (self.angulo + self.rotacao_vel) % 360

        if self.y > ALTURA + 80:
            self.x = random.randint(70, LARGURA - 70)
            self.y = random.randint(-500, -80)
            self.velocidade = random.randint(4, 8)

        self.atualizar_transformacao()

    def desenhar(self, tela):
        tela.blit(self.imagem_atual, self.rect)


class EstrelaColetavel:
    def __init__(self):
        self.imagem_base = criar_superficie_estrela()
        self.x = random.randint(70, LARGURA - 70)
        self.y = random.randint(-900, -100)
        self.velocidade = 5
        self.tempo = random.uniform(0, 2 * math.pi)

        self.imagem_atual = self.imagem_base
        self.rect = self.imagem_atual.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.imagem_atual)

    def atualizar(self):
        self.y += self.velocidade
        self.tempo += 0.05
        self.x += math.sin(self.tempo) * 1.5

        if self.y > ALTURA + 50:
            self.reposicionar()

        self.rect = self.imagem_atual.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.imagem_atual)

    def reposicionar(self):
        self.x = random.randint(70, LARGURA - 70)
        self.y = random.randint(-700, -100)

    def desenhar(self, tela):
        tela.blit(self.imagem_atual, self.rect)


class BonusReducao:
    def __init__(self):
        self.imagem_base = criar_superficie_bonus()
        self.x = random.randint(70, LARGURA - 70)
        self.y = random.randint(-1200, -300)
        self.velocidade = 4
        self.tempo = 0

        self.imagem_atual = None
        self.rect = None
        self.mask = None
        self.atualizar_transformacao()

    def atualizar_transformacao(self):
        fator = 1.0 + 0.20 * math.sin(self.tempo)
        largura = int(self.imagem_base.get_width() * fator)
        altura = int(self.imagem_base.get_height() * fator)

        self.imagem_atual = pygame.transform.smoothscale(
            self.imagem_base,
            (largura, altura)
        )
        self.rect = self.imagem_atual.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.imagem_atual)

    def atualizar(self):
        self.y += self.velocidade
        self.tempo += 0.08

        if self.y > ALTURA + 50:
            self.reposicionar()

        self.atualizar_transformacao()

    def reposicionar(self):
        self.x = random.randint(70, LARGURA - 70)
        self.y = random.randint(-1000, -300)

    def desenhar(self, tela):
        tela.blit(self.imagem_atual, self.rect)

# =========================
# TELAS
# =========================
def tela_inicio(estrelas_fundo):
    while True:
        RELOGIO.tick(FPS)
        atualizar_fundo(estrelas_fundo, 1)
        desenhar_fundo(estrelas_fundo)

        desenhar_texto("SPACE GALAXY", fonte, BRANCO, 395, 120)
        desenhar_texto("Setas ou WASD para mover", fonte_pequena, BRANCO, 390, 220)
        desenhar_texto("A nave-reflexo espelha seus movimentos", fonte_pequena, BRANCO, 330, 255)
        desenhar_texto("Colete estrelas e desvie dos asteroides", fonte_pequena, BRANCO, 330, 290)
        desenhar_texto("O bônus roxo DIMINUI a nave", fonte_pequena, BRANCO, 365, 325)
        desenhar_texto(f"Vitória: coletar {META_ESTRELAS} estrelas", fonte_pequena, VERDE, 380, 360)
        desenhar_texto("ENTER para começar", fonte_pequena, VERDE, 420, 400)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return

def tela_final(estrelas_fundo, venceu, pontuacao, coletadas):
    while True:
        RELOGIO.tick(FPS)
        atualizar_fundo(estrelas_fundo, 1)
        desenhar_fundo(estrelas_fundo)

        if venceu:
            desenhar_texto("VOCÊ VENCEU!", fonte, VERDE, 395, 170)
        else:
            desenhar_texto("GAME OVER", fonte, VERMELHO, 410, 170)

        desenhar_texto(f"Pontuação: {pontuacao}", fonte_pequena, BRANCO, 435, 250)
        desenhar_texto(f"Estrelas coletadas: {coletadas}/{META_ESTRELAS}", fonte_pequena, BRANCO, 385, 285)
        desenhar_texto("ENTER para jogar novamente", fonte_pequena, VERDE, 375, 350)
        desenhar_texto("ESC para sair", fonte_pequena, BRANCO, 445, 385)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# =========================
# LOOP DO JOGO
# =========================
def jogar():
    estrelas_fundo = criar_estrelas_fundo()

    nave = Nave()
    nave_reflexo = NaveReflexo(nave)

    asteroides = [Asteroide() for _ in range(6)]
    estrela = EstrelaColetavel()
    bonus = BonusReducao()

    pontuacao = 0
    coletadas = 0
    tempo_score = 0
    venceu = False

    rodando = True
    while rodando:
        RELOGIO.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()

        atualizar_fundo(estrelas_fundo, 2)
        nave.atualizar(teclas)

        for a in asteroides:
            a.atualizar()
            if colisao_precisa(nave, a):
                rodando = False
                venceu = False

        estrela.atualizar()
        if colisao_precisa(nave, estrela):
            coletadas += 1
            pontuacao += 10
            estrela.reposicionar()

            if coletadas >= META_ESTRELAS:
                venceu = True
                rodando = False

        bonus.atualizar()
        if colisao_precisa(nave, bonus):
            nave.ativar_bonus()
            pontuacao += 20
            bonus.reposicionar()

        tempo_score += 1
        if tempo_score >= FPS:
            pontuacao += 1
            tempo_score = 0

        desenhar_fundo(estrelas_fundo)

        for a in asteroides:
            a.desenhar(TELA)

        estrela.desenhar(TELA)
        bonus.desenhar(TELA)

        nave_reflexo.desenhar(TELA)
        nave.desenhar(TELA)

        desenhar_texto(f"Pontuação: {pontuacao}", fonte_pequena, BRANCO, 20, 20)
        desenhar_texto(f"Estrelas: {coletadas}/{META_ESTRELAS}", fonte_pequena, BRANCO, 20, 50)

        desenhar_texto("Transformações:", fonte_pequena, BRANCO, 20, 95)
        desenhar_texto("- Translação: movimento da nave e objetos", fonte_pequena, BRANCO, 20, 120)
        desenhar_texto("- Rotação: nave e asteroides", fonte_pequena, BRANCO, 20, 145)
        desenhar_texto("- Escala: bônus reduz temporariamente", fonte_pequena, BRANCO, 20, 170)
        desenhar_texto("- Reflexão: nave espelhada do outro lado", fonte_pequena, BRANCO, 20, 195)

        pygame.display.flip()

    tela_final(estrelas_fundo, venceu, pontuacao, coletadas)

# =========================
# EXECUÇÃO
# =========================
def main():
    estrelas_fundo = criar_estrelas_fundo()
    while True:
        tela_inicio(estrelas_fundo)
        jogar()

main()
