def create_sequence(list_of_tuples):
    sequence = []
    for tuple in list_of_tuples:
        for i in range(tuple[1]):
            sequence.append(tuple[0])
    return sequence


def list_from_OrderedDict(o):
    sequence = []
    for k, v in o.items():
        for i in range(v):
            sequence.append(k)
    return sequence


class Animation:
    def __init__(self, object, possible_states):
        self.object = object
        self.possible_states = possible_states
        self._current_state = possible_states[0]
        self.flip = False

        object_path = os.path.join("assets", "animations", object)
        self.animations = {}
        for state in possible_states:
            object_state_path = os.path.join(object_path, state)
            self.animations[state] = {
                os.path.splitext(item)[0]: load_animation_image(
                    object, action, item, -1
                )
                for item in os.listdir(object_state_path)
                if os.path.isfile(os.path.join(object_state_path, item))
            }
        self.animation_sequence = {
            "idle": create_sequence([("idle_0", 7), ("idle_1", 7), ("idle_2", 40)]),
            "run": create_sequence([("run_0", 7), ("run_1", 7)]),
        }
        self.current_frame = 0

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, value):
        if self._current_state != value:
            if value in self.possible_states:
                self._current_state = value
                self.current_frame = 0
            else:
                raise ValueError(
                    "%s is not a valid action for %s" % (value, self.object)
                )

    @property
    def current_image(self):
        image = self.animations[self.current_state][
            self.animation_sequence[self.current_state][self.current_frame]
        ]
        # PERFORMANCE: cache flipped image to prevent pygame.transform operation every frame
        return pygame.transform.flip(image, self.flip, False)

    def next_frame(self):
        self.current_frame += 1

        if self.current_frame >= len(self.animation_sequence[self.current_state]):
            self.current_frame = 0
