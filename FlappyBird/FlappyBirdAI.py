import pygame
import os
import random
import neat
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

GEN = 0

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


def draw_window(win, birds, pipes, base, score, level, gen, live):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    for bird in birds:
        bird.draw(win)

    score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))
    level_label = STAT_FONT.render("Time: " + str(level) + "s", 1, (255, 255, 255))
    win.blit(level_label, (WIN_WIDTH - level_label.get_width() - 15, 40))
    gen_label = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(gen_label, (10, 10))
    live_label = STAT_FONT.render("Alive: " + str(live), 1, (255, 255, 255))
    win.blit(live_label, (10, 40))

    pygame.display.update()


# def end_screen(win, score, level):
#     win.blit(END_IMG, (0, 0))
#
#     score_label = STAT_FONT.render("Score: " + str(score), 1, (0, 0, 0))
#     win.blit(score_label, (round(WIN_WIDTH/2 - score_label.get_width()/2), 500))
#     level_label = STAT_FONT.render("Difficulty: " + str(level), 1, (0, 0, 0))
#     win.blit(level_label, (round(WIN_WIDTH / 2 - score_label.get_width() / 2), 530))
#     pygame.display.update()


def eval_genomes(genomes, config):
    global GEN
    GEN += 1

    birds = []
    nets = []
    ge = []

    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        genome.fitness = 0
        ge.append(genome)

    base = Base(730)
    pipes = [Pipe(700, random.randrange(200, 250))]

    score = 0
    spawn_distance = 700
    counter = 0
    level = 0

    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    running = True
    while running:
        clock.tick(30)

        # Increasing difficulty
        counter += 1
        if counter >= 30:
            if spawn_distance > 510:
                spawn_distance -= 1
            else:
                spawn_distance = 510
            counter = 0
            level += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            print("NO BIRDS ALIVE")
            break

        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.move()
            output = nets[x].activate((bird.y,
                                       abs(bird.y - pipes[pipe_ind].height),
                                       abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        rem = []
        add_pipe = False

        for pipe in pipes:
            pipe.move()
            for bird in birds:
                if pipe.collide(bird):
                    for x, x_bird in enumerate(birds):
                        ge[x].fitness -= 1
                        birds.remove(x_bird)
                        nets.pop(x)
                        ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(spawn_distance, random.randrange(200, 250)))

        for r in rem:
            pipes.remove(r)

        for x, xbird in enumerate(birds):
            if xbird.y + BIRD_IMGS[0].get_height() - 10 >= 730 or xbird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        live = len(birds)
        draw_window(win, birds, pipes, base, score, level, GEN, live)


def run(cpath):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                cpath)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(eval_genomes, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
