# **Batch through your Blu-Ray- or DVD-MVs**

## **search**

```py
def search(path: str, bluray=True, output=".", create_output_folder=False, additional_folder_names = list("")) -> list[Media_File]
```

### Parameters:

* path `str`: Destination as str of the bd- or dvd-mv. - `./Anime`

* bluray `bool`: Whether you want to process a bluray or dvd. (helps to distinguish folder names) - `True`

* output `str`: What the output path of the files should be. (prefix) - `./encode`

* create_output_folder `bool`: Whether the output folder should be created or not. - `False`

* additional_folder_names `list(str)`: A list of folder names that should be ignored when searching for a volume/disc name. (like "BDMV") - `()`

* -> list[Media_File]: If all works as expected you'll get a list of Media_File objects. These are all the files found in the folder which parameters that should make batching very easy.

```py
class Media_File:
    def __init__(self, file_name, disc, path, output, name, output_folder):
        self.name = name # 00001
        self.file_name = file_name # 00001.m2ts
        self.disc = disc # Disc 1
        self.path = path # ./Anime/Disc 1/00001.m2ts
        self.output = output # ./encode/Anime/Disc 1/00001
        self.output_folder = output_folder # ./encode/Anime/Disc 1/
...
```
___

## **run_pipe**

```py
def run_pipe(command: str, print_all = False)
```

### Details:

Since running commands making use of pipes is pretty complicated in python, I decided to write a little function to make the use of it easier. As a bonus, this also carefully prints progress bar lines like the ones from opusenc so that the output doesn't turn into complete mess.

### Parameters:

* command `str`: The command which needs to be run. - `ffmpeg -i "file.m2ts" -map 0:a:0 -f wav - | opusenc - "output.opus"`

* print_all 'bool': Whether all outputs, instead of just the second command, should be printed. This is usefull if you don't need `ffmpeg` to ruin your interface. - `False`

___

## **Example script**:

```py
import os
import sys
import BlurryBatch

if len(sys.argv) > 1:
    arg=sys.argv[1]
else:
    arg=""

files = BlurryBatch.search(path="./Cool Anime", bluray=True, output="./encode", create_output_folder=True)

for file in files:
    # Check if the output file already exists
    if os.path.isfile(file.output+".mkv") and arg != "overwrite":
        continue
    
    # Check for audio track
    if os.path.isfile(file.output+".opus") and arg != "overwrite":
        continue
    
    print("Now working on {}".format(file.output))
    
    command = 'ffmpeg -i "{}" -map 0:a:0 -f wav - | opusenc - "{}.opus"'.format(file.path, file.output)
    BlurryBatch.run_pipe(command, print_all=False)
    ...
```

More features (bugfixes) are likely to come.
