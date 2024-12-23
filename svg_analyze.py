import os
import re
import sys
import xml.etree.ElementTree as ET

ET.register_namespace('', "http://www.w3.org/2000/svg")

# Quick and dirty tool to bulk analyze SVG files in a directory

def get_element_tag_name(elem):
    name = elem.tag
    if "}" in name:
        name = name[name.find("}")+1:]
    return name


def attributes_to_string(attrib):
    s = ""
    for key in attrib:
        s = s + key + "=\"" + attrib[key] + "\" "
    return s.strip()


def element_start_tag_string(elem):
    name = get_element_tag_name(elem)
    return "<" + name + " " + attributes_to_string(elem.attrib) + ">"


def element_end_tag_string(elem):
    name = get_element_tag_name(elem)
    return "</" + name + ">"


def iterate_tree(tree, depth, callback=None):
    depth += 1
    for elem in tree:
        if callback:
            callback(elem)
        if elem.text and elem.text.strip():
            pass
        iterate_tree(elem, depth, callback)
    depth -= 1


def analyze_element(elem):
    name = get_element_tag_name(elem)
    if name not in tag_names:
        tag_names.append(name)
    for name in elem.attrib:
        if name not in attribute_names:
            attribute_names.append(name)
        if name == "transform":
            transforms.append(elem.attrib[name])
        if name == "d":
            path = elem.attrib[name]
            cmds = re.findall(r"[A-z]", path)
            for cmd in cmds:
                if cmd not in path_commands:
                    path_commands.append(cmd)

def analyze_file(path):
    global tag_names, attribute_names, transforms, path_commands
    tag_names = []
    attribute_names = []
    transforms = []
    path_commands = []

    try:
        tree = ET.parse(path)
        root = tree.getroot()

        analyze_element(root)
        iterate_tree(root, 0, analyze_element)

        return {
            "tags": tag_names,
            "attributes": attribute_names,
            "transforms": transforms,
            "path_commands": path_commands
        }
    except Exception as e:
        print(f"Error analyzing SVG file: {str(e)}")
        return None