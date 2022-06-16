import /*;*/ edu.umd.cs.findbugs.annotations/*;*/.Nullable; /*;*/ // ;

class Class4 {
    <T extends @Nullable(value = "true") Object> T method(@Nullable(value = "true") Object o) {
        new @Nullable(value = "true") Object();
    }
}
