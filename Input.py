import pygame


class Input:
    def __init__(self, name, view, rect=pygame.Rect(200, 200, 280, 32), limit=17):
        self.active = False
        self.name = name
        self.content = ''
        self.view = view
        self.rect = rect
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.limit = limit

    def draw(self, screen):

        color = self.color_active if self.active else self.color_inactive

        pygame.draw.rect(screen, color, self.rect, 2)
        self.view.draw_text(self.name, self.rect, 'left_out')
        self.view.draw_text(self.content, self.rect, 'left_in')

    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False

    def handle_input(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.content = self.content[:-1]
        elif len(self.content) >= self.limit:
            pass
        elif 'z' >= event.unicode >= 'a' or 'Z' >= event.unicode >= 'A' or '9' >= event.unicode >= '0':
            self.content += event.unicode

    def get_content(self):
        return self.content

    def clear_content(self):
        self.content = ''
