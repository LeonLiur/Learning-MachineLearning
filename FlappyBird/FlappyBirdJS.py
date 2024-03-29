import pygame
import os
import random
pygame.font.init()
pygame.joystick.init()
j = pygame.joystick.Joystick(0)
j.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
END_IMG = pygame.image.load(os.path.join("imgs", "end.png"))
STAT_FONT = pygame.font.SysFont("Comicsans", 50)


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count = self.img_count + 1

        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]

        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]

        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]

        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]

        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        blitrotatecenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    WIN_HEIGHT = WIN_HEIGHT
    WIN_WIDTH = WIN_WIDTH
    VEL = 5

    def __init__(self, x, gap):
        self.x = x
        self.height = 0
        self.gap = gap

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False

        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True

        return False


class Base:
    VEL = 5
    WIN_WIDTH = WIN_WIDTH
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def blitrotatecenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    surf.blit(rotated_image, new_rect.topleft)


def draw_window(win, bird, pipes, base, score, level):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    bird.draw(win)

    score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))
    level_label = STAT_FONT.render("Time passed: " + str(level) + "s", 1, (255, 255, 255))
    win.blit(level_label, (WIN_WIDTH - level_label.get_width() - 15, 40))

    pygame.display.update()


def end_screen(win, score, level):
    win.blit(END_IMG, (0, 0))

    score_label = STAT_FONT.render("Score: " + str(score), 1, (0, 0, 0))
    win.blit(score_label, (round(WIN_WIDTH/2 - score_label.get_width()/2), 500))
    level_label = STAT_FONT.render("Time: " + str(level), 1, (0, 0, 0))
    win.blit(level_label, (round(WIN_WIDTH / 2 - score_label.get_width() / 2), 530))
    pygame.display.update()


def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700, random.randrange(200, 250))]
    score = 0
    spawn_distance = 700
    counter = 0
    started = False
    lost = False
    level = 0

    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True
    while run:
        clock.tick(25)
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if j.get_button(2):
                    run = False

                elif j.get_button(1) and not lost:
                    if not started:
                        started = True
                    bird.jump()

            elif event.type == pygame.QUIT:
                run = False

        if started and not lost:
            counter += 1
            if counter >= 30:
                if spawn_distance > 510:
                    spawn_distance -= 1
                else:
                    spawn_distance = 510
                counter = 0
                level += 1
            bird.move()

            rem = []
            add_pipe = False

            for pipe in pipes:
                if pipe.collide(bird):
                    lost = True

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

                pipe.move()

            if add_pipe:
                score += 1
                pipes.append(Pipe(spawn_distance, random.randrange(200, 250)))

            for r in rem:
                pipes.remove(r)

            base.move()

        if bird.y + BIRD_IMGS[0].get_height() - 10 >= 730:
            lost = True

        if lost:
            while lost:
                end_screen(win, score, level)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.JOYBUTTONDOWN:
                        if j.get_button(1):
                            main()
                        elif j.get_button(2):
                            pygame.quit()
                            quit()

        draw_window(win, bird, pipes, base, score, level)

    pygame.quit()
    quit()


main()
