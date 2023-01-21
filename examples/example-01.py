import os
import sys
import BlurryBatch

if len(sys.argv) > 1:
    arg=sys.argv[1]
else:
    arg=""

files = BlurryBatch.search(path="../Cool Anime", type=0, output="../Cool Anime-encode", create_output_folder=False)

for file in files:
    # Check if the output file already exists
    if os.path.isfile(file.output+".mkv") and arg != "overwrite":
        continue
    
    # Check for audio track
    if os.path.isfile(file.output+".opus") and arg != "overwrite":
        continue
    
    # Example of other kinds of filters
    if file.size > 5000 and not (file.disc == "Disc 1" and file.name == "00001"):
        continue
    
    print(file.full())
    # print("Now working on {}".format(file.output))
    
    command = 'ffmpeg -i "{}" -map 0:a:0 -f wav - | opusenc - "{}.opus"'.format(file.path, file.output)
    BlurryBatch.run_pipe(command, print_all=False) # This will fail since the media files aren't actual media files.
