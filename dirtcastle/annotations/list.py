import functools

from .base import Annotation
from .span import Span


class AnnotationList(list):
    
    def __init__(self, iterable=()):
        self._cells = None
        for annotation in iterable:
            self.append(annotation)

    def extend(self, new_annotations):
        for annotation in new_annotations:
            self.append(annotation)

    def append(self, new_annotation):
        i = 0
        for i, annotation in enumerate(self):
            if new_annotation.span < annotation.span:
                break
        else:  # no break
            i += 1
        self._cells = None
        return super().insert(i, new_annotation)

    def select_from_position(self, position):
        for index, annotation in enumerate(self):
            if annotation.span.start >= position:
                yield from self[index:]
                break

    def collisions(self, position):
        if isinstance(position, Annotation):
            position = position.span.end

        collisions = set()

        for annotation in self.select_from_position(position):
            if not collisions:
                # the first annotation gets a free pass
                collisions.add(annotation)
                shortest_collision = annotation
            else:
                # new annotations must collide with the shortest
                # annotation in the collision list
                if annotation.span not in shortest_collision.span:
                    return collisions
                if annotation.span.length < shortest_collision.span.length:
                    shortest_collision = annotation
                collisions.add(annotation)

        return collisions

    def combinations(self):
        """Yields all possible non-colliding combinations"""
        self._subcombination_cache = {}
        for root_annotation in self.collisions(0):
            yield from self._subcombinations(root_annotation)
        del self._subcombination_cache

    def _subcombinations(self, annotation):
        if annotation not in self._subcombination_cache:
            paths = []
            next_collisions = self.collisions(annotation)
            if not next_collisions:
                paths.append((annotation,))
            else:
                for collision in next_collisions:
                    for path in self._subcombinations(collision):
                        paths.append((annotation,) + path)
            self._subcombination_cache[annotation] = paths
        return self._subcombination_cache[annotation]

    def disambiguate(self, discard_others=False):
        """Computes the best total-scoring set of annotations to keep
        and discards the others.
        """
        best_score = 0
        best_combination = []

        for combination in self.combinations():
            score = sum([annotation.score for annotation in combination])
            if score > best_score:
                best_combination = combination
                best_score = score

        if discard_others:
            # make a copy of self in order to prevent a bug where some
            # items are not iterated when an item is removed
            for annotation in list(self):
                if annotation not in best_combination:
                    self.remove(annotation)

        return best_combination

    @property
    def cells(self):
        """Groups annotations into possible table cells.

        TODO: place annotations in cells on-the-go instead of complete
              recomputation on addition
        """
        if self._cells is None:
            cells = [AnnotationList(self.collisions(0))]

            while len(cells[-1]) > 0:
                next_position = min([
                    annotation.span.end for annotation in cells[-1]
                ])
                cells.append(AnnotationList(self.collisions(next_position)))

            self._cells = cells[:-1]
        return self._cells

    def boost(self, multiplier):
        for annotation in self:
            annotation.score *= multiplier

    def filter(self, **kwargs):
        sublist = AnnotationList()
        for index, annotation in enumerate(self):
            for key, value in kwargs.items():
                if getattr(annotation, key) != value:
                    break
            else:  # no break
                # prevent re-doing ordering (the data is already ordered)
                sublist.insert(index, annotation)
        return sublist

    def copy(self):
        return AnnotationList([a.copy() for a in self])
