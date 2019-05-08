# -*- coding: utf-8 -*-

# This file is part of Argos.
#
# Argos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Argos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Argos. If not, see <http://www.gnu.org/licenses/>.

""" Version and other info for this program
"""
import os

DEBUGGING = False

VERSION = '0.2.1.dev1'
REPO_NAME = "argosge"
#SCRIPT_NAME = "argos"
PACKAGE_NAME = "argos"
PROJECT_NAME = "Argos (Gaia Extension)"
DEFAULT_PROFILE = 'Panoptes'
SHORT_DESCRIPTION = "Argos Panoptes HDF/NCDF/scientific data viewer with extensions for Gaia."
PROJECT_URL = "https://github.com/soriaser/argos"
AUTHOR = "Sergio Soria"
EMAIL = "sergio.soria.nieto@gmail.com"
ORGANIZATION_NAME = "soriaser"
ORGANIZATION_DOMAIN = "soriaser.nl"


def program_directory():
    """ Returns the program directory where this program is installed
    """
    return os.path.abspath(os.path.dirname(__file__))

def icons_directory():
    """ Returns the program directory where this program is installed
    """
    return os.path.join(program_directory(), 'img/snipicons')

