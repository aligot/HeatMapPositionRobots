

search_dir="Plots"

for entry in "$search_dir"/*
do
  filename=$(basename -- "$entry")
  filename="${filename%.*}"
  echo "$filename"
  frame="LastFrames/"$filename"*"
  output="ComposedImages/"$filename".jpg"
  # Supperpose images
  cmd="composite -compose Over -gravity Center "$entry" "$frame" "$output
  eval $cmd

  # Rotate
  cmd="convert "$output" -rotate 181 "$output
  eval $cmd
   
  # Crop
  cmd="convert "$output" -crop 1170x1170+19+21 +repage "$output
  eval $cmd
done
