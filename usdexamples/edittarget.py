from pxr import Usd
from pxr import Sdf

from utils import createAttribute, createReferencedSubLayersWithMultipleRoots, createSimpleLayerWithAttribute


def targetAnEditToASubLayerThenSaveThatLayer():
    '''
    Show targetting non-default layer via a stage and saving results
    '''
    stage = createReferencedSubLayersWithMultipleRoots("root.usda")
    rootLayer = stage.GetRootLayer()
    sublayerPaths = rootLayer.subLayerPaths
    subLayer = Sdf.Layer.FindOrOpen(sublayerPaths[0])
    
    stage.SetEditTarget(subLayer)
    prim = stage.DefinePrim("/extraprim")
    subLayer.Save()
    
def targetAnEditToASubLayerAndFlatten():
    '''
    Show targetting non-default layer via a stage and saving results
    '''
    stage = createReferencedSubLayersWithMultipleRoots("root.usda")
    rootLayer = stage.GetRootLayer()
    sublayerPaths = rootLayer.subLayerPaths
    subLayer = Sdf.Layer.FindOrOpen(sublayerPaths[0])
    stage.SetEditTarget(subLayer)
    prim = stage.DefinePrim("/extraprim")
    print stage.Flatten().ExportToString()
    
    
if __name__=='__main__':
    targetAnEditToASubLayerThenSaveThatLayer()