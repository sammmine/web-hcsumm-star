#!/usr/bin/env bash
# Recursively convert files to Markdown using markitdown.
# Usage: ./convert-to-md.sh [--force] [DIR]
#   --force  Overwrite existing .md files even if newer than source
#   DIR      Target directory (default: current directory)

FORCE=0
DIR="."

for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    *) DIR="$arg" ;;
  esac
done

EXTENSIONS=(
  pdf pptx ppt docx doc
  xlsx xls csv
  html htm xml
  json yaml yml
  txt rst rtf epub zip
  jpg jpeg png gif bmp tiff
  wav mp3
)

find_args=()
for ext in "${EXTENSIONS[@]}"; do
  find_args+=(-o -iname "*.${ext}")
done
find_args=("${find_args[@]:1}")

processed=0
skipped=0
failed=0

while IFS= read -r -d '' file; do
  out="${file%.*}.md"

  if [[ $FORCE -eq 0 && -f "$out" && "$out" -nt "$file" ]]; then
    echo "[SKIP] $file"
    ((skipped++))
    continue
  fi

  if markitdown "$file" -o "$out" 2>/dev/null; then
    echo "[OK]   $file"
    ((processed++))
  else
    echo "[FAIL] $file"
    ((failed++))
  fi
done < <(find "$DIR" \( "${find_args[@]}" \) -not -path '*/.git/*' -print0 | sort -z)

echo ""
echo "Done: $processed converted, $skipped skipped, $failed failed"
