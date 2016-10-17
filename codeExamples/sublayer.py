
from pxr import Usd
from pxr import Sdf

from utils import createAttribute, createReferencedSubLayersWithMultipleRoots, createSimpleLayerWithAttribute



def showBasicSubLayering():
    '''
    show non overlapping def prims to start with for illustrative purposes..
    '''
    #root layer
    rootStage = createSimpleLayerWithAttribute("showSubLayerOrderRoot.usda", "/rootPrim",'alpha')
 
    #sublayer 1
    createSimpleLayerWithAttribute("showSubLayerOrderSubA.usda", "/subLayerAPrim", 'beta')
    createSimpleLayerWithAttribute("showSubLayerOrderSubB.usda", "/subLayerBPrim", 'gamma')
    
    rootStage.GetRootLayer().subLayerPaths.append("showSubLayerOrderSubA.usda")
    rootStage.GetRootLayer().subLayerPaths.append("showSubLayerOrderSubB.usda")
    print rootStage.Flatten().ExportToString()
    
def showSubLayerForest():
    stage = createReferencedSubLayersWithMultipleRoots("root.usda")
    print "inputFile",stage.GetRootLayer().ExportToString()
    print "composedOutput",stage.ExportToString()

def showSubLayerOrderRelativeToRoot():
    '''
    show overlapping def prims with same attribute 
    SHOWS that the layer that includes the sublayer wins
    '''
    #root layer
    rootStage = createSimpleLayerWithAttribute("showSubLayerOrderRoot.usda", "/rootie",'alpha')
 
    #sublayer 1 - same attributes
    createSimpleLayerWithAttribute("showSubLayerOrderSubA.usda", "/rootie", 'beta')
    rootStage.GetRootLayer().subLayerPaths.append("showSubLayerOrderSubA.usda")
    
    print rootStage.Flatten().ExportToString()
    

def showSubLayerWithOver():
    '''
    overlapping prims - one def (root) one over (sublayer)
    SHOWS that the referencing layer wins completely
    '''
    #root layer
    rootStage = createSimpleLayerWithAttribute("showSubLayerOrder4_root.usda", "/rootie",'alpha')
 
    #sublayer 1
    createSimpleLayerWithAttribute("showSubLayerOrderSubA.usda", "/rootie", 'beta', define=False)
    
    rootStage.GetRootLayer().subLayerPaths.append("showSubLayerOrderSubA.usda")
    print rootStage.Flatten().ExportToString() #The override is nowhere to be seen as it's weaker
    

def showOrderingOfMultipleSubLayers():
    '''
    show overlapping def prims
    Shows they're in order from strongest to weakest 
    '''
    #root layer
    rootStage = createSimpleLayerWithAttribute("showSubLayerOrderRoot.usda", "/rootPrim",'alpha')
 
    #sublayer 1
    createSimpleLayerWithAttribute("showSubLayerOrderSubA.usda", "/subLayerPrim", 'subLayerA')
    createSimpleLayerWithAttribute("showSubLayerOrderSubB.usda", "/subLayerPrim", 'subLayerB')
    
    rootStage.GetRootLayer().subLayerPaths.append("showSubLayerOrderSubA.usda")
    rootStage.GetRootLayer().subLayerPaths.append("showSubLayerOrderSubB.usda")
    print rootStage.Flatten().ExportToString()  #result is rootie2.greek=beta


    
    
if __name__=='__main__':
    showOrderingOfMultipleSubLayers()