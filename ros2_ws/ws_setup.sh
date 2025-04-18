# Run using:
#   . ./ws_setup.sh

# General ros setup
source /opt/ros/jazzy/setup.bash
/usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash

# -----

# Local jobs
cd ./ros2_ws
colcon build

# Local ws setup
source ./install/setup.bash





