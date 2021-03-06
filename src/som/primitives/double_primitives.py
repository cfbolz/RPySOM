from rpython.rlib.rfloat import (formatd, DTSF_ADD_DOT_0, DTSF_STR_PRECISION,
    NAN, INFINITY, isfinite, round_double)

from som.primitives.primitives import Primitives
from som.vmobjects.primitive   import Primitive
from som.vmobjects.double      import Double
from som.vmobjects.integer     import Integer

import math

def _coerce_to_double(obj, universe):
    if isinstance(obj, Double):
        return obj
    if isinstance(obj, Integer):
        return universe.new_double(float(obj.get_embedded_integer()))
    raise ValueError("Cannot coerce %s to Double!" % obj)

def _asString(ivkbl, frame, interpreter):
    rcvr = frame.pop()
    d = rcvr.get_embedded_double()
    s = formatd(d, "g", DTSF_STR_PRECISION, DTSF_ADD_DOT_0)
    frame.push(interpreter.get_universe().new_string(s))

def _sqrt(ivkbl, frame, interpreter):
    rcvr = frame.pop()
    frame.push(interpreter.get_universe().new_double(math.sqrt(rcvr.get_embedded_double())))

def _plus(ivkbl, frame, interpreter):
    op1 = _coerce_to_double(frame.pop(), interpreter.get_universe())
    op2 = frame.pop()
    frame.push(interpreter.get_universe().new_double(op1.get_embedded_double()
                                         + op2.get_embedded_double()))

def _minus(ivkbl, frame, interpreter):
    op1 = _coerce_to_double(frame.pop(), interpreter.get_universe())
    op2 = frame.pop()
    frame.push(interpreter.get_universe().new_double(op2.get_embedded_double()
                                         - op1.get_embedded_double()))
def _mult(ivkbl, frame, interpreter):
    op1 = _coerce_to_double(frame.pop(), interpreter.get_universe())
    op2 = frame.pop()
    frame.push(interpreter.get_universe().new_double(op2.get_embedded_double()
                                         * op1.get_embedded_double()))

def _doubleDiv(ivkbl, frame, interpreter):
    op1 = _coerce_to_double(frame.pop(), interpreter.get_universe())
    op2 = frame.pop()
    frame.push(interpreter.get_universe().new_double(op2.get_embedded_double()
                                           / op1.get_embedded_double()))

def _mod(ivkbl, frame, interpreter):
    op1 = _coerce_to_double(frame.pop(), interpreter.get_universe())
    op2 = frame.pop()
    
    o1 = float(op1.get_embedded_double())
    o2 = float(op2.get_embedded_double())
    r = math.fmod(o1, o2)
    frame.push(interpreter.get_universe().new_double(r))

def _equals(ivkbl, frame, interpreter):
    op1 = _coerce_to_double(frame.pop(), interpreter.get_universe())
    op2 = frame.pop()
    if op1.get_embedded_double() == op2.get_embedded_double():
        frame.push(interpreter.get_universe().trueObject)
    else:
        frame.push(interpreter.get_universe().falseObject)

def _lessThan(ivkbl, frame, interpreter):
    op1 = _coerce_to_double(frame.pop(), interpreter.get_universe())
    op2 = frame.pop()
    if op2.get_embedded_double() < op1.get_embedded_double():
        frame.push(interpreter.get_universe().trueObject)
    else:
        frame.push(interpreter.get_universe().falseObject)

def _and(ivkbl, frame, interpreter):
    op1 = _coerce_to_double(frame.pop(), interpreter.get_universe())
    op2 = frame.pop()
    
    left  = int(op2.get_embedded_double())
    right = int(op1.get_embedded_double())
    result = float(left & right)
    frame.push(interpreter.get_universe().new_double(result))

def _bitXor(ivkbl, frame, interpreter):
    op1 = _coerce_to_double(frame.pop(), interpreter.get_universe())
    op2 = frame.pop()
    
    left  = int(op2.get_embedded_double())
    right = int(op1.get_embedded_double())
    result = float(left ^ right)
    frame.push(interpreter.get_universe().new_double(result))

def _round(ivkbl, frame, interpreter):
    rcvr = frame.pop()
    int_value = int(round_double(rcvr.get_embedded_double(), 0))
    frame.push(interpreter.get_universe().new_integer(int_value))

class DoublePrimitives(Primitives):

    def install_primitives(self):        
        self._install_instance_primitive(Primitive("asString", self._universe, _asString))
        self._install_instance_primitive(Primitive("round",    self._universe, _round))
        self._install_instance_primitive(Primitive("sqrt", self._universe, _sqrt))
        self._install_instance_primitive(Primitive("+",  self._universe, _plus))
        self._install_instance_primitive(Primitive("-",  self._universe, _minus))
        self._install_instance_primitive(Primitive("*",  self._universe, _mult))
        self._install_instance_primitive(Primitive("//", self._universe, _doubleDiv))
        self._install_instance_primitive(Primitive("%",  self._universe, _mod))
        self._install_instance_primitive(Primitive("=",  self._universe, _equals))
        self._install_instance_primitive(Primitive("<",  self._universe, _lessThan))
        
        self._install_instance_primitive(Primitive("&",  self._universe, _and))
        self._install_instance_primitive(Primitive("bitXor:",  self._universe, _bitXor))
