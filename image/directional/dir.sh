# @REM https://www.imagemagick.org/Usage/convolve/#directional

# @REM "C:\Program Files\Autodesk\Maya2017\bin\imconvert.exe"  "F:\MayaTecent\MayaScript\image\directional\face.png" -define convolve:scale="50%!" -bias 50% -morphology Convolve Sobel:90 "F:\MayaTecent\MayaScript\image\directional\face_sobel.png" 

# @REM "C:\Program Files\Autodesk\Maya2017\bin\imconvert.exe" -size 10x120  gradient:snow-navy          gradient_ice-sea.jpg

# @REM "C:\Program Files\Autodesk\Maya2017\bin\imconvert.exe" face.png   -define convolve:scale="!"            -define morphology:compose=Lighten            -morphology Convolve  "Sobel:>"   face_sobel_maximum_2.png


# @REM "C:\Program Files\Autodesk\Maya2017\bin\imconvert.exe" face.png   -define convolve:scale='!'            ( -clone 0 -morphology Convolve Sobel:0 )            ( -clone 0 -morphology Convolve Sobel:90 )            ( -clone 0 -morphology Convolve Sobel:180 )            ( -clone 0 -morphology Convolve Sobel:270 )            -delete 0 -background Black -compose Lighten -flatten            face_sobel_maximum.png

# @REM "C:\Program Files\Autodesk\Maya2017\bin\imconvert.exe" -size 30x600 xc:"#0F0" -colorspace HSB           gradient: -compose CopyRed -composite           -colorspace RGB -rotate 90  rainbow.jpg

# @REM "C:\Program Files\Autodesk\Maya2017\bin\imconvert.exe" shapes.gif -define convolve:scale='50%!' -bias 50%       ( -clone 0 -morphology Convolve Sobel:0 )       ( -clone 0 -morphology Convolve Sobel:90 )       -delete 0       ( -clone 0,1 -fx "0.5+atan2(v-0.5,0.5-u)/pi/2" rainbow.jpg -clut )       ( -clone 0,1 -fx "u>0.48&&u<0.52&&v>0.48&&v<0.52 ? 0.0 : 1.0" )       -delete 0,1 -alpha off -compose CopyOpacity -composite       face_sobel_direction.png

# @REM "C:\Program Files\Autodesk\Maya2017\bin\imconvert.exe" shapes.gif -fx "0.5+atan2(v-0.5,0.5-u)/pi/2" rainbow.jpg -clut rainbow2.png



"C:\Program Files\Autodesk\Maya2017\bin\imconvert.exe" -size 30x360 xc:'#0F0' -colorspace HSB \
          gradient: -compose CopyRed -composite \
          -colorspace RGB -rotate 90  rainbow.jpg

"C:\Program Files\Autodesk\Maya2019\bin\imconvert.exe" dilation.jpg -define convolve:scale='50%!' -bias 50% \
    \( -clone 0 -morphology Convolve Sobel:0 \) \
    \( -clone 0 -morphology Convolve Sobel:90 \) \
    -delete 0 \
    \( -clone 0,1 -fx '0.5+atan2(v-0.5,0.5-u)/pi/2' rainbow.jpg -clut \) \
    \( -clone 0,1 -fx 'u>0.48&&u<0.52&&v>0.48&&v<0.52 ? 0.0 : 1.0' \) \
    -delete 0,1 -alpha off -compose CopyOpacity -composite \
    dilation3.png

