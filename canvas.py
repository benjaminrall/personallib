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
        self.visible = True
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

    def update(self, cam):
        self.surface.fill((0, 0, 0, 0))
        if not self.visible:
            return
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
        self.visible = True
        self.fade = [False, 0, 0, 0, 0]  # (fading, targetOpacity, increment, incrementTime, previousIncrement)

    def draw(self, surface):
        if not self.visible:
            return
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

    def set_visible(self, state):
        if self.fade[0]:
            self.opacity = self.fade[1]
            self.fade[0] = False
        self.visible = state

    def toggle_visible(self):
        self.set_visible(not self.visible)

    def fade_to(self, opacity, duration, update=0.01):
        if not self.visible:
            return
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

    def __init__(self, label, pos, font, size, text="", colour=(0,0,0), antialiasing=True):
        self.label = label
        self.x = pos[0]
        self.y = pos[1]
        self.font = pygame.font.SysFont(font, size)
        self.colour = colour
        self.visible = True
        self.render(text, colour, antialiasing)

    def render(self, text, colour=None, antialiasing=True):
        if colour is None:
            colour = self.colour
        else:
            self.colour = colour
        self.text = self.font.render(text, antialiasing, colour)

    def draw(self, surface):
        if not self.visible:
            return
        surface.blit(self.text, (self.x, self.y))

    def set_visible(self, state):
        self.visible = state

    def toggle_visible(self):
        self.set_visible(not self.visible)

# Python Button object
# A UI element that creates an interactable button
# Dependencies : pygame
class Button:
    def __init__(self, label, pos, dimensions=None, text=None, colour=None, hoverColour=None, clickColour=None, animation=None, onClick=None):
        if animation is not None and "default" not in animation:
            animation = None
        if animation is None and (dimensions is None or text is None or colour is None):
            raise Exception("Animation or all other parameters must be specified.")
        self.label = label
        self.x = pos[0]
        self.y = pos[1]
        self.animation = animation
        self.animated = animation is not None
        self.image = animation["default"] if self.animated else None
        self.width = self.image.get_width() if self.animated else dimensions[0]
        self.height= self.image.get_height() if self.animated else dimensions[1]
        self.text = text
        self.drawingColour = colour
        self.colour = colour
        self.hoverColour = hoverColour
        self.clickColour = clickColour
        self.visible = True
        self.enabled = True
        self.onClick = onClick

    def draw(self, surface):
        if not self.visible:
            return
        if self.animated:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(surface, self.drawingColour, (self.x, self.y, self.width, self.height))
            surface.blit(self.text.text, (
                self.x + (self.width / 2) - (self.text.text.get_width() / 2) + self.text.x, 
                self.y + (self.height / 2) - (self.text.text.get_height() / 2) + self.text.y
            ))

    def set_visible(self, state):
        if self.animated:
            self.image = self.animation["default"]
        else:
            self.drawingColour = self.colour
        self.visible = state

    def toggle_visible(self):
        self.set_visible(not self.visible)

    def set_enabled(self, state):
        self.enabled = state

    def toggle_enabled(self):
        self.set_enabled(not self.enabled)

    def hover(self, pos):
        if not self.visible or (self.animated and "hover" not in self.animation) or (self.hoverColour is None and not self.animated):
            return
        relX = pos[0] - self.x
        relY = pos[1] - self.y
        if self.animated:
            if 0 <= relX <= self.width and 0 <= relY <= self.height:
                self.image = self.animation["hover"]
            else:
                self.image = self.animation["default"]
        else:
            if 0 <= relX <= self.width and 0 <= relY <= self.height:
                self.drawingColour = self.hoverColour
            else:
                self.drawingColour = self.colour

    def click(self, pos):
        if not self.visible or not self.enabled:
            return
        relX = pos[0] - self.x
        relY = pos[1] - self.y
        if self.animated:
            if 0 <= relX <= self.width and 0 <= relY <= self.height:
                if self.onClick is not None:
                    self.onClick()
                if "click" in self.animation:
                    self.image = self.animation["click"]
            else:
                self.image = self.animation["default"]
        else:
            if 0 <= relX <= self.width and 0 <= relY <= self.height:
                if self.onClick is not None:
                    self.onClick()
                if self.clickColour is not None:
                    self.drawingColour = self.clickColour
            else:
                self.drawingColour = self.colour

# Python Button object
# A UI element that creates an interactable text box
# Dependencies : pygame
class TextBox:
    def __init__(self, label, pos, dimensions, text, colour, borderColour=None, borderWidth=1, hoverColour=None, activeColour=None, onEnter=None):
        self.label = label
        self.x = pos[0]
        self.y = pos[1]
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.text = text
        self.drawingColour = colour
        self.colour = colour
        self.hoverColour = hoverColour
        self.activeColour = activeColour
        self.border = borderColour is not None and borderWidth > 0
        self.borderColour = borderColour
        self.borderWidth = borderWidth if self.border else 0
        self.active = False
        self.visible = True
        self.enabled = True
        self.onEnter = onEnter
    
    def draw(self, surface):
        if self.border:
            pygame.draw.rect(surface, self.borderColour, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.drawingColour, (
            self.x + self.borderWidth, self.y + self.borderWidth, 
            self.width - (2 * self.borderWidth), self.height - (2 * self.borderWidth)
        ))
        surface.blit(self.text.text, (
            self.x + self.borderWidth + (self.text.text.get_height() / 4), self.y + (self.height / 2) - (self.text.text.get_height() / 2)
        ))
        
    def set_visible(self, state):
        self.visible = state

    def toggle_visible(self):
        self.set_visible(not self.visible)

    def set_enabled(self, state):
        self.enabled = state

    def toggle_enabled(self):
        self.set_enabled(not self.enabled)

    def hover(self, pos):
        if not self.visible or self.hoverColour is None or self.active:
            return
        relX = pos[0] - self.x
        relY = pos[1] - self.y
        if 0 <= relX <= self.width and 0 <= relY <= self.height:
            self.drawingColour = self.hoverColour
        else:
            self.drawingColour = self.colour

    def click(self, pos):
        if not self.visible or not self.enabled:
            return
        relX = pos[0] - self.x
        relY = pos[1] - self.y
        if 0 <= relX <= self.width and 0 <= relY <= self.height:
            self.active = True
            if self.activeColour is not None:
                self.drawingColour = self.activeColour
        else:
            self.active = False
            self.drawingColour = self.colour

    def input_event(self):
        pass