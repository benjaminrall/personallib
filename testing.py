import pygame
from personallib.camera import Camera
from personallib.canvas import *
import os

# Constants
WIN_WIDTH = 800
WIN_HEIGHT = 600
FRAMERATE = 60

# Pygame Setup
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Canvas Testing")
clock = pygame.time.Clock()

# Methods
def button1():
    ui.find_element("text1").render("button1")
def button2():
    ui.find_element("text1").render("button2")
def button3():
    ui.find_element("text1").render("button3")
    ui.find_element("button4").toggle_visible()
def button4():
    ui.find_element("text1").render("button4")
    ui.find_element("button5").toggle_enabled()
def button5():
    ui.find_element("text1").render("button5")
    ui.find_element("textBox4").toggle_enabled()
def enterTextBox():
    ui.find_element("text1").render(ui.find_element("textBox4").get_text())

# Objects
cam = Camera(win, 0, 0, 1)
ui = Canvas(WIN_WIDTH, WIN_HEIGHT)
ui.add_element(Fill("fill", (0, 0, 0), 0))
ui.add_element(Text("text1", (20, 20), "georgia", 48, "test"))

button_animation = {
    "default": pygame.image.load(os.path.join("test_imgs", "default.png")),
    "hover": pygame.image.load(os.path.join("test_imgs", "hover.png")),
    "click": pygame.image.load(os.path.join("test_imgs", "click.png"))
}

ui.add_element(Button("button1", (5, 80), animation=button_animation, onClick=button1))
ui.add_element(Button("button2", (20, 200), (120, 60), Text("buttonText2", (0, 0), "georgia", 24, "click me!"), (200, 200, 200), (150, 150, 150), (100, 100, 100), onClick=button2))
ui.add_element(Button("button3", (20, 300), (120, 60), Text("buttonText3", (0, 0), "georgia", 24, "click me!"), (200, 200, 200), (150, 150, 150), (100, 100, 100), onClick=button3))
ui.add_element(Button("button4", (20, 400), (120, 60), Text("buttonText4", (0, 0), "georgia", 24, "click me!"), (200, 200, 200), (150, 150, 150), (100, 100, 100), onClick=button4))
ui.add_element(Button("button5", (20, 500), (120, 60), Text("buttonText5", (0, 0), "georgia", 24, "click me!"), (200, 200, 200), (150, 150, 150), (100, 100, 100), onClick=button5))
ui.add_element(TextBox("textBox1", (160, 100), (160, 30), Text("textBoxText1", (0, 0), "georgia", 16, "enter..."), "entered", (0, 0, 0), (250, 250, 250), "enter...", (100, 100, 100), (255, 0, 0), 5, (230, 230, 230), (200, 200, 200)))
ui.add_element(TextBox("textBox2", (160, 150), (160, 30), Text("textBoxText2", (0, 0), "georgia", 16, "enter..."), "", (0, 0, 0), (250, 250, 250), "enter...", (100, 100, 100), (0, 0, 0), 1, (230, 230, 230), (200, 200, 200)))
ui.add_element(TextBox("textBox3", (160, 200), (160, 30), Text("textBoxText3", (0, 0), "georgia", 16, "enter..."), "", (255, 0, 0), (0, 255, 0), "enter...", (200, 0, 0), (0, 0, 255), 3, (0, 150, 0), (0, 130, 0)))
ui.add_element(TextBox("textBox4", (160, 250), (160, 80), Text("textBoxText4", (0, 0), "georgia", 24, "enter..."), "", (0, 0, 0), (250, 250, 250), "enter...", (100, 100, 100), (0, 0, 0), 1, (230, 230, 230), (200, 200, 200), onEnter=enterTextBox))

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
            elif event.type == pygame.KEYDOWN:
                ui.run_method_on_type(TextBox, "input_key_event", [event])
            elif event.type == pygame.MOUSEMOTION:
                ui.run_method_on_type(Button, "hover", [pygame.mouse.get_pos()])
                ui.run_method_on_type(TextBox, "hover", [pygame.mouse.get_pos()])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    ui.run_method_on_type(Button, "click", [pygame.mouse.get_pos()])
                    ui.run_method_on_type(TextBox, "click", [pygame.mouse.get_pos()])
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    ui.run_method_on_type(Button, "hover", [pygame.mouse.get_pos()])
                    
        win.fill((255, 255, 255))

        ui.update(cam)
        
        pygame.display.update()