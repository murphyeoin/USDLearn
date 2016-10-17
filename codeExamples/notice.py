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



def createBasicReference():
    '''
    Diagram: "USD Referencing 1"
    show that we can reference, and we keep attributes from both referenced and referencing layers
    '''
    
    createSimpleLayerWithAttribute("layerB.usda", "/X/Y/Z", "referencedLayer")
    currStage = Usd.Stage.Open("layerB.usda")
    prim = currStage.GetPrimAtPath('/X')
    createAttribute(prim, "testAttribute2", Sdf.ValueTypeNames.String, "referencedLayer")
    currStage.GetRootLayer().Save()
    
    print dir(Usd.Notice)
    print dir(Usd.Notice.StageNotice.GetStage())
    
    
    




if __name__=='__main__':
    createBasicReference()