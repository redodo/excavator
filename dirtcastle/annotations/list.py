from .base import Annotation
from .span import Span


class AnnotationList(list):
    
    def __init__(self, iterable=()):
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
        return super().insert(i, new_annotation)

    def select_from_position(self, position):
        for index, annotation in enumerate(self):
            if annotation.span.start >= position:
                yield from self[index:]
                break

    def collisions_at(self, position):
        if isinstance(position, Annotation):
            position = position.span.end + 1

        annotations = self.select_from_position(position)
        collisions = set()
        for annotation in annotations:
            if not collisions:
                # the first annotation gets a free pass
                collisions.add(annotation)
            else:
                # following annotations must collide with all the annotations
                # of the collision set
                for collision in collisions:
                    if annotation.span not in collision.span:
                        # annotation does not collide, return the collisions
                        return collisions
                collisions.add(annotation)

        return collisions

    def combinations(self):
        """Yields all possible non-colliding combinations"""
        self._subcombination_cache = {}
        for root_annotation in self.collisions_at(0):
            yield from self._subcombinations(root_annotation)
        del self._subcombination_cache

    def _subcombinations(self, annotation):
        if annotation not in self._subcombination_cache:
            paths = []
            next_collisions = self.collisions_at(annotation)
            if not next_collisions:
                paths.append((annotation,))
            else:
                # TODO: Performance improvement
                # Checking against all other collisions in the group
                # is actually not needed.
                # For a new collision to be added, it is only required
                # check against the shortest annotation.
                for collision in next_collisions:
                    for path in self._subcombinations(collision):
                        paths.append((annotation,) + path)
            self._subcombination_cache[annotation] = paths
        return self._subcombination_cache[annotation]

    # TODO: maybe rename combinations to interpretations
    interpretations = combinations

    def disambiguate(self, discard_others=False):
        """Computes the best total-scoring set of annotations to keep
        and discards the others.
        """
        best_score = 0
        best_interpretation = []

        for interpretation in self.interpretations():
            score = sum([annotation.score for annotation in interpretation])
            if score > best_score:
                best_interpretation = interpretation
                best_score = score

        if discard_others:
            for annotation in self:
                if annotation not in best_interpretation:
                    self.remove(annotation)

        return best_interpretation

    def to_cells(self):
        """Groups annotations into possible table cells."""
        cells = [self.collisions_at(0)]

        while len(cells[-1]) > 0:
            next_position = 1 + min([
                annotation.span.end for annotation in cells[-1]
            ])
            cells.append(self.collisions_at(next_position))

        return cells[:-1]

    def boost(self, multiplier):
        for annotation in self:
            annotation.score *= multiplier
        return self

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
