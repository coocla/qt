#coding:utf-8
from PyQt5.QtGui import QColor

def darker(color, degree=1, a=255): 
    r, g, b = color.red(), color.green(), color.blue() 
    r = r - 10 * degree if (r - 10 * degree) > 0 else 0 
    g = g - 10 * degree if (g - 10 * degree) > 0 else 0 
    b = b - 10 * degree if (b - 10 * degree) > 0 else 0 
    return QColor(r, g, b, a) 