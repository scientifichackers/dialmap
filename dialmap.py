class Normalizer:
    def __init__(self, start=0, stop=1):
        self.min, self.max = 0, 0
        self.start, self.stop = start, stop

        self._size = self.stop - self.start
        self._nm_ratio = 0

    def _refresh_nm_ratio(self):
        self._nm_ratio = self._size / (self.max - self.min)

    def _refresh_limits(self, input_value):
        if input_value < self.min:
            self.min = input_value
            self._refresh_nm_ratio()
        elif input_value > self.max:
            self.max = input_value
            self._refresh_nm_ratio()

    def normalize(self, input_value):
        self._refresh_limits(input_value)
        return (input_value - self.min) * self._nm_ratio + self.start


def linspace(start, stop, num):
    delta = (stop - start) / (num - 1)
    return [start + (delta * i) for i in range(num)]


def _gen_dial_zones(start, stop, count, deadzone):
    midpts = linspace(start, stop, count + 1)

    deadzone_size = (midpts[1] - midpts[0]) * (deadzone / 100)

    for i, left in enumerate(midpts[:-2]):
        right = midpts[i + 1]
        yield range(int(left), int(right - deadzone_size))

    left, right = midpts[i + 1], midpts[i + 2]
    if not deadzone_size >= right - left:
        yield range(int(left), int(right))


def _filter_output_pts(dial_zones, output_pts):
    for i, dial_pts in enumerate(dial_zones):
        for dial_pt in dial_pts:
            yield dial_pt, output_pts[i]


class DialMap:
    def __init__(self, output_pts, deadzone=0):
        num_output_pts = len(output_pts)

        self.mapping = {}

        self._store = output_pts[0]
        self._nm = Normalizer(stop=num_output_pts * 2 if num_output_pts > 50 else 100)

        for dial_pt, output_pt in _filter_output_pts(
            _gen_dial_zones(self._nm.start, self._nm.stop, num_output_pts, deadzone),
            output_pts,
        ):
            self.mapping[dial_pt] = output_pt

    def translate(self, raw):
        dial_pt = int(self._nm.normalize(raw))
        try:
            self._store = self.mapping[dial_pt]
        except KeyError:
            pass
        return self._store
