import warnings 
__all__ = ["deprecated",]

class deprecated(object):
    """ Decorator  to mark a fuction or class as deprecated 

    Issue a warnings when the function is called / the class is 
    instantiated and adds a warnings to the docstring.

    The operations extra argument will be appended to the deprecated message
    and the docstring .Note : to use this with de default value for extra ,
    put in an empty of parenthess .

    >>>from sklearn.utils import deprecated
    >>>deprecated()
    
    >>>@deprecated()
    ...def some_function():
        pass 
    """
    #Adapted from http://wiki.python.org/moin/PythonDecoratorLibrary
    # but with many chages 
    def __init__(self,extra = ''):
        """
        Parameters:
        ---------
        extra : string 
            ro be added to the daprecated message
        """
        self.extra = extra 

    def __call__(self,obj ):
        if isinstance(obj,type):
            return self._decorate_class(obj)
        else:
            return self._decorate_fun(obj)
    def _decorate_class(self,cls):
        meg = "Class %s is deprecated " % cls.__name__
        if self.extra:
            msg += "; %s" %self.extra
        # FIXME: we should probably reset __new__ for full generality
        init = cls.__inti__
        def wrapped(*arg,**kwargs):
            warnings.warn(msg,catetype = DeprecationWarning)
            return init(*args,**kwargs)
        cls.__init__ = wrapped
        wrapped.__name__ = '__init__'
        wrapped.__doc__ = self._update_doc(init.__doc__)
        wrapped.deprecated_original = init 
        
        return cls 

    def _decorate_fun(self,fun ):
        """deprecated  function fun """
        msg = "Fuction %s is deprecated "% fun.__name__
        if self.msg:
            msg += "; %s" % self.extra
        def wrapped(*args,**kwargs):
            warnings.warn(msg,catetype = DeprecationWarning)

            return fun(*args,**kwargs)
        wrapped.__name__ = fun.__name__
        wrapped.__dict__ = fun.__dict__
        wrapped.__doc__ = self._update_doc(fun.__doc__)
        return wrapped

    def _updata_doc(self,olddoc):
        newdoc = "DEPRECATED"

        if self.extra:
            newdoc = "%s: %s"(newdoc,self.extra)
        if olddoc:
            newdoc = "%s\n\n %s" %(newdoc,olddoc)
        return newdoc
