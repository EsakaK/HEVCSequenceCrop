# HEVCSequenceCrop
Crop General HEVC Sequence to adapt Neural Network Input.

# Usage
change root path in the code.

the file tree should be like follows:
```angular2html
E:\DATASET\HEVC_RAW
├─ClassA
│      PeopleOnStreet_2560x1600_30_crop.yuv
│      Traffic_2560x1600_30_crop.yuv
│
├─ClassB
│      BasketballDrive_1920x1024_50.yuv
│      BasketballDrive_1920x1080_50.yuv
│      BQTerrace_1920x1024_60.yuv
│      BQTerrace_1920x1080_60.yuv
│      Cactus_1920x1024_50.yuv
│      Cactus_1920x1080_50.yuv
│      Kimono1_1920x1024_24.yuv
│      Kimono1_1920x1080_24.yuv
│      ParkScene_1920x1024_24.yuv
│      ParkScene_1920x1080_24.yuv
│
├─ClassC
│      BasketballDrill_832x448_50.yuv
│      BasketballDrill_832x480_50.yuv
│      BQMall_832x448_60.yuv
│      BQMall_832x480_60.yuv
│      PartyScene_832x448_50.yuv
│      PartyScene_832x480_50.yuv
│      RaceHorses_832x448_30.yuv
│      RaceHorses_832x480_30.yuv
│
├─ClassD
│      BasketballPass_384x192_50.yuv
│      BasketballPass_416x240_50.yuv
│      BlowingBubbles_384x192_50.yuv
│      BlowingBubbles_416x240_50.yuv
│      BQSquare_384x192_60.yuv
│      BQSquare_416x240_60.yuv
│      RaceHorses_384x192_30.yuv
│      RaceHorses_416x240_30.yuv
│
├─ClassE
│      FourPeople_1280x704_60.yuv
│      FourPeople_1280x720_60.yuv
│      Johnny_1280x704_60.yuv
│      Johnny_1280x720_60.yuv
│      KristenAndSara_1280x704_60.yuv
│      KristenAndSara_1280x720_60.yuv
│      vidyo1_1280x704_60.yuv
│      vidyo1_1280x720_60.yuv
│      vidyo3_1280x704_60.yuv
│      vidyo3_1280x720_60.yuv
│      vidyo4_1280x704_60.yuv
│      vidyo4_1280x720_60.yuv
│
├─ClassF
│      BasketballDrillText_832x448_50.yuv
│      BasketballDrillText_832x480_50.yuv
│      ChinaSpeed_1024x768_30.yuv
│      SlideEditing_1280x704_30.yuv
│      SlideEditing_1280x720_30.yuv
│      SlideShow_1280x704_20.yuv
│      SlideShow_1280x720_20.yuv
```