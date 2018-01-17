import sys
import PyQt5.QtGui as qtgui
import PyQt5.QtCore as qtcore
import PyQt5.QtWidgets as widgets
from PyQt5.QtWebKitWidgets import QWebPage

class Render(QWebPage):
    def __init__(self,url):
        self.app = widgets.QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(qtcore.QUrl(url))
        self.app.exec()
        
    def _loadFinished(self):
        self.frame = self.mainFrame()
        self.app.quit()
    
    def __del__(self):
        print('__del__')
        
if __name__ == '__main__':
    URL_HUPU = 'https://nba.hupu.com/games'

    r = Render(URL_HUPU)

    result = r.frame.toHtml()
    type(result)
    r._loadFinished()