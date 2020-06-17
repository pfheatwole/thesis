#!/bin/sh

rm -f commands.txt forces/*
python build_commands.py
avl belloc.avl < commands.txt
python build_datasets.py
mkdir -p polars
mv -f beta*.txt polars
