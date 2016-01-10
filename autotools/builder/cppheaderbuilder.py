#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" CPPheaderBuilder
CPP头文件建造者
"""

import basebuilder

import os
import xml.etree.cElementTree as xmllib
import xml.dom.minidom as minidom

class CPPHeaderBuilder(basebuilder.BaseBuilder):
    def __init__(self, datamodel, folder):
        super(CPPHeaderBuilder, self).__init__(datamodel)
        if type(folder) == str:
            self.folder = os.path.abspath(folder.decode('utf-8'))
        elif type(folder) == unicode:
            self.folder = folder
        else:
            raise TypeError("folder type (%s) is invalid!", str(type(folder)))
        
        self.outfiles = []
        
        
    def CloseCPPHeaderFile(self,filename):
        """关闭头文件 """    
        with open(filename, 'a') as class_definition_file:
                         # End the class definition.
            class_definition_file.write('\n};\n\n')
            # Close the conditional include statement
            class_definition_file.write('#endif\n')
      

    def CreateCPPHeaderFile(self,ns):
        """ 为每个类新建头文件 """    
        author = ''
        class_definition_file_name = '{0}.h'.format(ns)
        conditional_include_name_text = '{0}_H'.format(ns)
        conditional_include_name_text = conditional_include_name_text.upper()      
        with open(class_definition_file_name, 'w') as class_definition_file:
            # Write the class definition file header.
            stars_text = '//**********************************************************************'
            class_definition_file.write('{0}\n'.format(stars_text))
            class_definition_file.write('// Class Definition File: {0}\n'.format(class_definition_file_name))
            class_definition_file.write('// Author: {0}\n'.format(author))
            class_definition_file.write('//\n')
            class_definition_file.write('// Abstract:\n')
            class_definition_file.write('//\n')
            class_definition_file.write('//   This file contains the class definition for class {0}.\n'.format(ns))
            class_definition_file.write('//\n')
            class_definition_file.write('//\n')
            class_definition_file.write('{0}\n'.format(stars_text))
            class_definition_file.write('\n')
            class_definition_file.write('#ifndef {0}\n'.format(conditional_include_name_text))
            class_definition_file.write('#define {0}\n'.format(conditional_include_name_text))
            class_definition_file.write('#include<vector>\n')

            # Write the class definition include statements.
            # Write the bracketed include statements first.
             # Write the class definition header.
            function_header_separator_text = '//======================================================================'
            class_definition_file.write('\n{0}\n'.format(function_header_separator_text))
            class_definition_file.write('// Class Definition\n')
            class_definition_file.write('{0}\n\n'.format(function_header_separator_text))
            # Start the class definition.
            class_definition_file.write('class {0}\n{1}\n'.format(ns, '{'))
            # Write the class definition data member declarations.
            # Skip the static data members in this loop and write
            # the static declarations afterward.
            class_definition_file.write('protected:\n')
            class_definition_file.write('\n')
        return class_definition_file_name

    def CreateEnumCPPHeader(self, filename, ed_ns, ctx):
        """ 生成枚举类型头文件 """
        ed_type, ed_desc, ed_items = ctx[:3]
        ed_id = "%s.%s" %(ed_ns, ed_type)
        '''tnode = xmllib.SubElement(node, "Type", {"Id": ed_id,"Name":ed_type,
                                         "Uuid": self.GetTypeUuid(ed_type, ed_ns),
                                         "xsi:type":"Types:Enumeration",
                                         "Description":ed_desc} )'''
        with open(filename, 'a') as class_definition_file:
            # Write the class definition file header.
            class_definition_file.write('\n\n// ID: {0}'.format(ed_id))
            class_definition_file.write('\n')
            class_definition_file.write('Enum {0}'.format(ed_type))
            class_definition_file.write('{')
            buffer_item=None
            for item in ed_items:
                if buffer_item!=None:
                    it_name, it_value, it_desc = item[:3]
                    it_id = "%s.%s" %(ed_id, it_name)      
                    class_definition_file.write('{0}'.format(it_name))
                    class_definition_file.write('=')
                    class_definition_file.write('{0}'.format(it_value))
                    class_definition_file.write(',')
                buffer_item=item
            it_name, it_value, it_desc = buffer_item[:3]
            it_id = "%s.%s" %(ed_id, it_name)      
            class_definition_file.write('{0}'.format(it_name))
            class_definition_file.write('=')
            class_definition_file.write('{0}'.format(it_value))
            class_definition_file.write('};')  


 
    def BuildBegin(self):
        """ 构建准备，检查构建条件以及初始化 """
        
        if not os.path.isdir(self.folder):
            raise RuntimeError(u"folder(%s) is not exist!" % self.folder)

        self.elements = {}
        self.outfiles = []
        #append default XML namespace
    def Build(self):
        """开始构建 为每一个Namespace创建一个CPP头文件 """
        #创建Namespace element
        for ns in self.GetNamespaces():#namespace表示各种不同的类，平台类、传感器器类，
            filename = self.CreateCPPHeaderFile(ns)#为每个类建立一个枚举的头文件
            for item in self.GetItemByNamespace(ns):
                if   item.item_type == "EnumData":    #枚举类型
                    #print "enum item"
                    self.CreateEnumCPPHeader(filename, item.item_ns, item.item_val)#在头文件中加入值
            self.CloseCPPHeaderFile(filename) 
        
    def BuildEnd(self):
        """结束构建 关闭所有头文件 """
        '''for ns in self.elements:
            root = self.elements[ns]
            self.SaveNamespaceFile(ns, root)'''

    def GetFiles(self):
        return self.outfiles
