#!/usr/bin/python2 -t
from gi.repository import Gtk
import os

w_path = os.getcwd()
envars = os.environ
user_home_dir = envars['HOME']
Ardis_colors = {}
Ardis_colors = {'Blackish':'#111111', 'Blue':'#0078ad', 'Dark Green':'#66ae4a', 'Light Green':'#79c843', 'Olive Green':'#669966', 'Orange':'#f38725', 'Peach':'#ef6a47', 'Pink':'#e65177', 'Red':'#cd1d31', 'Shadow Grey':'#666666', 'Sky Blue':'#6788cc', 'Soft Red':'#b93d48', 'Violet':'#924565', 'Yellow':'#ffcc67'}

def Hide_Page(p_num_to_hide):
    winbox = builder.get_object("box2")
    vp_to_hide = p_num_to_hide+1
    vp_str_to_hide = str(vp_to_hide)
    old_vp = builder.get_object('viewport'+vp_str_to_hide)
    winbox.remove(old_vp)
    
def Show_page(p_num_to_show):
    winbox = builder.get_object("box2")
    vp_to_show = p_num_to_show+1
    vp_str_to_show = str(vp_to_show)
    new_vp = builder.get_object('viewport'+vp_str_to_show)
    try:
        winbox.add(new_vp)
        setPosInCont('curr_page_dot', 'box1', p_num_to_show)
    except TypeError:
        #This captures any attempt to advance to a page that doesnt exist
        radio_choice_page1 = getPosInCont('event_box_curr_radio1', 'box7')
        label_choice_page1 = getNthChildLabel('box5', radio_choice_page1)
        
        radio_choice_page2 = getPosInCont('event_box_curr_radio2', 'box11')
        label_choice_page2 = getNthChildLabel('box12', radio_choice_page2)
        
        radio_choice_page4 = getPosInCont('event_box_curr_radio4', 'box16')
        label_choice_page4 = getNthChildLabel('box17', radio_choice_page4)
        
        radio_choice_page5 = getPosInCont('event_box_curr_radio5', 'box21')
        label_choice_page5 = getNthChildLabel('box22', radio_choice_page5)
        
        if label_choice_page5 == 'KDE':
            user_icon_dir = str(user_home_dir+'/.kde/share/icons/')
        elif label_choice_page5 is not None:
            user_icon_dir = str(user_home_dir+'/.icons/')
        else:
            user_icon_dir = None
            
        print 'Action style='+'"'+label_choice_page1+'"'
        print 'Places color='+Ardis_colors[label_choice_page2], '"'+label_choice_page2+'"'
        print 'Start here='+label_choice_page4
        print 'DesktopEnvironment='+label_choice_page5
        print 'Install Location='+user_icon_dir
        

        Gtk.main_quit()
        exit()
        
    #setPageDot(p_num_to_show)
    setPosInCont('curr_page_dot', 'box1', p_num_to_show)
    if p_num_to_show == 0:
        backbutton.hide()
    else:
        backbutton.show()


class Handler:

    def on_window1_delete_event(self, arg1, arg2):
        #Captures exit request made by a window manager
        #Disabling this means closing the window leaves a ZOMBIE!!!
        gtkicons = Gtk.IconTheme()
        gtksettings = Gtk.Settings()
        context_list = gtkicons.list_contexts()
        curicontheme = gtkicons.get_default()
        print context_list
        print '.'*50
        print gtkicons.get_search_path()
        print '.'*50
        print curicontheme.get_search_path()
        print '.'*50
        print gtksettings.props.gtk_icon_theme_name
        print '.'*50
        print gtksettings.props.gtk_icon_sizes
        Gtk.main_quit()
        exit()

    def on_Next_clicked(self, button):
        #exitbutton.show()
        cur_page = getPosInCont('curr_page_dot', 'box1')
        nex_page = cur_page+1
        Hide_Page(cur_page)
        Show_page(nex_page)
        #if the next page doesnt exist, the app exits now
        setPosInCont('curr_page_dot', 'box1', nex_page)
        #setPageDot(nex_page)
      
    def on_Back_clicked(self, button):
        exitbutton.hide()
        cur_page = getPosInCont('curr_page_dot', 'box1')
        prev_page = cur_page-1
        Hide_Page(cur_page)
        Show_page(prev_page)
        setPosInCont('curr_page_dot', 'box1', prev_page)


    def on_Exit_clicked(self, button):
        exit()
        
    def on_eventbox_radio_press(self, radio, button2):
        cur_page = getPosInCont('curr_page_dot', 'box1')
        active_radio_box = builder.get_object('event_box_curr_radio'+str(cur_page))
        rad_parent = radio.get_parent()
        rad_list = rad_parent.get_children()
        for i, v in enumerate(rad_list):
            if v == radio:
                rad_parent.reorder_child(active_radio_box, i)

        
def setPageDot(n):
    pageDot = builder.get_object("curr_page_dot")
    mainbox = builder.get_object("box1")
    mainbox.reorder_child(pageDot, n)
    
    
def setPosInCont(targ_obj, targ_con, targ_pos):
    target_object = builder.get_object(targ_obj)
    taget_container = builder.get_object(targ_con)
    taget_container.reorder_child(target_object, targ_pos)
    
    
def getPosInCont(targ_obj, targ_con):
    target_object = builder.get_object(targ_obj)
    taget_container = builder.get_object(targ_con)
    objects_list = taget_container.get_children()
    for i, v in enumerate(objects_list):
        if v == target_object:
            return int(i)
    
def getNthChildLabel(targ_con, child_n):
    taget_container = builder.get_object(targ_con)
    objects_list = taget_container.get_children()
    target_label = objects_list[child_n]
    return target_label.get_text()

builder = Gtk.Builder()
builder.add_from_file(w_path+'/Ardis setup unified.glade')
builder.connect_signals(Handler())

window = builder.get_object("window1")
pageDot = builder.get_object("curr_page_dot")
mainbox = builder.get_object("box1")
backbutton = builder.get_object("button2")
exitbutton = builder.get_object("button3")
pageone = builder.get_object("viewport1")
current_page = 0
window.show_all()
backbutton.hide()
exitbutton.hide()
#pageone.show()



Gtk.main()
exit()
