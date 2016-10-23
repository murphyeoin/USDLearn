#!/usr/bin
from pxr import Usd, UsdGeom
from pxr import Sdf

'''
@otodo set doc
'''


def create():
    
    currStage = Usd.Stage.CreateNew('./primForest.usda')
    
    '''
    Create 3 separate Hierarchies
    '''
   
    prim1 = currStage.DefinePrim("/A1/B1/C1")
    prim2= currStage.DefinePrim("/A2/B2/C2")
    prim3 = currStage.DefinePrim("/A3/B3/C3")
    
    currStage.SetDefaultPrim(currStage.GetPrimAtPath('/A1'))
    
    currStage.GetRootLayer().Save()
    print "flattened", currStage.ExportToString()
    
    
def referenceIn():
    currStage = Usd.Stage.CreateInMemory()
    
    prim1 = currStage.DefinePrim("/root")
    prim1.GetReferences().Add('./primForest.usda')
    print "referenceIn", currStage.Flatten().ExportToString()


def subLayerIn():
    currStage = Usd.Stage.CreateInMemory()
    currStage.GetRootLayer().comment = "sublayer in the original primForest.usda "
    currStage.GetRootLayer().documentation = "docs"
    currStage.GetRootLayer().subLayerPaths.append('./primForest.usda')
    print "subLayerIn Unflattened    ", currStage.GetRootLayer().ExportToString()
    print "subLayerIn Flattened", currStage.Flatten().ExportToString()

if __name__=='__main__':
    create()
    referenceIn()
    subLayerIn()