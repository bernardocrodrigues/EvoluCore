from lxml import etree
import copy

class qsysFactory:

    def __init__(self, workingDir, base, output):

        self.__base = base
        self.__workingDir = workingDir
        self.__output = output

        with open(workingDir + base,'r') as f:
            output = f.read()
            output = output.encode('ascii')
            self.__baseXml = etree.fromstring(output)

        self.__currentXml = copy.copy(self.__baseXml)

    def getBaseQsys(self):
        return etree.tostring(self.__baseXml, pretty_print=True)

    def getCurrentQsys(self):
        return etree.tostring(self.__currentXml, pretty_print=True)

    def modifyNios(self, params):
        for element in self.__currentXml:
            if element.get('name') == 'nios2':
                for attribute in element:
                    try:
                        attribute.set('value', params[attribute.get('name')])
                    except:
                        pass
                break

    def writeCurrentQsys(self):
        with open(self.__workingDir + self.__output, 'wb') as f:
            f.write(etree.tostring(self.__currentXml))






    # for i in root:
    #     if i.get('name') == 'nios2':
    #         for x in i:
    #             if x.get('name') == "icache_size":
    #                 print(x.tag, end=' ')
    #                 print(x.text, end=' ')
    #                 print(x.get('name'), end=' ')
    #                 print(x.get('value'))
    #
    #                 x.attrib['value'] = '0'
    #
    #                 print(x.tag, end=' ')
    #                 print(x.text, end=' ')
    #                 print(x.get('name'), end=' ')
    #                 print(x.get('value'))


    #a = StringIO(output)

    #tree = etree.parse(a)

#
# # create XML
# root = etree.Element('root')
# root.append(etree.Element('child'))
# # another child with text
# child = etree.Element('child')
# child.text = 'some text'
# root.append(child)
# pretty string
#     s = etree.tostring(root, pretty_print=True)
#     print(s.decode("utf-8"))



# with open(base+"qsys/base.qsys", 'wb') as f:
#     f.write(etree.tostring(root))


if __name__ == "__main__":

    workingDir = "/home/bcrodrigues/Dropbox/tcc/script/base/qsys/"
    baseFile = "baseOriginal.qsys"
    outputFile = "base.qsys"

    qFac = qsysFactory(workingDir, baseFile, outputFile)

    nios = {'icache_size': '0',
            'dcache_size': '0'}

    qFac.modifyNios(nios)
    qFac.writeCurrentQsys()
