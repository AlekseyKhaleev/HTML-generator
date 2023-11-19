to install dependencies exec commands:<br>
pip install poetry<br>
cd *project_path*<br>
poetry install

to solve an issue in ubuntu, sounds like:<br>

*qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.*

try to use:<br>
sudo apt-get install '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev
libxkbcommon-x11-dev