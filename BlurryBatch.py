import os
import subprocess

class Media_File:
    def __init__(self, file_name: str, size: float, root: str, disc: str, path: str, output: str, name: str, output_folder: str):
        self.name = name
        self.file_name = file_name
        self.size = size
        self.root = root
        self.disc = disc
        self.path = path
        self.output = output
        self.output_folder = output_folder
    def full(self) -> str:
        return "Name: \"{name}\"\nFilename: \"{filename}\"\nSize: {size} MB\nRoot: \"{root}\"\nDisc: \"{disc}\"\nPath: \"{path}\"\nOutput: \"{output}\"\nOutput-folder: \"{output_folder}\"".format(
            name=self.name, filename=self.file_name, size=self.size, root=self.root, path=self.path, disc=self.disc, output=self.output, output_folder=self.output_folder
        )

"""
BlurryBatch - search

Searches a directory given a few parameters and returns a list of files with easy to use parameters.

Parameters:

- path
    Path to folder containing files

- type
    The script will try to determine the simplest output structure, based on the type:
        + 0: Blu-ray. "STREAM", "BDMV".
        + 1: DVDmv. "VIDEO_TS"
        + 2: Remux.
        
- extension
    Only files with this extension will be indexed.
        + If left unspecified, BlurrBatch will use the `type` parameter to determine this. (0: `.m2ts`; 1:`.vob`; 2:`.mkv`)

- output
    The root directory, which is going to be used in the `output`-path parameter of the file.

- create_output_folder
    Whether to create the output folder automatically.
    
- additional_folder_names
    A list of foldernames which should be ignored when determining an output folder name.
        - The script is still going to search within folders like these, but will just avoid this being the output-folder for the file.

"""
def search(path: str, type: int, extension=None, output="./encode", create_output_folder=False, additional_folder_names = list("")) -> list[Media_File]:
    if not os.path.isdir(path):
        raise Exception("path: This folder does not exist.")
    if output.endswith("/"):
        output=output[:-1]
    elif output == "":
        raise Exception("output: Cannot be an empty str. Maybe you wanted to type \".\"?")
    if extension != None and not extension.startswith("."):
        extension="."+extension
    
    folders=[]
    files=[]
    
    # Collect folders and files for recursive search
    for entry in os.listdir(path):
        if os.path.isdir(path + "/" + entry):
            folders.append(path + "/" + entry)
        else:
            files.append(path + "/" + entry)
    
    # Loop through the folders list as long as there are entries in it
    while len(folders) > 0:
        for folder in folders:
            for entry in os.listdir(folder):
                if os.path.isdir(folder + "/" + entry):
                    folders.append(folder + "/" + entry)
                else:
                    files.append(folder + "/" + entry)
            folders.remove(folder)
    
    # Sort files alphabetically
    files.sort()
    
    # Find media files and their volume / disc folder.
    if type == 0:
        ext=".m2ts"
        common_dirs: list[str] = ["BDMV", "STREAM", "bdmv", "stream"]
    elif type == 1:
        ext=".vob"
        common_dirs: list[str] = ["VIDEO_TS", "video_ts"]
    else:
        ext=".mkv"
        common_dirs: list[str] = []
    if extension != None:
        ext=extension
    
    if additional_folder_names != (""):
        common_dirs = common_dirs+additional_folder_names
    
    media=[]
    duplicates = 0
    skip = 0
    while(1):
        if len(media) > 0:
            media.clear()

        for file in files:
            if str(file).lower().endswith(ext):
                directories=str(file).split("/")
                reverse_dirs=directories.copy()
                reverse_dirs.reverse()
                disc=""
                root = file.removesuffix(directories[-1])
                skip = duplicates
                for dir in reverse_dirs[1:]:
                    root = root.removesuffix("/").removesuffix(dir)
                    if dir in common_dirs:
                        continue
                    else:
                        if duplicates > 0:
                            if skip == 0:
                                disc=dir
                                break
                            else:
                                skip = skip - 1
                                continue
                        disc=dir
                        break
                size = os.path.getsize(file) / (1024 * 1024)
                media.append(Media_File(
                    name=directories[-1].removesuffix(ext).removesuffix(ext.upper()),
                    file_name=directories[-1],
                    size=size,
                    root=root,
                    disc=disc,
                    path=file,
                    output=output+"/"+disc+"/"+directories[-1].removesuffix(ext),
                    output_folder=output+"/"+disc+"/"
                ))

        if len(media) != len(set(output_list(media))):
            duplicates = duplicates + 1
        else:
            break
        
    if create_output_folder:
        for file in media:
            if not os.path.isdir(file.output_folder):
                os.makedirs(file.output_folder)
    if len(media) == 0:
        print("No files could be found.\nPlease make sure you've specified the correct file extention and/or folder structure type!")
    return media

def run_pipe(command: str, print_all = False):
    if len(command.split("|")) == 1:
        raise Exception("command: Please make sure to properly include the '|' terminator once.")
    elif len(command.split("|")) > 2:
        raise Exception("command: Please make sure to include the '|' terminator only once.")
    
    pipe_read, pipe_write = os.pipe()
    
    command1 = command.split("|")[0]
    command2 = command.split("|")[1]
    
    if print_all:
        process = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE, stderr=pipe_write)
    else:
        process = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    process2 = subprocess.Popen(command2, shell=True, stdin=process.stdout, stdout=subprocess.PIPE, stderr=pipe_write)
    
    os.close(pipe_write)
    
    while True:
        output = os.read(pipe_read, 1024).decode()
        if output == '' and process2.poll() is not None:
            break
        if output:
            if output.strip() == '':
                continue
            if '\r' in output:
                print(output.strip(), end="\r")
            else:
                print(output.strip())

    os.close(pipe_read)
    
    print("Pipe closed.\n")
    
    process2.wait()

def output_list(list: list[Media_File]) -> list[str]:
    output=[]
    for x in list:
        output.append(x.output)
    return output

