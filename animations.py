import os
import pygame
from resources import load_animation_image


def create_sequence(list_of_tuples):
    sequence = []
    for tuple in list_of_tuples:
        for i in range(tuple[1]):
            sequence.append(tuple[0])
    return sequence


class AnimationMixin:
    def initialize_animation(self, object, sequence_dict):
        self.animation = Animation(object, list(sequence_dict.keys()))
        self.animation.set_sequence(sequence_dict)

    @property
    def image(self):
        return self.animation.current_image


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
                os.path.splitext(item)[0]: load_animation_image(object, state, item, -1)
                for item in os.listdir(object_state_path)
                if os.path.isfile(os.path.join(object_state_path, item))
            }
        self.current_frame = 0

    def set_sequence(self, sequence_dict):
        self.animation_sequence = {}
        for state, sequence, in sequence_dict.items():
            self.animation_sequence[state] = create_sequence(sequence)

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
        if self.animation_sequence is None:
            raise AttributeError("Animation sequence is not set. Use .set_sequence().")
        image = self.animations[self.current_state][
            self.animation_sequence[self.current_state][self.current_frame]
        ]
        # PERFORMANCE: cache flipped image to prevent pygame.transform operation every frame
        return pygame.transform.flip(image, self.flip, False)

    def next_frame(self):
        self.current_frame += 1

        if self.current_frame >= len(self.animation_sequence[self.current_state]):
            self.current_frame = 0
