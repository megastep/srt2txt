# srt2txt - Subtitle converter
## Convert subtitles from SRT to the Adobe Encore script format (.txt)

This Python script translates subtitle files in the SRT format (as exported by YouTube) to a text
format suitable to be used with the Adobe Encore suite for the purposes of making DVD subtitle tracks.

## Usage

`srt2txt [--format {ntsc,pal}] [--gap N] [input file] [output file]`

- `--gap` is used to specify the minimum number of frames between text clips, default is 5. This is a requirement
in Encore for Blu-ray discs. Frames are padded at the beginning of clips when needed.
- `--format` specifies the framerate in use for the project (default is PAL at 25)

## Requirements

Python 2.7, developed and tested on MacOS X 10.9.

## Author

Written by Stéphane Peter (megastep@megastep.org)
