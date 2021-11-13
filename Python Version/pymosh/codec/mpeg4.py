IFRAME_HEADER = b'\x00\x00\x01\xb0'


def is_iframe(frame):
    """Determine whether frame is an I frame."""
    return frame[:4] == IFRAME_HEADER
