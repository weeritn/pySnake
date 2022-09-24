import sys
import pygame
import random
import time

# Snake game by Weerit Nopcharoenwong

class Snake:
    def __init__(self):
        print("init ran")

    # Display
    dis = None

    # Colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)
    lighter_green = (0, 200, 0)

    # Game over
    game_over = False

    # Starting position
    x1 = 400
    y1 = 400

    # Random apples
    random_x = random.randint(45, 750)
    random_y = random.randint(80, 750)

    # Snake movement
    x1_change = 0
    y1_change = 0

    # Game clock
    clock = pygame.time.Clock()

    # How many apples have been eaten
    snake_score = 1

    # Top left score
    scoreboard = 0

    # Size of snake
    snake_length = []

    # Snake direction
    snake_direction = None

    # Sets game start, initially false
    game_start = False

    # Create the start button
    start_button = pygame.image.load("start_button.png")
    start_button = pygame.transform.smoothscale(start_button, (200, 100))
    start_button_rect = start_button.get_rect()
    start_button_rect.center = (400, 400)
    start_button_mask = pygame.mask.from_surface(start_button)

    # Snake image
    snake_art = pygame.image.load("snakeart.png")
    snake_art = pygame.transform.smoothscale(snake_art, (250, 250))

    def apple_randomizer(self):
        self.random_x = random.randint(45, 750)
        self.random_y = random.randint(80, 750)

    def check_self_collision(self):
        if self.snake_score != 1:
            for position in self.snake_length:
                if self.x1 in range(position[0] - 1, position[0] + 1) and self.y1 in range(position[1] - 1, position[1] + 1):
                    self.game_over = True
                    # print(f"current snake: {self.snake_length}\n{self.x1} {self.y1}")

    def check_position(self):
        # X variable list
        xlist = []
        ylist = []

        for position in self.snake_length:
            xlist.append(position[0])
            ylist.append(position[1])

        # If snake hits edge of screen, return game over
        if self.x1 < 0 or self.x1 > 800 or self.y1 < 45 or self.y1 > 800:
            self.game_over = True
        self.check_self_collision()

    def apple_spawn(self):
        self.apple_randomizer()
        # print(f"apple spawn = {self.random_x}, {self.random_y}")

    def game_start(self):
        # Snake speed
        snake_speed = 5

        # Snake size
        snake_size = 20

        # Initializing pygame import
        pygame.init()

        # Font of top left score
        score_font = pygame.font.SysFont("comicsansms", 35)

        # Apple consumption sound effect
        apple_eat = pygame.mixer.Sound('apple_bite.wav')

        # Start button sound
        start_sound = pygame.mixer.Sound('startGame.wav')
        start_sound.set_volume(0.2)

        # Creating pygame window
        dis = pygame.display.set_mode((800, 800))

        # Setting game title
        pygame.display.set_caption("Snake")

        self.dis = dis

        # Starts display and quits when exit button is pressed
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True

                # Clicking start starts the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.start_button_rect.collidepoint(event.pos):
                            self.game_start = True
                            start_sound.play()
                            print("start")

                # Snake movement
                if self.game_start == True:
                    if event.type == pygame.KEYDOWN:

                        # For WASD & Arrow Key movement
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            if self.snake_direction != "down":
                                self.snake_direction = "up"
                                self.x1_change = 0
                                self.y1_change = -snake_speed
                        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            if self.snake_direction != "right":
                                self.snake_direction = "left"
                                self.x1_change = -snake_speed
                                self.y1_change = 0
                        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            if self.snake_direction != "left":
                                self.snake_direction = "right"
                                self.x1_change = snake_speed
                                self.y1_change = 0
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            if self.snake_direction != "up":
                                self.snake_direction = "down"
                                self.x1_change = 0
                                self.y1_change = snake_speed

            # Movement changes
            self.x1 += self.x1_change
            self.y1 += self.y1_change

            # Checks position of snake
            self.check_position()

            # Snake length increase
            self.snake_length.append((self.x1, self.y1))
            self.snake_length = self.snake_length[-self.snake_score * 5:]
            # print(self.snake_score)

            # Draw start button
            self.dis.fill(self.white)
            self.dis.blit(self.snake_art, (260, 100))
            self.dis.blit(self.start_button, self.start_button_rect)

            # Fill background
            if self.game_start == True:
                self.dis.fill(self.white)

            # Track last snake length
            last_point = len(self.snake_length) - 1

            # Draw snake head
            if self.game_start == True:
                for i in range(0, len(self.snake_length) - 1):
                    pygame.draw.rect(self.dis, self.green, [self.snake_length[i][0], self.snake_length[i][1], snake_size, snake_size])
                pygame.draw.rect(self.dis, self.lighter_green, [self.snake_length[last_point][0], self.snake_length[last_point][1], snake_size, snake_size])

            # Spawn apple
            if self.game_start == True:
                pygame.draw.rect(self.dis, self.red, [self.random_x, self.random_y, snake_size, snake_size])

            # If apple touched, spawn another apple
            if self.x1 in range(self.random_x-22, self.random_x+22) and self.y1 in range(self.random_y-22, self.random_y+22):
                # print(f"Collision point = {self.x1}, {self.y1}, {self.random_x}, {self.random_y}")
                self.apple_spawn()
                self.snake_score += 1
                self.scoreboard += 1
                # print(self.snake_score)
                print(self.scoreboard)
                apple_eat.play()

            # Scoreboard top left
            score_value = score_font.render("Score: " + str(self.scoreboard), True, self.black)
            self.dis.blit(score_value, [0, 0])
            pygame.draw.line(dis, self.black, (0, 45), (800, 45))

            # Loss message
            if self.game_over == True:
                lost_message = score_font.render("You lose! Final Score: " + str(self.scoreboard), True, self.black)
                dis.fill(self.white)
                self.dis.blit(lost_message, [230, 300])
                pygame.display.update()
                time.sleep(3)
                print("lost")

            # Update game
            pygame.display.update()

            # Sets game tick to 30
            self.clock.tick(30)


def main():
    snake_game = Snake()
    snake_game.game_start()


if __name__ == "__main__":
    main()
    sys.exit()
