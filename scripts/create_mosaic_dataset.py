"""
Licensing

Copyright 2020 Esri

Licensed under the Apache License, Version 2.0 (the "License"); You
may not use this file except in compliance with the License. You may
obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing
permissions and limitations under the License.

A copy of the license is available in the repository's
LICENSE file.
"""
__title__ = 'create_mosaic_dataset'
__version__ = '0.0.0'
__author__ = 'Joel McCune and TJ Abbenhaus'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2023 by Joel McCune and TJ Abbenhaus'

from pathlib import Path

import arcpy

# list of possible raster extensions
raster_extensions = ['.tif', '.tiff']

# output mosaic dataset name
mosaic_name = 'NDVI_OrganicFarm'

if __name__ == '__main__':

    # get the path to top level project directory
    dir_prj = Path(__file__).parent.parent

    # path to the data directory
    dir_data = dir_prj / 'data'

    # path to location to find rasters and location for mosaic dataset
    dir_rasters = dir_data / 'raw' / 'raw_rasters'
    mosaic_pth = dir_data / 'processed' / 'processed.gdb' / mosaic_name

    # get the source rasters as a list of paths
    raster_lst = [f for f in dir_rasters.glob(r'**/*') if f.suffix in raster_extensions]

    # ensure all source rasters are same data type
    extension_lst = list(set(r.suffix for r in raster_lst))
    if len(extension_lst) > 1:
        raise ValueError('Can only add a single raster type to a Mosaic dataset. Found more than one in the source '
                         f'raster directory, {extension_lst}')

    # read properties from the first raster
    desc = arcpy.da.Describe(str(raster_lst[0]))

    # create the mosaic dataset using properties of the first raster
    arcpy.management.CreateMosaicDataset(
        in_workspace=str(mosaic_pth.parent),
        in_mosaicdataset_name=str(mosaic_pth.name),
        coordinate_system=desc['spatialReference'],
        num_bands=desc['bandCount']
    )

    # load the rasters from the source directory to the mosaic dataset
    # https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/add-rasters-to-mosaic-dataset.htm
    arcpy.management.AddRastersToMosaicDataset(
        in_mosaic_dataset=str(mosaic_pth),
        raster_type='Raster Dataset',
        input_path=[str(pth) for pth in raster_lst],
        update_cellsize_ranges=True,
        update_boundary=True,
        update_overviews=True,
        # maximum_pyramid_levels=,
        # maximum_cell_size=,
        # minimum_dimension=,
        spatial_reference=desc['spatialReference'],
        # filter=,
        # sub_folder=,
        duplicate_items_action='EXCLUDE_DUPLICATES',
        build_pyramids=True,
        calculate_statistics=True,
        build_thumbnails=True,
        # operation_description=,
        # force_spatial_reference=,
        estimate_statistics=True,
        # aux_inputs=,
        enable_pixel_cache=True,
        # cache_location=
    )
