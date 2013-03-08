
package org.fedoraproject.helloworld;

// import Input class from org.fedoraproject.helloworld.input package
import org.fedoraproject.helloworld.input.Input;
// import Output class from org.fedoraproject.helloworld.output package
import org.fedoraproject.helloworld.output.Output;

class HelloWorld {
    public static void main(String[] args) {
        System.out.print("What is your name?: ");
        String reply = Input.getInput();
        Output.output(reply);
    }
}
