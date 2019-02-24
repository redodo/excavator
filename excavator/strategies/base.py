# TODO: Find a better name for 'Strategy'. Also, figure out if using a numpy array
#       could greatly improve the implementation of a strategy.
class Strategy:

    def apply(self, text):
        raise NotImplementedError(
            '%s does not implement the `apply` method'
            % self.__class__.__name
        )


class CellStrategy(Strategy):

    def apply(self, text):
        for y, line in enumerate(text.lines):
            for x, cell in enumerate(line.cells):
                for annotation in cell:
                    self.apply_to_annotation(text, line, annotation, x, y)

    def apply_to_annotation(self, text, line, annotation, x, y):
        raise NotImplementedError(
            '%s does not implement the `apply_to_annotation` method'
            % self.__class__.__name__
        )
