#! /usr/bin/env bash
pandoc "whats-new.md" -c ./main.css --number-sections -o whats-new.html
