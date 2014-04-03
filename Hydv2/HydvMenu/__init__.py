#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Olivier LARRIEU"
__version__ = "0.1"

import os
import locale

class HydvDesktopEntries(object):
    """
    Return a dictionnary with applications categories
    Is not based on XDG but stay soft and quick.
    """
    @classmethod
    def display_all(cls):
        tot_applications = 0
        apps = HydvDesktopEntries.get_applications()
        keys = apps.keys()
        for k in keys:
            tot_applications += len(apps[k])
            print "========================================================="
            print "Category :", k, str(len(apps[k]))
            for app in apps[k]:
                print "    -", app['name']
        print "========================================================="
        print "Total categories :", str(len(apps))
        print "Total applications :", str(tot_applications)

    @classmethod
    def get_applications(self):
        language = locale.getdefaultlocale()[0][0:2]
        CATEGORIES_DIC = {'AudioVideo': [],
                         'Network': ['X-GNOME-NetworkSettings',],
                         'Office':['Development',],
                         'Settings': [],
                         'System':['PackageManager','Security', 'Qt',],
                         'Application':['Emulator', 'Core', 'Utility',],
                         'Game': [],
                         'Graphics': [],
                         'Wine': ['Wine-Programs-Accessories',],
                         }
        dir_list = os.listdir('/usr/share/applications')
        dic = {}
        nodisplay = False
        command = False
        for desktop_file in dir_list:
            try:
                if desktop_file.split('.')[1] == "desktop":
                    applications_dic = {}
                    file_content = open('/usr/share/applications/'+desktop_file, 'r').readlines()
                    for line in file_content:
                        if "Name" in line and not "TypeName" in line and not "GenericName" in line :
                            if not 'name' in applications_dic:
                                applications_dic['name'] = line.split('=')[1].replace('\n','')
                        if "Exec" in line:
                            command = True
                            applications_dic['command'] = line.split('=')[1].replace('\n','').split('%')[0]
                        if "Icon" in line:
                            icon = HydvDesktopEntries.findicon(line.split('=')[1].replace('\n',''))
                            applications_dic['icon'] = icon
                        if "Comment[%s]"%language in line:
                            applications_dic['comment'] = line.split('=')[1].replace('\n','')
                        if "Categories" in line:
                            category = line.replace('GNOME;','').replace('GTK;','').replace('\n','').split('=')[1].split(';')[0]                     
                        if "NoDisplay=true" in line:
                            nodisplay = True
                    if command:
                        if not nodisplay:
                            applications_dic['desktopentry'] = desktop_file
                            for cat in CATEGORIES_DIC:
                                if category in CATEGORIES_DIC[cat]:
                                    category = cat
                            if not category in dic:
                                dic[category] = []                        
                            dic[category].append({applications_dic['name']:applications_dic, })
                        else:
                            nodisplay = False
                    command = False
            except:
                pass
        return dic

    @classmethod
    def findicon(cls, icon_name):
        realpath = os.path.dirname(__file__)
        base_category_icons = os.listdir(realpath + "/base/categories/")
        for elem in base_category_icons:
            if os.path.isfile(realpath + "/base/categories/"+elem):
                if elem.split('.')[0] == icon_name:
                    del base_category_icons
                    return realpath + "/base/categories/" +elem

        usr_share_icons = os.listdir('/usr/share/icons/')                
        for elem in usr_share_icons:
            if os.path.isdir("/usr/share/icons/"+elem):
                if os.path.isdir("/usr/share/icons/"+elem+"/48x48/"):
                    icon_dir_list = os.listdir('/usr/share/icons/'+elem+"/48x48/")
                    for directory in icon_dir_list:
                        tmp_list = os.listdir('/usr/share/icons/'+elem+"/48x48/"+directory)
                        for icon in tmp_list:
                            if icon.split('.')[0] == icon_name:
                                del usr_share_icons
                                return "/usr/share/icons/"+elem+"/48x48/"+directory+"/"+icon
        usr_share_pixmaps = os.listdir('/usr/share/pixmaps/')
        for elem in usr_share_pixmaps:
            if  os.path.isfile('/usr/share/pixmaps/'+elem):
                if elem.split('.')[0] == icon_name:
                    del usr_share_pixmaps
                    return '/usr/share/pixmaps/'+elem
        for elem in usr_share_icons:
            if  os.path.isfile('/usr/share/icons/'+elem):
                if elem.split('.')[0] == icon_name:
                    del usr_share_icons
                    return '/usr/share/icons/'+elem

        return realpath + "/base/categories/applications-system.png"
