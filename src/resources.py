from os import listdir, getcwd
from os.path import isfile, join, dirname

RESOURCES_PATH = join(getcwd(), 'resources')

def list_resources():
    path = RESOURCES_PATH
    return [f for f in listdir(path) if not isfile(join(path, f))]

def create_texture_path(resource, texture):
    path = join(RESOURCES_PATH, resource, 'textures', texture)
    return path

def list_textures(resource):
    path = create_texture_path(resource, '')
    return [create_texture_path(resource, f) for f in listdir(path) if isfile(join(path, f))]

def create_obj_path(resource):
    return join(RESOURCES_PATH, resource, 'figure.obj')

def build_resources():
    metadata = dict()
    resources = list_resources()
    for resource in resources:
        metadata[resource] = {
            'obj': create_obj_path(resource),
            'textures': list_textures(resource)
        }

    return metadata

