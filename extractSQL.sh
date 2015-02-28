file=${1:-"l2p/dbw/__init__.py"}
regex="s/(^.*')(SELECT|INSERT|UPDATE|CREATE)(.*)('.*)/\2\3/p"
if [[ -f ${file} ]]; then
    sed -nr ${regex} ${file} | xargs -d \n echo
fi
