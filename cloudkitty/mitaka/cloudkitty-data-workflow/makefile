NAME := $(notdir $(shell pwd))

pdf:
	pandoc $(NAME).md --slide-level 2 -t beamer -o $(NAME).tex
	pdflatex main.tex
	mv main.pdf $(NAME).pdf
	rm ${NAME}.tex

clean:
	-rm *.log *.aux *.nav *.toc *.snm *.out
	-rm $(NAME).tex
	-rm $(NAME).pdf
