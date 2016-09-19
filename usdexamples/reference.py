#!/usr/bin
from pxr import Usd
from pxr import Sdf

from utils import createAttribute
    

def showPrimReferenceOrder1():
    '''
    Shows that when there's a namespace clash when referencing, the referencing layer wins
    '''
    
    layers = ['rootLayer','referencedLayer']
    layerContents = ['/a/b/c', '/xx/c']
    cnt = 0
    for layerName, primHierarchy in zip(layers, layerContents):
        filepath = "./" + layerName + '.usda'
        currStage = Usd.Stage.CreateNew(filepath)
        prim = currStage.DefinePrim(primHierarchy)
        createAttribute(prim, 'layerName', 'string', layerName)
        if cnt==0:
            currStage.SetDefaultPrim(prim.GetParent().GetParent())
        else:
            currStage.SetDefaultPrim(prim.GetParent())
        currStage.GetRootLayer().Save()
        cnt+=1

    
    rootStage = Usd.Stage.Open('rootLayer.usda')
    prim = rootStage.GetPrimAtPath('/a/b')
    prim.GetReferences().Add('referencedLayer.usda')
    rootStage.GetRootLayer().Save()
    print "basic", rootStage.ExportToString() #shows different result to save!
    print "flattened", rootStage.Flatten().ExportToString()
    

def showPrimReferenceOrder2():
    '''
    Show a namespace clash with 2 references at different points in the hierarchy
    .. the reference lower down in the hierarchy wins...
    '''
    
    layers = ['rootLayer','referencedLayerA', 'referencedLayerB']
    layerContents = ['/a/b/c', '/xx/d', '/xx/b/d']
    cnt = 0
    for layerName, primHierarchy in zip(layers, layerContents):
        filepath = "./" + layerName + '.usda'
        currStage = Usd.Stage.CreateNew(filepath)
        prim = currStage.DefinePrim(primHierarchy)
        createAttribute(prim, 'layerName', 'string', layerName)
        #createAttribute(prim.GetParent(), 'layerNameParent', 'string', layerName)
        if cnt==0 or cnt==2:
            currStage.SetDefaultPrim(prim.GetParent().GetParent())
        else:
            currStage.SetDefaultPrim(prim.GetParent())
        currStage.GetRootLayer().Save()
        cnt+=1

    
    rootStage = Usd.Stage.Open('rootLayer.usda')
    prim = rootStage.GetPrimAtPath('/a')
    prim.GetReferences().Add('referencedLayerB.usda')
    prim = rootStage.GetPrimAtPath('/a/b')
    prim.GetReferences().Add('referencedLayerA.usda')
    rootStage.GetRootLayer().Save()
    print "basic", rootStage.ExportToString() #shows different result to save!
    print "flattened", rootStage.Flatten().ExportToString()

def showPrimReferenceOrdering():
    
    layers = ['showBasicReferencingOrderRoot','layerB','layerC']
    layerContents = ['/a1/b1/c1', '/a2/b2/c2', '/a3/b3/c3']
    for layerName, primHierarchy in zip(layers, layerContents):
        filepath = "./" + layerName + '.usda'
        currStage = Usd.Stage.CreateNew(filepath)
        prim = currStage.DefinePrim(primHierarchy)
        currStage.SetDefaultPrim(prim.GetParent().GetParent())
        currStage.GetRootLayer().Save()

    
    rootStage = Usd.Stage.Open('showBasicReferencingOrderRoot.usda')
    prim = rootStage.GetPrimAtPath('/a1/b1/c1')
    assert(prim)
    prim.GetReferences().Add('layerB.usda')
    prim.GetReferences().Add('layerC.usda')
    rootStage.GetRootLayer().Save()
    print "basic", rootStage.ExportToString() #shows different result to save!
    print "flattened", rootStage.Flatten().ExportToString()
    

def showBasicPrimReferencingOrder():
    
    layers = ['showBasicReferencingOrderRoot','layerB','layerC']
    layerContents = ['/rootLayer_a1/rootLayer_b1/rootLayer_c1', '/reflayer1_a2/reflayer1_b2/reflayer1_c2', '/reflayer2_a3/reflayer2_b3/reflayer2_c3']
    for layerName, primHierarchy in zip(layers, layerContents):
        filepath = "./" + layerName + '.usda'
        currStage = Usd.Stage.CreateNew(filepath)
        prim = currStage.DefinePrim(primHierarchy)
        currStage.SetDefaultPrim(prim.GetParent().GetParent())
        currStage.GetRootLayer().Save()

    
    rootStage = Usd.Stage.Open('showBasicReferencingOrderRoot.usda')
    prim = rootStage.GetPrimAtPath('/rootLayer_a1/rootLayer_b1/rootLayer_c1')
    assert(prim)
    prim.GetReferences().Add('layerB.usda')
    prim.GetReferences().Add('layerC.usda')
    rootStage.GetRootLayer().Save()
    print "basic", rootStage.ExportToString() #shows different result to save!
    print "flattened", rootStage.Flatten().ExportToString()
    

def showPrimReferencingWithOverrides():
    '''same as above but with some overs instead of defs...shows  the node itself is stronger'''
    
    layers = ['showPrimRefereningWithOverrideRoot','layerB','layerC']
    layerContents = ['/a1/b1/c1', '/b1/c1', '/b1/c1'] #this wont show any overrides as the prims are overs and the names are not at the same level (change to def to see)
    layerContents = ['/a1/b1/c1', '/a1/b1/c1', '/a1/b1/c1']
    cnt = 0
    for layerName, primHierarchy in zip(layers, layerContents):
        filepath = "./" + layerName + '.usda'
        currStage = Usd.Stage.CreateNew(filepath)
        if cnt==0:
            prim = currStage.DefinePrim(primHierarchy)
        else:
            prim = currStage.OverridePrim(primHierarchy)
            createAttribute(prim, 'layerNameOverride', 'string', layerName)
        createAttribute(prim, 'layerName', 'string', layerName)
            
        currStage.SetDefaultPrim(prim.GetParent().GetParent())
        currStage.GetRootLayer().Save()
        cnt = cnt+1

    
    rootStage = Usd.Stage.Open('showPrimRefereningWithOverrideRoot.usda')
    prim = rootStage.GetPrimAtPath('/a1')
    assert(prim)
    prim.GetReferences().Add('layerB.usda')
    prim.GetReferences().Add('layerC.usda')
    rootStage.GetRootLayer().Save()
    print "----basic----", rootStage.ExportToString() #shows different result to save!
    print "---flattened----", rootStage.Flatten().ExportToString()
    

def showPrimReferencing2HierarchicalNodes():
    
    layers = ['showPrimReferencing2HierarchicalNodesWithOverrides','layerB','layerC']
    layerContents = ['/a1/b1/c1', '/a2/b2/c2', '/a3/b3/c3']
    cnt = 0
    for layerName, primHierarchy in zip(layers, layerContents):
        filepath = "./" + layerName + '.usda'
        currStage = Usd.Stage.CreateNew(filepath)
        prim = currStage.DefinePrim(primHierarchy)
        createAttribute(prim, 'layerName', 'string', layerName)
            
        currStage.SetDefaultPrim(prim.GetParent().GetParent())
        currStage.GetRootLayer().Save()
        cnt = cnt+1

    
    rootStage = Usd.Stage.Open('showPrimReferencing2HierarchicalNodesWithOverrides.usda')
    prim = rootStage.GetPrimAtPath('/a1')
    prim.GetReferences().Add('layerB.usda')
    prim = rootStage.GetPrimAtPath('/a1/b1')
    prim.GetReferences().Add('layerC.usda')
    rootStage.GetRootLayer().Save()
    print "basic", rootStage.ExportToString() #shows different result to save!
    print "flattened", rootStage.Flatten().ExportToString()


def showPrimReferencing2HierarchicalNodesWithOverrides():
    '''
    shows the fairly complex hierarchical overriding behaviour
    
    def "a1"
    {
        def "b1"
        {
            def "c1"
            {
                custom string layerName = "showPrimReferencing2HierarchicalNodesWithOverrides"
                custom string layerNameOverride = "layerC"
            }
        }
    }

    
    '''
    
    layers = ['showPrimReferencing2HierarchicalNodesWithOverrides','layerB','layerC']
    layerContents = ['/a1/b1/c1', '/a1/b1/c1', '/b1/c1']
    cnt = 0
    for layerName, primHierarchy in zip(layers, layerContents):
        filepath = "./" + layerName + '.usda'
        currStage = Usd.Stage.CreateNew(filepath)
        if cnt==0:
            prim = currStage.DefinePrim(primHierarchy)
        else:
            prim = currStage.OverridePrim(primHierarchy)
            createAttribute(prim, 'layerNameOverride', 'string', layerName)
        createAttribute(prim, 'layerName', 'string', layerName)
        
        if cnt==0 or cnt==1:
            currStage.SetDefaultPrim(prim.GetParent().GetParent())
        else:
            currStage.SetDefaultPrim(prim.GetParent())
        currStage.GetRootLayer().Save()
        cnt = cnt+1

    
    rootStage = Usd.Stage.Open('showPrimReferencing2HierarchicalNodesWithOverrides.usda')
    prim = rootStage.GetPrimAtPath('/a1')  #at a1, we reference /a1/b1/c1.. the leading node disappears
    prim.GetReferences().Add('layerB.usda')
    prim = rootStage.GetPrimAtPath('/a1/b1')
    prim.GetReferences().Add('layerC.usda') #at b1, we reference /b1/c1.. the leading node disappears
    rootStage.GetRootLayer().Save()
    print "basic", rootStage.GetRootLayer().ExportToString() #shows different result to save!
    print "flattened", rootStage.Flatten().ExportToString()

def showPrimReferencingWithRelativePrimPath():
    
    #make the layers
    layers = ['showReferencingWithPathRoot','layerB']
    layerContents = ['/a1/b1/c1', '/a2/b2/c2/d2/e2/f2']
    for layerName, primHierarchy in zip(layers, layerContents):
        filepath = "./" + layerName + '.usda'
        currStage = Usd.Stage.CreateNew(filepath)
        prim = currStage.DefinePrim(primHierarchy)
        currStage.SetDefaultPrim(prim.GetParent().GetParent())
        currStage.GetRootLayer().Save()

    #make the referencing
    currStage = Usd.Stage.Open('showReferencingWithPathRoot.usda')
    prim = currStage.GetPrimAtPath('/a1')
    prim.GetReferences().Add('layerB.usda','/a2/b2') #Can only add a reference to a root prim! 
    #so cant do a2/b2 "pxr/usd/lib/usd/references.cpp : 'Cannot make a reference to a non-root prim: @layerB.usda@</a2/b2>"
    print "unflattened", currStage.GetRootLayer().ExportToString() 
    print "flattened", currStage.Flatten().ExportToString()
    
    
def showInternalReference():
    '''
    def "a1"
    {
        def "b1"
        {
            def "c1"
            {
            }
        }
    }
    
    def "a2"
    {
        def "b2"
        {
            def "c2"
            {
                def "b1"
                {
                    def "c1"
                    {
                    }
                }
            }
        }
    }
    '''

    
    #make the layers
    layerContents = ['/a1/b1/c1', '/a2/b2/c2']
    filepath = './showInternalReference.usda'
    currStage = Usd.Stage.CreateNew(filepath)
    prim1 = currStage.DefinePrim(layerContents[0])
    prim2 = currStage.DefinePrim(layerContents[1])
    currStage.SetDefaultPrim(prim1.GetParent().GetParent().GetParent())
    prim2.GetReferences().AddInternal('/a1')
    
    print "unflattened", currStage.GetRootLayer().ExportToString() 
    print "flattened", currStage.Flatten().ExportToString()
    
if __name__ == '__main__':
    showInternalReference()    
