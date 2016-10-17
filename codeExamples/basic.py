#!/usr/bin
from pxr import Usd
from pxr import Sdf

from utils import createAttribute, createReferencedSubLayersWithMultipleRoots, createSimpleLayerWithAttribute

def createSomeDefs():
    '''
    '''
    currStage = Usd.Stage.CreateNew('bottomLayer.usda')
    prim1 = currStage.DefinePrim("/a/b/c")
    currStage.GetRootLayer().Save()
    print "flattened", currStage.Flatten().ExportToString()


def createOverrideOnTopOfSubLayer():
    '''
    '''
    currStage = Usd.Stage.CreateNew('bottomLayer.usda')
    prim1 = currStage.DefinePrim("/a/b/c")
    currStage.GetRootLayer().Save()
    
    currStage = Usd.Stage.CreateNew('topLayer.usda')
    currStage.GetRootLayer().subLayerPaths.append('bottomLayer.usda')
    prim2 = currStage.DefinePrim("/a/b/c/d")
    
    print "unflattened", currStage.GetRootLayer().ExportToString() #shows different result to save!
    print "flattened", currStage.Flatten().ExportToString()


def createBasicReference():
    '''
    Diagram: "USD Referencing 1"
    show that we can reference, and we keep attributes from both referenced and referencing layers
    '''
    
    createSimpleLayerWithAttribute("layerB.usda", "/X/Y/Z", "referencedLayer")
    currStage = Usd.Stage.Open("layerB.usda")
    prim = currStage.GetPrimAtPath('/X')
    createAttribute(prim, "testAttribute2", "string", "referencedLayer")
    currStage.GetRootLayer().Save()
    
    createSimpleLayerWithAttribute("layerA.usda", "/A/B/C", "referencingLayer")
    currStage = Usd.Stage.Open("layerA.usda")
    prim = currStage.GetPrimAtPath("/A/B/C")
    prim.GetReferences().Add("layerB.usda")
    
    print "unflattened", currStage.GetRootLayer().ExportToString() #shows different result to save!
    print "flattened", currStage.Flatten().ExportToString()
    
    
def testHierarchicalInheritanceOfAttribute():
    '''
    looks like no!
    '''
    currStage = Usd.Stage.CreateNew('hierarchicalAttribs.usda')
    prim1 = currStage.DefinePrim("/a/b/c")
    prim = currStage.GetPrimAtPath('/a')
    createAttribute(prim, "testAttribute", Sdf.ValueTypeNames.String, "shazam")
    attrib = prim1.GetAttribute('testAttribute')
    print attrib
    attrib = prim.GetAttribute('testAttribute')
    print attrib

def createMultipleReference():
    '''
    Diagram: "USD Referencing 2"
    show that we can reference, and we keep attributes from both referenced and referencing layers
    '''
    
    createSimpleLayerWithAttribute("layerB.usda", "/X/Y/Z")
    currStage = Usd.Stage.Open("layerB.usda")
    prim = currStage.GetPrimAtPath('/X')
    createAttribute(prim, "testAttribute2", "string", "referencedLayer")
    currStage.GetRootLayer().Save()
    
    
    createSimpleLayerWithAttribute("layerA.usda", "/A/B/C", "referencingLayer")
    currStage = Usd.Stage.Open("layerA.usda")
    primA = currStage.GetPrimAtPath("/A/B/C")
    primB = currStage.DefinePrim('/A/B/D')
    createAttribute(primB, "testAttribute3", "string", "referencingLayer")
    
    primA.GetReferences().Add("layerB.usda")
    primB.GetReferences().Add("layerB.usda")
    
    print "unflattened", currStage.GetRootLayer().ExportToString() #shows different result to save!
    print "flattened", currStage.Flatten().ExportToString()

def createDefAndOverrideInSameLayer():
    '''
    we can see that for a/b only writes the composed result as the override is local
    
    def "a"
    {
        def "b"
        {
            custom string testattr = "override"
        }
    
        over "c"
        {
            custom string testattr = "override2"
        }
    }
    '''
    currStage = Usd.Stage.CreateNew('createDefAndOverrideInSameLayer.usda')
    prim1 = currStage.DefinePrim("/a/b")
    createAttribute(prim1,"testattr", "string", "definition")
    prim2 = currStage.OverridePrim("/a/b")
    createAttribute(prim2,"testattr", "string", "override")
    prim3 = currStage.OverridePrim("/a/c")
    createAttribute(prim3,"testattr", "string", "override2")
    currStage.GetRootLayer().Save()
    print "basic", currStage.ExportToString() #shows different result to save!
    print "flattened", currStage.Flatten().ExportToString()




if __name__=='__main__':
    testHierarchicalAttributes()