#!/usr/bin/env python
"""
srt2txt - Convert text subtitles from the SRT format to Adobe text scripts (for use in Encore)

SRT files as exported from YouTube include timestamps in this format:

1
00:03:17,440 --> 00:03:19,440
Subtitle text

2
...

Adobe TXT uses timecode frames, so we depend on the framerate (NTSC or PAL) :

Text subtitle scripts should follow this format
(from http://help.adobe.com/en_US/encore/cs/using/WSbaf9cd7d26a2eabfe807401038582db29-7ea2a.html)

Subtitle_# Start_Timecode End_Timecode Subtitle_text

Additional_line_of_subtitle_text

Additional_line_of_subtitle_text

NTSC: Frame # = (milliseconds * 29.97) / 1000

PAL: Frame # = (milliseconds * 25) / 1000

"""

__author__ = 'Stephane Peter'
__email__ = 'megastep@megastep.org'

import sys
import argparse

# Input states
SUB_NUMBER = 1
SUB_TIMES = 2
SUB_STRINGS = 3


def convert(srtfile, txtfile, format, gap):
    if format == 'pal':
        sep = ':'
        fps = 25
    else:  # NTSC
        sep = ';'
        fps = 29.97

    def to_frames(timecode):
        (t, ms) = timecode.split(',')
        elts = t.split(':')
        return ((int(elts[0])*3600 + int(elts[1])*60 + int(elts[2]))*1000 + int(ms)) * fps / 1000

    def convert_timecode(timecode, inc=0):
        (t, ms) = timecode.split(',')
        elts = t.split(':')
        return "%s%s%d" % (sep.join(elts), sep, (int(ms) * fps / 1000)+inc)

    last_end = 0
    state = SUB_NUMBER
    for line in srtfile.readlines():
        if state == SUB_NUMBER:
            subnum = int(line)
            state = SUB_TIMES
        elif state == SUB_TIMES:
            times = line.strip().split(" --> ")
            txt = ""
            state = SUB_STRINGS
        elif state == SUB_STRINGS:
            if len(line.strip()) == 0:  # Just \n, end of entry
                diff = to_frames(times[0]) - last_end
                if diff < gap:
                    start = convert_timecode(times[0], gap - diff)
                else:
                    start = convert_timecode(times[0])
                print >> txtfile, "{0:d} {1:s} {2:s} {3:s}".format(subnum, start, convert_timecode(times[1]), txt)
                last_end = to_frames(times[1])
                state = SUB_NUMBER
            else:
                txt += line

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert subtitles to Adobe text format.')
    parser.add_argument('--format', default='pal', choices=['ntsc', 'pal'],
                        help="Encoding to use (NTSC or PAL [default])")
    parser.add_argument('--gap', default=5, type=int,
                        help="Number of frames to insert between subsequent clips if needed (default = 5)")
    parser.add_argument('srtfile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help="Filename for source SRT file.")
    parser.add_argument('txtfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                        help="Destination file for converted Adobe data.")
    args = parser.parse_args()
    convert(args.srtfile, args.txtfile, args.format, args.gap)

