@REM TODO 识别颜色


"C:\Program Files\Autodesk\Maya2019\bin\imconvert.exe" ^
  gradient_filter.png ^
  -morphology Distance:40^! Euclidean:4 ^
  gradient3.png



@REM "C:\Program Files\Autodesk\Maya2019\bin\imconvert.exe" ^
@REM   is_src_border.png ^
@REM   -morphology Distance Euclidean:4,550^! ^
@REM   -negate ^
@REM   is_bord_dist2.png

@REM call fanComp.bat ^
@REM   is_bord_dist2.png ^
@REM   is_isl_dist2.png ^
@REM   is_grad2.png