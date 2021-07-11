import pygame
import personallib.maths as maths

# Python 2D camera controller script
# Manages camera functionality including panning and zooming the camera
# Dependencies : pygame, personallib.maths
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
        self.bounds = ()                        # Coordinates for the camera follow boundaries
        self.active_bounds = (False, False,     # Toggle whether the camera follow boundaries should be enforced
                              False, False)

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

    # Draws a line to the screen
    def draw_line(self, start, end, colour, width = 1):
        x = min(start[0], end[0])
        y = min(start[1], end[1])
        w = max(start[0], end[0]) - x
        h = max(start[1], end[1]) - y
        rect = (x, y, w, h)
        if self.rect_in_bounds(rect):
            pygame.draw.line(self.win, colour, self.get_screen_coord(start), self.get_screen_coord(end), width)

    def draw_polygon(self, points, colour):
        screenPoints = [ self.get_screen_coord(point) for point in points]
        pygame.draw.polygon(self.win, colour, screenPoints)

    # Gets the given coordinate as a screen coordinate
    def get_screen_coord(self, coord):
        x = (-self.x * self.zoom) + ((coord[0] + (self.width / 2)) * self.zoom)
        y = (-self.y * self.zoom) + ((coord[1] + (self.height / 2)) * self.zoom)
        return (x, y)

    # Gets the given coordinate as a world coordinate
    def get_world_coord(self, coord):
        centre = (self.width / 2, self.height / 2)
        x = ((coord[0] - (self.width / 2 * self.zoom))) / self.zoom
        y = ((coord[1] - (self.height / 2 * self.zoom))) / self.zoom
        return (x, y)

    # Blits a surface onto the screen
    def blit(self, source, dest, area = None): 
        if self.rect_in_bounds(source.get_rect(topleft=dest)):
            self.win.blit(source, self.get_screen_coord(dest), area=area)

    # Zooms out the camera by set amount
    def zoom_out(self, amount, limit = 1):
        self.zoom = max(self.zoom - amount, max(limit, 1))
        self.width = self.winWidth / self.zoom
        self.height = self.winHeight / self.zoom
    
    # Zooms in the camera by set amount
    def zoom_in(self, amount, limit = 1024):
        self.zoom = min(self.zoom + amount, min(limit, 1024))
        self.width = self.winWidth / self.zoom
        self.height = self.winHeight / self.zoom

    # Zooms out the camera by one step
    def zoom_out_step(self, limit = 1):
        self.zoom = max(self.zoom / 2, max(limit, 1))
        print(self.zoom)
        self.width = self.winWidth / self.zoom
        self.height = self.winHeight / self.zoom
    
    # Zooms in the camera by one step
    def zoom_in_step(self, limit = 1024):
        self.zoom = min(self.zoom * 2, min(limit, 1024))
        self.width = self.winWidth / self.zoom
        self.height = self.winHeight / self.zoom
    
    # Pans the camera by a given amount
    def pan(self, pos):
        self.x -= pos[0] / self.zoom
        self.y -= pos[1] / self.zoom
        
    # Moves camera towards a given point with some smoothing
    def follow(self, pos, offset = (0, 0), smoothing = None):
        if smoothing == None:
            smoothing = self.smoothing
        self.x = maths.lerp(self.x, pos[0] + offset[0], smoothing)
        self.y = maths.lerp(self.y, pos[1] + offset[1], smoothing)
        if self.active_bounds:
            self.enforce_bounds()

    # Sets boundaries for camera position
    def set_bounds(self, pos1 = (0, 0), pos2 = (0, 0), active = (True, True, True, True)):
        self.active_bounds = active
        self.bounds = ((pos1[0], pos1[1]), (pos2[0], pos2[1]))

    # Enforces set camera boundaries
    def enforce_bounds(self):
        if self.active_bounds[0] and self.x - (self.width / 2) <= self.bounds[0][0]:
            self.x = self.bounds[0][0] + (self.width / 2)
        if self.active_bounds[1] and self.x + (self.width / 2) >= self.bounds[1][0]:
            self.x = self.bounds[1][0] - (self.width / 2)
        if self.active_bounds[2] and self.y - (self.height / 2) <= self.bounds[0][1]:
            self.y = self.bounds[0][1] + (self.height / 2)
        if self.active_bounds[3] and self.y + (self.height / 2) >= self.bounds[1][1]:
            self.y = self.bounds[1][1] - (self.height / 2)