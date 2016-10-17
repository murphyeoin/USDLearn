#!/usr/bin
from pxr import Usd
from pxr import Sdf

from utils import createAttribute, createReferencedSubLayersWithMultipleRoots, createSimpleLayerWithAttribute

def createColourVariantSet(rootPrim):
    '''
    and set green to be the default
    '''
    vset = rootPrim.GetVariantSets().FindOrCreate('shadingVariant')
    vset.FindOrCreateVariant('red')
    vset.FindOrCreateVariant('blue')
    vset.FindOrCreateVariant('green')
    
    vset.SetVariantSelection("red")
    with vset.GetVariantEditContext():
        createAttribute(rootPrim, 'colour', 'string', vset.GetVariantSelection())
    vset.SetVariantSelection("blue")
    with vset.GetVariantEditContext():
        createAttribute(rootPrim, 'colour', 'string', vset.GetVariantSelection())
    vset.SetVariantSelection("green")
    with vset.GetVariantEditContext():
        createAttribute(rootPrim, 'colour', 'string', vset.GetVariantSelection())
        
        

        #createAttribute(rootPrim, 'colour', 'string', vset.GetVariantSelection())

def variantCreationSimple1():
    layerInfo = ['variantCreationSimple1', '/a1/b1/c1']
    filepath = "./" + layerInfo[0] + '.usda'
    currStage = Usd.Stage.CreateNew(filepath)
    rootPrim = currStage.DefinePrim(layerInfo[1])
    createColourVariantSet(rootPrim)
    print currStage.GetRootLayer().ExportToString()
    currStage.GetRootLayer().Save()
    

def variantCreationWithPrims():
    '''
    create a prim for each variant
    '''
    layerInfo = ['variantCreationWithPrims', '/a1/b1/c1']
    filepath = "./" + layerInfo[0] + '.usda'
    currStage = Usd.Stage.CreateNew(filepath)
    rootPrim = currStage.DefinePrim('/a1/b1/c1')
    vset = rootPrim.GetVariantSets().FindOrCreate('modellingVariant')
    
    vset.FindOrCreateVariant('red1')
    vset.SetVariantSelection("red1")
    with vset.GetVariantEditContext():
        currStage.DefinePrim('/a1/b1/c1/xx')
    
    vset.FindOrCreateVariant('green1')
    vset.SetVariantSelection("green1")
    with vset.GetVariantEditContext():
        currStage.DefinePrim('/a1/b1/c1/yy')
    
    vset.FindOrCreateVariant('blue1')
    vset.SetVariantSelection("blue1")
    with vset.GetVariantEditContext():
        currStage.DefinePrim('/a1/b1/c1/zz')

    print currStage.GetRootLayer().ExportToString()
    print "\t\t\t ===== Flattened ====== "
    print currStage.Flatten().ExportToString()
    currStage.GetRootLayer().Save()
    

def variantsWithReferenceModification():
    '''
    '''
    createSimpleLayerWithAttribute('layerA.usda', '/a0/b0/c0', attrValue="firstLayerRef", define=True)
    createSimpleLayerWithAttribute('layerB.usda', '/a1/b1/c1', attrValue="secondLayerRef", define=True)
    
    layerInfo = ['variantCreationWithReferenceModification', '/x']
    filepath = "./" + layerInfo[0] + '.usda'
    currStage = Usd.Stage.CreateNew(filepath)
    rootPrim = currStage.DefinePrim(layerInfo[1])
    vset = rootPrim.GetVariantSets().FindOrCreate('bazVariant')
    
    vset.FindOrCreateVariant('first')
    vset.SetVariantSelection("first")
    with vset.GetVariantEditContext():
        rootPrim = currStage.GetPrimAtPath('/x')
        rootPrim.GetReferences().Add('layerA.usda')
    
    vset.FindOrCreateVariant('second')
    vset.SetVariantSelection("second")
    with vset.GetVariantEditContext():
        rootPrim = currStage.GetPrimAtPath('/x')
        rootPrim.GetReferences().Add('layerB.usda')

    vset.SetVariantSelection("first")
    print currStage.GetRootLayer().ExportToString()
    print "\t\t\t ===== Flattened ====== "
    print currStage.Flatten().ExportToString()
    currStage.GetRootLayer().Save()
    
    
    
def variantsWithReferenceModificationAndHierarchySelfModification():
    '''
    '''
    createSimpleLayerWithAttribute('./layerA.usda', '/a0/y/z', attrValue="firstLayerRef", define=False)
    createSimpleLayerWithAttribute('./layerB.usda', '/a1/y/z', attrValue="secondLayerRef", define=False)
    
    layerInfo = ['variantsWithReferenceModificationAndHierarchySelfModification', '/x/y/z']
    filepath = "./" + layerInfo[0] + '.usda'
    currStage = Usd.Stage.CreateNew(filepath)
    rootPrim = currStage.DefinePrim(layerInfo[1])
    vset = currStage.GetPrimAtPath('/x').GetVariantSets().FindOrCreate('bazVariant')
    
    vset.FindOrCreateVariant('first')
    vset.SetVariantSelection("first")
    with vset.GetVariantEditContext():
        rootPrim = currStage.GetPrimAtPath('/x')
        rootPrim.GetReferences().Add('./layerA.usda')
    
    vset.FindOrCreateVariant('second')
    vset.SetVariantSelection("second")
    with vset.GetVariantEditContext():
        rootPrim = currStage.GetPrimAtPath('/x')
        rootPrim.GetReferences().Add('./layerB.usda')

    currStage.GetRootLayer().Save()
    print currStage.GetRootLayer().ExportToString()
    print "\t\t\t ===== Flattened ====== "
    print currStage.Flatten().ExportToString()

def variantsWithReferenceModificationAndHierarchySelfModificationNested():
    '''
    '''
    def createLayerWithSurfVariantSelectionOvers(path, attrValue):
        layerInfo = [path, '/blah/y/z']
        filepath = "./" + layerInfo[0] + '.usda'
        currStage = Usd.Stage.CreateNew(filepath)
        rootPrim = currStage.OverridePrim(layerInfo[1])
        currStage.SetDefaultPrim(rootPrim.GetParent().GetParent())
        createAttribute(rootPrim, 'surfVarName', 'string', attrValue)    
        createColourVariantSet(rootPrim)
        currStage.GetRootLayer().Save()
    
    createLayerWithSurfVariantSelectionOvers('layerSurfvarA', "SurfVarA")
    createLayerWithSurfVariantSelectionOvers('layerSurfvarB', "SurfVarB")
    
    layerInfo = ['variantsWithReferenceModificationAndHierarchySelfModificationNested', '/x/y/z']
    filepath = "./" + layerInfo[0] + '.usda'
    currStage = Usd.Stage.CreateNew(filepath)
    rootPrim = currStage.DefinePrim(layerInfo[1])
    vset = currStage.GetPrimAtPath('/x').GetVariantSets().FindOrCreate('bazVariant')
    
    vset.FindOrCreateVariant('first')
    vset.SetVariantSelection("first")
    with vset.GetVariantEditContext():
        rootPrim = currStage.GetPrimAtPath('/x')
        createAttribute(rootPrim, 'geoVarName', 'string', "geoFirst")    
        rootPrim.GetReferences().Add('./layerSurfvarA.usda')
    
    vset.FindOrCreateVariant('second')
    vset.SetVariantSelection("second")
    with vset.GetVariantEditContext():
        rootPrim = currStage.GetPrimAtPath('/x')
        createAttribute(rootPrim, 'geoVarName', 'string', "geoSecond")    
        rootPrim.GetReferences().Add('./layerSurfvarB.usda')
        
        #This selects the red surfvar inside
        prim = currStage.OverridePrim('/x/y/z')
        variantSet = prim.GetVariantSets().GetVariantSet('shadingVariant')
        variantSet.SetVariantSelection('red')

    currStage.GetRootLayer().Save()
    print currStage.GetRootLayer().ExportToString()
    print "\t\t\t ===== Flattened ====== "
    print currStage.Flatten().ExportToString()

def variantCreationNested():
    '''
    an example of how nested variants work
    While the in-memory representation seems fine, the serialised form looks a bit weird - 
    some details here:
    http://www.al.com.au/display/rnd/USD+-+Discussions+with+Pixar#USD-DiscussionswithPixar-Variants
    '''
    
    layerInfo = ['variantCreationNested', '/a1/b1/c1']
    filepath = "./" + layerInfo[0] + '.usda'
    currStage = Usd.Stage.CreateNew(filepath)
    rootPrim = currStage.DefinePrim('/a1/b1/c1')
    vset = rootPrim.GetVariantSets().FindOrCreate('meal')
    
    vset.FindOrCreateVariant('breakfast')
    vset.FindOrCreateVariant('lunch')
    
    vset.SetVariantSelection("breakfast")
    with vset.GetVariantEditContext():
        prim = currStage.DefinePrim('/a1/b1/c1/breakfast')
        vset2 = prim.GetVariantSets().FindOrCreate('mealChoice')
        vset2.FindOrCreateVariant('muesli')
        vset2.FindOrCreateVariant('granola')
        
        vset2.SetVariantSelection("muesli")
        with vset2.GetVariantEditContext():
            prim = currStage.DefinePrim('/a1/b1/c1/breakfast/muesli')
            createAttribute(prim, 'milk', 'bool', True)
        
        vset2.SetVariantSelection("granola")
        with vset2.GetVariantEditContext():
            prim = currStage.DefinePrim('/a1/b1/c1/breakfast/granola')
            createAttribute(prim, 'milk', 'bool', True)
            
    
    vset.SetVariantSelection("lunch")
    with vset.GetVariantEditContext():
        prim = currStage.DefinePrim('/a1/b1/c1/lunch')
        vset2 = prim.GetVariantSets().FindOrCreate('mealChoice')
        vset2.FindOrCreateVariant('sandwich')
        vset2.FindOrCreateVariant('pasta')
        
        vset2.SetVariantSelection("sandwich")
        with vset2.GetVariantEditContext():
            prim = currStage.DefinePrim('/a1/b1/c1/lunch/sandwich')
            createAttribute(prim, 'salt', 'bool', True)
        
        vset2.SetVariantSelection("pasta")
        with vset2.GetVariantEditContext():
            prim = currStage.DefinePrim('/a1/b1/c1/lunch/pasta')
            createAttribute(prim, 'salt', 'bool', True)

    currStage.GetRootLayer().Save()
    print currStage.GetRootLayer().ExportToString()
    print currStage.Flatten().ExportToString()


def variantCreationNestedReadBack():
    '''
    read back a file containing what looks like the correct serialised form (formatted the way we want)
    see notes on variantCreationNested above
    '''
    
    filepath = "./variantCreationNestedRight.usda"
    currStage = Usd.Stage.Open(filepath)
    print currStage.GetRootLayer().ExportToString()
    print currStage.Flatten().ExportToString()
    

    
def controlVariantSelectionFromLayer():
    layerInfo = ['basicVariant', '/a1/b1/c1']
    filepath = "./" + layerInfo[0] + '.usda'
    currStage = Usd.Stage.CreateNew(filepath)
    rootPrim = currStage.DefinePrim(layerInfo[1])
    createColourVariantSet(rootPrim)
    currStage.GetRootLayer().Save()
    
    currStage = Usd.Stage.CreateNew('topLayer.usda')
    currStage.GetRootLayer().subLayerPaths.append(layerInfo[0] + '.usda')
    primWithVariant = currStage.GetPrimAtPath(layerInfo[1])
    variantSet = primWithVariant.GetVariantSets().GetVariantSet('shadingVariant')
    variantSet.SetVariantSelection('red')
    currStage.GetRootLayer().Save()
    
    print "unflattened", currStage.GetRootLayer().ExportToString() 
    print "flattened", currStage.Flatten().ExportToString()

if __name__=='__main__':
    variantsWithReferenceModificationAndHierarchySelfModificationNested()
