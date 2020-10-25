import pygame

pygame.init()
size=(1024,768)
fps=25

pygame.display.set_caption("Jetpack")
screen=pygame.display.set_mode(size)
clock=pygame.time.Clok()


done=False
while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True

    
    clock.tick(fps)

    screen.display.flip()
pygame.quit()
