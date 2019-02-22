from .base import Strategy


class CombinationStrategy(Strategy):

    def __init__(self, combinations):
        self.combinations = combinations

    def apply(self, text):
        for line in text.lines:
            annotations = line.annotations
            for annotation in annotations.collisions(0):
                self.seek(annotations, annotation, [], self.combinations.copy())

    def seek(self, line, annotation, buffer, combinations):
        # add annotation to buffer
        buffer.append(annotation)

        # remove impossible combinations
        check_pos = len(buffer) - 1
        check_type = buffer[check_pos].type

        removal_list = []
        for combination in combinations:

            # check if the combination is too long or
            # if the current position does not match
            if check_pos >= len(combination) or \
                    combination[check_pos] != check_type:
                removal_list.append(combination)

            # the combination matches, check if we
            # matched the complete combination
            elif len(combination) == len(buffer):
                # boost annotations and remove combination
                for annotation in buffer:
                    boost = combinations[combination]
                    annotation.score *= boost
                removal_list.append(combination)

        for combination in removal_list:
            combinations.pop(combination)

        # check if we need to seek further
        if len(combinations) != 0:
            for subann in line.collisions(annotation.span.end):
                self.seek(line, subann, buffer.copy(), combinations.copy())
