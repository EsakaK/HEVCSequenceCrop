## Dependency

```shell
ffmpeg -r 50 -i xx%5dxx.png -pix_fmt yuv444p -s 208x120 out.yuv 
```

# HEVCSequenceCompose

Compose png files into .yuv file.

# Usage

Change root path in the code and then open terminal in current directory. Use the command below:

```bash
python main.py
```

Before compose.

```shell
E:\DATASET\HEVC
├─ClassA
│  ├─PeopleOnStreet_2560x1600_30_crop
│  └─Traffic_2560x1600_30_crop
├─ClassB
│  ├─BasketballDrive_1920x1024_50
│  ├─BQTerrace_1920x1024_60
│  ├─Cactus_1920x1024_50
│  ├─Kimono1_1920x1024_24
│  └─ParkScene_1920x1024_24
├─ClassC
│  ├─BasketballDrill_832x448_50
│  ├─BQMall_832x448_60
│  ├─PartyScene_832x448_50
│  └─RaceHorses_832x448_30
├─ClassD
│  ├─BasketballPass_384x192_50
│  ├─BlowingBubbles_384x192_50
│  ├─BQSquare_384x192_60
│  └─RaceHorses_384x192_30
├─ClassE
│  ├─FourPeople_1280x704_60
│  ├─Johnny_1280x704_60
│  ├─KristenAndSara_1280x704_60
│  ├─vidyo1_1280x704_60
│  ├─vidyo3_1280x704_60
│  └─vidyo4_1280x704_60
└─ClassF
    ├─BasketballDrillText_832x448_50
    ├─ChinaSpeed_1024x768_30
    ├─SlideEditing_1280x704_30
    └─SlideShow_1280x704_20
```

After

```shell
E:\DATASET\HEVC_yuv
├─ClassA
│      PeopleOnStreet_2560x1600_30_crop.yuv
│      Traffic_2560x1600_30_crop.yuv
│
├─ClassB
│      BasketballDrive_1920x1080_50.yuv
│      BQTerrace_1920x1080_60.yuv
│      Cactus_1920x1080_50.yuv
│      Kimono1_1920x1080_24.yuv
│      ParkScene_1920x1080_24.yuv
│
├─ClassC
│      BasketballDrill_832x480_50.yuv
│      BQMall_832x480_60.yuv
│      PartyScene_832x480_50.yuv
│      RaceHorses_832x480_30.yuv
│
├─ClassD
│      BasketballPass_416x240_50.yuv
│      BlowingBubbles_416x240_50.yuv
│      BQSquare_416x240_60.yuv
│      RaceHorses_416x240_30.yuv
│
├─ClassE
│      FourPeople_1280x720_60.yuv
│      Johnny_1280x720_60.yuv
│      KristenAndSara_1280x720_60.yuv
│      vidyo1_1280x720_60.yuv
│      vidyo3_1280x720_60.yuv
│      vidyo4_1280x720_60.yuv
│
├─ClassF
│      BasketballDrillText_832x480_50.yuv
│      ChinaSpeed_1024x768_30.yuv
│      SlideEditing_1280x720_30.yuv
│      SlideShow_1280x720_20.yuv
```