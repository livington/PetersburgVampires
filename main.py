# -"- coding: utf-8 -"-
from Persons import *
import sys

class Game:
    def __init__(self, screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))):
        self.screen = screen
        self.player = Player()
        self.enemies = []
        self.background = pygame.image.load(BACK_GROUND_PATH)
        self.running = True
        self.state = FIRST_ENTER
        self.all_objects = []
        self.cell_size = np.zeros((1, GRID_WIDTH * GRID_HEIGHT), dtype=np.int8)
        self.grid_np = np.empty((GRID_WIDTH + 2, GRID_HEIGHT + 2), dtype=Persons)

        """init pygame"""
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font('C:\Windows\Fonts\Arial.TTF', 50)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if self.state == FIRST_ENTER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
                    self.state = GAME
                    self.player.event = event
            elif self.state == GAME:
                self.player.event = event
            elif self.state == END:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER:
                        self.state = GAME
                    elif event.key == pygame.K_n:
                        self.running = False

    def render(self):
        """rendering all game state"""

        self.screen.blit(self.background, (0, 0))

        """work with ever game state"""
        if self.state == FIRST_ENTER:
            """welcome screen))"""
            self.screen.blit(pygame.image.load(START_BUTTON_PATH), (SCREEN_WIDTH / 5, SCREEN_HEIGHT / 8))
        elif self.state == GAME:
            """rendering enemies and player"""
            for obj in self.all_objects:
                obj.render(self.screen)
            """rendering HP status"""
            text = self.font.render("HP: " + str(self.player.HP), True, (255, 0, 0))
            self.screen.blit(text, (0, 10))
        elif self.state == END:
            """The end screen"""
            self.screen.blit(pygame.image.load(END_BUTTON_PATH), (SCREEN_WIDTH / 5, SCREEN_HEIGHT / 8))

        pygame.display.flip()

    def add_enemies(self):
        """add all enemies"""

        #for i in range(10):
        #    self.all_objects.append(Bat(start_position=[random.randint(0, SCREEN_WIDTH), random.randint(0, 200)]))
        """adding zombies, half to left side and half to other"""
        #for i in range(ZOMBIES_AMOUNT):
        #    self.all_objects.append(Zombie(name="zombie " + str(i),
        #                                   start_position=[SCREEN_WIDTH*int(i > ZOMBIES_AMOUNT / 2),
        #                                   random.randint(400, 700)]))
#
        """add 2 zombies to test a change direction algorithm"""
        zombie_left = Zombie(name="zombie1 ", start_position=[400, SCREEN_HEIGHT / 2])
        zombie_left.direction_np = RIGHT_np
        self.all_objects.append(zombie_left)

        zombie_right = Zombie(name="zombie1 ", start_position=[SCREEN_WIDTH-400, SCREEN_HEIGHT / 2])
        zombie_right.direction_np = LEFT_np
        self.all_objects.append(zombie_right)

        zombie_up = Zombie(name="zombie1 ", start_position=[SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
        zombie_up.direction_np = DOWN_np
        self.all_objects.append(zombie_up)

        zombie_down = Zombie(name="zombie1 ", start_position=[SCREEN_WIDTH/2, SCREEN_HEIGHT])
        zombie_down.direction_np = UP_np
        self.all_objects.append(zombie_down)

        # self.all_objects.extend(self.enemies)

    def check_player_hp(self):
        """check player HP, if it's zero, game will stop"""

        if self.player.HP <= 0:
            self.state = END

    def fill_grid_np(self):
        """fill game grid for all objects in the game"""

        self.grid_np = np.empty((1, GRID_HEIGHT*GRID_HEIGHT), dtype=Persons)
        grid = self.grid_np[0]
        cell_size = self.cell_size[0]
        for i in np.arange(len(self.all_objects)):
            obj = self.all_objects[i]
            x, y = get_grid_xy(obj.position_np, ZOMBIE_SIZE)
            grid[y*GRID_WIDTH + x] = obj
            if cell_size[y*GRID_WIDTH + x] < MAX_CELL_SIZE:
                cell_size[y*GRID_WIDTH + x] += 1

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

        x, y = get_grid_xy(obj.position_np, ZOMBIE_SIZE)
        radx, rady = get_grid_visible(obj.direction_np, 3)
        for i in np.arange(radx[MIN], radx[MAX]):
            for j in np.arange(rady[MIN], rady[MAX]):
                get_obj = self.grid_np[0][(y + j)*GRID_WIDTH + (x + i)]
                if get_obj is not None:
                    obj.visible_objects = get_obj
                    obj.visible_distance = abs(i) + abs(j)
                    obj.reaction()

    def main(self):
        """main program loop"""

        old_k_delay, old_k_interval = pygame.key.get_repeat()
        pygame.key.set_repeat(50, 50)
        try:
            while self.running is True:
                self.render()
                self.handle_events()

                if self.state == GAME:
                    if old_state in [FIRST_ENTER, END]:
                        self.player.HP = MAX_HP
                        self.all_objects.append(self.player)
                        self.add_enemies()
                    """push grid"""
                    self.fill_grid_np()
                    """check position in grid"""
                    for i in np.arange(len(self.all_objects)):
                        obj = self.all_objects[i]
                        if obj is not self.player:
                            self.get_reaction(obj)
                        obj.motions()
                    self.check_player_hp()
                elif self.state == END:
                    self.all_objects = []

                old_state = self.state
        finally:
            pygame.key.set_repeat(old_k_delay, old_k_interval)
            pygame.quit()

if __name__ == '__main__':
    petersburg_vampires = Game()
    petersburg_vampires.main()
