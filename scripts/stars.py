class Stars:
    # https://youtu.be/2gABYM5M0ww
    # adapted technique for moving background elements
    def __init__(self, pos, img, speed):
        self.pos = list(pos)
        self.img = img
        self.speed = speed

    def update(self):
        self.pos[0] += self.speed

    def render(self, surf):
        render_x = self.pos[0]
        render_y = self.pos[1]

        w = self.img.get_width()
        x = render_x % w

        surf.blit(self.img, (x - w, render_y))
        surf.blit(self.img, (x, render_y))