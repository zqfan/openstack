openstack
=========

anything related to openstack handled by myself

File Format Convertion
======================

MarkDown
-------------
Need to install pandoc before do the convertion:
```
sh pandoc-install
```
Convert MarkDown to HTML
```
pandoc source.md -s -c main.css -o target.html
```
Convert MarkDown to PDF
```
pandoc source.md -s -o --latex-engine=xelatex -o target.pdf
```
```
