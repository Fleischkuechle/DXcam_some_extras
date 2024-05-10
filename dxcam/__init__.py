import weakref
import time
from dxcam.dxcam import DXCamera, Output, Device
import re
from dxcam.util.io import (
    enum_dxgi_adapters,
    get_output_metadata,
)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            print(f"Only 1 instance of {cls.__name__} is allowed.")

        return cls._instances[cls]


class DXFactory(metaclass=Singleton):

    _camera_instances = weakref.WeakValueDictionary()

    def __init__(self) -> None:
        p_adapters = enum_dxgi_adapters()
        self.devices, self.outputs = [], []
        for p_adapter in p_adapters:
            device = Device(p_adapter)
            p_outputs = device.enum_outputs()
            if len(p_outputs) != 0:
                self.devices.append(device)
                self.outputs.append([Output(p_output) for p_output in p_outputs])
        self.output_metadata = get_output_metadata()

    def create(
        self,
        device_idx: int = 0,
        output_idx: int = None,
        region: tuple = None,
        output_color: str = "RGB",
        max_buffer_len: int = 64,
    ):
        device = self.devices[device_idx]
        if output_idx is None:
            # Select Primary Output
            output_idx = [
                idx
                for idx, metadata in enumerate(
                    self.output_metadata.get(output.devicename)
                    for output in self.outputs[device_idx]
                )
                if metadata[1]
            ][0]
        instance_key = (device_idx, output_idx)
        if instance_key in self._camera_instances:
            print(
                "".join(
                    (
                        f"You already created a DXCamera Instance for Device {device_idx}--Output {output_idx}!\n",
                        "Returning the existed instance...\n",
                        "To change capture parameters you can manually delete the old object using `del obj`.",
                    )
                )
            )
            return self._camera_instances[instance_key]

        output = self.outputs[device_idx][output_idx]
        output.update_desc()
        camera = DXCamera(
            output=output,
            device=device,
            region=region,
            output_color=output_color,
            max_buffer_len=max_buffer_len,
        )
        self._camera_instances[instance_key] = camera
        time.sleep(0.1)  # Fix for https://github.com/ra1nty/DXcam/issues/31
        return camera

    def device_info(self) -> str:
        ret = ""
        for idx, device in enumerate(self.devices):
            ret += f"Device[{idx}]:{device}\n"
        return ret

    def output_info(self) -> str:
        ret = ""
        for didx, outputs in enumerate(self.outputs):
            for idx, output in enumerate(outputs):
                ret += f"Device[{didx}] Output[{idx}]: "
                ret += f"Res:{output.resolution} Rot:{output.rotation_angle}"
                ret += f" Primary:{self.output_metadata.get(output.devicename)[1]}\n"
        return ret

    def clean_up(self):
        for _, camera in self._camera_instances.items():
            camera.release()
   

    
        
    def extract_width_height_generic(self,input_str: str) -> tuple:
        '''
        Example:
        teststring = "(1980,2300)"
        width, height = extract_width_height_generic(input_str=teststring)
        should return width= 1980  heiht=2300
        '''
        input_str = input_str.replace("(", "").replace(")", "")  # Entferne Klammern aus dem Eingabestring
        res_match = re.search(r'(\d+),(\d+)', input_str)
        
        if res_match:
            width = int(res_match.group(1))
            height = int(res_match.group(2))
            return width, height
        else:
            return None, None

    
    # def extract_width_height_generic(self,input_str: str) -> tuple:
    #     '''# Example usage
    #     input_string = 'Res:(1920, 1200)'
    #     width, height = extract_width_height_generic(input_string)
    #     print("Width:", width)
    #     print("Height:", height)
    #     '''
    #     # Using regular expression to extract the resolution values
    #     res_match = re.search(r'Res:$((\d+), (\d+))$', input_str)
        
    #     if res_match:
    #         width = int(res_match.group(1))
    #         height = int(res_match.group(2))
    #         return width, height
    #     else:
    #         return None, None

    #newly added
    def get_monitor_resolutions(self)->list[dict]:
        _output:list[dict]=[]
        for didx, outputs in enumerate(self.outputs):
            for idx, output in enumerate(outputs):
                width, height = self.extract_width_height_generic(output.resolution)
                #print(width)
                #print(height)
                bla:str=self.output_metadata.get(output.devicename)[1]
                #monitor:dict={"Monitor:":idx,"Resolution:":output.resolution,"Primary:":bla}
                monitor:dict={"Monitor:":idx,"width":width,"height":height,"Primary:":self.output_metadata.get(output.devicename)[1]}
                _output.append(monitor)
                _output.update(monitor)
                #ret += f"Device[{didx}] Output[{idx}]: "
                #ret += f"Res:{output.resolution} Rot:{output.rotation_angle}"
                #ret += f" Primary:{self.output_metadata.get(output.devicename)[1]}\n"
        return _output



__factory = DXFactory()


def create(
    device_idx: int = 0,
    output_idx: int = None,
    region: tuple = None,
    output_color: str = "RGB",
    max_buffer_len: int = 64,
):
    return __factory.create(
        device_idx=device_idx,
        output_idx=output_idx,
        region=region,
        output_color=output_color,
        max_buffer_len=max_buffer_len,
    )


def device_info():
    return __factory.device_info()


def output_info():
    return __factory.output_info()

#newly added
def get_monitor_resolutions()->list[dict]:
    # test=__factory.get_monitor_resolutions()
    # return test
    return __factory.get_monitor_resolutions()

