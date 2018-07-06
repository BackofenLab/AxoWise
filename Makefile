
genia_tagger:
	wget http://www.nactem.ac.uk/tsujii/GENIA/tagger/geniatagger-3.0.2.tar.gz
	tar -xvzf geniatagger-3.0.2.tar.gz
	rm -rf geniatagger-3.0.2.tar.gz
	$(MAKE) -C geniatagger-3.0.2
	git clone https://github.com/bornabesic/genia-tagger-py
	mv genia-tagger-py/geniatagger.py .
	rm -rf genia-tagger-py/

stanford_core_nlp:
	wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip
	unzip stanford-corenlp-full-2018-02-27.zip
	rm -rf stanford-corenlp-full-2018-02-27.zip

stanford_parser:
	wget https://nlp.stanford.edu/software/stanford-parser-full-2018-02-27.zip
	unzip stanford-parser-full-2018-02-27.zip
	rm -rf stanford-parser-full-2018-02-27.zip
