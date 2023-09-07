#! python

from gimpfu import *
import gimp
import sys

label_parameters = [
    (PF_STRING, "label", "label", "1"),
    (PF_COLOR, "color", "Highlight color", (255,0,0))
]

class Python_Label_Log:
    def __init__(self) :
        self.fh = None
        log_path = gimp.directory+'/tmp/dot.log'
        try :
            self.fh = open(log_path,'w')
            success = True
        except :
            success = False
        if not success :
            try :
                self.fh = open('/tmp/dot.log','w')
            except :
                return
            fh.write('Attempt to open "%s" failed'%(log_path))
    def __deinit__(self) :
        if None != self.fh :
            self.fh.write('Closing via deinit()\n')
            self.fh.close()
            self.fh = None
    def write(self,content) :
        if None != self.fh :
            self.fh.write(content)
    def close(self) :
        if None != self.fh :
            self.fh.write('Closing via close()\n')
            self.fh.close()
            self.fh = None

def python_label(image, drawable, label, color):
    fh = Python_Label_Log()
    fh.write('python_label():Hello, World!\n')
    selection = pdb.gimp_selection_bounds(image)
    fh.write('selection bounds: %s\n'%(selection.__str__()))
    fh.write('label_parameters: %s\n'%(label_parameters.__str__()))
    fh.write('image: "%s", drawable: "%s", label: "%s, color: %s"\n'%(image.__str__(),drawable.__str__(),label, color.__str__()))
    active_layer = image.active_layer
    fg_orig = gimp.get_foreground()
    fh.write('fg_orig: "%s"\n'%(fg_orig.__str__()))
    pixels = 20
    font = pdb.gimp_context_get_font()
    fh.write('font: "%s"\n'%(font.__str__()))
    t_width,t_height,t_ascent,t_descent = pdb.gimp_text_get_extents_fontname(label,pixels,PIXELS,font)
    fh.write('t_width:%d, t_height:%d, t_ascent:%d, t_descent:%d\n'%(t_width,t_height,t_ascent,t_descent))
    gimp.set_foreground((1.0, 1.0, 1.0, 1.0))
    if 0 == selection[0] :
        label_x = 50
        label_y = 50
    else :
        label_x = selection[1]
        label_y = selection[2]
    floating = pdb.gimp_text_fontname(image,drawable,label_x,label_y,label,0,TRUE,pixels,PIXELS,font)
    fh.write('gimp_text_fontname returns "%s"\n'%(floating.__str__()))
    #fh.close() ; return
    text = pdb.gimp_floating_sel_to_layer(floating)
    fh.write('gimp_floating_sel_to_layer returns "%s"\n'%(text.__str__()))
    if None == text : text = floating
    pdb.gimp_item_set_name(text,"Text")
    offsets = [-1,0,1]
    copies = []
    for dx in offsets :
        for dy in offsets :
            if 0 == dx and 0 == dy : continue
            copies.append(pdb.gimp_layer_copy(text,TRUE))
            image.insert_layer(copies[-1])
            pdb.gimp_item_set_name(copies[-1],"Translated %d,%d"%(dx,dy))
            pdb.gimp_layer_translate(copies[-1],dx,dy)
    merged = copies.pop(-1)
    while len(copies) > 0 :
        copies.pop(-1)
        merged = pdb.gimp_image_merge_down(image,merged,0)
    white = pdb.gimp_image_merge_down(image,merged,0)
    pdb.gimp_item_set_name(white,"White")
    pdb.gimp_layer_resize(white,white.width+32,white.height+32,16,16)
    gimp.pdb.plug_in_gauss(image,white,3.5,3.5,0)
    gimp.set_foreground((0.0, 0.0, 0.0, 1.0))
    floating = pdb.gimp_text_fontname(image,white,label_x,label_y,label,0,TRUE,pixels,PIXELS,font)
    text = pdb.gimp_floating_sel_to_layer(floating)
    if None == text : text = floating
    pdb.gimp_item_set_name(text,"Text") 
    text = pdb.gimp_image_merge_down(image,text,0)
    pdb.gimp_item_set_name(text,"Text")
    # create dot layer
    dot = text
    pdb.gimp_item_set_name(dot,"Dot")
    text = pdb.gimp_layer_copy(text,TRUE)
    image.insert_layer(text)
    pdb.gimp_item_set_name(text,"Text")
    x = dot.offsets[0]
    y = dot.offsets[1]
    pdb.gimp_image_select_ellipse(image,2,x+8,y+8,dot.width-16,dot.height-16)
    # gimp.set_foreground((1.0, 0.0, 0.0, 1.0))
    gimp.set_foreground(color)
    pdb.gimp_drawable_edit_fill(dot,0)
    pdb.gimp_selection_all(image)
    pdb.plug_in_gauss(image,dot,10,10,0)

    # merge down text on to dot
    merged = pdb.gimp_image_merge_down(image,text,0)
    pdb.gimp_item_set_name(merged,"Dot(%s)"%(label))

    # restore original settings
    gimp.set_foreground(fg_orig)
    pdb.gimp_image_set_active_layer(image,active_layer)
    fh.close()
    return

register(
        "python_fu_highlighted_label",
        "Add highlighted label",
        "Add blurred dot",
        "Mark Orchard-Webb",
        "Mark Orchard-Webb",
        "2022",
        "<Image>/Filters/Label...",
        "",
        label_parameters,
        [],
        python_label)
main()
