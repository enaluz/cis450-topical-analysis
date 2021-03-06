def exceptionHandler(childFunction):
    def higherOrderFunction(*args, **kwargs):
        try:
            return childFunction(*args, **kwargs)
        except Exception as e:
            print("Caught Error: ", e)
            pass
    return higherOrderFunction


def classDecorator(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate
