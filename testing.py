import pygame
from personallib.camera import Camera
from personallib.canvas import *

# Constants
WIN_WIDTH = 800
WIN_HEIGHT = 600
FRAMERATE = 60

# Pygame Setup
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("NAME")
clock = pygame.time.Clock()

# Methods
def button1():
    ui.find_element("text1").render("button1")
def button2():
    ui.find_element("text1").render("button2")
def button3():
    ui.find_element("text1").render("button3")
def button4():
    ui.find_element("text1").render("button4")
def button5():
    ui.find_element("text1").render("button5")

# Objects
cam = Camera(win, 0, 0, 1)
ui = Canvas(WIN_WIDTH, WIN_HEIGHT)
ui.add_element(Fill("fill", (0, 0, 0), 0))
ui.add_element(Text("text1", 20, 20, "georgia", 48, "test"))
ui.add_element(Button("button1", 200, 100, 120, 60, Text("buttonText1", 0, 0, "georgia", 20, "click me!"), (200, 200, 200), (150, 150, 150), (100, 100, 100), function=button1))
ui.add_element(Button("button2", 200, 200, 120, 60, Text("buttonText2", 0, 0, "georgia", 20, "click me!"), (200, 200, 200), (150, 150, 150), (100, 100, 100), function=button2))
ui.add_element(Button("button3", 200, 300, 120, 60, Text("buttonText3", 0, 0, "georgia", 20, "click me!"), (200, 200, 200), (150, 150, 150), (100, 100, 100), function=button3))
ui.add_element(Button("button4", 200, 400, 120, 60, Text("buttonText4", 0, 0, "georgia", 20, "click me!"), (200, 200, 200), (150, 150, 150), (100, 100, 100), function=button4))
ui.add_element(Button("button5", 200, 500, 120, 60, Text("buttonText5", 0, 0, "georgia", 20, "click me!"), (200, 200, 200), (150, 150, 150), (100, 100, 100), function=button5))

# Variables
running = True

# Main Loop
if __name__ == '__main__':
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEMOTION:
                ui.run_method_on_type(Button, "hover", [pygame.mouse.get_pos()])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    ui.run_method_on_type(Button, "click", [pygame.mouse.get_pos()])
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    ui.run_method_on_type(Button, "hover", [pygame.mouse.get_pos()])
                    
        win.fill((255, 255, 255))

        ui.update(cam)
        
        pygame.display.update()