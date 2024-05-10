import dxcam

#from dxcam import DXFactory
#factory=DXFactory()
#test=DXFactory.self.get_monitor_resolutions()
test=dxcam.get_monitor_resolutions()
print(test)