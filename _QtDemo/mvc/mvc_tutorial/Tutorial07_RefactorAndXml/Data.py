'''
Created on 3 maj 2011

@author: Yasin
'''

from Qt import QtXml



def enum(*enumerated):
    enums = dict(zip(enumerated, range(len(enumerated))))
    enums["names"] = enumerated
    return type('enum', (), enums)
    
    

LIGHT_SHAPES = enum("Point", "Spot", "Directional", "Area", "Volumetric", "End")


class Node(object):
    
    def __init__(self, name, parent=None):
        
        super(Node, self).__init__()
        
        self._name = name
        self._children = []
        self._parent = parent
        
        if parent is not None:
            parent.addChild(self)


    def attrs(self):

        classes = self.__class__.__mro__

        kv = {}

        for cls in classes:
            for k, v in cls.__dict__.iteritems():
                if isinstance(v, property):
                    print "Property:", k.rstrip("_"), "\n\tValue:", v.fget(self)
                    kv[k] = v.fget(self)

        return kv



    def asXml(self):
        
        doc = QtXml.QDomDocument()
        

        node = doc.createElement(self.typeInfo())
        doc.appendChild(node)
       
        for i in self._children:
            i._recurseXml(doc, node)

        return doc.toString(indent=4)


    def _recurseXml(self, doc, parent):
        node = doc.createElement(self.typeInfo())
        parent.appendChild(node)

        attrs = self.attrs().iteritems()
        
        for k, v in attrs:
            node.setAttribute(k, v)

        for i in self._children:
            i._recurseXml(doc, node)





    def typeInfo(self):
        return "NODE"

    def addChild(self, child):
        self._children.append(child)
        child._parent = self

    def insertChild(self, position, child):
        
        if position < 0 or position > len(self._children):
            return False
        
        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        
        if position < 0 or position > len(self._children):
            return False
        
        child = self._children.pop(position)
        child._parent = None

        return True



    def name():
        def fget(self): return self._name
        def fset(self, value): self._name = value
        return locals()
    name = property(**name())


    def child(self, row):
        return self._children[row]
    
    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent
    
    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)


    def log(self, tabLevel=-1):

        output     = ""
        tabLevel += 1
        
        for i in range(tabLevel):
            output += "\t"
        
        output += "|------" + self._name + "\n"
        
        for child in self._children:
            output += child.log(tabLevel)
        
        tabLevel -= 1
        output += "\n"
        
        return output

    def __repr__(self):
        return self.log()


    def data(self, column):
        
        if   column is 0: return self.name
        elif column is 1: return self.typeInfo()
    
    def setData(self, column, value):
        if   column is 0: self.name = value
        elif column is 1: pass
    
    def resource(self):
        return None


class TransformNode(Node):
    
    def __init__(self, name, parent=None):
        super(TransformNode, self).__init__(name, parent)

        self._x = 0
        self._y = 0
        self._z = 0

    def typeInfo(self):
        return "TRANSFORM"


    def x():
        def fget(self): return self._x
        def fset(self, value): self._x = value
        return locals()
    x = property(**x())

    def y():
        def fget(self): return self._y
        def fset(self, value): self._y = value
        return locals()
    y = property(**y())
    
    def z():
        def fget(self): return self._z
        def fset(self, value): self._z = value
        return locals()
    z = property(**z())



    def data(self, column):
        r = super(TransformNode, self).data(column)
        
        if   column is 2: r = self.x
        elif column is 3: r = self.y
        elif column is 4: r = self.z
        
        return r
    
    def setData(self, column, value):
        super(TransformNode, self).setData(column, value)
        
        if   column is 2: self.x = value
        elif column is 3: self.y = value
        elif column is 4: self.z = value
    
    def resource(self):
        return ":/Transform.png"


class CameraNode(Node):
    
    def __init__(self, name, parent=None):
        super(CameraNode, self).__init__(name, parent)
          
        self._motionBlur = True
        self._shakeIntensity = 50.0
                    
    def typeInfo(self):
        return "CAMERA"


    def motionBlur():
        def fget(self): return self._motionBlur
        def fset(self, value): self._motionBlur = value
        return locals()
    motionBlur = property(**motionBlur())
     
    def shakeIntensity():
        def fget(self): return self._shakeIntensity
        def fset(self, value): self._shakeIntensity = value
        return locals()
    shakeIntensity = property(**shakeIntensity()) 


        
    def data(self, column):
        r = super(CameraNode, self).data(column)
        
        if   column is 2: r = self.motionBlur
        elif column is 3: r = self.shakeIntensity
        
        return r
    
    def setData(self, column, value):
        super(CameraNode, self).setData(column, value)
        
        if   column is 2: self.motionBlur     = value
        elif column is 3: self.shakeIntensity = value
    
    def resource(self):
        return ":/Camera.png"



class LightNode(Node):
    
    def __init__(self, name, parent=None):
        super(LightNode, self).__init__(name, parent)

        self._intensity = 1.0
        self._nearRange = 40.0
        self._farRange = 80.0
        self._castShadows = True
        self._shape = LIGHT_SHAPES.names[0]

    def typeInfo(self):
        return "LIGHT"
    



    def intensity():
        def fget(self): return self._intensity
        def fset(self, value): self._intensity = value
        return locals()
    intensity = property(**intensity())
    
    def nearRange():
        def fget(self): return self._nearRange
        def fset(self, value): self._nearRange = value
        return locals()
    nearRange = property(**nearRange())
    
    def farRange():
        def fget(self): return self._farRange
        def fset(self, value): self._farRange = value
        return locals()
    farRange = property(**farRange())
        
    def castShadows():
        def fget(self): return self._castShadows
        def fset(self, value): self._castShadows = value
        return locals()
    castShadows = property(**castShadows())

    def shape():
        def fget(self): return self._shape
        def fset(self, value): self._shape = value
        return locals()
    shape = property(**shape())
        
        
        
    def data(self, column):
        r = super(LightNode, self).data(column)
        
        if   column is 2: r = self.intensity
        elif column is 3: r = self.nearRange
        elif column is 4: r = self.farRange
        elif column is 5: r = self.castShadows
        elif column is 6: r = LIGHT_SHAPES.names.index(self.shape)
        
        return r
    
    def setData(self, column, value):
        super(LightNode, self).setData(column, value)
        
        if   column is 2: self.intensity   = value
        elif column is 3: self.nearRange   = value
        elif column is 4: self.farRange    = value
        elif column is 5: self.castShadows = value
        elif column is 6: self.shape       = LIGHT_SHAPES.names[value]
        
    def resource(self):
        return ":/Light.png"
        
        
        
        
        

        
