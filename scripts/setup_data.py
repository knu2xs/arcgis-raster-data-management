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
__title__ = 'setup_data'
__version__ = '0.0.0'
__author__ = 'Joel McCune and TJ Abbenhaus'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2023 by Joel McCune and TJ Abbenhaus'

from pathlib import Path

import arcpy

if __name__ == '__main__':

    # list of data resources to create
    data_lst = ['external', 'interim', 'processed', 'raw']

    # get the path to top level project directory
    dir_prj = Path(__file__).parent.parent

    # path to the data directory
    dir_data = dir_prj / 'data'

    # iteratively walk into and create the data directories if needed
    for child_nm in data_lst:

        # create the path to the directory
        dir_child = dir_data / child_nm

        # if it does not exist, create it
        if not dir_child.exists():
            dir_child.mkdir(parents=True)

        # create the path to the file geodatabase
        gdb = dir_child / f'{child_nm}.gdb'

        # if the child gdb does not exist, create it
        if not gdb.exists():
            arcpy.CreateFileGDB_management(str(gdb.parent), str(gdb.name))
