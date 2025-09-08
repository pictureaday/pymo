#!/bin/bash

PRINTER="D450"
MEDIA="media=oe_square-multipurpose-label_1x1in"
LABEL_PNG=label.png

function main
{
        # create png
        convert -size 150x150 xc:white -pointsize 60 -fill black -gravity Center -bordercolor Black -border 5 -annotate 0 "`date +"%m/%d"`" $LABEL_PNG

        #lprint submit -d "${PRINTER}" -o "${MEDIA}" "$LABEL_PNG"
	#lp -o page-top=4 -o page-bottom=4 -o media=Custom.1x1in label.png
	lp -o media=Custom.1x1in label.png

}

main

