
package org.fedoraproject.helloworld.input;

import java.util.Scanner;

public class Input {
    public static String getInput() {
        Scanner s = new Scanner(System.in);
        return s.next();
    }
}
