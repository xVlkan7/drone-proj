from setuptools import find_packages, setup

package_name = "pellet_pacman"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", ["launch/game.launch.py"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    description="A small ROS 2 keyboard-controlled pellet collection game.",
    entry_points={
        "console_scripts": [
            "game = pellet_pacman.game_node:main",
        ],
    },
)
