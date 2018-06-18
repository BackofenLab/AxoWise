
genia_tagger:
	wget http://www.nactem.ac.uk/tsujii/GENIA/tagger/geniatagger-3.0.2.tar.gz
	tar -xvzf geniatagger-3.0.2.tar.gz
	rm -rf geniatagger-3.0.2.tar.gz/
	$(MAKE) -C geniatagger-3.0.2
