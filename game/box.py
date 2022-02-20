
import pygame
from .camera import Camera
from .math import Vector3
from .actor import Actor


class Box(Actor):
    def __init__(self, **kargs) -> None:
        super().__init__(**kargs)

        self.size = Vector3(60, 60, 60)

    
    def transform(self, camera: Camera) -> None:
        super().transform(camera)

        points = [
            Vector3(self.size.x / 2 *  1, self.size.y / 2 *  1, 0),
            Vector3(self.size.x / 2 *  1, self.size.y / 2 * -1, 0),
            Vector3(self.size.x / 2 * -1, self.size.y / 2 * -1, 0),
            Vector3(self.size.x / 2 * -1, self.size.y / 2 *  1, 0),
            Vector3(self.size.x / 2 *  1, self.size.y / 2 *  1, self.size.z),
            Vector3(self.size.x / 2 *  1, self.size.y / 2 * -1, self.size.z),
            Vector3(self.size.x / 2 * -1, self.size.y / 2 * -1, self.size.z),
            Vector3(self.size.x / 2 * -1, self.size.y / 2 *  1, self.size.z)
        ]

        self.points_t = [camera.transform(p + self.position).xy for p in points]


    def draw(self, screen: pygame.surface.Surface):
        super().draw(screen)
        pygame.draw.line(screen, 'blue', self.points_t[2], self.points_t[2 + 4], 2)
        pygame.draw.polygon(screen, 'red', self.points_t[:4])
        pygame.draw.line(screen, 'blue', self.points_t[0], self.points_t[0 + 4], 2)
        pygame.draw.line(screen, 'blue', self.points_t[1], self.points_t[1 + 4], 2)
        pygame.draw.line(screen, 'blue', self.points_t[3], self.points_t[3 + 4],2 )
        pygame.draw.polygon(screen, 'green', self.points_t[4:], 2)
        pygame.draw.circle(screen, 'white', self.screen_position.xy, 3)