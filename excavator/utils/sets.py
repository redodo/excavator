class ReverseSet(set):

    def __init__(self, owner, reverse_attr, *elements):
        self.owner = owner
        self.reverse_attr = reverse_attr
        super().__init__(*elements)

    def add(self, elem, reverse=True):
        super().add(elem)
        if reverse:
            reverse_set = getattr(elem, self.reverse_attr)
            reverse_set.add(self.owner, reverse=False)

    def remove(self, elem, reverse=True):
        super().remove(elem)
        if reverse:
            reverse_set = getattr(elem, self.reverse_attr)
            reverse_set.remove(self.owner, reverse=False)

    def discard(self, elem, reverse=True):
        super().discard(elem)
        if reverse:
            reverse_set = getattr(elem, self.reverse_attr)
            reverse_set.discard(self.owner, reverse=False)

    def clear(self):
        try:
            while True:
                elem = self.pop()
                reverse_set = getattr(elem, self.reverse_attr)
                reverse_set.discard(self.owner, reverse=False)
        except KeyError:
            pass

    # TODO: implement `update`, `intersection_update`, `difference_update`,
    #       and `symmetric_difference_update`
