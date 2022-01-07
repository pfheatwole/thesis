# The SVG hierarchy in Matplotlib output adds extraneous whitespace. This
# script deletes the bounding boxes and fits the canvas to the result.

actions="select-by-id:patch_1;EditDelete;EditDelete"
actions+=";select-by-id:figure_1;SelectionUnGroup"
actions+=";FitCanvasToDrawing"
actions+=";FileSave"

for svgfile in *.svg; do
  echo "Cleaning $svgfile..."
  inkscape --actions="$actions" --with-gui --batch-process "$svgfile"
done
