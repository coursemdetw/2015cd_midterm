# coding=utf-8
# 上面的程式內容編碼必須在程式的第一或者第二行才會有作用

################# (1) 模組導入區
# 導入 cherrypy 模組, 為了在 OpenShift 平台上使用 cherrypy 模組, 必須透過 setup.py 安裝



import cherrypy
# 導入 Python 內建的 os 模組, 因為 os 模組為 Python 內建, 所以無需透過 setup.py 安裝
import os
# 導入 random 模組
import random
# 導入 gear 模組
#import gear

################# (2) 廣域變數設定區
# 確定程式檔案所在目錄, 在 Windows 下有最後的反斜線
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
# 設定在雲端與近端的資料儲存目錄
if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示程式在雲端執行
    download_root_dir = os.environ['OPENSHIFT_DATA_DIR']
    data_dir = os.environ['OPENSHIFT_DATA_DIR']
else:
    # 表示程式在近端執行
    download_root_dir = _curdir + "/local_data/"
    data_dir = _curdir + "/local_data/"


################# (3) 程式類別定義區
# 以下改用 CherryPy 網際框架程式架構
# 以下為 Hello 類別的設計內容, 其中的 object 使用, 表示 Hello 類別繼承 object 的所有特性, 包括方法與屬性設計
class Midterm(object):

    # Midterm 類別的啟動設定
    _cp_config = {
    'tools.encode.encoding': 'utf-8',
    'tools.sessions.on' : True,
    'tools.sessions.storage_type' : 'file',
    #'tools.sessions.locking' : 'explicit',
    # session 以檔案儲存, 而且位於 data_dir 下的 tmp 目錄
    'tools.sessions.storage_path' : data_dir+'/tmp',
    # session 有效時間設為 60 分鐘
    'tools.sessions.timeout' : 60
    }

    def __init__(self):
        # hope to create downloads and images directories　
        if not os.path.isdir(download_root_dir+"downloads"):
            try:
                os.makedirs(download_root_dir+"downloads")
            except:
                print("mkdir error")
        if not os.path.isdir(download_root_dir+"images"):
            try:
                os.makedirs(download_root_dir+"images")
            except:
                print("mkdir error")
        if not os.path.isdir(download_root_dir+"tmp"):
            try:
                os.makedirs(download_root_dir+"tmp")
            except:
                print("mkdir error")
    # 以 @ 開頭的 cherrypy.expose 為 decorator, 用來表示隨後的成員方法, 可以直接讓使用者以 URL 連結執行
    @cherrypy.expose
    # index 方法為 CherryPy 各類別成員方法中的內建(default)方法, 當使用者執行時未指定方法, 系統將會優先執行 index 方法
    # 有 self 的方法為類別中的成員方法, Python 程式透過此一 self 在各成員方法間傳遞物件內容
    def index(self):
        #return "Github 2015cd_midterm 已經與 OpenShift 網站同步!"
        return "學號: scrum2"
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def spur(self, N=20, M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">
        
    <form method=POST action=spuraction>
    齒數:<input type=text name=N value='''+str(N)+'''><br />
    模數:<input type=text name=M value = '''+str(M)+'''><br />
    壓力角:<input type=text name=P value = '''+str(P)+'''><br />
    <input type=submit value=send>
    </form>
    </body>
    </html>
    '''

        return outstring
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def spuraction(self, N=20, M=5, P=15):
        output = '''
        <!doctype html><html>
        <head>
        <meta http-equiv="content-type" content="text/html;charset=utf-8">
        <title>2015CD Midterm</title>
        </head> 
        <body>
        '''
        output += "齒數為"+str(N)+"<br />"
        output += "模數為"+str(M)+"<br />"
        output += "壓力角為"+str(P)+"<br />"
        output +='''<br /><a href="/spur">spur</a>(按下後再輸入)<br />
        </body>
        </html>
        '''
        
        return output
        
        
################# (4) 程式啟動區
# 配合程式檔案所在目錄設定靜態目錄或靜態檔案
application_conf = {'/static':{
        'tools.staticdir.on': True,
        # 程式執行目錄下, 必須自行建立 static 目錄
        'tools.staticdir.dir': _curdir+"/static"},
        '/downloads':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/downloads"},
        '/images':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/images"}
    }
    
root = Midterm()
#root.gear = gear.Gear()

if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示在 OpenSfhit 執行
    application = cherrypy.Application(root, config=application_conf)
else:
    # 表示在近端執行
    cherrypy.quickstart(root, config=application_conf)
