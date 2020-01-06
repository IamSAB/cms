def auto_repr(obj, attrs):
    arglist = ', '.join(f'{k}={getattr(obj, k)}' for k in attrs)
    return f'{type(obj).__name__}({arglist})'
