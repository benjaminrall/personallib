import time
import pygame
import win32clipboard

# Python Canvas object
# A collection of UI elements that can be drawn to the screen in conjunction with the 2D camera controller
# Dependencies : pygame, personallib.camera
class Canvas:
    def __init__(self, width, height):
        self.elements = []
        self.width = width
        self.height = height
        self.visible = True
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

    def update(self, cam):
        if not self.visible:
            return
        self.surface.fill((0, 0, 0, 0))
        for element in self.elements:
            element.draw(self.surface)
        cam.blit(self.surface, cam.get_world_coord((0, 0)))

    def set_visible(self, state):
        self.visible = state

    def toggle_visible(self):
        self.set_visible(not self.visible)

    def add_element(self, element):
        self.elements.append(element)

    def find_element(self, label):
        for e in self.elements:
            if e.label == label:
                return e
        raise Exception(f"Element '{label}' not found")

    def run_method_on_type(self, type, method, params=[]):
        if not self.visible:
            return
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
        self.fontName = font
        self.size = size
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

# Python Text object
# A UI element that displays text on the screen
# Dependencies : pygame
class Image:
    def __init__(self, label, pos, path="", image=None):
        if image is None:
            try:
                image = pygame.image.load(path)
            except:
                raise Exception("Image or valid path must be specified.")
        self.label = label
        self.x = pos[0]
        self.y = pos[1]
        self.image = image
        self.visible = True

    def draw(self, surface):
        if not self.visible:
            return
        surface.blit(self.image, (self.x, self.y))

    def set_path(self, path):
        try:
            self.image = pygame.image.load(path)
        except:
            raise Exception("Invalid path specified.")

    def set_image(self, image):
        self.image = image

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
        if self.animated:
            self.image = self.animation["default"]
        else:
            self.drawingColour = self.colour
        self.enabled = state

    def toggle_enabled(self):
        self.set_enabled(not self.enabled)

    def hover(self, pos):
        if not self.enabled or not self.visible or (self.animated and "hover" not in self.animation) or (self.hoverColour is None and not self.animated):
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
# Dependencies : pygame, time, pywin32
class TextBox:

    VALID_KEYS = [
        pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
        pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p,
        pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_z, 
        pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_m, pygame.K_SPACE, pygame.K_EXCLAIM, pygame.K_HASH, 
        pygame.K_DOLLAR, pygame.K_AMPERSAND, pygame.K_LEFTPAREN, pygame.K_RIGHTPAREN, pygame.K_ASTERISK, pygame.K_PLUS,
        pygame.K_COMMA, pygame.K_MINUS, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_COLON, pygame.K_SEMICOLON, pygame.K_LESS,
        pygame.K_GREATER, pygame.K_EQUALS, pygame.K_QUESTION, pygame.K_AT, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET, 
        pygame.K_BACKSLASH, pygame.K_CARET, pygame.K_UNDERSCORE, pygame.K_BACKQUOTE
    ]

    def __init__(self, label, pos, dimensions, text, textContents, textColour, colour, placeholderText = "",
                 placeholderColour=None, borderColour=None, borderWidth=1, hoverColour=None, activeColour=None,
                 cursorSpeed = 0.5, onEnter=None):
        self.label = label
        self.x = pos[0]
        self.y = pos[1]
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.text = text
        self.frontText = None
        self.endText = None
        self.textContents = textContents
        self.textColour = textColour
        self.placeholderText = placeholderText
        self.placeholderColour = placeholderColour
        self.placeholder = self.placeholderText != "" and self.placeholderColour is not None
        self.drawingColour = colour
        self.colour = colour
        self.hoverColour = hoverColour
        self.activeColour = activeColour
        self.border = borderColour is not None and borderWidth > 0
        self.borderColour = borderColour
        self.borderWidth = borderWidth if self.border else 0
        self.cursorPos = len(self.textContents)
        self.cursorVisible = False
        self.cursorTime = 0
        self.cursorSpeed = cursorSpeed
        self.contents = pygame.Surface((self.width - (2 * self.borderWidth), self.height - (2 * self.borderWidth)), pygame.SRCALPHA)
        self.active = False
        self.visible = True
        self.enabled = True
        self.onEnter = onEnter
        self.update_text()
    
    def draw(self, surface):
        self.contents.fill((0, 0, 0, 0))
        if self.border:
            pygame.draw.rect(surface, self.borderColour, (self.x, self.y, self.width, self.height))
        self.contents.fill(self.drawingColour)
        self.contents.blit(self.frontText, (
            (self.frontText.get_height() / 4), (self.height / 2) - (self.frontText.get_height() / 2) - self.borderWidth
        ))
        self.contents.blit(self.endText, (
            (self.frontText.get_height() / 4) + self.frontText.get_width(),
            (self.height / 2) - (self.endText.get_height() / 2) - self.borderWidth
        ))
        if self.active and self.cursorVisible:
            pygame.draw.rect(self.contents, self.textColour, (
                (self.frontText.get_height() / 4) + self.frontText.get_width(),
                (self.height / 2) - (self.frontText.get_height() / 2) - self.borderWidth, 2, self.frontText.get_height()
            ))
        surface.blit(self.contents, (self.x + self.borderWidth, self.y + self.borderWidth))
        
    def set_visible(self, state):
        self.active = False
        self.drawingColour = self.colour
        self.visible = state

    def toggle_visible(self):
        self.set_visible(not self.visible)

    def set_enabled(self, state):
        self.active = False
        self.drawingColour = self.colour
        self.enabled = state

    def toggle_enabled(self):
        self.set_enabled(not self.enabled)

    def get_text(self):
        return self.textContents

    def clear_text(self):
        self.set_text("")

    def set_text(self, text):
        self.textContents = text
        self.cursorPos = len(text)
        self.update_text()

    def update_text(self):
        usePlaceholder = self.placeholder and self.textContents == ""
        if usePlaceholder:
            self.text.render(self.textContents[:self.cursorPos], self.textColour)
            self.frontText = self.text.text
            self.text.render(self.placeholderText, self.placeholderColour)
            self.endText = self.text.text
        else:
            self.text.render(self.textContents[:self.cursorPos], self.textColour)
            self.frontText = self.text.text
            self.text.render(self.textContents[self.cursorPos:], self.textColour)
            self.endText = self.text.text

    def enable_cursor(self):
        self.cursorVisible = True
        self.cursorTime = time.time()

    def update_cursor(self):
        if not self.active or not self.enabled or not self.visible:
            return
        if time.time() - self.cursorTime > self.cursorSpeed:
            self.cursorVisible = not self.cursorVisible
            self.cursorTime = time.time()

    def hover(self, pos):
        if not self.enabled or not self.visible or self.hoverColour is None or self.active:
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
            self.enable_cursor()
            if self.activeColour is not None:
                self.drawingColour = self.activeColour
        else:
            self.active = False
            self.drawingColour = self.colour

    def input_key_event(self, event):
        if not self.active or event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.active = False
            self.drawingColour = self.colour
        elif event.key == pygame.K_TAB:
            self.textContents = self.textContents[:self.cursorPos] + "    " + self.textContents[self.cursorPos:]
            self.cursorPos += 4
        elif event.key == pygame.K_DELETE:
            if self.cursorPos < len(self.textContents):
                self.textContents = self.textContents[:self.cursorPos] + self.textContents[self.cursorPos + 1:]
        elif event.key == pygame.K_RETURN:
            if self.onEnter is not None:
                self.onEnter()
            self.active = False
            self.drawingColour = self.colour
        elif event.key == pygame.K_BACKSPACE:
            if self.cursorPos > 0:
                toRemove = 1
                if pygame.key.get_mods() & pygame.K_LCTRL:
                    foundNonSpace = False
                    toRemove = 0
                    for char in reversed(self.textContents[:self.cursorPos]):
                        if char == ' ' and foundNonSpace:
                            break
                        elif char != ' ':
                            foundNonSpace = True
                        toRemove += 1
                self.textContents = self.textContents[:self.cursorPos - toRemove] + self.textContents[self.cursorPos:]
                self.cursorPos -= toRemove
        elif event.key == pygame.K_LEFT:
            if pygame.key.get_mods() & pygame.K_LCTRL:
                foundNonSpace = False
                toJump = 0
                for char in reversed(self.textContents[:self.cursorPos]):
                    if char == ' ' and foundNonSpace:
                        break
                    elif char != ' ':
                        foundNonSpace = True
                    toJump += 1
                self.cursorPos -= toJump
            else:
                self.cursorPos = max(0, self.cursorPos - 1)
        elif event.key == pygame.K_RIGHT:
            if pygame.key.get_mods() & pygame.K_LCTRL:
                foundNonSpace = False
                toJump = 0
                for char in self.textContents[self.cursorPos:]:
                    if char == ' ' and foundNonSpace:
                        break
                    elif char != ' ':
                        foundNonSpace = True
                    toJump += 1
                self.cursorPos += toJump
            else:
                self.cursorPos = min(len(self.textContents), self.cursorPos + 1)
        elif event.key == pygame.K_HOME or event.key == pygame.K_DOWN:
            self.cursorPos = 0
        elif event.key == pygame.K_END or event.key == pygame.K_UP:
            self.cursorPos = len(self.textContents)
        elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.K_LCTRL:
            win32clipboard.OpenClipboard(0)
            try:
                result = str(win32clipboard.GetClipboardData()).replace("\n", "")
            except TypeError:
                result = ''
            win32clipboard.CloseClipboard()
            self.textContents = self.textContents[:self.cursorPos] + result + self.textContents[self.cursorPos:]
            self.cursorPos += len(result)
        elif event.key in TextBox.VALID_KEYS and not pygame.key.get_mods() & pygame.K_LCTRL:
            self.textContents = self.textContents[:self.cursorPos] + event.unicode + self.textContents[self.cursorPos:]
            self.cursorPos += 1
        self.enable_cursor()
        self.update_text()

# Python Button object
# A UI element that creates an interactable slider
# Dependencies : pygame
class Slider:
    def __init__(self, label, pos, dimensions, sliderColour, notchSize, notchColour):
        pass
