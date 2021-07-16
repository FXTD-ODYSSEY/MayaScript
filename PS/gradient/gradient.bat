@REM generate linear gradient base on two texture  

set imconvert="%~dp0imconvert.exe"
set input_1="%temp%\input_1.png"
set input_2="%temp%\input_2.png"

@REM convert png to black and white

%imconvert% ^
    %input_2% ^
    -gamma 0 -background "#FFFFFF" -flatten ^
    %input_2% 
%imconvert% ^
    %input_1% ^
    -gamma 0 -background "#FFFFFF" -flatten ^
    %input_1% 

@REM then using morphology generate two distant gradient texture

%imconvert% ^
    %input_2% ^
    -negate ^
    -morphology Distance Euclidean:4,100^! ^
    -negate ^
    "%temp%\gradient_1.png"

%imconvert% ^
    %input_1% ^
    -morphology Distance Euclidean:4,100^! ^
    "%temp%\gradient_2.png"

@REM generate linear gradient texture

%imconvert% ^
  "%temp%\gradient_1.png" ^
  "%temp%\gradient_2.png" ^
  ( -clone 1 -evaluate Divide 2 ) ^
  ( -clone 0-1 ^
    -compose Mathematics ^
      -define compose:args=0,0.5,-0.5,0.5 ^
      -composite ^
  ) ^
  -delete 0-1 ^
  -compose DivideSrc -composite ^
  "%temp%\output.png"

@REM genertate mask

%imconvert% ^
    "%input_1%" ^
    "%input_2%" ^
    -compose Change-mask -composite  ^
    -background black -alpha background -alpha off ^
    "%temp%\mask.png"

@REM mask the gradient texture

%imconvert% ^
  "%temp%\output.png" ^
  "%temp%\mask.png" ^
  -alpha Off -compose CopyOpacity -composite ^
  "%temp%\output.png"

