#!/bin/bash

# This cleans up the matplotlib canopy diagrams:
#
#  1. Removes the unused `patch_1` and `patch_2` elements
#
#  2. Ungroups `figure_1`, which should only contain `axes_1`
#
#  3. Simplifies the canopy surface curves (they're too high resolution)
#
#  4. Fits the canvas to the diagram

for svgfile in *canopy.svg
do
	echo "Cleaning $svgfile..."
	inkscape --actions="select-by-id:patch_1;EditDelete;select-by-id:patch_2;EditDelete;select-by-id:figure_1;SelectionUnGroup;select-by-id:axes_1;SelectionSimplify;FitCanvasToDrawing;FileSave" --with-gui --batch-process "$svgfile"
done

# Notes to self:
#
#  * This monstrosity works as of Inkscape 1.0
#
#  * Remember `inkscape --action-list` and `inkscape --verb-list`
#
#  * I could cleanup the curves diagrams (make straight lines into 2-node paths,
#    etc) but for now I don't care. If you blindly simplify the entire `axes_1`
#    it ruins the fonts.
