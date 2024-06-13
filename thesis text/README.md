# AIML LaTeX thesis template

Getting started
---------------

1. Install an up-to-date LaTeX distribution (e.g. [TeX Live](https://www.tug.org/texlive/))
2. Clone the repository `git clone https://gitlab.lrz.de/kiml/latex-thesis-template.git`
3. Build the document using `latexmk` or another build tool of your choice:
```latexmk -pdf main.tex```
4. The finished document will be called `main.pdf`
5. Customize your thesis settings in `my-thesis-setup.tex`

Best practices
------------------

### References
The thesis template uses the LaTeX package [BibLaTeX](https://www.ctan.org/pkg/biblatex?lang=de) in conjunction with the [Biber](http://biblatex-biber.sourceforge.net/) engine which supports UTF-8 bibliographies.

A well curated source of BibTeX entries is the [dblp](http://dblp.uni-trier.de/). Search for your references here, export the record and download the file as `.bib` file. The contents you can paste into your `bib-refs.bib` file.

#### Useful BibLaTeX commands:
* `\textcite{doe2015}`: Inserts the name(s) of the author(s) at the current position and 
follows it with the reference.
* `\parencite{doe2015}`: Insert only the reference(s) at this position in parentheses.
* `\citeauthor{doe2015}`: Output the name(s) of the author(s).
* `\citeyear{doe2015}`: Inserts the year of the publication.
* Capitalize the commands if it is at the beginning of a sentence (e.g. `\Textcite{doe2015}`)
* For more commands check out the detailed [BibLaTeX documentation](https://ftp.uni-erlangen.de/ctan/macros/latex/contrib/biblatex/doc/biblatex.pdf)
