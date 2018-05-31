import functools
import math

from .base import CellStrategy


class NearbyTypeStrategy(CellStrategy):

    def __init__(self, max_boost, min_boost, v_reach, h_reach):
        self.max_boost = max_boost
        self.min_boost = min_boost
        self.boost = self.max_boost - self.min_boost

        self.v_reach = v_reach
        self.h_reach = h_reach

        self.min_reach = 1
        self.max_reach = math.sqrt(self.h_reach**2 + self.v_reach**2)
        self.reach = self.max_reach - self.min_reach

    def compute_boost(self, dx, dy):
        dx = abs(dx)
        dy = abs(dy)

        if (dx == 0 and dy == 0) or dx > self.h_reach or dy > self.v_reach:
            return 1.0

        return self._compute_boost(
            dx=min(dx, dy),
            dy=max(dx, dy),
        )

    @functools.lru_cache(256)
    def _compute_boost(self, dx, dy):
        distance = math.sqrt(dx**2 + dy**2)
        factor = 1 - (distance - self.min_reach) / self.reach
        return self.min_boost + factor * self.boost

    def apply_to_annotation(self, text, line, annotation, x, y):
        for dx in range(-self.h_reach, self.h_reach+1):
            for dy in range(-self.v_reach, self.v_reach+1):
                if dx == 0 and dy == 0:
                    continue
                try:
                    boost = self.compute_boost(dx, dy)
                    text.lines[y+dy] \
                        .cells[x+dx] \
                        .filter(type=annotation.type) \
                        .boost(boost)
                except IndexError:
                    continue
