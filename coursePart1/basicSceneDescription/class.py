#!/usr/bin
from pxr import Usd
from pxr import Sdf

def doIt():
    '''
    '''
    currStage = Usd.Stage.CreateNew('class2.usda')
    primClass = currStage.CreateClassPrim("/SimpleClass")
    attr = primClass.CreateAttribute("attrDefinedOn", Sdf.ValueTypeNames.String )
    attr.Set("class-SimpleClass") 
    
    '''
    inheriting only prim
    '''
    
    prim1 = currStage.DefinePrim("/MyPrim")
    prim1.GetInherits().Add(primClass.GetPath())
    
    '''
    inheriting and overriding prim
    '''
    prim1 = currStage.DefinePrim("/MyOverridingPrim")
    prim1.GetInherits().Add(primClass.GetPath())
    attr = prim1.CreateAttribute("attrDefinedOn", Sdf.ValueTypeNames.String )
    attr.Set("MyOverridingPrim") 
    
    currStage.GetRootLayer().Save()
    print "unflattened", currStage.GetRootLayer().ExportToString()
    print "flattened", currStage.Flatten().ExportToString() #flattened version of file removes class


if __name__=='__main__':
    doIt()