from PyQt5.QtCore import QSize,QEventLoop,QThread,QObject,pyqtSignal as signal,pyqtSlot as slot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QDialog, QProgressDialog, QProgressBar
import time
import sys

# class to make the progressing work
class player(QObject):
    progress = signal(int)
    completed = signal(int)

    @slot(int)
    def do_work(self, n):
        for i in range(1, n+1):
            time.sleep(1)
            print("working")
            # LOOP AREA
            # ...
            # ...
            # ...
            # ...
            # END LOOP AREA
            self.progress.emit(i)

        self.completed.emit(i)

class barwin(QProgressDialog):
    work_requested = signal(int)  
    def __init__(self, title, limit):
        QProgressDialog.__init__(self)
        self.setMinimumSize(400,100)
        self.setWindowTitle(title)
        self.setLabelText("Loading...")
        self.setMaximum(limit)
        self.worker = player()
        self.worker_thread = QThread()
        self.setCancelButton(None)

        # signal connections
        self.worker.progress.connect(self.update_progress)
        self.worker.completed.connect(self.complete)
        self.work_requested.connect(self.worker.do_work)      
        
        # move worker to the worker thread
        self.worker.moveToThread(self.worker_thread)

        # start the thread
        self.worker_thread.start()

        # show the window
        #self.show()
        self.work_requested.emit(limit)


    def update_progress(self, v):
        print("signal arrived update")
        print(v)
        self.setValue(v)     

    def complete(self, v):
        print("signal arrived complete")
        print("stops")
        self.setValue(v) 
        self.worker_thread.quit()
        self.worker_thread.wait()

# ----------------------------------------------------------------
class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.btn_start = QPushButton('Start', clicked=self.start)
        self.setMinimumWidth(200)
        self.setMinimumHeight(100)
        self.btn_start.setMaximumWidth(200)
        self.btn_start.setMaximumHeight(100)              
        self.layout().addWidget(self.btn_start)

    def start(self):
        print("START")
        bar = barwin("progress",5)
        bar.exec()
# ----------------------------------------------------------------
app = QApplication(sys.argv)
window = main()
window.show()
app.exec()

