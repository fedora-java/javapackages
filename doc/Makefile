all: index.html

index.html: *.txt images/xmvn.svg
	asciidoc -b html5 -a icons -a toc2 -a toclevels=3 -a theme=flask index.txt

%.svg: %.dia
	dia -e $@ $<

.images_uploaded: images/* images/icons/*
	scp -r images/ fedorapeople.org:public_html/java-packaging-howto/
	touch .images_uploaded


upload: index.html .images_uploaded
	scp -r index.html fedorapeople.org:public_html/java-packaging-howto/

clean:
	rm -f *.html images/*.svg
