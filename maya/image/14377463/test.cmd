@REM 过滤出主要的 8 个颜色输出颜色数据 
@REM https://www.imagemagick.org/discourse-server/viewtopic.php?t=22261
@REM https://www.imagemagick.org/discourse-server/viewtopic.php?t=27953
@REM "C:\Program Files\Autodesk\Maya2019\bin\imconvert.exe" input.png -colors 8 -unique-colors txt:


@REM "G:\ImageMagick\magick.exe" input.png  -alpha off ^
@REM           -fill blue -colorize 100% ^
@REM           -alpha on  colorize_shape.png                        

@REM "G:\ImageMagick\magick.exe" input.png                                    ^
@REM  -negate -threshold 10%      -auto-level     ^
@REM  output.png


"G:\ImageMagick\magick.exe" "F:\MayaTecent\MayaScript\image\14377463\objects.gif" -connected-components 4 -auto-level -depth 8 objects.png