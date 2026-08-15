"""Launch the isolated pellet game node."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    """Return a launch description containing only the game node."""

    return LaunchDescription(
        [
            Node(
                package="pellet_pacman",
                executable="game",
                name="pellet_pacman",
                output="screen",
            )
        ]
    )
