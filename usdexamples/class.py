#!/usr/bin
from pxr import Usd
from pxr import Sdf

from utils import createAttribute, createReferencedSubLayersWithMultipleRoots, createSimpleLayerWithAttribute, getRootPrim


def createLayerWithClass(filePath, rootPrimPath, attrValue=None):
    '''
    create a simple layer with some prims
    '''
    currStage = Usd.Stage.CreateNew(filePath)
    rootLayer = currStage.GetRootLayer()
    prim = currStage.CreateClassPrim(rootPrimPath)
    if attrValue:
        createAttribute(prim, 'testAttribute', Sdf.ValueTypeNames.String, attrValue)    
   
    return currStage, prim


def useClassToDefineType():
    '''
    '''
    currStage, classPrim = createLayerWithClass('class1.usda',"/myClass", "bolix")
    currStage.DefinePrim('/myClass/myClassChild')
    inheritingPrim = currStage.DefinePrim('/a/b/c', 'myClass')
    attr = inheritingPrim.GetAttribute("benny")
    rootLayer = currStage.GetRootLayer()
    
    #rootLayer.Save()
    print rootLayer.ExportToString()
    print currStage.Flatten().ExportToString()
    
def createLayerWithInheritanceInClass():
    '''
    '''
    currStage, classPrim = createLayerWithClass('class2.usda',"/myClass", "defaultClassValue")
    currStage.DefinePrim('/myClass/myClassChild')
    inheritingPrim = currStage.DefinePrim('/a/b/c')
    inheritingPrim.GetInherits().Add('/myClass')
    attr = inheritingPrim.GetAttribute("testAttribute")
    attr.Set("haveOverridenInstancedPrimDirectly")
    inheritingPrim = currStage.DefinePrim('/a/b/d')
    inheritingPrim.GetInherits().Add('/myClass')
    
    currStage.SetDefaultPrim(getRootPrim(inheritingPrim, '/a/b/c'))
    rootLayer = currStage.GetRootLayer()
    
    rootLayer.Save()
#     print rootLayer.ExportToString()
#     print currStage.Flatten().ExportToString()    
    
def referenceLayerWithClassIntoPrim():
    '''
    the class disappears (See spiffs note about this)
    But according to example in "http://graphics.pixar.com/usd/overview.html#USDFeatureSpecification-Classes" 
    we should still be able to override the book?
    '''
    createLayerWithInheritanceInClass()
    currStage = Usd.Stage.CreateNew("referenceLayerWithClassIntoPrim.usda")
    rootLayer = currStage.GetRootLayer()
    prim = currStage.DefinePrim('/x/y/z')
    prim.GetReferences().Add('class2.usda')
    prim.GetReferences().Add('class2.usda','/myClass') #dont know about this
    
#     prim = currStage.GetPrimAtPath('/x/y/myClass')
#     attr = prim.GetAttribute("testAttribute")
#     attr.Set('XXX')
    
    prim = currStage.GetPrimAtPath('/myClass')
    print "this prim will be null", prim
    rootLayer.Save()
    print rootLayer.ExportToString()
    print currStage.Flatten().ExportToString()    
    
def referenceLayerWithClassIntoSublayer():
    '''
    we still have access to the class
    we override the attribute value in the class and then 
    '''
    createLayerWithInheritanceInClass()
    currStage = Usd.Stage.CreateNew("referenceLayerWithClassIntoSublayer.usda")
    rootLayer = currStage.GetRootLayer()
    rootLayer.subLayerPaths.append('class2.usda')
    
    prim = currStage.GetPrimAtPath('/myClass')
    attr = prim.GetAttribute("testAttribute")
    attr.Set("haveOverridenClassReferencedViaSubLayer") #This creates an Over for us
    rootLayer.Save()
    print rootLayer.ExportToString()
    print currStage.Flatten().ExportToString()    



if __name__=='__main__':
    referenceLayerWithClassIntoPrim()