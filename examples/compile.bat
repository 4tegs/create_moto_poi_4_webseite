@echo off
@REM ##########################################################################################
@REM compile the create_moto_poi_4_webseite
@REM Hans Straßgütl
@REM 
@REM ..........................................................................................
@REM Changes:
@REM                    
cls
@REM pause
copy /Y C:\SynologyDrive\Python\00_import_h_utils\h_utils.py C:\SynologyDrive\Python\create_moto_poi_4_webseite\
pyinstaller --onefile --icon gravelmaps.ico create_moto_poi_4_webseite.py

copy /Y C:\SynologyDrive\Python\create_moto_poi_4_webseite\dist\create_moto_poi_4_webseite.exe                  C:\SynologyDrive\Python\create_moto_poi_4_webseite\

copy /Y C:\SynologyDrive\Python\create_moto_poi_4_webseite\create_moto_poi_4_webseite.py                        C:\SynologyDrive\Python\xx_PY_on_Github\create_moto_poi_4_webseite
copy /Y C:\SynologyDrive\Python\create_moto_poi_4_webseite\gravelmaps.ico                                       C:\SynologyDrive\Python\xx_PY_on_Github\create_moto_poi_4_webseite\examples
copy /Y C:\SynologyDrive\Python\create_moto_poi_4_webseite\h_utils.py                                           C:\SynologyDrive\Python\xx_PY_on_Github\create_moto_poi_4_webseite
copy /Y C:\SynologyDrive\Python\create_moto_poi_4_webseite\compile.bat                                          C:\SynologyDrive\Python\xx_PY_on_Github\create_moto_poi_4_webseite\examples
copy /Y C:\SynologyDrive\Python\create_moto_poi_4_webseite\BMP\*.bmp                                            C:\SynologyDrive\Python\xx_PY_on_Github\create_moto_poi_4_webseite\BMP
del create_moto_poi_4_webseite.spec
del h_utils.py
rmdir C:\SynologyDrive\Python\create_moto_poi_4_webseite\build /S /Q
rmdir C:\SynologyDrive\Python\create_moto_poi_4_webseite\dist /S /Q
rmdir C:\SynologyDrive\Python\create_moto_poi_4_webseite\__pycache__ /S /Q