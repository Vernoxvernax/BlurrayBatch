# **Easily batch through your Blu-Ray- or DVD-MVs**

___

## **search**

```py
def search(path: str, bluray=True, output=".", create_output_folder=False, additional_folder_names = list("")) -> list[Media_File]
```

### Parameters:

* **path** `str`: Destination as str of the bd- or dvd-mv. - `./Cool Anime`

* **type** `int`: What kind of folder you want to process. (helps to distinguish folder names)
    *   `0` - Blu-ray
    *   `1` - DVDmv
    *   `2` - Remux

* **extension** `str/None`: Extension of the file which should be indexed.
    * If left unspecified, `type` will be used.

* **output** `str`: What the output path of the files should be. (prefix) - `./encode`

* **create_output_folder** `bool`: Whether the output folder should be created or not. - `False`

* **additional_folder_names** `list(str)`: A list of folder names that should be ignored when searching for a volume/disc name. (like "BDMV") - `()`

* -> **list[Media_File]**: If all works as expected you'll get a list of Media_File objects. These are all the files found in the folder which parameters that should make batching very easy.

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

Since making use of pipes in python is pretty complicated, I decided to write a little wrapper around it. As a bonus, this also carefully prints the progress bar lines like the ones from opusenc so that the output doesn't turn into complete mess. You can selectively turn of the output of the first command.

### Parameters:

* **command** `str`: The command which needs to be run. - `ffmpeg -i "file.m2ts" -map 0:a:0 -f wav - | opusenc - "output.opus"`

* **print_all** 'bool': Whether all outputs, instead of just the second command, should be printed. This is useful if you don't need `ffmpeg` to ruin your interface. - `False`

___

For a comprehensive example take a look at examples

More features (bug fixes) are likely to come.
