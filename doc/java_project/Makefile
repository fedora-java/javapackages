#!/usr/bin/make -f

compile: 
	rm -rf compiled/
	mkdir compiled/
	javac `find . -name *java` -d compiled -cp src/

jar: compile
	rm -f helloworld.jar
	jar cfe helloworld.jar org.fedoraproject.helloworld.HelloWorld -C compiled .


clean:
	rm -rf *jar compiled
