import re
import xml.etree.ElementTree as ET
from svg.path.parser import _tokenize_path


__author__ = "Richard Lewis"
__editsby__ = "EPIXJAVA"
__copyright__ = "Copyright 2024, Richard Lewis,"
__license__ = "MIT"
__status__ = "Development"
__version__ = "0.1.5"


description = """
Normalize SVG files so that the OP-1 understands them.
"""

"""
NOTES

- Group transformations are not supported. Only transformations for individual elements.
- Only the following transforms are supported: matrix, translate, scale (TODO: verify this)

DONE:
- Remove unsupported tags and attributes
- Remove comments
- Convert styles to attributes, and drop unsupported styles
- Fix decimals. A maximum of 4 decimals is supported by the OP-1
- Reformat the path data in paths. Use svg.path to stringify them into a uniform format
- Check what color notations are supported. The original graphics files only use hex notation.
- Normalized color HEX values. Apply Uppercase to values as well as correct white 'fff' to 'FFFFFF'

TODO:
- Fix group transforms (they are unsnupported by the OP-1)


"""

# Supported tags
TAGS = ["svg", "rect", "g", "line", "path", "polyline", "circle", "polygon", "ellipse", "defs", "clipPath", "use"]

# Supported attributes
ATTR_ALL = [
    "xmlns", "xmlns:xlink",
    "version", "id", "x", "y", "width", "height", "viewBox",
    "enable-background", "space", "fill", "stroke", "d", "stroke-width",
    "cx", "cy", "r", "x1", "y1", "x2", "y2", "stroke-dasharray", "display",
    "stroke-linecap", "points", "rx", "ry", "stroke-linejoin", "transform",
    "stroke-miterlimit", "href", "overflow", "clip-path", "opacity",
]

# Numeric attributes 
ATTR_NUMERIC = [
    "x", "y", "width", "height", "stroke-width", "cx", "cy", "r", "x1", "y1",
    "x2", "y2", "rx", "ry", "opacity" , "points"
]


DECIMAL_PRECISION = 4


def is_self_closing(elem):
    return ET.tostring(elem).strip().endswith(b"/>")


def is_supported_tag(elem):
    return get_element_tag_name(elem) in TAGS


def is_supported_attr(name):
    return name in ATTR_ALL


def normalize_name(name):
    if "}" in name:
        name = name[name.find("}")+1:]
    return name


def token_is_command(token):
    return token.isalpha()


def normalize_tokens(tokens):
    """
    The OP-1 gets confused with multiple line segments in one command.
    This fixes that by splitting multiple segments into separate commands.

    Convert from e.g.:
    ["l", "20", "20", "20", "-20", "10", "10"]
    To:
    ["l", "20", "20", "l", "20", "-20", "l", "10", "10"]

    This could be done better but this works fine.
    """
    result = []
    curr_command = ""
    curr_command_token = 0
    for token in tokens:
        if token_is_command(token):
            curr_command = token
            curr_command_token = 0
        else:
            if curr_command in ["L", "l"]:
                if curr_command_token == 2:
                    curr_command_token = 0
                    result.append(curr_command)
            curr_command_token += 1
        result.append(token)

    return result


def _tokenize_path(pathdef):
    tokens = re.findall(r"[A-Za-z]|-?\d*\.?\d+(?:e[-+]?\d+)?", pathdef)
    return tokens


def fix_svg_path(data, value_formatter=lambda v: v):
    tokens =list(_tokenize_path(data))
    tokens = normalize_tokens(tokens)
    result = ""
    previous_was_command = False
    for token in tokens:
        if token_is_command(token):
            # Remove the preceding comma
            result = result[:-1]
            result += token
        else:
            # If the previous token was a numeric value, and
            # the current value starts with a `-` then the
            # comma preceding the value can be omitted.
            if token[0] == "-" and not previous_was_command:
                result = result[:-1]
            result += value_formatter(token) + ","
        previous_was_command = token_is_command(token)

    return result.strip(" ,")


def limit_decimals(n):
    if "." not in n:
        return n
    end = ""
    if n.endswith("px"):
        end = "px"
        n = n[:-2]

    s = str(round(float(n), DECIMAL_PRECISION))
    return s + end


def get_element_tag_name(elem):
    return normalize_name(elem.tag)


def parse_styles(styles_str):
    # Inkscape (and others) store SVG properties in the style attribute instead of
    # using a real attribute for each value. OP-1 doesn't like that. This converts
    # the styles to real attributes.
    if not styles_str:
        return {}

    if ";" in styles_str:
        items = styles_str.split(";")
    else:
        items = [styles_str]

    styles = {}
    for item in items:
        parts = item.split(":")
        styles[parts[0]] = parts[1]

    return styles


def attributes_to_string(attrs):
    s = ""
    if "style" in attrs:
        styles = parse_styles(attrs["style"])
        del attrs["style"]
        attrs.update(styles)

    for key in attrs:
        if not is_supported_attr(key):
            continue
        value = attrs[key]
        # Limit decimals
        if key in ATTR_NUMERIC:
            value = limit_decimals(value)
        # Normalize svg paths
        if key == "d":
            value = fix_svg_path(value, value_formatter=limit_decimals)
        # Normalize color HEX values
        if key == "stroke" or key == "fill":
            if value.startswith('#') or value.lower() == 'fff':
                value = normalize_color_hex(value)
        s = s + " " + normalize_name(key) + "=\"" + value + "\""
    return s


def element_start_tag_string(elem):
    name = get_element_tag_name(elem)
    attrs = attributes_to_string(elem.attrib)
    return "<" + name + attrs + ("/>" if is_self_closing(elem) else ">")


def element_end_tag_string(elem):
    if is_self_closing(elem):
        return ""
    name = get_element_tag_name(elem)
    return "</" + name + ">"


def iterate_tree(tree, indent, depth=None, callback=None):
    output = ""
    if depth is None:
        depth = 0

    depth += 1

    for elem in tree:
        if not is_supported_tag(elem):
            continue
        if callback:
            callback(elem)
        # Set indent level
        indentation = "\t" * depth if indent else ""

        # Add start tag to output
        output += indentation + element_start_tag_string(elem) + "\n"

        # Add text contents if element has any
        if elem.text and elem.text.strip():
            output += elem.text

        # Add children
        output += iterate_tree(elem, indent, depth, callback)

        # Add end tag if necessary
        end_tag = element_end_tag_string(elem)
        if end_tag:
            output += indentation + end_tag + "\n"

    depth -= 1

    return output


def clean_svg_tree(tree):
    root = tree.getroot()

    root.attrib["xmlns"] = "http://www.w3.org/2000/svg"
    root.attrib["xmlns:xlink"] = "http://www.w3.org/1999/xlink"

    output = '<?xml version="1.0" encoding="utf-8"?>\n'
    output += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
    output += element_start_tag_string(root) + "\n"
    output += iterate_tree(root, indent=False) + "\n"
    output += element_end_tag_string(root)

    return output


def normalize_color_hex(color):
    """
    Normalize color HEX values:
    - Ensure HEX codes are in uppercase
    - Convert 'fff' to 'FFFFFF'
    """
    if color.startswith('#'):
        color = color[1:]
    
    if color.lower() == 'fff':
        return '#FFFFFF'
    
    return '#' + color.upper()


def normalize_svg(in_path, out_path):
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree = ET.parse(in_path)

    output = clean_svg_tree(tree)

    with open(out_path, "w") as f:
        f.write(output)

    return True