# Run using:
#   . ./ws_setup.sh

# General ros setup
source /opt/ros/jazzy/setup.bash
/usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash

# -----

# Local jobs
colcon build --symlink-install

# Local ws setup
source ./install/setup.bash





