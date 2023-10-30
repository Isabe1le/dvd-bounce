from random import randint, randrange, uniform
from typing import Final, List, Tuple

import pygame

# Define some colors
BLACK: Final[Tuple[int, int, int]] = (0, 0, 0)
WHITE: Final[Tuple[int, int, int]] = (255, 255, 255)

SCREEN_WIDTH: Final[int] = 960
SCREEN_HEIGHT: Final[int] = 540
IMG_MAX_SIZE: Final[float] = 100
SCREEN_DIMENSIONS: Final[Tuple[int, int]] = (SCREEN_WIDTH, SCREEN_HEIGHT)

INITIAL_TILE_MOVEMENT_SPEED: Final[float] = 2
RANDOM_SPEED_DELTA: Final[float] = 0.1
RANDOM_SIZE_DELTA: Final[float] = 2
STARTING_NUMBER_OF_SPRITES: Final[int] = 1
CONFETTI_PARTICLE_SIZE: Final[int] = 5
CONFETTI_PARTICLE_SPEED: Final[int] = 5
NUMBER_OF_CONFETTI_PARTICLES: Final[int] = 200

BASE_IMAGE: Final[pygame.Surface] = pygame.image.load("dvd_logo.png")
IMAGE_SCALE_FACTOR: Final[float] = max(max(BASE_IMAGE.get_size()) / IMG_MAX_SIZE, 1)
PYGAME_IMAGE_NEW_SIZE: Final[Tuple[float, float]] = (
    BASE_IMAGE.get_size()[0] / IMAGE_SCALE_FACTOR,
    BASE_IMAGE.get_size()[1] / IMAGE_SCALE_FACTOR,
)


class SpriteAsset:
    def __init__(self) -> None:
        self.pygame_image = pygame.image.load("dvd_logo.png")
        self.pygame_image = pygame.transform.scale(self.pygame_image, PYGAME_IMAGE_NEW_SIZE)
        self.pygame_image_size = self.pygame_image.get_size()
        self.object = Sprite()


class Sprite:
    def __init__(self):
        self.x: float = 0
        self.y: float = 0
        self.change_x: float = 0
        self.change_y: float = 0


def randsign(n: float) -> float:
    if randint(0, 1) == 0:
        return -n
    return n


def make_ball() -> SpriteAsset:
    ball = SpriteAsset()
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
    ball.object.x = randrange(IMG_MAX_SIZE, SCREEN_WIDTH  - IMG_MAX_SIZE)
    ball.object.y = randrange(IMG_MAX_SIZE, SCREEN_HEIGHT - IMG_MAX_SIZE)

    # Speed and direction of rectangle
    ball.object.change_y = randsign(INITIAL_TILE_MOVEMENT_SPEED + uniform(-RANDOM_SPEED_DELTA, RANDOM_SPEED_DELTA))
    ball.object.change_x = randsign(INITIAL_TILE_MOVEMENT_SPEED + uniform(-RANDOM_SPEED_DELTA, RANDOM_SPEED_DELTA))

    return ball


def rand_colour() -> Tuple[int, int, int]:
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (r, g, b)


class Particle:
    def __init__(self, starting_pos: Tuple[float, float], vector: pygame.math.Vector2) -> None:
        self.pos: Tuple[float, float] = starting_pos
        self.vector = vector
        self.colour = rand_colour()

    def update_pos(self) -> None:
        self.pos = (
            self.pos[0] + uniform(self.vector.x, self.vector.x*2),
            self.pos[1] + uniform(self.vector.y, self.vector.y*2),
        )


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_DIMENSIONS)

    pygame.display.set_caption("Bouncing")
    pygame.display.set_icon(
        BASE_IMAGE,
    )

    done = False
    clock = pygame.time.Clock()
    sprite_list: List[SpriteAsset] = []
    speed_multiplier: float = 1
    pygame.key.set_repeat(600, 60)

    confetti_particles: List[Particle] = []

    for _ in range(STARTING_NUMBER_OF_SPRITES):
        sprite = make_ball()
        sprite_list.append(sprite)

    while not done:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    done = True
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_s:
                            sprite = make_ball()
                            sprite_list.append(sprite)
                        case pygame.K_d:
                            sprite_list.pop(0)
                        case pygame.K_j:
                            speed_multiplier += 0.1
                        case pygame.K_k:
                            speed_multiplier -= 0.1
                        case _:
                            pass
                case _:
                    pass

        for sprite in sprite_list:
            # Move the sprites's center
            sprite.object.x += sprite.object.change_x * speed_multiplier
            sprite.object.y += sprite.object.change_y * speed_multiplier

            # Bounce the sprites if needed: walls
            y_collided = False
            x_collided = False
            normal_vector = None
            if sprite.object.y > SCREEN_HEIGHT - sprite.pygame_image_size[1]:
                sprite.object.change_y = abs(sprite.object.change_y)
                normal_vector = pygame.Vector2(0, -1)
                y_collided = True
            elif sprite.object.y < 0:
                sprite.object.change_y = -abs(sprite.object.change_y)
                normal_vector = pygame.Vector2(0, 1)
                y_collided = True
            if sprite.object.x > SCREEN_WIDTH - sprite.pygame_image_size[0]:
                sprite.object.change_x = abs(sprite.object.change_x)
                normal_vector = pygame.Vector2(-1, 0)
                x_collided = True
            elif sprite.object.x < 0:
                sprite.object.change_x = -abs(sprite.object.change_x)
                normal_vector = pygame.Vector2(1, 0)
                x_collided = True

            if normal_vector:
                normal_vector.rotate_ip(randint(-3, 3))
                move_vector = pygame.Vector2(sprite.object.change_x, sprite.object.change_y)
                reflect_vector = move_vector.reflect(normal_vector)
                sprite.object.change_x = reflect_vector.x
                sprite.object.change_y = reflect_vector.y
                particle_vector = pygame.math.Vector2(
                    CONFETTI_PARTICLE_SPEED * speed_multiplier,
                    CONFETTI_PARTICLE_SPEED * speed_multiplier,
                )
                if y_collided and x_collided:
                    for _ in range(NUMBER_OF_CONFETTI_PARTICLES):
                        confetti_particles.append(
                            Particle(
                                (sprite.object.x, sprite.object.y),
                                particle_vector.rotate(randrange(360)),
                            ),
                        )

        screen.fill(WHITE)

        for sprite in sprite_list:
            dvd_logo_rect = pygame.Rect(
                sprite.object.x,
                sprite.object.y,
                sprite.pygame_image_size[0],
                sprite.pygame_image_size[1],
            )
            screen.blit(sprite.pygame_image, dvd_logo_rect)

        for particle in confetti_particles:
            particle.update_pos()
            offscreen_buffer = 100 # stop instant despawn
            particle_is_on_screen = (
                particle.pos[0] <= (SCREEN_DIMENSIONS[0] + offscreen_buffer)
                and particle.pos[1] <= (SCREEN_DIMENSIONS[1] + offscreen_buffer)
                and particle.pos[0] >= -offscreen_buffer
                and particle.pos[1] >= -offscreen_buffer
            )
            if not particle_is_on_screen:
                confetti_particles.remove(particle)
            else:
                pygame.draw.rect(
                    screen,
                    particle.colour,
                    (
                        particle.pos[0],
                        particle.pos[1],
                        CONFETTI_PARTICLE_SIZE,
                        CONFETTI_PARTICLE_SIZE,
                    ),
                )

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    print("""
        +------ CONTROLS ------+
        | s = spawn new tile   |
        | d = kill oldest tile |
        | j = increase speed   |
        | k = decrease speed   |
        +-------- HINT --------+
        | hold down a key to   |
        | rapidly use it       |
        +----------------------+
    """)
    main()
