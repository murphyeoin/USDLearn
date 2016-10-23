from pxr import Usd, Sdf

'''
Convenient access to a fairly wide range of layer functionality via Stage...
'''



'''Create a stage with a root layer called "bottomLayer.usda"... '''
currStage = Usd.Stage.CreateNew('/var/tmp/bottomLayer66.usda')  
prim1 = currStage.DefinePrim("/test")
attr = prim1.CreateAttribute("testAttribute", Sdf.ValueTypeNames.String )
attr.Set("originalValue")

'''Open an existing layer'''
#currStage = Usd.Stage.Open('./def.usda')


'''get the root layer'''
rootLayer = currStage.GetRootLayer()


'''save the root layer to disk - if it's an existing layer, will overwrite it'''
currStage.GetRootLayer().Save()


'''Return a single, anonymous, merged layer for this composite scene.'''
flattenedLayer = currStage.Flatten()
print "flattenedLayer", flattenedLayer.ExportToString()


'''
SESSION LAYER/EDIT TARGET
'''



'''show that the session layer is empty'''
print "sessionLayer (empty?) ", currStage.GetSessionLayer().ExportToString(), "\n-------"

print 'editTarget before change (rootLayer)', currStage.GetEditTarget().GetLayer() #show editTarget is the RootLayer

currStage.SetEditTarget(currStage.GetSessionLayer())

print 'editTarget after change (sessionLayer)', currStage.GetEditTarget().GetLayer() #show editTarget is the SessionLayer

'''add some stuff to the session layer (which is the default edit target)'''
prim = currStage.GetPrimAtPath('/test')
attr = prim1.GetAttribute("testAttribute")
attr.Set("newValue")

'''now show that the session layer has some stuff in it'''
print "sessionLayer contents ", currStage.GetSessionLayer().ExportToString(), "\n-------"
#print "xxx", currStage.Flatten().ExportToString(),"yyy"

'''
Can also access layer functionality directly via Sdf Layer
'''
subLayer = Sdf.Layer.FindOrOpen('./def.usda')
