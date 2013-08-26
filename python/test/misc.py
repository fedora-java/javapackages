
def exception_expected(ex):
    """Marks test to expect the specified exception. Call assertRaises internally"""
    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            self.assertRaises(ex, fn, self, *args, **kwargs)
        return test_decorated
    return test_decorator
