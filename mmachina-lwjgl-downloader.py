#!/usr/bin/env python

from os import makedirs, listdir
from os.path import exists, isdir, isfile, join, basename, abspath
from sys import exit
from shutil import rmtree
from glob import glob
from urllib.parse import urljoin
from zipfile import ZipFile
from requests import get
from tqdm import tqdm


def download(url, output, chunk_size = 1024):
    response = get(url, stream = True)
    total = int(response.headers.get("content-length", 0))
    with open(output, "wb") as file, tqdm(
        desc = output,
        total = total,
        unit = "iB",
        unit_scale = True,
        unit_divisor = 1024,
    ) as bar:
        for data in response.iter_content(chunk_size = chunk_size):
            bar.update(file.write(data))


def construct_asset_name(binding, is_native = False):
	# Based on naming pattern in
	# https://github.com/MinecraftMachina/lwjgl3/releases/tag/3.3.1-mmachina.1
	asset_name = "lwjgl"
	if binding:
		asset_name += '-' + binding
	if is_native:
		asset_name += "-natives-macos-arm64"
	return asset_name + ".jar"


def get_lwjgl(base_url, output_directory, binding = ''):
	file_path = ''
	for i in range(2):
		file_name = construct_asset_name(binding, is_native = (i == 1) )
		file_path = join(output_directory, file_name)
		download(urljoin(base_url, file_name), file_path)

	with ZipFile(file_path, mode = 'r') as jar:
		natives_path = join("macos/arm64/org/lwjgl", binding)
		for file in jar.namelist():
			if file.startswith(natives_path) and file.endswith(".dylib"):
				zipfile_info_obj = jar.getinfo(file)
				# remove parent directory information.
				# this prevents ZipFile from extracting parent diretories
				# along with the .dylib
				zipfile_info_obj.filename = basename(file)
				jar.extract(zipfile_info_obj, path = join(output_directory, "natives"))


if __name__ == "__main__":
	base_url = "https://github.com/MinecraftMachina/lwjgl3/releases/download/3.3.1-mmachina.1/"
	bindings = [
		"glfw",
		"jemalloc",
		"openal",
		"opengl",
		"stb",
		"tinyfd"
	]
	output_directory = "mmachina-lwjgl"

	if not exists(output_directory):
		makedirs(output_directory)
	elif isdir(output_directory) and glob(join(output_directory, '*')):
		print("The output directory specified (" + abspath(output_directory) + ") is not empty. Existing files in the directory with the same name as the files to be downloaded will be overwritten.")
		while True:
			clear = input("Would you like to delete the contents of the directory first? ( [y]es, [n]o, [c]ancel ): ").lower()
			if clear == 'y' or clear == "yes":
				rmtree(output_directory)
				makedirs(output_directory)
			elif clear == 'c' or clear == "cancel":
				print("Aborted by user.")
				exit(1)
			elif clear != 'n' and clear != "no": continue
			break
	elif isfile(output_directory):
		print("A file already exists with the same name as the specified output directory.")
		exit(1)

	get_lwjgl(base_url, output_directory)
	for binding in bindings:
		get_lwjgl(base_url, output_directory, binding = binding)

	print("Finished downloading LWJGL libraries at " + abspath(output_directory))
	print("Natives have been extracted to a separate 'natives' directory inside in the output directory above.")
