#!/bin/bash

PRINTER="DYMO LabelWriter 450 Turbo"
MEDIA="media=oe_square-multipurpose-label_1x1in"
LABEL_PNG=label.png

function main
{
        # create png
        convert -size 150x150 xc:white -pointsize 60 -fill black -gravity Center -annotate 0 "`date +"%m/%d"`" $LABEL_PNG

        lprint submit -d "${PRINTER}" -o "${MEDIA}" "$LABEL_PNG"


}

main
