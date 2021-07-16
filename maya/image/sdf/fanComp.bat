@rem A compose like a fan.
@rem
@rem result = src / (src-dest+1)

@if "%3"=="" findstr /B "rem @rem" %~f0 & exit /B 1

"C:\Program Files\Autodesk\Maya2019\bin\imconvert.exe" ^
  %1 ^
  %2 ^
  ( -clone 1 -evaluate Divide 2 ) ^
  ( -clone 0-1 ^
    -compose Mathematics ^
      -define compose:args=0,0.5,-0.5,0.5 ^
      -composite ^
  ) ^
  -delete 0-1 ^
  -compose DivideSrc -composite ^
  %3