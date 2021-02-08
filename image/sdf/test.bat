@REM "C:\Program Files\Autodesk\Maya2019\bin\imconvert.exe" ^
@REM   is_src_island.png ^
@REM   -morphology Distance Euclidean:4,100^! ^
@REM   is_isl_dist2.png

@REM "C:\Program Files\Autodesk\Maya2019\bin\imconvert.exe" ^
@REM   is_src_border.png ^
@REM   -morphology Distance Euclidean:4,100^! ^
@REM   -negate ^
@REM   is_bord_dist2.png


@REM call fanComp.bat ^
@REM   is_bord_dist2.png ^
@REM   is_isl_dist2.png ^
@REM   is_grad2.png

@REM "C:\Program Files\Autodesk\Maya2019\bin\imconvert.exe" is_grad1.png^
@REM   ( -size 1x500 gradient: -rotate 90 -duplicate 1 +append ) ^
@REM   -clut ^
@REM   is_grad2.png

@REM "C:\Program Files\Autodesk\Maya2019\bin\imconvert.exe" is_grad1.png^
@REM   ( -size 1x100 gradient: -rotate -90 -duplicate 1 +append ) ^
@REM   -clut ^
@REM   is_grad3.png

@REM "C:\Program Files\Autodesk\Maya2019\bin\imconvert.exe" ^
@REM   is_grad1.png ^
@REM   ( -size 1x500 gradient: -rotate 90 -duplicate 10 +append ) ^
@REM   -clut ^
@REM   -morphology edgein diamond:1 ^
@REM   is_grad2.png
