from pxr import Usd
from pxr import Sdf

def createAttribute(prim, attrName, attrType, attrValue):
    attr = prim.CreateAttribute(attrName, attrType )
    attr.Set(attrValue)
    
def getRootPrim(prim, primPath):
    numElements = len(primPath.split('/'))-1
    
    currPrim = prim
    for x in range(0, numElements-1):
        currPrim = currPrim.GetParent()
    return currPrim

def createSimpleLayer(primHierarchy, filepath):
    currStage = Usd.Stage.CreateNew(filepath)
    for item in primHierarchy.split('/'):
        prim = currStage.DefinePrim('/' + item)
    currStage.GetRootLayer().Save()
    return currStage, currStage.GetRootLayer()
    

def createReferencedSubLayersWithMultipleRoots(rootFilePath):
    '''
    create a root layer, and reference in 3 other layers (layerA,layerB,layerC) as sublayers
    @rtype USDStage
    '''
    shotStage = Usd.Stage.CreateNew(rootFilePath)
    rootLayer = shotStage.GetRootLayer()
    subLayers = ['layerA','layerB','layerC']
    subLayerContents = ['layerA_a/layerA_b/layerA_c', 'layerB_a/layerB_b/layerB_c', 'layerC_a/layerC_b/layerC_c']
    for subLayerPath, subLayerHierarchy in zip(subLayers, subLayerContents):
        path = "./" + subLayerPath + '.usda'
        createSimpleLayer(subLayerHierarchy, path)
        rootLayer.subLayerPaths.append(path)
    rootLayer.Save()
    return shotStage
    
def createSimpleLayerWithAttribute(filePath, rootPrimPath, attrValue=None, define=True):
    '''
    create a simple layer with some prims
    '''
    currStage = Usd.Stage.CreateNew(filePath)
    rootLayer = currStage.GetRootLayer()
    if define:
        prim = currStage.DefinePrim(rootPrimPath)
        currStage.SetDefaultPrim(getRootPrim(prim, rootPrimPath))
    else:
        prim = currStage.OverridePrim(rootPrimPath)
        currStage.SetDefaultPrim(getRootPrim(prim, rootPrimPath))
    
    if attrValue:
        createAttribute(prim, 'testAttribute', Sdf.ValueTypeNames.String, attrValue)    
    rootLayer.Save()
    return currStage



class CreateRefLayers(object):
    '''
    Utility creation
    '''
    @staticmethod
    def createA():
        print "Sdf.ValueTypeName", dir(Sdf.ValueTypeName)
        
        #Referenced Layer  A
        layerInfo = ['refdLayerA', '/a2/b2/c2']
        filepath = "./" + layerInfo[0] + '.usda'
        currStage = Usd.Stage.CreateNew(filepath)
        prim = currStage.DefinePrim(layerInfo[1])
        createAttribute(prim, 'randomAttributeInReferencedLayerA', Sdf.ValueTypeNames.String, layerInfo[0])
        currStage.SetDefaultPrim(prim.GetParent().GetParent())
        currStage.GetRootLayer().Save()
        return Sdf.Reference(layerInfo[0] + '.usda')
    
    @staticmethod
    def createB():
        #Referenced Layer  B
        layerInfo = ['refdLayerB', '/a3/b3/c3']
        filepath = "./" + layerInfo[0] + '.usda'
        currStage = Usd.Stage.CreateNew(filepath)
        prim = currStage.DefinePrim(layerInfo[1])
        createAttribute(prim, 'randomAttributeInReferencedLayerB', Sdf.ValueTypeNames.String, layerInfo[0])
        currStage.SetDefaultPrim(prim.GetParent().GetParent())
        currStage.GetRootLayer().Save()
        return Sdf.Reference(layerInfo[0] + '.usda')
    
    @staticmethod
    def createC():
    #Referenced Layer  C
        layerInfo = ['refdLayerC', '/a4/b4/c4']
        filepath = "./" + layerInfo[0] + '.usda'
        currStage = Usd.Stage.CreateNew(filepath)
        prim = currStage.DefinePrim(layerInfo[1])
        createAttribute(prim, 'randomAttributeInReferencedLayerC', Sdf.ValueTypeNames.String, layerInfo[0])
        currStage.SetDefaultPrim(prim.GetParent().GetParent())
        currStage.GetRootLayer().Save()
        return Sdf.Reference(layerInfo[0] + '.usda')