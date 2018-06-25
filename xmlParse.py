from lxml import etree
import copy, os
import datetime

class qsysFactory:

    def __init__(self, baseFile, targetDir):

        self.__base = baseFile
        self.__target = targetDir

        with open(self.__base,'r') as f:
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

    def writeCurrentQsys(self, fileName):
        try:
            if os.path.isdir(self.__target):
                pass
            else:
                os.makedirs(self.__target)
        except OSError:
            print('Erro no setup das pastas')
            exit(1)

        with open(self.__target + fileName, 'wb') as f:
            f.write(etree.tostring(self.__currentXml))

    def resetCurrentQsys(self):
        self.__currentXml = copy.copy(self.__baseXml)




if __name__ == "__main__":

    baseFile = "/home/bcrodrigues/Dropbox/tcc/script/base/qsys/baseOriginal.qsys"
    targetDir = "/home/bcrodrigues/tcc/qsys/"

    qFac = qsysFactory(baseFile, targetDir)


    for x in range(1,2):

        nios = {'icache_size': str((x-1)*100),
                'dcache_size': str((x-1)*100)}

        qFac.modifyNios(nios)
        qFac.writeCurrentQsys('q'+str(x)+'.qsys')
        qFac.resetCurrentQsys()

