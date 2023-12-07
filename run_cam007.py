import vmbpy
import matplotlib.pyplot as plt

id = 'DEV_000F314D57E9'

try:
    vmb = vmbpy.VmbSystem.get_instance()
    vmb._startup()
    c=vmb.get_camera_by_id(id)
    c._open()
    f = c.get_frame()
    f.conver_pixel_format(PixelFormat.Mono)
    c._close()
    vmb._shutdown()
except:
    c._close()
    vmb._shutdown()
    print('failed')

vmb._shutdown()