all: index.html

index.html: *.txt images/xmvn.svg
	asciidoc -b html5 -a icons -a toc2 -a toclevels=3 -a theme=flask index.txt

%.svg: %.dia
	dia -e $@ $<

.images_uploaded: images/* images/icons/*
	mkdir -p doc || :
	cp -r images/ doc/
	scp -r doc fedorahosted.org:javapackages
	touch .images_uploaded


upload: index.html .images_uploaded
	mkdir doc || :
	cp *.html doc
	scp -r doc fedorahosted.org:javapackages

clean:
	rm -f *.html images/*.svg
