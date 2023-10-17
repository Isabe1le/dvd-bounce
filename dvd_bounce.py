# pyright: reportUnknownMemberType=false

import random
from typing import Final, List, Tuple

import pygame

# Define some colors
BLACK: Final[Tuple[int, int, int]] = (0, 0, 0)
WHITE: Final[Tuple[int, int, int]] = (255, 255, 255)

SCREEN_WIDTH: Final[int] = 960
SCREEN_HEIGHT: Final[int] = 540
IMG_MAX_SIZE: Final[float] = 100

SPEED: Final[float] = 2
RANDOM_SPEED_DELTA: Final[float] = 0.1
RANDOM_SIZE_DELTA: Final[float] = 2

BASE_IMAGE: Final[pygame.Surface] = pygame.image.load("dvd_logo.png")
IMAGE_SCALE_FACTOR: Final[float] = max(max(BASE_IMAGE.get_size()) / IMG_MAX_SIZE, 1)
PYGAME_IMAGE_NEW_SIZE: Final[Tuple[float, float]] = (
    BASE_IMAGE.get_size()[0] / IMAGE_SCALE_FACTOR,
    BASE_IMAGE.get_size()[1] / IMAGE_SCALE_FACTOR,
)


class BallAsset:
    def __init__(self) -> None:
        self.pygame_image = pygame.image.load("dvd_logo.png")
        self.pygame_image = pygame.transform.scale(self.pygame_image, PYGAME_IMAGE_NEW_SIZE)
        self.pygame_image_size = self.pygame_image.get_size()
        self.ball = Ball()

class Ball:
    def __init__(self):
        self.x: float = 0
        self.y: float = 0
        self.change_x: float = 0
        self.change_y: float = 0

def randsign(n: float) -> float:
    if random.randint(0, 1) == 0:
        return -n
    return n

def make_ball() -> BallAsset:
    ball = BallAsset()
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
    ball.ball.x = random.randrange(IMG_MAX_SIZE, SCREEN_WIDTH  - IMG_MAX_SIZE)
    ball.ball.y = random.randrange(IMG_MAX_SIZE, SCREEN_HEIGHT - IMG_MAX_SIZE)

    # Speed and direction of rectangle
    ball.ball.change_y = randsign(SPEED + random.uniform(-RANDOM_SPEED_DELTA, RANDOM_SPEED_DELTA))
    ball.ball.change_x = randsign(SPEED + random.uniform(-RANDOM_SPEED_DELTA, RANDOM_SPEED_DELTA))

    return ball

def main():
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Bouncing")
    pygame.display.set_icon(
        BASE_IMAGE,
    )

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    ball_list: List[BallAsset] = []

    for _ in range(0, 1):
        ball = make_ball()
        ball_list.append(ball)

    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    ball = make_ball()
                    ball_list.append(ball)
                elif event.key == pygame.K_k:
                    ball_list.pop(0)

        # --- Logic
        for ball in ball_list:
            # Move the ball's center
            ball.ball.x += ball.ball.change_x
            ball.ball.y += ball.ball.change_y

            # Bounce the ball if needed: walls
            normal_vector = None
            if ball.ball.y > SCREEN_HEIGHT - ball.pygame_image_size[1]:
                ball.ball.change_y = abs(ball.ball.change_y)
                normal_vector = pygame.Vector2(0, -1)
            elif ball.ball.y < 0:
                ball.ball.change_y = -abs(ball.ball.change_y)
                normal_vector = pygame.Vector2(0, 1)
            elif ball.ball.x > SCREEN_WIDTH - ball.pygame_image_size[0]:
                ball.ball.change_x = abs(ball.ball.change_x)
                normal_vector = pygame.Vector2(-1, 0)
            elif ball.ball.x < 0:
                ball.ball.change_x = -abs(ball.ball.change_x)
                normal_vector = pygame.Vector2(1, 0)

            if normal_vector:
                normal_vector.rotate_ip(random.randint(-3, 3))
                move_vector = pygame.Vector2(ball.ball.change_x, ball.ball.change_y)
                reflect_vector = move_vector.reflect(normal_vector)
                ball.ball.change_x = reflect_vector.x
                ball.ball.change_y = reflect_vector.y

        # --- Drawing
        # Set the screen background
        screen.fill(WHITE)

        # Draw the balls
        for ball in ball_list:
            dvd_logo_rect = pygame.Rect(ball.ball.x, ball.ball.y, ball.pygame_image_size[0], ball.pygame_image_size[1])
            screen.blit(ball.pygame_image, dvd_logo_rect)

        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Close everything down
    pygame.quit()

if __name__ == "__main__":
    main()
