# Space Galaxy

## 📋 Descrição

**Space Galaxy** é um jogo 2D desenvolvido em Python com Pygame, criado como trabalho da disciplina de **Computação Gráfica** da CESUPA. O projeto demonstra os principais conceitos de transformações geométricas aplicadas na prática.

## 🎮 Gameplay

No jogo, o jogador controla uma nave espacial que deve:
- **Coletar 15 estrelas** para vencer
- **Desviar de asteroides** que descem pela tela
- **Pegar o bônus roxo** para encolher temporariamente e ficar mais ágil

## 🎨 Transformações Gráficas Implementadas

Este projeto aplica os principais conceitos de transformações geométricas estudados em Computação Gráfica:

### 1. **Translação** ➡️
- Movimento da nave controlado pelo jogador (setas/WASD)
- Deslocamento de asteroides, estrelas e bônus pela tela
- Movimento do fundo com estrelas animadas

### 2. **Rotação** 🔄
- Nave rotaciona 18° para esquerda/direita durante movimento lateral
- Asteroides giram continuamente em seus próprios eixos
- Rotação controlada por ângulo e velocidade angular

### 3. **Escala** 📏
- Bônus roxo oscila de tamanho continuamente usando função seno
- Nave reduz para 65% do tamanho ao coletar o bônus
- Implementação de transformação de escala não-uniforme

### 4. **Reflexão** 🪞
- Nave-reflexo espelhada no lado oposto da tela
- Cria efeito de "espelho invisível" vertical
- Sincroniza movimento e transformações com a nave principal

## 🕹️ Controles

| Tecla | Ação |
|-------|------|
| **Setas** | Mover nave |
| **WASD** | Mover nave (alternativo) |
| **ENTER** | Iniciar jogo / Jogar novamente |
| **ESC** | Sair |

## 📊 Características Técnicas

- **Resolução**: 1000x650 pixels
- **FPS**: 60 quadros por segundo
- **Detecção de Colisão**: Pixel-perfect usando máscaras (mask collision)
- **Renderização de Formas**: Polígonos e elipses usando Pygame
- **Animação**: Síntese de transformações e physics

## 🛠️ Estrutura do Código

### Classes Principais

```
Nave                - Jogador principal com todas as transformações
NaveReflexo         - Reflexão da nave
Asteroide           - Inimigos com rotação
EstrelaColetavel    - Objetivo do jogo
BonusReducao        - Power-up especial com escala animada
```

### Funções Auxiliares

- `desenhar_texto()` - Renderização de texto na tela
- `criar_estrelas_fundo()` - Geração procedural do fundo
- `colisao_precisa()` - Detecção de colisão em nível de pixel

## 📦 Dependências

```
pygame>=2.0.0
```

## 🚀 Como Executar

### 1. Instalar dependências
```bash
pip install pygame
```

### 2. Executar o jogo
```bash
python "import pygame.py"
```

## 🎯 Objetivos do Jogo

- ⭐ **Coletar 15 estrelas** = **VITÓRIA**
- 💥 **Bater em um asteroide** = **GAME OVER**
- 💜 **Bônus roxo** = Nave diminui por 2 segundos (pontos extras)

## 📈 Sistema de Pontuação

- Estrela coletada: **+10 pontos**
- Bônus roxo coletado: **+20 pontos**
- Por segundo: **+1 ponto**

## 🎓 Conceitos de Computação Gráfica Aplicados

### Transformações Afins
- Matrizes de transformação (implícitas no Pygame)
- Composição de transformações (rotação + escala + translação)

### Rendering
- Double buffering (automático no Pygame)
- Surface transformation e blitting
- Alpha blending para transparência

### Física
- Mudança de quadro
- Velocidade e aceleração constante
- Movimento senoidal (estrelas)

### Detecção de Colisão
- Bounding box collision
- Pixel-perfect collision com máscaras

## 👨‍💻 Desenvolvedor

Desenvolvido para a disciplina de **Computação Gráfica** - **CESUPA**

## 📝 Licença

Acadêmico - CESUPA

---

**Divirta-se explorando o espaço! 🚀✨**
