git config filter.stripoutput.clean "$(git rev-parse --show-toplevel)/nb/_strip_output.py" 
git config filter.stripoutput.smudge cat
git config filter.stripoutput.required true
echo '*.ipynb filter=stripoutput' >> "$(git rev-parse --show-toplevel)"/.gitattributes
