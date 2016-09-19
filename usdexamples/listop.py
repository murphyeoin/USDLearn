#!/usr/bin
from pxr import Usd
from pxr import Sdf

from utils import createAttribute, CreateRefLayers
    
def showListOpManipulationWithWeakerLayer():
    '''
    can we remove/add/clear a referenced layer via listops?
    looks like if the referenced layer is lower down in the hierarchy than the override, 
    we can only add..
    
    '''
    ''
    CreateRefLayers.createA()
    CreateRefLayers.createB()
    CreateRefLayers.createC()
 
    #Overriding layer
    layerInfo = ['overridingLayer', '/a1/b1/c1']
    filepath = "./" + layerInfo[0] + '.usda'
    currStage = Usd.Stage.CreateNew(filepath)
    prim = currStage.OverridePrim(layerInfo[1])
    createAttribute(prim, 'layerNameOverride', Sdf.ValueTypeNames.String, layerInfo[0])
    ref = Sdf.Reference('refdLayerA.usda')
    prim.GetReferences().Remove(ref) #gets serialised - seems to not have the intended effect?
    #prim.GetReferences().Clear()  #Clear is not serialisable - happens in place
    prim.GetReferences().Add('refdLayerB.usda') #can do an add and a remove together. The add seems to have the intended effect
    ref2 = Sdf.Reference('refdLayerC.usda')
    #prim.GetReferences().SetItems([ref2]) #even a setitems doesnt seem to delete the underlying refdLayerA, but it does remove refdLayerB
    currStage.SetDefaultPrim(prim.GetParent().GetParent())
    currStage.GetRootLayer().Save()
    
    #root layer
    layerInfo = ['showListOpOverridingRoot1', '/a1/b1/c1']
    filepath = "./" + layerInfo[0] + '.usda'
    currStage = Usd.Stage.CreateNew(filepath)
    prim = currStage.DefinePrim('/a1/b1/c1')
    prim.GetReferences().Add(ref)
    prim2 = currStage.GetPrimAtPath('/a1')
    prim2.GetReferences().Add('overridingLayer.usda')
    currStage.SetDefaultPrim(prim.GetParent().GetParent())
    #currStage.GetRootLayer().subLayerPaths.append('overridingLayer.usda')
    currStage.GetRootLayer().Save()
    

    
    rootStage = Usd.Stage.Open('showListOpOverridingRoot1.usda')
    rootStage.GetRootLayer().Save()
    print "basic", rootStage.ExportToString() #shows different result to save!
    print "flattened", rootStage.Flatten().ExportToString()
    
    
def showListOpManipulationWithStrongerLayer():
    '''
    can we remove/add/clear a referenced layer via listops?
    looks like if the referenced layer is lower down in the hierarchy than the override, 
    we can only add..
    
    '''
    ''
    refA = CreateRefLayers.createA()
    refB = CreateRefLayers.createB()
    refC = CreateRefLayers.createC()

    
    #sub layer with reference at c1
    layerInfo = ['subLayer1', '/aSub/bSub']
    filepath = "./" + layerInfo[0] + '.usda'
    currStage = Usd.Stage.CreateNew(filepath)
    prim = currStage.DefinePrim(layerInfo[1])
    prim.GetReferences().SetItems([refA, refB])
    currStage.SetDefaultPrim(prim.GetParent())
    currStage.GetRootLayer().Save()
    
 
    #Root layer - reference in the sublayer
    layerInfo = ['rootLayer', '/aRoot']
    filepath = "./" + layerInfo[0] + '.usda'
    currStage = Usd.Stage.CreateNew(filepath)
    
    #this doesnt work - i.e the references dont get removed.. 
    #prim = currStage.DefinePrim(layerInfo[1])
    #prim.GetReferences().Add('subLayer1.usda')
    #createAttribute(prim, 'layerNameOverride', 'string', layerInfo[0])
    
    #but doing it this way does..
    currStage.GetRootLayer().subLayerPaths.append('subLayer1.usda')
    prim2 = currStage.OverridePrim('/aSub/bSub')
    
    #like this 
    prim2.GetReferences().Remove(refA)
    prim2.GetReferences().Remove(refB)
    prim2.GetReferences().Add(refC)
    
    #doing this undoes the changes we've just added
    #prim2.GetReferences().Clear()
    
    currStage.GetRootLayer().Save()
    
    rootStage = Usd.Stage.Open('rootLayer.usda')
    rootStage.GetRootLayer().Save()
    print "basic", rootStage.ExportToString() #shows different result to save!
    print "flattened", rootStage.Flatten().ExportToString()
    
if __name__=='__main__':
    showListOpManipulationWithWeakerLayer()