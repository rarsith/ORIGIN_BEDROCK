class XXX:
    def method1(self):
        print("Method 1 is available.")

    def method2(self):
        print("Method 2 is available.")

    # Define other methods...


class WWW:
    allowed_methods = {'method1'}

    def __init__(self):
        self.x_instance = XXX()

    def __getattr__(self, attr):
        if attr in self.allowed_methods:
            return getattr(self.x_instance, attr)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")


class QQQ:
    allowed_methods = {'method2'}

    def __init__(self):
        self.x_instance = XXX()

    def __getattr__(self, attr):
        if attr in self.allowed_methods:
            return getattr(self.x_instance, attr)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")


# Example usage
www_obj = WWW()
www_obj.method1()  # Method 1 is called
# www_obj.method2()  # This will raise an AttributeError because method2 is not available in WWW

qqq_obj = QQQ()
qqq_obj.method2()  # Method 2 is called
# qqq_obj.method1()  # This will raise an AttributeError because method1 is not available in QQQ
