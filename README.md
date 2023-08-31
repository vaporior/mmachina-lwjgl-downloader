# MinecraftMachina LWJGL Downloader
Automatically download [MinecraftMachina](https://github.com/MinecraftMachina)'s [LWJGL 3 builds](https://github.com/MinecraftMachina/lwjgl3) and extract their respective natives into a directory of your choice.

This script **does not** place the libraries and natives in the directories they need to be in to be used by your Minecraft launcher. This is an upcoming feature. If you would like to add support for your favourite launcher, please submit an Issue or Pull Request.

### Instructions
1. Install python and add it to your path
2. Clone the repo and navigate to it in your terminal
3. Run `pip install -r requirements.txt`
4. Run `python mmachina-lwjgl-downloader.py`

> If you are on MacOS and the above commands don't work, try replacing `pip` and `python` with `pip3` and `python3`.
