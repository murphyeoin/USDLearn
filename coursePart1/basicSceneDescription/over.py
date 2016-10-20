#!/usr/bin
from pxr import Usd
from pxr import Sdf

def doIt():
    '''
    '''
    currStage = Usd.Stage.CreateNew('over2.usda')
   
    currStage.OverridePrim("/AA/BB/CC")

    prim = currStage.GetPrimAtPath('/AA')
    attr = prim.CreateAttribute("testAttribute", Sdf.ValueTypeNames.String )
    attr.Set("myAttribute1") 
    
    prim = currStage.GetPrimAtPath('/AA/BB')
    attr = prim.CreateAttribute("testAttribute", Sdf.ValueTypeNames.String )
    attr.Set("myAttribute2") 
    
    prim = currStage.GetPrimAtPath('/AA/BB/CC')
    attr = prim.CreateAttribute("testAttribute", Sdf.ValueTypeNames.String )
    attr.Set("myAttribute3") 
  
    
    currStage.GetRootLayer().Save()
    print "flattened", currStage.Flatten().ExportToString()




if __name__=='__main__':
    doIt()