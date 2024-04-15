import config

# TODO: Return dungeon grid instead of default spawn map
def generate_dungeon(incoming_direction):
    """
    :param incoming_direction: The direction the player is coming from relative to prior room
    """
    return config.SPAWN_MAP