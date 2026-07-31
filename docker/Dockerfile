FROM ubuntu:26.04

ENV DEBIAN_FRONTEND=noninteractive

# 1. Set up locale (important for minimal Docker environments)
RUN apt update && apt install -y locales && \
    locale-gen en_US en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

ENV LANG=en_US.UTF-8

# 2. Enable required repositories and install base tools
RUN apt install -y \
    software-properties-common \
    curl \
    git \
    python3-pip \
    build-essential \
    cmake \
    vim && \
    add-apt-repository universe

# 3. Install ROS 2 apt source (official method)
RUN apt update && apt install -y curl && \
    export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}') && \
    curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb" && \
    dpkg -i /tmp/ros2-apt-source.deb && \
    rm /tmp/ros2-apt-source.deb

# 4. Install ROS 2 and colcon
RUN apt update && \
    apt install -y ros-lyrical-desktop && \
    apt install -y python3-colcon-ros

# 5. Source ROS environment on startup
RUN echo "source /opt/ros/lyrical/setup.bash" >> /root/.bashrc

ENTRYPOINT ["/bin/bash"]
