import pygame

# Python camera controller script
# Manages camera functionality including panning and zooming the camera
# Relies on : pygame
class Camera:
    def __init__(self, win, x, y, zoom):
        self.zoom = zoom                        # Camera zoom such that zoom = pixels per coordinate increment
        self.win = win                          # Pygame window to draw onto
        self.winWidth = win.get_width()         # Pygame window width
        self.winHeight =  win.get_height()      # Pygame window height
        self.width = self.winWidth / zoom       # Width of camera view
        self.height = self.winHeight / zoom     # Height of camera view
        self.x = x                              # X position of camera in world space
        self.y = y                              # Y position of camera in world space
        self.smoothing = 0                      # Smoothing for camera follow

    # Draws a rectangle to the screen
    def draw_rect(self, rect, colour):
        r = self.get_screen_rect(rect)
        if self.rect_in_bounds(rect):
            pygame.draw.rect(self.win, colour, r)

    # Checks if a given rectangle is inside of the current camera view
    def rect_in_bounds(self, rect):
        return (rect[0] <= self.x + (self.width / 2)) and (rect[0] + rect[2] >= self.x - (self.width / 2)) and (rect[1] + rect[3] >= self.y - (self.height / 2)) and (rect[1] <= self.y + (self.height / 2))

    # Gets the coordinates and dimensions of a given rectangle as screen coordinates
    def get_screen_rect(self, rect):
        w = rect[2] * self.zoom
        h = rect[3] * self.zoom
        x = (-self.x * self.zoom) + ((rect[0] + (self.width / 2)) * self.zoom)
        y = (-self.y * self.zoom) + ((rect[1] + (self.height / 2)) * self.zoom)
        return (x, y, w, h)

    # Draws a circle to the screen
    def draw_circle(self, centre, radius, colour):
        c, r = self.get_screen_circle(centre, radius)
        if self.circle_in_bounds(centre, radius):
            pygame.draw.circle(self.win, colour, c, r)

    # Checks if a given circle is inside of the current camera view
    def circle_in_bounds(self, centre, radius):
        return (centre[0] - radius <= self.x + (self.width / 2)) and (centre[0] + radius >= self.x - (self.width / 2)) and (centre[1] + radius >= self.y - (self.height / 2)) and (centre[1] - radius <= self.y + (self.height / 2))

    # Gets the centre coordinates and radius of a given circle as screen coordinates
    def get_screen_circle(self, centre, radius):
        r = radius * self.zoom
        x = (-self.x * self.zoom) + ((centre[0] + (self.width / 2)) * self.zoom)
        y = (-self.y * self.zoom) + ((centre[1] + (self.height / 2)) * self.zoom)
        return (x, y), r

    # Zooms out the camera by one step
    def zoom_out(self):
        self.zoom = max(self.zoom / 2, 1)
        self.width = self.winWidth / self.zoom
        self.height = self.winHeight / self.zoom
    
    # Zooms in the camera by one step
    def zoom_in(self):
        self.zoom = min(self.zoom * 2, 1024)
        self.width = self.winWidth / self.zoom
        self.height = self.winHeight / self.zoom
    
    # Pans the camera by a given amount
    def pan(self, pos):
        self.x -= pos[0] / self.zoom
        self.y -= pos[1] / self.zoom
        
    # Moves camera towards a given point with some smoothing
    def follow(self, pos, smoothing = None):
        if smoothing == None:
            smoothing = self.smoothing
        self.x = self.lerp(self.x, pos[0], abs(smoothing - 1))
        self.y = self.lerp(self.y, pos[1], abs(smoothing - 1))

    # Linear interpolation for following function
    def lerp(self, a, b, w):
        return a + w * (b - a)

    # Sets boundaries for camera position
    def set_bounds(self, x, y):
        pass

    # Enforces set camera boundaries
    def enforce_bounds(pos, x, y):
        pass