import pygame

pygame.init()
size = width, height = (520, 360)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

anim_cross = [pygame.image.load(f"data/textures/cross.png"),
              pygame.image.load(f"data/textures/cross_a1.png"),
              pygame.image.load(f"data/textures/cross_a2.png"),
              pygame.image.load(f"data/textures/cross_a1.png"),
              pygame.image.load(f"data/textures/cross_a3.png"),
              pygame.image.load(f"data/textures/cross_a1.png"),
              pygame.image.load(f"data/textures/cross.png")]

anim_peaks = [pygame.image.load(f"data/textures/peaks.png"),
              pygame.image.load(f"data/textures/peaks_a1.png"),
              pygame.image.load(f"data/textures/peaks_a2.png"),
              pygame.image.load(f"data/textures/peaks_a1.png"),
              pygame.image.load(f"data/textures/peaks_a3.png"),
              pygame.image.load(f"data/textures/peaks_a1.png"),
              pygame.image.load(f"data/textures/peaks.png")]

anim_heart = [pygame.image.load(f"data/textures/heart.png"),
              pygame.image.load(f"data/textures/heart_a1.png"),
              pygame.image.load(f"data/textures/heart_a2.png"),
              pygame.image.load(f"data/textures/heart_a1.png"),
              pygame.image.load(f"data/textures/heart_a3.png"),
              pygame.image.load(f"data/textures/heart_a1.png"),
              pygame.image.load(f"data/textures/heart.png")]

anim_diamonds = [pygame.image.load(f"data/textures/diamonds.png"),
                 pygame.image.load(f"data/textures/diamonds_a1.png"),
                 pygame.image.load(f"data/textures/diamonds_a2.png"),
                 pygame.image.load(f"data/textures/diamonds_a1.png"),
                 pygame.image.load(f"data/textures/diamonds_a3.png"),
                 pygame.image.load(f"data/textures/diamonds_a1.png"),
                 pygame.image.load(f"data/textures/diamonds.png")]

anim_jack = [pygame.image.load(f"data/textures/jack.png"),
             pygame.image.load(f"data/textures/jack_a1.png"),
             pygame.image.load(f"data/textures/jack_a2.png"),
             pygame.image.load(f"data/textures/jack_a1.png"),
             pygame.image.load(f"data/textures/jack_a3.png"),
             pygame.image.load(f"data/textures/jack_a4.png"),
             pygame.image.load(f"data/textures/jack.png")]

anim_queen = [pygame.image.load(f"data/textures/queen.png"),
              pygame.image.load(f"data/textures/queen_a1.png"),
              pygame.image.load(f"data/textures/queen_a2.png"),
              pygame.image.load(f"data/textures/queen_a1.png"),
              pygame.image.load(f"data/textures/queen_a3.png"),
              pygame.image.load(f"data/textures/queen_a4.png"),
              pygame.image.load(f"data/textures/queen.png")]

anim_king = [pygame.image.load(f"data/textures/king.png"),
             pygame.image.load(f"data/textures/king_a1.png"),
             pygame.image.load(f"data/textures/king_a2.png"),
             pygame.image.load(f"data/textures/king_a1.png"),
             pygame.image.load(f"data/textures/king_a3.png"),
             pygame.image.load(f"data/textures/king_a4.png"),
             pygame.image.load(f"data/textures/king.png")]

i = 0
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill((0, 0, 0))
    screen.blit(anim_cross[i], (0, 0))
    screen.blit(anim_peaks[i], (130, 0))
    screen.blit(anim_heart[i], (260, 0))
    screen.blit(anim_diamonds[i], (390, 0))

    screen.blit(anim_jack[i], (0, 180))
    screen.blit(anim_queen[i], (130, 180))
    screen.blit(anim_king[i], (260, 180))

    i = (i + 1) % len(anim_cross)
    pygame.display.flip()
    clock.tick(2)