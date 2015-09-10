GOLD=$1
OUT=$2

cut -d" " -f3 $OUT | paste -d" " $GOLD - | perl conlleval.txt

