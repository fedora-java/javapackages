all: index.html

index.html: index.txt
	asciidoc -b html5 -a icons -a toc2 -a theme=flask index.txt

upload: index.html
	scp -r index.html images/ fedorapeople.org:public_html/java-packaging-howto/

clean:
	rm *html
