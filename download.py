import os
import argparse

slash = os.sep
parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, default=30, help='the number of images to download,\
    if you don\'t want images > 65°, please input n <= 16')
opt = parser.parse_args()

if not os.path.isdir('raw_images'):
    os.system('mkdir raw_images')

links = [
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Amenthes_DayIR_15April2016/THEMIS_DayIR_ControlledMosaic_Amenthes_000N090E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Memnonia_DayIR_15April2016/THEMIS_DayIR_ControlledMosaic_Memnonia_30S180E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/PhoenicisLacus_DayIR_15April2016/THEMIS_DayIR_ControlledMosaic_PhoenicisLacus_30S225E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/OxiaPalus_DayIR_31Jan2014/THEMIS_DayIR_ControlledMosaic_OxiaPalus_00N315E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/MargaritiferSinus_DayIR_31Jan2014/THEMIS_DayIR_ControlledMosaic_MargaritiferSinus_30S315E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/LunaePalus_DayIR_31Jan2014/THEMIS_DayIR_ControlledMosaic_LunaePalus_00N270E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Coprates_DayIR_31Jan2014/THEMIS_DayIR_ControlledMosaic_Coprates_30S270E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Amazonis_DayIR_31Jan2013/THEMIS_DayIR_ControlledMosaic_Amazonis_00N180E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Aeolis_DayIR_31Jan2014/THEMIS_DayIR_ControlledMosaic_Aeolis_30S135E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/SinusSabaeus_DayIR_31Jan2014/THEMIS_DayIR_ControlledMosaic_SinusSabaeus_30S00E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/MareTyrrhenum_DayIR_30April2015/THEMIS_DayIR_ControlledMosaic_MareTyrrhenum_30S090E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Tharsis_DayIR_30April2015/THEMIS_DayIR_ControlledMosaic_Tharsis_000N225E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Arabia_DayIR_30April2015/THEMIS_DayIR_ControlledMosaic_Arabia_000N000E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/SyrtisMajor_DayIR_31July2014/THEMIS_DayIR_ControlledMosaic_SyrtisMajor_00N45E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Iapygia_DayIR_31July2014/THEMIS_DayIR_ControlledMosaic_Iapygia_30S45E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Elysium_DayIR_31July2014/THEMIS_DayIR_ControlledMosaic_Elysium_00N135E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Eridania_DayIR_30Sept2017/THEMIS_DayIR_ControlledMosaic_Eridania_65S120E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Thaumasia_DayIR_30Sept2017/THEMIS_DayIR_ControlledMosaic_Thaumasia_65S240E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Phaethontis_DayIR_30Sept2017/THEMIS_DayIR_ControlledMosaic_Phaethontis_65S180E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Cebrenia_DayIR_30Sept2017/THEMIS_DayIR_ControlledMosaic_Cebrenia_30N120E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Diacria_DayIR_30Sept2017/THEMIS_DayIR_ControlledMosaic_Diacria_30N180E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Arcadia_DayIR_30Sept2016/THEMIS_DayIR_ControlledMosaic_Arcadia_30N240E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Argyre_DayIR_15April2016/THEMIS_DayIR_ControlledMosaic_Argyre_65S300E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Noachis_DayIR_31Jan2014/THEMIS_DayIR_ControlledMosaic_Noachis_65S00E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/MareAcidalium_DayIR_31Jan2014/THEMIS_DayIR_ControlledMosaic_MareAcidalium_30N300E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/IsmeniusLacus_DayIR_30Sept2016/THEMIS_DayIR_ControlledMosaic_Ismenius_30N00E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Casius_DayIR_30April2015/THEMIS_DayIR_ControlledMosaic_Casius_30N060E_100mpp.tif', \
    'https://planetarymaps.usgs.gov/mosaic/Mars/THEMIS_controlled_mosaics/Hellas_DayIR_31July2014/THEMIS_DayIR_ControlledMosaic_Hellas_65S060E_100mpp.tif', \
]

n = opt.n

for link in links[:n]:
    if not os.path.isfile('raw_images' + os.sep + link.split('/')[-1]):
        os.system('wget -P raw_images ' + link)