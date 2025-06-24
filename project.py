import pygame
import math
import multiprocessing as mp
from elements_config import ELEMENTS, SHELLS_CAPACITY, MAX_ATOMIC_NUM
from pygame.locals import *


WIDTH, HEIGHT = 700, 500
FPS = 60
QUEUE = mp.Queue()


def total_electrons(config):
    return sum(config)


def get_shell_label(index):
    return chr(75 + index)


def calculate_configuration(atomic_number):
    remaining = atomic_number
    config = []
    for shell in SHELLS_CAPACITY:
        if remaining == 0:
            break
        electrons = min(remaining, shell)
        config.append(electrons)
        remaining -= electrons
    return config


def table_window(queue):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Periodic Table and Slider")
    font = pygame.font.SysFont("Arial", 20)
    clock = pygame.time.Clock()

    slider_value = 1
    dragging = False
    slider_rect = pygame.Rect(
        WIDTH // 20, HEIGHT - HEIGHT // 12, WIDTH - WIDTH // 10, HEIGHT // 30
    )

    cell_size = WIDTH // 20
    offset_x = WIDTH // 40
    offset_y = HEIGHT // 20

    running = True
    while running:
        screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                queue.put(None)
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if slider_rect.collidepoint(event.pos):
                    dragging = True
                for elem in ELEMENTS:
                    x, y = elem["pos"]
                    rect = pygame.Rect(
                        offset_x + x * cell_size,
                        offset_y + y * cell_size,
                        cell_size,
                        cell_size,
                    )
                    if rect.collidepoint(event.pos):
                        slider_value = elem["atomic_number"]
                        queue.put(slider_value)
            elif event.type == MOUSEBUTTONUP:
                dragging = False
            elif event.type == MOUSEMOTION and dragging:
                relative_x = mouse_pos[0] - slider_rect.x
                relative_x = max(0, min(relative_x, slider_rect.w))
                slider_value = (
                    int((relative_x / slider_rect.w) * (MAX_ATOMIC_NUM - 1)) + 1
                )
                queue.put(slider_value)

        # Draw periodic table cells
        for elem in ELEMENTS:
            x, y = elem["pos"]
            rect = pygame.Rect(
                offset_x + x * cell_size, offset_y + y * cell_size, cell_size, cell_size
            )
            color = (
                (255, 100, 100)
                if elem["atomic_number"] == slider_value
                else (80, 80, 80)
            )
            pygame.draw.rect(screen, color, rect)
            text = font.render(elem["symbol"], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        # Draw slider background
        pygame.draw.rect(screen, (180, 180, 180), slider_rect)
        # Draw slider handle
        handle_x = int(
            slider_rect.x + ((slider_value - 1) / (MAX_ATOMIC_NUM - 1)) * slider_rect.w
        )
        pygame.draw.rect(
            screen,
            (50, 150, 255),
            pygame.Rect(handle_x - 10, slider_rect.y - 5, 20, slider_rect.h + 10),
        )
        element_name = next(
            (e["name"] for e in ELEMENTS if e["atomic_number"] == slider_value),
            "Unknown",
        )
        name_label = font.render(element_name, True, (255, 255, 255))
        screen.blit(
            name_label,
            (
                slider_rect.x + slider_rect.w // 2 - name_label.get_width() // 2,
                slider_rect.y - 55,
            ),
        )
        # Draw slider label
        label = font.render(f"Atomic Number: {slider_value}", True, (255, 255, 255))
        screen.blit(
            label,
            (
                slider_rect.x + slider_rect.w // 2 - label.get_width() // 2,
                slider_rect.y - 30,
            ),
        )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def visualizer_window(queue):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 150))
    pygame.display.set_caption("Atom Visualizer")
    font = pygame.font.SysFont("Arial", 20)
    clock = pygame.time.Clock()

    angle_offsets = [0 for _ in SHELLS_CAPACITY]
    atomic_number = 1
    configuration = calculate_configuration(atomic_number)
    center = (WIDTH - 450, HEIGHT // 2)
    running = True

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Check for updates from slider
        while not queue.empty():
            msg = queue.get()
            if msg is None:
                running = False
                break
            atomic_number = msg
            configuration = calculate_configuration(atomic_number)
            angle_offsets = [0 for _ in SHELLS_CAPACITY]

        # Draw nucleus
        pygame.draw.circle(screen, (255, 215, 0), center, 10)
        # Draw electron shells and electrons
        for i, e_count in enumerate(configuration):
            radius = 32 * (i + 1)
            pygame.draw.circle(screen, (100, 100, 255), center, radius, 2)
            for j in range(e_count):
                angle = 2 * math.pi * j / e_count + angle_offsets[i]
                x = center[0] + radius * math.cos(angle)
                y = center[1] + radius * math.sin(angle)
                pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 6)
            angle_offsets[i] += 0.005 * (i + 1)

        # Draw energy bars
        x_start = WIDTH - 300
        y_start = HEIGHT // 2 + 200
        max_electrons = max(SHELLS_CAPACITY)
        for i, electrons in enumerate(configuration):
            bar_height = int((electrons / max_electrons) * 150)
            bar_rect = pygame.Rect(
                x_start + i * 40, y_start + 150 - bar_height, 30, bar_height
            )
            pygame.draw.rect(screen, (50, 200, 50), bar_rect)
            shell_label = chr(75 + i)  # Starting from 'K' shell
            label = font.render(shell_label, True, (255, 255, 255))
            screen.blit(label, (bar_rect.x + 5, y_start + 160))
            count_label = font.render(str(electrons), True, (255, 255, 255))
            screen.blit(count_label, (bar_rect.x + 5, bar_rect.y - 30))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def main():
    process1 = mp.Process(target=table_window, args=(QUEUE,))
    process2 = mp.Process(target=visualizer_window, args=(QUEUE,))
    process1.start()
    process2.start()
    process1.join()
    process2.join()


if __name__ == "__main__":
    try:
        mp.set_start_method("spawn")
    except RuntimeError:
        pass  # context already set
    main()
