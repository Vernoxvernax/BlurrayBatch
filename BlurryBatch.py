import os
import subprocess

class Media_File:
    def __init__(self, file_name: str, disc: str, path: str, output: str, name: str, output_folder: str, size: float):
        self.name = name
        self.file_name = file_name
        self.size = size
        self.disc = disc
        self.path = path
        self.output = output
        self.output_folder = output_folder
    def full(self) -> str:
        return "Name: \"{name}\"\nFilename: \"{filename}\"\nSize: {size} MB\nPath: \"{path}\"\nOutput: \"{output}\"\nOutput-folder: \"{output_folder}\"\nDisc: \"{disc}\"".format(
            name=self.name, filename=self.file_name, path=self.path, output=self.output, disc=self.disc, output_folder=self.output_folder, size=self.size
        )

def output_list(list: list[Media_File]) -> list[str]:
    output=[]
    for x in list:
        output.append(x.output)
    return output

def search(path: str, bluray=True, output=".", create_output_folder=False, additional_folder_names = list("")) -> list[Media_File]:
    if not os.path.isdir(path):
        raise Exception("path: This folder does not exist.")
    if output.endswith("/"):
        output=output[:-1]
    elif output == "":
        raise Exception("output: Cannot be an empty str. Maybe you wanted to type \".\"?")
    
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
        for index, folder in enumerate(folders):
            for entry in os.listdir(folder):
                if os.path.isdir(folder + "/" + entry):
                    folders.append(folder + "/" + entry)
                else:
                    files.append(folder + "/" + entry)
            folders.remove(folder)
            folders.index
    
    # Sort files alphabetically
    files.sort()
    
    # Find media files and their volume / disc folder.
    if bluray:
        srch=".m2ts"
        common_dirs: list[str] =["BDMV", "STREAM", "bdmv", "stream"]
    else:
        srch=".vob"
        common_dirs: list[str] =["VIDEO_TS", "video_ts"]
    
    if additional_folder_names != (""):
        common_dirs = common_dirs+additional_folder_names
    
    media=[]
    duplicates = 0
    skip = 0
    while(1):
        if len(media) > 0:
            media.clear()
            
        for file in files:
            if str(file).lower().endswith(srch):
                directories=str(file).split("/")
                reverse_dirs=directories.copy()
                reverse_dirs.reverse()
                disc=""
                skip = duplicates
                for dir in reverse_dirs[1:]:
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
                    name=directories[-1].lower().removesuffix(srch),
                    file_name=directories[-1],
                    size=size,
                    disc=disc,
                    path=file,
                    output=output+"/"+disc+"/"+directories[-1].lower().removesuffix(srch),
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
    return media

def run_pipe(command: str, print_all = False):
    if len(command.split("|")) == 1:
        raise Exception("command: Please make sure to properly include the '|' terminator once.")
    elif len(command.split("|")) > 2:
        raise Exception("command: '|' can only be used once.")
    
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
