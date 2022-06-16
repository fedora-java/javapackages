import org.junit.jupiter.api.Test;
import edu.umd.cs.findbugs.annotations.SuppressFBWarnings;

@SuppressWarnings
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
class Class3 {
    @Test
    public void test1() {
    }
    
    @org.junit.Test
    public void test2() {
    }
    
    @org.junit.jupiter.api.Test
    public void test3() {
    }
}
