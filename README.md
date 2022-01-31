# ha-files-sensor

Fork from https://github.com/TarheelGrad1998/files

To install, copy the files-folder to your homeassistant config (folder custom_components)

Define Sensor in sensor.yaml (Entities)

```yaml

- platform: files
  folder: /config/www/cam
  filter: '**/*.jpg'
  name: kamera_eingang
  sort: date
  recursive: True
  limit: 300

```

Sensor Data will look like this:

```
path: /config/www/cam/
filter: **/*.jpg
number_of_files: 3
bytes: 0
fileList: 
'2022-01-31':
  '07:00':
    eingang:
      '07:11:47': eingang/2022-01-31/image22-01-31_07-11-47-70.jpg
      '07:11:46': eingang/2022-01-31/image22-01-31_07-11-46-69.jpg
      '07:11:07': eingang/2022-01-31/image22-01-31_07-11-07-68.jpg
      '07:03:59': eingang/2022-01-31/image22-01-31_07-03-59-68.jpg
      '07:02:23': eingang/2022-01-31/image22-01-31_07-02-23-69.jpg
      '07:01:17': eingang/2022-01-31/image22-01-31_07-01-17-69.jpg
  '06:00':
    eingang:
      '06:59:21': eingang/2022-01-31/image22-01-31_06-59-21-70.jpg
      '06:58:05': eingang/2022-01-31/image22-01-31_06-58-05-68.jpg
  '05:00':
    eingang:
      '05:56:29': eingang/2022-01-31/image22-01-31_05-56-29-69.jpg
      '05:53:22': eingang/2022-01-31/image22-01-31_05-53-22-66.jpg
      '05:50:25': eingang/2022-01-31/image22-01-31_05-50-25-67.jpg
'2022-01-30':
  '20:00':
    eingang:
      '20:47:23': eingang/2022-01-30/image22-01-30_20-47-23-72.jpg
      '20:07:09': eingang/2022-01-30/image22-01-30_20-07-09-72.jpg
      '20:07:08': eingang/2022-01-30/image22-01-30_20-07-08-69.jpg
  '19:00':
    eingang:
      '19:21:24': eingang/2022-01-30/image22-01-30_19-21-24-68.jpg
      '19:21:23': eingang/2022-01-30/image22-01-30_19-21-23-67.jpg
'2022-01-29':
  '22:00':
    eingang:
      '22:01:08': eingang/2022-01-29/image22-01-29_22-01-08-68.jpg
      '22:00:22': eingang/2022-01-29/image22-01-29_22-00-22-76.jpg
      '22:00:15': eingang/2022-01-29/image22-01-29_22-00-15-64.jpg
      '22:00:14': eingang/2022-01-29/image22-01-29_22-00-14-68.jpg
  '21:00':
    eingang:
      '21:56:46': eingang/2022-01-29/image22-01-29_21-56-46-70.jpg

sort: date
recursive: true
limit: 300
unit_of_measurement: MB
icon: mdi:folder
friendly_name: kamera_eingang
}


