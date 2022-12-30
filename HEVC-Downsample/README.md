# HEVCSequenceDowsample

Downsample General HEVC Sequence at 2x.

# Requirements

Need torch to parallelizing processing. If not, use a cpu-version. Downsampling will use matlab's method to adapt most Deep Learning standard.

# Usage

Change root path in the code and then open terminal in current directory. Use the command below:

```bash
python main.py
```

Before down sample png images, you have to use tool in HEVC-Crop to generate sequence png with `crop_flag=false`.
The file tree of the original HEVC Sequence png should be like follows:

```angular2html
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

After downsampeling, every sub ClassX dir will generating several subdirectories corresponding to directory name in which all frames are downsampled to size of 0.5x(
default).
You can change downsample scale directly in code for convenience.

```angular2html
E:\DATASET\HEVC_ds
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
