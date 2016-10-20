#!/usr/bin
from pxr import Usd, UsdGeom
from pxr import Sdf
from pxr import Vt
import itertools

'''
@otodo set doc
'''


def doIt():
    '''
    Create a simple Prim
    '''
    
    currStage = Usd.Stage.CreateNew('def2.usda')
    prim = currStage.DefinePrim("/A")
    attr = prim.CreateAttribute("testAttribute", Sdf.ValueTypeNames.String )
    attr.Set("myAttribute")
    
    '''
    Create a Simple Hierarchy
    '''
   
    prim = currStage.DefinePrim("/AA/BB/CC")
    
    #note this will return a primSpec, not a prim
    rootLayer = currStage.GetRootLayer()
    primSpec = rootLayer.GetPrimAtPath('/AA')
    
    prim = currStage.GetPrimAtPath('/AA')
    attr = prim.CreateAttribute("testAttribute", Sdf.ValueTypeNames.String )
    attr.Set("myAttribute1") 
    
    prim = currStage.GetPrimAtPath('/AA/BB')
    attr = prim.CreateAttribute("testAttribute", Sdf.ValueTypeNames.String )
    attr.Set("myAttribute2") 
    
    prim = currStage.GetPrimAtPath('/AA/BB/CC')
    attr = prim.CreateAttribute("testAttribute", Sdf.ValueTypeNames.String )
    attr.Set("myAttribute3") 
    
    
    prim = currStage.DefinePrim("/TheThing", "InventedThing")
    
    '''
    Mesh - using UsdGeomMesh schema example
    '''
    prim = currStage.DefinePrim("/Box", "Mesh")
    
    mesh = UsdGeom.Mesh(prim)
    points =  Vt.Vec3dArray([(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5)])
    mesh.CreatePointsAttr(points)
    mesh.CreateFaceVertexIndicesAttr([0, 1, 3, 2, 2, 3, 5, 4, 4, 5, 7, 6, 6, 7, 1, 0, 1, 7, 5, 3, 6, 0, 2, 4])
    mesh.CreateFaceVertexCountsAttr(list(itertools.repeat(4,6)))
    mesh.CreateExtentAttr([(-0.5, -0.5, -0.5), (0.5, 0.5, 0.5)])
    
    currStage.GetRootLayer().Save()
    print "flattened", currStage.Flatten().ExportToString()


if __name__=='__main__':
    doIt()