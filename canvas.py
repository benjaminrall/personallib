import time
import pygame

# Python Canvas object
# A collection of UI elements that can be drawn to the screen in conjunction with the 2D camera controller
# Dependencies : pygame, personallib.camera
class Canvas:
    def __init__(self, width, height):
        self.elements =[]
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

    def update(self, cam):
        self.surface.fill((0, 0, 0, 0))
        for element in self.elements:
            element.draw(self.surface)
        cam.blit(self.surface, cam.get_world_coord((0, 0)))

    def add_element(self, element):
        self.elements.append(element)

    def find_element(self, label):
        for e in self.elements:
            if e.label == label:
                return e
        raise Exception(f"Element '{label}' not found")

    def run_method_on_type(self, type, method, params=[]):
        for element in self.elements:
            if isinstance(element, type):
                getattr(element, method)(*params)

# Python Fill object
# A UI element that fills the screen with a given colour and can fade in and out
# Dependencies : pygame, time
class Fill:
    def __init__(self, label, colour, opacity):
        if not isinstance(colour, tuple) or len(colour) != 3 or min(colour) < 0 or max(colour) > 255:
            raise Exception("Invalid colour given")
        if opacity < 0 or opacity > 1:
            raise Exception("Invalid opacity given")
        self.label = label
        self.colour = colour
        self.opacity = opacity
        self.fade = [False, 0, 0, 0, 0]  # (fading, targetOpacity, increment, incrementTime, previousIncrement)

    def draw(self, surface):
        if self.fade[0]:
            timeChange = time.time() - self.fade[4]
            if timeChange >= self.fade[3]:
                self.opacity += self.fade[2]
                if round(self.opacity, 10) == self.fade[1]:
                    self.opacity = self.fade[1]
                    self.fade[0] = False
                else:
                    self.fade[4] += timeChange - self.fade[3]
        surface.fill((self.colour[0], self.colour[1], self.colour[2], self.opacity * 255))

    def fade_to(self, opacity, duration, update=0.01):
        if opacity < 0 or opacity > 1:
            raise Exception("Invalid opacity given")
        if self.fade[0]:
            self.opacity = self.fade[1]
        increment = (opacity - self.opacity) / (duration / update)
        self.fade = [True, opacity, increment, update, time.time()]

# Python Text object
# A UI element that displays text on the screen
# Dependencies : pygame
class Text:

    pygame.font.init()

    def __init__(self, label, x, y, font, size, text="", colour=(0,0,0), antialiasing=True):
        self.label = label
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(font, size)
        self.colour = colour
        self.render(text, colour, antialiasing)

    def render(self, text, colour=None, antialiasing=True):
        if colour is None:
            colour = self.colour
        else:
            self.colour = colour
        self.text = self.font.render(text, antialiasing, colour)

    def draw(self, surface):
        surface.blit(self.text, (self.x, self.y))

# Python Button object
# A UI element that creates an interactable button
# Dependencies : pygame
class Button:
    def __init__(self, label, x, y, width=None, height=None, text=None, colour=None, hoverColour=None, clickColour=None, animation=None, function=None):
        if animation is not None and "default" not in animation:
            animation = None
        if animation is None and (width is None or height is None or text is None or colour is None):
            raise Exception("Animation or all other parameters must be specified.")
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height= height
        self.text = text
        self.drawingColour = colour
        self.colour = colour
        self.hoverColour = hoverColour
        self.clickColour = clickColour
        self.animation = animation
        self.animated = animation is not None
        self.function = function

    def draw(self, surface):
        if self.animated:
            pass
        else:
            pygame.draw.rect(surface, self.drawingColour, (self.x, self.y, self.width, self.height))
            surface.blit(self.text.text, (
                self.x + (self.width / 2) - (self.text.text.get_width() / 2) + self.text.x, 
                self.y + (self.height / 2) - (self.text.text.get_height() / 2) + self.text.y
            ))

    def hover(self, pos):
        if (self.animation is not None and "hover" not in self.animation) or self.hoverColour is None:
            return
        relX = pos[0] - self.x
        relY = pos[1] - self.y
        if self.animated:
            pass
        else:
            if 0 <= relX <= self.width and 0 <= relY <= self.height:
                self.drawingColour = self.hoverColour
            else:
                self.drawingColour = self.colour

    def click(self, pos):
        relX = pos[0] - self.x
        relY = pos[1] - self.y
        if self.animated:
            if 0 <= relX <= self.width and 0 <= relY <= self.height:
                if self.function is not None:
                    self.function()
        else:
            if 0 <= relX <= self.width and 0 <= relY <= self.height:
                if self.function is not None:
                    self.function()
                if self.clickColour is not None:
                    self.drawingColour = self.clickColour
            else:
                self.drawingColour = self.colour  