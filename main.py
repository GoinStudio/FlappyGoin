import pygame
from pygame.locals import *
import sys
import Window
import Player
import Pipe

pygame.init()


class Main:
    def __init__(self):
        self.wd = Window.Window()

        self.FPS = 30
        self.FramesPerSecond = pygame.time.Clock()

        self.themeSong = pygame.mixer.Sound("./assets/Theme.wav")
        self.startSound = pygame.mixer.Sound("./assets/start.wav")
        self.dieSound = pygame.mixer.Sound("./assets/die.wav")
        self.dingSound = pygame.mixer.Sound("./assets/ding.wav")
        self.flappSound = pygame.mixer.Sound("./assets/flapp.wav")

        self.p = Player.Player(self.wd, self)

        self.pipes = []
        self.breakLoop = False

        

    def start(self):
        pygame.mixer.Sound.play(self.themeSong)
        self.wd.window.fill(self.wd.WHITE)
        self.wd.draw_bg()
        self.wd.display_text(100, "Flappy Goin", self.wd.BLACK, self.wd.width/2, 100)
        self.wd.display_text(50, "Press Space to start", self.wd.BLACK, self.wd.width/2, 400)
        self.p.draw()
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[K_ESCAPE]:
                        pygame.quit()
                        quit()
                    elif keys[K_SPACE]:
                        pygame.mixer.Sound.stop(self.themeSong)
                        pygame.mixer.Sound.play(self.startSound)
                        self.main()
            self.wd.window.fill(self.wd.WHITE)
            self.wd.update_bg()
            self.wd.display_text(100, "Flappy Goin", self.wd.BLACK, self.wd.width/2, 100)
            self.wd.display_text(50, "Press Space to start", self.wd.BLACK, self.wd.width/2, 400)
            self.p.draw()
            pygame.display.update()

    def main(self):
        self.pipes.append(Pipe.Pipe(self.wd))
        while not self.breakLoop:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[K_ESCAPE]:
                        pygame.quit()
                        quit()
                    elif keys[K_SPACE] and self.p.dead:
                        pygame.mixer.Sound.stop(self.themeSong)
                        pygame.mixer.Sound.play(self.startSound)
                        main = Main()
                        main.main()
            if not self.p.dead: 

                self.wd.window.fill(self.wd.WHITE)
                self.wd.update_bg()
                

                if self.pipes[-1].downPipeX <= self.wd.width - 400:
                    self.pipes.append(Pipe.Pipe(self.wd))

                if self.pipes[0].downPipeX < self.p.x: pipe = self.pipes[1]
                else: pipe = self.pipes[0]

                if self.p.x + self.p.heigth > pipe.downPipeX and self.p.x < pipe.downPipeX + pipe.width:
                    if self.p.y < pipe.upPipeY + pipe.heigth:
                        self.p.die()
                        continue
                    elif self.p.y+self.p.width > pipe.downPipeY:
                        self.p.die()
                        continue

                if self.p.x+self.p.heigth == pipe.downPipeX + (pipe.width/2):
                    self.p.score += 1
                    pygame.mixer.Sound.play(self.dingSound)

                i = 0
                for pipe in self.pipes:
                    if pipe.isOutOfScreen():
                        self.pipes.pop(i)
                    else:
                        pipe.update()
                    i += 1

                self.p.update(self)
                self.wd.display_text(100, f"{self.p.score}", self.wd.BLACK, self.wd.width/2, 100)

            pygame.display.update()
            self.FramesPerSecond.tick(self.FPS)


if __name__ == "__main__":
    Game = Main()
    Game.start()