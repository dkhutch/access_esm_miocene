# access_esm_miocene
Scripts to generate input and restart files for running ACCESS-ESM1.5 in a Miocene configuration. This is a work in progress, so please treat with care and healthy scepticism. Here is a rough outline of what I do to generate a new set of restart/input files for ACCESS-ESM.

## 1 Create the ocean input files

Go into the directory **make_ocean**. Run the following scripts:

- **make_topog.py** : This interpolates the original Miocene topography (0.5 deg resolution) onto the model grid.
- **adjust_topo_mio.py** : This gets rid of the isolated ocean grid cells (lakes and narrow straits), and makes a few manual adjustments. The output is **topog_mio_v3.nc** which is the new ocean bathymetry file.
- **fill_restart_gaps_mio.py** : This extrapolates the pre-industrial temperature/salinity restart file onto the new land-seak mask.
- **basin_mask_mio.py** : Adjusts basin_mask.nc for the new land-sea mask
- **bgc_restart_mio.py** : Adjusts csiro_bgc.res.nc for the new land-sea mask
- **bgc_sediment_mio.py** : Adjusts csiro_bgc_sediment.res.nc for the new land-sea mask
- **fix_kmt.py** : Adjusts kmt.nc for the new land-sea mask
- **ssw_mio.py** : Adjusts ssw_atten_depth.nc for the new land-sea mask

