class Animation:

    def __init__(self, images, is_looped: bool):
        self.images = images
        self.current_frame_index = 0
        self.animation_time = .1
        self.current_time = 0
        self.last_updated_time = 0
        self.is_looped = is_looped

    def update(self, dt):
        self.current_time += dt

        if self.current_time > self.last_updated_time + self.animation_time:
            self.current_frame_index += 1
            self.last_updated_time = self.current_time

    def get_image(self):
        return self.images[self.current_frame_index % len(self.images)]

    def reset(self):
        self.current_frame_index = 0
        self.last_updated_time = 0

    def is_finished(self):
        if self.current_frame_index > len(self.images) and not self.is_looped:
            return True

        return False