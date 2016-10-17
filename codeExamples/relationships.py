#!/usr/bin
from pxr import Usd
from pxr import Sdf

from utils import createAttribute

def doTheThing():
    '''
    '''
    currStage = Usd.Stage.CreateNew('bottomLayer.usda')
    prim1 = currStage.DefinePrim("/a/b/c")
    createAttribute(prim1,"testSource", Sdf.ValueTypeNames.String, "xxx")
    prim1.CreateRelationship('xxxx')
    prim2 = currStage.DefinePrim("/a/b/d")
    createAttribute(prim2,"testDest", Sdf.ValueTypeNames.String, "yyy")
    relationship = prim2.CreateRelationship('xxx', False) #Just creates an empty relationship called "xxx"
    relationship.AddTarget('/a/b/c')
    relationship = prim2.CreateRelationship('xxx', False) #add to relationship called xxxx
    relationship.AddTarget('/a/b/c.testSource')
    relationship.AddTarget('/a/b/c.testSource2') #It doesnt have to be a valid path
    
    relationshipRes = prim2.GetRelationship('xxx')
    targets = relationshipRes.GetTargets()
    for t in targets:
        print t, t.IsPrimPath(), t.IsPrimPropertyPath() #will just tell you if it LOOKS like a primpath or propertypath.. no validity
  
    print "flattened", currStage.Flatten().ExportToString()

# 

if __name__=='__main__':
    doTheThing()