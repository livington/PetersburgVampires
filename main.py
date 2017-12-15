# -"- coding: utf-8 -"-
from Persons import *
import sys
import time
from Constants import level_characteristics
from Objects import Level
from six.moves import xrange

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.init()


class Game:
    def __init__(self, screen=SCREEN):
        self.screen = screen
        self.player = Player()
        self.enemies = []
        self.background = pygame.image.load(BACK_GROUND_PATH)
        self.running = True
        self.state = FIRST_ENTER
        self.all_objects = []
        self.cell_size = [0 for i in range(GRID_HEIGHT*GRID_WIDTH*MAX_CELL_SIZE)]
        self.grid_np = []
        """A work with levels"""
        self.types = {
            'Zombie': type(Zombie())
        }
        self.levels = []
        self.curient_level = 0
        self.curient_level_grid = np.array([0, 0])

        """init pygame"""
        pygame.font.init()
        self.font = pygame.font.Font('C:\Windows\Fonts\Arial.TTF', 50)
        self.debug_font = pygame.font.Font('C:\Windows\Fonts\Arial.TTF', 20)
        self.render_time = []

    def handle_events(self):
        """keyboard event processing is depended by game state"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if self.state == FIRST_ENTER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
                    self.state = GAME
                    self.player.event = event
            elif self.state == GAME:
                self.player.event = event
            elif self.state in [END, WIN]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER:
                        self.state = GAME
                    elif event.key == pygame.K_n:
                        self.running = False

    def make_levels(self):
        for each in level_characteristics:
            kwarg = level_characteristics[each]
            self.levels.append(Level(name=each, types=self.types, **kwarg))

    def render(self):
        """rendering all game state"""

        # self.screen.blit(self.background, (0, 0))

        """work with ever game state"""
        if self.state == FIRST_ENTER:
            """welcome screen))"""
            text = self.font.render("PETERSBURG VAMPIRES", True, (255, 0, 0))
            self.screen.blit(text, (SCREEN_WIDTH / 5, SCREEN_HEIGHT / 3))
            text = self.font.render("press ENTER to start", True, (255, 0, 0))
            self.screen.blit(text, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2))
        elif self.state == GAME:
            """rendering enemies and player"""
            old_time = time.time()
            self.levels[self.curient_level].render(self.screen)
            # self.levels[self.curient_level].render(self.screen)
            for obj in self.levels[self.curient_level].objects:
                """debug mode"""
                # text = self.debug_font.render("koor:" + str(obj.position_np), True, (255, 0, 0))
                # self.screen.blit(text, (obj.position_np[X], obj.position_np[Y]))

                # text = self.debug_font.render("x", True, (255, 0, 0))
                # self.screen.blit(text, (obj.position_np[X]+obj.image_size[X], obj.position_np[Y]))
                #
                # text = self.debug_font.render("x", True, (255, 0, 0))
                # self.screen.blit(text, (obj.position_np[X], obj.position_np[Y]+obj.image_size[Y]))
                #
                # text = self.debug_font.render("x", True, (255, 0, 0))
                # self.screen.blit(text, (obj.position_np[X]+obj.image_size[X], obj.position_np[Y]+obj.image_size[Y]))
                #
                # x, y = get_grid_xy(obj.position_np, ZOMBIE_SIZE)
                # text = self.debug_font.render("x_grid: " + str(x) + ",y_grid: " + str(y), True, (255, 0, 0))
                # self.screen.blit(text, (obj.position_np[X], obj.position_np[Y]+20))

                obj.render(self.screen)
            """rendering HP status"""
            text = self.font.render("HP: " + str(self.player.HP), True, (255, 0, 0))
            self.screen.blit(text, (0, 10))
            new_time = time.time()
            self.render_time.append(new_time - old_time)
        elif self.state == END:
            """The end screen"""
            self.screen.blit(pygame.image.load(END_BUTTON_PATH), (SCREEN_WIDTH / 5, SCREEN_HEIGHT / 8))
        elif self.state == WIN:
            text = self.font.render("YOU WIN, REPEAT? ", True, (255, 0, 0))
            self.screen.blit(text, (SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2))

        pygame.display.flip()

    def add_enemies(self):
        """add all enemies"""

        """adding zombies, half to left side and half to other"""
        for i in range(ZOMBIES_AMOUNT):
            self.all_objects.append(Zombie(name="zombie " + str(i)))

        """add 2 zombies to test a change direction algorithm"""
        zombie_left = Zombie(name="zombie_left ", start_position=[400, SCREEN_HEIGHT / 2])
        zombie_left.direction_np = RIGHT_np
        self.all_objects.append(zombie_left)

        zombie_right = Zombie(name="zombie_right ", start_position=[SCREEN_WIDTH-400, SCREEN_HEIGHT / 2])
        zombie_right.direction_np = LEFT_np
        self.all_objects.append(zombie_right)

        zombie_up = Zombie(name="zombie_up ", start_position=[SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
        zombie_up.direction_np = DOWN_np
        self.all_objects.append(zombie_up)

        zombie_down = Zombie(name="zombie_down ", start_position=[SCREEN_WIDTH/2, SCREEN_HEIGHT])
        zombie_down.direction_np = UP_np
        self.all_objects.append(zombie_down)

    def check_player_hp(self):
        """check player HP, if it's zero, game will stop"""

        if self.player.HP <= 0:
            self.state = END

        if self.player.attack is True:
            fireball = FireBall(name="FireBall", start_position=self.player.position_np - 30,
                                direction=self.player.direction_np)
            self.levels[self.curient_level].objects.append(fireball)
            self.player.attack = False

    def fill_grid_np(self):
        """fill game grid for all objects in the game"""

        self.grid_np = [None for i in range(GRID_HEIGHT*GRID_HEIGHT*MAX_CELL_SIZE)]
        grid = self.grid_np
        # cell_size = self.cell_size
        for obj in self.levels[self.curient_level].objects:
            obj.position_grid[X], obj.position_grid[Y] = get_grid_xy(obj.position_np, ZOMBIE_SIZE)
            x, y = obj.position_grid[X], obj.position_grid[Y]
            grid[y*GRID_WIDTH + x] = obj
            # if cell_size[y*GRID_WIDTH + x] < MAX_CELL_SIZE:
            #     cell_size[y*GRID_WIDTH + x] += 1

    def grid_update_np(self):
        grid = self.grid_np[0]
        cell_size = self.cell_size[0]
        for i in np.arange(GRID_WIDTH*GRID_HEIGHT):
            for j in np.arange(cell_size[i]):
                if grid[i * MAX_CELL_SIZE + j] is not None:
                    x = np.int32(grid[i * MAX_CELL_SIZE + j].position_np[X] / (2.0*ZOMBIE_SIZE[X]))
                    y = np.int32(grid[i * MAX_CELL_SIZE + j].position_np[Y] / (2.0*ZOMBIE_SIZE[Y]))

                    if x < 0:
                        x = 0
                    if y < 0:
                        y = 0
                    if x >= GRID_WIDTH:
                        x = GRID_WIDTH - 1
                    if y >= GRID_HEIGHT:
                        y = GRID_HEIGHT - 1

                    if (x * GRID_HEIGHT + y) != i and cell_size[x * GRID_HEIGHT + y] < MAX_CELL_SIZE:
                        grid[(x * GRID_HEIGHT + y) * MAX_CELL_SIZE + cell_size[x * GRID_HEIGHT + y] + 1] = \
                        grid[i * GRID_HEIGHT + j]
                        cell_size[x * GRID_HEIGHT + y] += 1
                        grid[i*MAX_CELL_SIZE + j] = grid[i * MAX_CELL_SIZE + cell_size[i] - 1]
                        cell_size[i] -= 1

    def get_reaction(self, obj):
        """loop for all objects, get reaction"""

        x, y = obj.position_grid[X], obj.position_grid[Y]

        radx, rady = get_grid_visible(obj.direction_np, obj.view_rad)
        for i in range(radx[MIN], radx[MAX]):
            for j in range(rady[MIN], rady[MAX]):
                if i == 0 and j == 0:
                    pass
                else:
                    get_obj = self.grid_np[(y + j)*GRID_WIDTH + (x + i)]
                    if get_obj is not None:
                        obj.visible_objects = get_obj
                        obj.visible_distance = abs(i) + abs(j)
                        obj.reaction()

    def change_level(self):
        if self.player.check_ability_to_move() is False:
            self.curient_level_grid += self.player.direction_np
            amount_axes = int(len(self.levels) // 2)
            buf_level_number = self.curient_level_grid[X]*amount_axes + self.curient_level_grid[Y]
            if buf_level_number in range(len(self.levels)) \
                    and amount_axes > self.curient_level_grid[X] >= 0 \
                    and amount_axes > self.curient_level_grid[Y] >= 0:
                self.levels[self.curient_level].objects.remove(self.player)
                self.curient_level = buf_level_number

                if np.dot(self.player.direction_np, LEFT_np) == 1:
                    self.player.position_np[X] = GAME_ZONE_DEFAULT[X][MAX] - 50
                if np.dot(self.player.direction_np, RIGHT_np) == 1:
                    self.player.position_np[X] = GAME_ZONE_DEFAULT[X][MIN] + 50
                if np.dot(self.player.direction_np, DOWN_np) == 1:
                    self.player.position_np[Y] = GAME_ZONE_DEFAULT[Y][MIN] - 50
                if np.dot(self.player.direction_np, UP_np) == 1:
                    self.player.position_np[Y] = GAME_ZONE_DEFAULT[Y][MAX] + 50

                self.levels[self.curient_level].objects.append(self.player)
            else:
                self.curient_level_grid -= self.player.direction_np

    def main(self):
        """main program loop"""

        old_k_delay, old_k_interval = pygame.key.get_repeat()
        pygame.key.set_repeat(50, 50)
        all_time = []

        clk = pygame.time.Clock()
        try:
            while self.running is True:
                self.render()
                self.handle_events()
                clk.tick(cnst_ticks)

                if self.state == GAME:
                    if old_state in [FIRST_ENTER, END, WIN]:
                        self.player.HP = MAX_HP
                        self.curient_level = 0
                        self.make_levels()
                        self.levels[self.curient_level].objects.append(self.player)
                        # self.add_enemies()
                        first_enter_time = time.time()
                        objects_amount = len(self.levels[self.curient_level].objects)

                    old_time = time.time()
                    """push grid"""
                    self.fill_grid_np()

                    """check position in grid"""
                    for obj in self.levels[self.curient_level].objects:
                        if obj is not self.player:
                            if obj.state is DEAD:
                                self.levels[self.curient_level].objects.remove(obj)
                            else:
                                self.get_reaction(obj)
                        obj.motions()
                    all_time.append(time.time() - old_time)

                    # if time.time() - first_enter_time > 15:
                    #     self.player.HP = 0
                            
                    self.check_player_hp()
                    if len(self.levels[self.curient_level].objects) < 2:
                        self.state = WIN

                    self.change_level()

                elif self.state in [END, WIN]:
                    self.levels = []

                old_state = self.state
        finally:
            pygame.key.set_repeat(old_k_delay, old_k_interval)
            pygame.quit()
            print("objects amount: {0}, iteration time: {1}".format(objects_amount, sum(all_time) / len(all_time)))
            print("render iteration time: {0}".format(sum(self.render_time) / len(self.render_time)))

if __name__ == '__main__':
    petersburg_vampires = Game()
    petersburg_vampires.main()
