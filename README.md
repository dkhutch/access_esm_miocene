# access_esm_miocene
Scripts to generate input and restart files for running ACCESS-ESM1.5 in a Miocene configuration. This is a work in progress, so please treat with care and healthy scepticism. Here is a rough outline of what I do to generate a new set of restart/input files for ACCESS-ESM.

## 1 Create the ocean input files

Go into the directory **make_ocean**. Run the following:

- **make_topog.py** : This interpolates the original Miocene topography (0.5 deg resolution) onto the model grid.
- **adjust_topo_mio.py** : This gets rid of the isolated ocean grid cells (lakes and narrow straits), and makes a few manual adjustments. The output is **topog_mio_v3.nc** which is the new ocean bathymetry file.
- **fill_restart_gaps_mio.py** : This extrapolates the pre-industrial temperature/salinity restart file onto the new land-seak mask.
- **basin_mask_mio.py** : Adjusts basin_mask.nc for the new land-sea mask
- **bgc_restart_mio.py** : Adjusts csiro_bgc.res.nc for the new land-sea mask
- **bgc_sediment_mio.py** : Adjusts csiro_bgc_sediment.res.nc for the new land-sea mask
- **fix_kmt.py** : Adjusts kmt.nc for the new land-sea mask
- **ssw_mio.py** : Adjusts ssw_atten_depth.nc for the new land-sea mask

## 2 Create the coupler grids

Go into the directory **make_coupler_grids**. Run the following:

- **regrid_um_mask.py** : Updates the masks.nc for the new land-sea mask (using topog_mio_v3.nc). This also generates **landfrac_um1t.nc**, which is the fractional land-sea mask for the Miocene.
- **make_scrip_files.ncl** : An NCL script to convert the grids and masks into SCRIP files for ESMF
- **run_esmf_regrid.sh** : Generates the remapping files using ESMF_RegridWeightGen
- **run_rename_oasis.sh** : Renames the remapping files using OASIS conventions for the model

## 3 Create the atmos restart files

Go into the directory **make_atmos**. Run the following:

- **make_lsm.py** : Generates a netcdf file of the new binary land-sea mask called **lsm_mio_v3.nc**, using the landfrac_um1t.nc fractional land mask.
- **interp_fields_mio.py** : Uses nearest neighbour interpolation to create a new atmos restart file on the updated land-sea mask. The new restart file is called **restart.mio**. This script relies on utility scripts located in:
/g/data/access/projects/access/apps/pythonlib/umfile_utils/
- **interp_fields_mio_arg.py** : This is a command-line script (using argparse) requiring an input and output file of ancillary files. This should be done as in the following:
- ./interp_fields_mio_arg.py cable_vegfunc_N96.anc cable_vegfunc_N96.anc.mio
- ./interp_fields_mio_arg.py qrclim.slt qrclim.slt.mio
- ./interp_fields_mio_arg.py qrclim.smow qrclim.smow.mio
- ./interp_fields_mio_arg.py qrparm.mask qrparm.mask.mio
- ./interp_fields_mio_arg.py qrparm.soil_igbp_vg qrparm.soil_igbp_vg.mio

In each case above, the "input" is the pre-industrial ancillary file, and the "output" is the Miocene one.

## 4 Make coupler restart files

Go to directory **coupler_inputs**. Run the following:

- **fix_a2i_mio.py** : Adjusts a2i.nc flux file for the new mask.
- **fix_i2a_mio.py** : Adjusts i2a.nc flux file for the new mask.
- **fix_o2i_mio.py** : Adjusts o2i.nc flux file for the new mask.

## 5 Make ocean common files

Go to directory **oc_common**. Run the following:

- **dust_mio.py** : Adjusts dust.nc file for new mask.
- **fice_mio.py** : Adjusts ocmip2_fice_monthly_om1p5_bc.nc file for the new mask.
- **press_mio.py** : Adjusts ocmip2_press_monthly_om1p5_bc.nc file for the new mask.
- **xkw_mio.py** : Adjusts ocmip2_xkw_monthly_om1p5_bc.nc file for the new mask.