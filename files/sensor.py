import glob
import logging
import os
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

CONF_FOLDER_PATHS = "folder"
CONF_FILTER = "filter"
CONF_NAME = "name"
CONF_SORT = "sort"
CONF_LIMIT = "limit"
CONF_RECURSIVE = "recursive"
DEFAULT_FILTER = "*"
DEFAULT_SORT = "date"
DEFAULT_LIMIT = 100
DEFAULT_RECURSIVE = False

DOMAIN = "files"

SCAN_INTERVAL = timedelta(minutes=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_FOLDER_PATHS): cv.isdir,
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_FILTER, default=DEFAULT_FILTER): cv.string,
        vol.Optional(CONF_SORT, default=DEFAULT_SORT): cv.string,
        vol.Optional(CONF_RECURSIVE, default=DEFAULT_RECURSIVE): cv.boolean,
        vol.Optional(CONF_LIMIT, default=DEFAULT_LIMIT): cv.positive_int,
    }
)


def get_files_list(folder_path, filter_term, sort, recursive, limit):
    """Return the list of files, applying filter."""
    query = folder_path + filter_term
    """files_list = glob.glob(query)"""
    if sort == "name":
        files_list = sorted(glob.glob(query, recursive=recursive))
    elif sort == "size":
        files_list = sorted(glob.glob(query, recursive=recursive), key=os.path.getsize)
    else:
        files_list = sorted(glob.glob(query, recursive=recursive), key=os.path.getmtime, reverse=True)

# fileList: /config/www/cam/eingang/2022-01-27/image22-01-27_18-53-42-62.jpg, /config/www/cam/eingang/2022-01-27/image22-01-27_18-50-11-70.jpg, /config/www/cam/eingang/2022-01-27/image22-01-27_18-46-32-75.jpg, /config/www/cam/eingang/2022-01-27/image22-01-27_18-45-40-67.jpg
#   folder: /config/www/cam

    imageDicts = {}
    # Files nun in die Struktur bringen
    for pic in files_list[0:limit]:
        try:
            # folder aus url entfernen, dann startet die url mit der camera
            picUrl = pic[len(folder_path):]
            # cam rausschälen
            parts = picUrl.split('/')
            camera = parts[0]
            # tag ermitteln
            day = parts[1]
            # datum ermitteln
            time = parts[2].split('_')[1][0:8].replace("-",":")
            hour = time[0:2] + ':00'
            # bild an die richtige reihe im objekt hinzufügen

            # imageDicts[day][camera][time] = picUrl

            if day in imageDicts.keys():
                if hour in imageDicts[day].keys():
                    if camera in imageDicts[day][hour].keys():
                        imageDicts[day][hour][camera][time] = picUrl
                    else:
                        imageDicts[day][hour][camera] = { time : picUrl}
                else:
                    imageDicts[day][hour] = { camera : { time: picUrl} }
            else:
                imageDicts[day] = { hour: { camera: { time: picUrl} } }
        except:
            _LOGGER.warning("Fehler in files-componente beim Auslesen des Files Pic: %s picUrl: %s ",
                            pic, picUrl)
    
    return imageDicts


def get_size(files_list):
    """Return the sum of the size in bytes of files in the list."""
    size_list = [os.stat(f).st_size for f in files_list if os.path.isfile(f)]
    return sum(size_list)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the folder sensor."""
    path = config.get(CONF_FOLDER_PATHS)
    name = config.get(CONF_NAME)

    if not hass.config.is_allowed_path(path):
        _LOGGER.error("folder %s is not valid or allowed", path)
    else:
        folder = FilesSensor(
            path,
            name,
            config.get(CONF_FILTER),
            config.get(CONF_SORT),
            config.get(CONF_RECURSIVE),
            config.get(CONF_LIMIT),
        )
        add_entities([folder], True)

class PictureGallery:
    def __init__(self, _tage):
        """Initialize the data object."""
        self.tage = _tage  


class Tag:
    def __init__(self, _date, _cams):
        self.date = _date
        self.cams = _cams


class Cam:
    def __init__(self, _name, _pictures) -> None:
        self.name = _name
        self.pictures = _pictures

class Picture:
    def __init__(self, _url, _timestamp) -> None:
        self.url = _url
        self.timestamp = _timestamp
    


class FilesSensor(Entity):
    """Representation of a folder."""

    ICON = "mdi:folder"

    def __init__(self, folder_path, name, filter_term, sort, recursive, limit):
        """Initialize the data object."""
        folder_path = os.path.join(folder_path, "")  # If no trailing / add it
        self._folder_path = folder_path  # Need to check its a valid path
        self._filter_term = filter_term
        self._number_of_files = None
        self._size = None
        # self._name = os.path.split(os.path.split(folder_path)[0])[1]
        self._name = name
        self._unit_of_measurement = "MB"
        self._sort = sort
        self._recursive = recursive
        self._limit = limit

    def update(self):
        """Update the sensor."""
        files_list = get_files_list(
            self._folder_path, self._filter_term, self._sort, self._recursive, self._limit
        )
        self.fileList = files_list
        self._number_of_files = len(files_list)
        self._size = get_size(files_list)
        

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        decimals = 2
        size_mb = round(self._size / 1e6, decimals)
        return size_mb

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self.ICON

    @property
    def extra_state_attributes(self):
        """Return other details about the sensor state."""
        attr = {
            "path": self._folder_path,
            "filter": self._filter_term,
            "number_of_files": self._number_of_files,
            "bytes": self._size,
            "fileList": self.fileList,
            "sort": self._sort,
            "recursive": self._recursive,
            "limit": self._limit,
        }
        return attr

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement
