# Complete your game here
import pygame, random, datetime, sys

class CoinHoarder:
    def __init__(self):
        pygame.init()

        self.load_images()
        self.w_width = 640
        self.w_height = 480
        self.window = pygame.display.set_mode((self.w_width, self.w_height + 50))
        self.font = pygame.font.SysFont(None, 36)
        self.font2 = pygame.font.SysFont(None, 24)
        pygame.display.set_caption("Coin Hoarder")
        self.clock = pygame.time.Clock()
        self.new_game()
        self.main_loop()

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()
            self.move()
            self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_F1:
                    self.new_game()
                if event.key == pygame.K_RIGHT:
                    self.direction["right"] = True
                if event.key == pygame.K_LEFT:
                    self.direction["left"] = True
                if event.key == pygame.K_UP:
                    self.direction["up"] = True
                if event.key == pygame.K_DOWN:
                    self.direction["down"] = True          
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.direction["right"] = False
                if event.key == pygame.K_LEFT:
                    self.direction["left"] = False
                if event.key == pygame.K_UP:
                    self.direction["up"] = False
                if event.key == pygame.K_DOWN:
                    self.direction["down"] = False  

    def move(self): #move robot and monster and check for collisions
        if self.game_over():
            return
        if self.direction["right"]:
            self.pos["robot"][0] += 3
        if self.direction["left"]:
            self.pos["robot"][0] -= 3
        if self.direction["up"]:
            self.pos["robot"][1] -= 3
        if self.direction["down"]:
            self.pos["robot"][1] += 3 
        if datetime.timedelta(seconds=2) < datetime.datetime.now() - self.advantage: #monster starts to move after 2s passed
            if self.pos["robot"][0] > self.pos["monster"][0]:
                self.pos["monster"][0] += 1
            else:
                self.pos["monster"][0] -= 1
            if self.pos["robot"][1] > self.pos["monster"][1]:
                self.pos["monster"][1] += 1
            else:
                self.pos["monster"][1] -= 1
        self.coin_collision()
        self.wall_collision()
        self.door_collision()

    def collision(self, sprite: str): #returns True if robot touches a sprite
        coin_x = self.pos[sprite][0] + self.images[sprite].get_width()/2
        coin_y = self.pos[sprite][1] + self.images[sprite].get_height()/2
        robot_x = self.pos["robot"][0] + self.images["robot"].get_width()/2
        robot_y = self.pos["robot"][1] + self.images["robot"].get_height()/2
        if abs(coin_x-robot_x) < (self.images[sprite].get_width() + self.images["robot"].get_width())/2 * 0.8:
            if abs(coin_y-robot_y) < (self.images[sprite].get_height() + self.images["robot"].get_height())/2 * 0.8:
                return True
        return False

    def monster_collision(self):
        if self.collision("monster"):
            return True
        return False

    def door_collision(self):
        if self.collision("door"):
            self.next_level()

    def game_over(self):
        return self.monster_collision()

    def wall_collision(self): #make sure robot's position is within window
        self.pos["robot"][0] = min(self.pos["robot"][0], self.w_width - self.images["robot"].get_width())
        self.pos["robot"][0] = max(0, self.pos["robot"][0])
        self.pos["robot"][1] = min(self.pos["robot"][1], self.w_height - self.images["robot"].get_height())
        self.pos["robot"][1] = max(0, self.pos["robot"][1])

    def coin_collision(self): #if robot touches the coin, add point and spawn new coin
        if self.collision("coin"):
            self.pos["coin"] = self.new_pos("coin")
            self.coins += 1
            if self.coins % 5 == 0:
                self.pos["coin"] = [-500, -500]
                self.pos["door"] = self.new_pos("door")
                return
            self.pos["coin"] = self.new_pos("coin")

    def draw_window(self):
        self.window.fill((0, 50, 0))
        for sprite in self.images:
            self.window.blit(self.images[sprite], self.pos[sprite])
        pygame.draw.rect(self.window, (0, 0, 0), (0, self.w_height, self.w_width, self.w_height + 50))
        text = self.font2.render("Kolikot: " + str(self.coins) + " "*20 + "Taso: " + str(self.level) + " "*20 + "Uusi peli: F1" + " "*20 + "Lopeta peli: ESC", True, (200, 0, 0))
        self.window.blit(text, (25, self.w_height + 15))
        if self.game_over():
            text = self.font.render("GAME OVER", True, (200, 0, 0))
            pygame.draw.rect(self.window, (0, 0, 0), (self.w_width/2 - text.get_width(), self.w_height/2 - text.get_height(), text.get_width()*2, text.get_height()*2))
            self.window.blit(text, ((self.w_width - text.get_width())/2, (self.w_height - text.get_height())/2))
        pygame.display.flip()

    def load_images(self):
        self.images = {}
        images = ["coin", "door", "monster", "robot"]
        for name in images:
            self.images[name] = pygame.image.load(name + ".png")

    def new_pos(self, sprite):
        x = random.randint(0, self.w_width - self.images[sprite].get_width())
        y = random.randint(0, self.w_height - self.images[sprite].get_height())
        return [x, y]

    def next_level(self):
        self.advantage = datetime.datetime.now()
        self.direction = {"right": False, "left": False, "up": False, "down": False}
        self.level += 1
        for sprite in self.pos:
            if sprite == "door":
                self.pos[sprite] = [-500, -500]
                continue
            self.pos[sprite] = self.spawn_check(self.new_pos(sprite), sprite)

    def new_game(self):
        self.advantage = datetime.datetime.now()
        self.pos = {}
        self.coins = 0
        self.level = 1
        self.direction = {"right": False, "left": False, "up": False, "down": False}
        positions = ["robot", "monster", "coin", "door"]
        for sprite in positions:
            if sprite == "door":
                self.pos[sprite] = [-500, -500]
                continue
            self.pos[sprite] = self.spawn_check(self.new_pos(sprite), sprite)

    def spawn_check(self, new_coord: list, new_sprite: str): #checks that new sprite is not spawned on top of other sprite, if does - creates new pos recursively
        for sprite in self.pos:
            x_delta = abs(self.pos[sprite][0] + self.images[sprite].get_width()/2 - (new_coord[0] + self.images[new_sprite].get_width()/2))
            y_delta = abs(self.pos[sprite][1] + self.images[sprite].get_height()/2 - (new_coord[1] + self.images[new_sprite].get_height()/2))
            if x_delta < (self.images[sprite].get_width() + self.images[new_sprite].get_width())/2:
                if y_delta < (self.images[sprite].get_height() + self.images[new_sprite].get_height())/2:
                    return self.spawn_check(self.new_pos(new_sprite), new_sprite)
        return new_coord

CoinHoarder()