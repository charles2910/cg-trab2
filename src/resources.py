#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 17/12/2022
# ---------------------------------------------------------------------------

from os import listdir, getcwd
from os.path import isfile, join

RESOURCES_PATH = join(getcwd(), 'resources')

def list_resources():
    path = RESOURCES_PATH
    return [f for f in listdir(path) if not isfile(join(path, f))]

def list_textures(resource):
    path = create_texture_path(resource, '')
    return [create_texture_path(resource, f) for f in listdir(path) if isfile(join(path, f))]

def create_texture_path(resource, texture):
    return join(RESOURCES_PATH, resource, 'textures', texture)

def create_obj_path(resource):
    return join(RESOURCES_PATH, resource, 'figure.obj')

def build_resources():
    metadata = {}

    for resource in list_resources():
        metadata[resource] = {
            'obj': create_obj_path(resource),
            'textures': list_textures(resource)
        }

    return metadata

