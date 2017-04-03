# Coupler desing

## Creating geometry - create_geo.py
$ python create_geo.py -h
usage: create_geo.py [-h] [--LX LX] [--LY LY] [--n_low N_LOW]
                     [--n_high N_HIGH] [-r RESOLUTION] [--x_in X_IN]
                     [--y_in Y_IN] [--lx_in LX_IN] [--ly_in LY_IN]
                     [--x_out X_OUT] [--y_out Y_OUT] [--lx_out LX_OUT]
                     [--ly_out LY_OUT] [--x_dev X_DEV] [--y_dev Y_DEV]
                     [--lx_dev LX_DEV] [--ly_dev LY_DEV] [-i DEVICE_FILE]
                     [-o INDEX_FILE]

create computational domain to meep(refractive index map).Positions and sizes
in micro meters.

optional arguments:
  -h, --help       show this help message and exit
  --LX LX          comp. domain X size
  --LY LY          comp. domain Y size
  --n_low N_LOW    Low refractive index
  --n_high N_HIGH  High refractive index
  -r RESOLUTION    resolution
  --x_in X_IN      Input wg X position (left corner)
  --y_in Y_IN      Input wg Y position (botton corner)
  --lx_in LX_IN    Input wg X length
  --ly_in LY_IN    Input wg Y length
  --x_out X_OUT    Output wg X position (left corner)
  --y_out Y_OUT    Output wg Y position (botton corner)
  --lx_out LX_OUT  Output wg X length
  --ly_out LY_OUT  Output wg Y length
  --x_dev X_DEV    Device X position (left corner)
  --y_dev Y_DEV    Device Y position (botton corner)
  --lx_dev LX_DEV  Device X length
  --ly_dev LY_DEV  Device Y length
  -i DEVICE_FILE   CVS file mapping the device refractive index
  -o INDEX_FILE    H5 file mapping full domain the refractive index

# Use example
Creating a h5 file with a straigth waveguide.




# Remeber that:
Courant [number]
Specify the Courant factor S which relates the time step size to the spatial discretization: cΔt = SΔx. Default is 0.5. For numerical stability, the Courant factor must be at most n_\textrm{min}/\sqrt{\textrm{\# dimensions}}, where nmin is the minimum refractive index (usually 1), and in practice S should be slightly smaller.

