'''
CableComputing v1.1 alpha
'''
#подключение библиотек
#библиотека matplotlib, изпользуется для визуализации графа
import matplotlib.pyplot as plt
#библиотека networkx, используется для работы с графами
import networkx as nx
#библиотека csv, используется для хранения графов в csv-файле
import csv
#библиотека sqlite3, используется для подключения СУБД SQLiteStudio
import sqlite3
#библиотека sys, используется для доступа к системным параметрам и функциям
import sys
#библиотека os, используется для взаимодействия с операционной системой
import os
#библиотека pyqt5, используется для работы с графическим пользовательским интерфейсом
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QFileDialog, QComboBox, \
    QMessageBox, QDialog, QTextBrowser, QTableView, QTableWidget, QTableWidgetItem
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QRect, QCoreApplication, QUrl
import io

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

HELP_FILE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body>
    <!-- Content -->
    <p><strong>CableComputing, ver. 1.1 alpha, 2023, &copy; Атаев Давид</strong></p>
    <p>&nbsp;</p>
    <h1>СПРАВКА</h1>
    <h1>Информация о версии</h1>
    <h2>Версия 1.1 alpha</h2>
    <h3>Выпущена 12.11.2023</h3>
    <h3>Предыдущая версия - 1.0 alpha</h3>
    <h2>Нововведения:</h2>
    <ul>
    <li>Расширена обработка исключений - добавлена обработка ошибок создания кабеля (ошибки -4001, -4002, -4003)</li>
    <li>Переработана система проверки имени узла, решена проблема с пропуском некорректных имен</li>
    <li>Исправлена ошибка, позволяющая создавать&nbsp;кабели с пустым значением&nbsp;типа кабеля</li>
    <li>Добавлено отображение типов кабеля в выпадающем списке при создании нового кабеля</li>
    <li>Добавлена возможность сохранения файлов</li>
    <li>Добавлена возможность изменения финальных значений общей длины кабеля</li>
    </ul>
    <h1>Ошибки</h1>
    <p>В настоящем разделе&nbsp;описаны ошибки, которые могут возникнуть в ходе работы приложения, возможные причины их возникновения и способы решения.</p>
    <h2>&nbsp;1. Неизвестная ошибка</h2>
    <h3>-1001: неизвестная ошибка</h3>
    <h2>&nbsp;2.&nbsp;Ошибки чтения файла</h2>
    <h3>-2001: несоответсвие формата csv-файла (пустая строка в неположенном месте)</h3>
    <p>Запись элементов в csv-файле графа CableComputing ведется без пустых строк. Ошибка чаще всего возникает если файл создавался вручную и не был соблюден формат, или если файл не является файлом графа.</p>
    <p>Следовательно, для решения следует проверить загружаемый файл и загрузить корректный файл.</p>
    <h3>-2002: неизвестная ошибка чтения csv-файла</h3>
    <p>Ошибка свидетельствует о несоответствии csv-файла формату, суть которого установить не удалось. Ошибка также может возникать, если файл не является файлом графа.</p>
    <p>Решение такое же как и в случае с ошибкой -2001&nbsp;&mdash; проверить загружаемый файл и загрузить корректный файл.</p>
    <h3>-2003: неизвестная ошибка чтения базы данных</h3>
    <p>Возникает при&nbsp;неудачном&nbsp;подключении&nbsp;файла базы данных и/или инициализации курсора. Возникать может если указанный файл базы данных не существует, недоступен или заблокирован.</p>
    <p>Убедитесь, что файл существует база данных доступна (не имеет пароля и т. п.). Если база данных заблокирована, закройте все соединения с базой данных и/или перезапустите её.</p>
    <h3>-2004: не выбраны все требуемые файлы</h3>
    <p>Возникает если не выбран один или оба файла.</p>
    <p>Для решения проблемы выберите оба файла.</p>
    <h2>&nbsp;3.&nbsp;Ошибки чтения файла</h2>
    <h3>-3001: узел с таким именем существует</h3>
    <p>Ошибка может возникать при создании нового узла. В таком случае её причина&nbsp;&mdash; несоблюденное условие об уникальносnи имени узла.</p>
    <p>Поменяйте имя узла, на то, которое еще не было использовано.</p>
    <p>Если ошибка возникла на этапе загрузки файла графа причиной может быть ошибка формата или дублирование внутри файла.</p>
    <p>В этом случае ошибка решается проверкой csv-файла и загрузкой корректного.</p>
    <h3>-3002: имя узла не соответсвует требованиям</h3>
    <p>Ошибка может возникать при вводе некоректного имени узла при его создании. Имя узла должно соответствовать формату A0 или AA0, где:</p>
    <p>A - любая латинская буква;</p>
    <p>0 - число от 0 до 1023 включительно.</p>
    <p>Следовательно, проблема решается сменой имени узла на соответствующее формату.</p>
    <p>Также может возникать при загрузке файла графа, что означает некорректное имя узла в csv-файле.</p>
    <p>Cоответственно, ошибка решается ручной проверкой и исправлением csv-файла.</p>
    <h3>-3003: начальный и/или конченый узел не существует</h3>
    <p>Ошибка может возникать при создаии нового кабель-канала. В таком случае её причина - указание имени несуществующего узла в поле "Начальный узел" и/или "Конечный узел".</p>
    <p>Проверьте указанные имена узлов и укажите имена существующих узлов.</p>
    <p>Если ошибка возникла на этапе загрузки файла графа причиной может быть ошибка формата или присутствие неверной записи в csv-файле.</p>
    <p>В этом случае ошибка решается проверкой csv-файла и загрузкой корректного.</p>
    <h3>-3004: неверное значение длины</h3>
    <p>Длина кабель-канала должна быть целым положительным числом. Ошибка возникает если введенное значение таковым не является.</p>
    <p>Для решения проблемы исправьте значение длины кабель-канала.</p>
    <h3>-3005: не удалось отобразить граф</h3>
    <p>Ошибка возникает при попытке визуализации графа. Может возникать при некорректном взаимодействии с модулем работы с графами или модулем визуализации.</p>
    <h2>4.&nbsp;Ошибки создания кабеля</h2>
    <h3>-4001: узлы не соединены кабель-каналами</h3>
    <p>Возникает при создании нового кабеля, если начальный и конечный путь не имеют соединения кабель-каналами между собой.</p>
    <p>Для решения проблемы либо проверьте указанные узлы, либо создайте между нужными узлами кабель-канал(ы).</p>
    <h3>-4002:&nbsp;начальный и/или конечный узел не существует</h3>
    <p>Ошибка&nbsp;возникает при создаии нового кабеля. В таком случае её причина - указание имени несуществующего узла в поле "Начальный узел" и/или "Конечный узел".</p>
    <p>Проверьте указанные имена узлов и укажите имена существующих узлов.</p>
    <h3>-4003: не указан тип кабеля</h3>
    <p>Возникает при создании нового кабеля, если указан пустой тип.</p>
    <p>Для решения укажите тип кабеля.</p>
    <h2>5.&nbsp;Ошибки сохранения файлов</h2>
    <h3>-5001:&nbsp;неизвестная ошибка</h3>
    <p>Наиболее часто возникает из-за конфликта доступа к файлу.</p>
    <p>Проверьте не открыты ли файлы в другом приложении, если да - закройте его.</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <!-- End -->
</body>
</html>
'''

UI_FILE = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>600</width>
    <height>500</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QTabWidget" name="tab_TW">
    <property name="enabled">
     <bool>true</bool>
    </property>
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>0</y>
      <width>600</width>
      <height>500</height>
     </rect>
    </property>
    <property name="currentIndex">
     <number>0</number>
    </property>
    <property name="documentMode">
     <bool>false</bool>
    </property>
    <property name="tabBarAutoHide">
     <bool>false</bool>
    </property>
    <widget class="QWidget" name="first_Tb">
     <property name="enabled">
      <bool>true</bool>
     </property>
     <attribute name="title">
      <string>Файлы проекта</string>
     </attribute>
     <widget class="QLineEdit" name="db_path_LE">
      <property name="geometry">
       <rect>
        <x>400</x>
        <y>170</y>
        <width>190</width>
        <height>20</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>190</width>
        <height>20</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>190</width>
        <height>20</height>
       </size>
      </property>
      <property name="inputMask">
       <string/>
      </property>
      <property name="readOnly">
       <bool>true</bool>
      </property>
     </widget>
     <widget class="QLabel" name="csv_info_Lb">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>15</y>
        <width>190</width>
        <height>70</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>190</width>
        <height>70</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>190</width>
        <height>70</height>
       </size>
      </property>
      <property name="text">
       <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;Выберите файл формата *.csv с записанным графом системы кабель-каналов или выберите директорию для создания нового файла и введите имя&lt;/p&gt;&lt;p&gt;&lt;br/&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
      </property>
      <property name="wordWrap">
       <bool>true</bool>
      </property>
     </widget>
     <widget class="QLabel" name="logo_Lb">
      <property name="geometry">
       <rect>
        <x>210</x>
        <y>20</y>
        <width>180</width>
        <height>120</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>180</width>
        <height>120</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>180</width>
        <height>120</height>
       </size>
      </property>
      <property name="text">
       <string>TextLabel</string>
      </property>
     </widget>
     <widget class="QPushButton" name="new_csv_PB">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>130</y>
        <width>190</width>
        <height>30</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>190</width>
        <height>30</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>190</width>
        <height>30</height>
       </size>
      </property>
      <property name="text">
       <string>Создать файл графа</string>
      </property>
     </widget>
     <widget class="QPushButton" name="new_db_PB">
      <property name="geometry">
       <rect>
        <x>400</x>
        <y>130</y>
        <width>190</width>
        <height>30</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>190</width>
        <height>30</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>190</width>
        <height>30</height>
       </size>
      </property>
      <property name="text">
       <string>Создать базу данных</string>
      </property>
     </widget>
     <widget class="QLabel" name="db_info_Lb">
      <property name="geometry">
       <rect>
        <x>400</x>
        <y>15</y>
        <width>190</width>
        <height>70</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>190</width>
        <height>70</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>190</width>
        <height>70</height>
       </size>
      </property>
      <property name="text">
       <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;Выберите файл базы данных формата *.sqlite с таблицами кабелей и общих длин или выберите директорию для создания нового файла и введите имя&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
      </property>
      <property name="wordWrap">
       <bool>true</bool>
      </property>
     </widget>
     <widget class="QLineEdit" name="csv_path_LE">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>170</y>
        <width>190</width>
        <height>20</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>190</width>
        <height>20</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>190</width>
        <height>20</height>
       </size>
      </property>
      <property name="inputMask">
       <string/>
      </property>
      <property name="readOnly">
       <bool>true</bool>
      </property>
      <property name="clearButtonEnabled">
       <bool>false</bool>
      </property>
     </widget>
     <widget class="QPushButton" name="open_db_PB">
      <property name="geometry">
       <rect>
        <x>400</x>
        <y>90</y>
        <width>190</width>
        <height>30</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>190</width>
        <height>30</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>190</width>
        <height>30</height>
       </size>
      </property>
      <property name="text">
       <string>Открыть базу данных</string>
      </property>
     </widget>
     <widget class="Line" name="line">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>430</y>
        <width>580</width>
        <height>10</height>
       </rect>
      </property>
      <property name="orientation">
       <enum>Qt::Horizontal</enum>
      </property>
     </widget>
     <widget class="QPushButton" name="load_files_PB">
      <property name="geometry">
       <rect>
        <x>250</x>
        <y>160</y>
        <width>100</width>
        <height>30</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>100</width>
        <height>30</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>100</width>
        <height>30</height>
       </size>
      </property>
      <property name="text">
       <string>Загрузить</string>
      </property>
     </widget>
     <widget class="QLabel" name="work">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>440</y>
        <width>580</width>
        <height>13</height>
       </rect>
      </property>
      <property name="text">
       <string>Проект &quot;CableComputing&quot;. Выполнил Атаев Давид, 2023 год, Москва</string>
      </property>
     </widget>
     <widget class="QPushButton" name="open_csv_PB">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>90</y>
        <width>190</width>
        <height>30</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>190</width>
        <height>30</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>190</width>
        <height>30</height>
       </size>
      </property>
      <property name="text">
       <string>Открыть файл графа</string>
      </property>
     </widget>
     <widget class="QPushButton" name="save_PB">
      <property name="geometry">
       <rect>
        <x>250</x>
        <y>200</y>
        <width>100</width>
        <height>30</height>
       </rect>
      </property>
      <property name="text">
       <string>Сохранить</string>
      </property>
     </widget>
    </widget>
    <widget class="QWidget" name="second_Tb">
     <property name="enabled">
      <bool>false</bool>
     </property>
     <attribute name="title">
      <string>Граф</string>
     </attribute>
     <widget class="QLineEdit" name="node_name_LE">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>95</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
     </widget>
     <widget class="QLabel" name="node_name_Lb">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>115</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
      <property name="text">
       <string>Имя узла</string>
      </property>
     </widget>
     <widget class="QLabel" name="new_node_h_Lb">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>15</y>
        <width>200</width>
        <height>20</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>200</width>
        <height>20</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>200</width>
        <height>20</height>
       </size>
      </property>
      <property name="font">
       <font>
        <family>MS Shell Dlg 2</family>
        <pointsize>10</pointsize>
        <weight>75</weight>
        <bold>true</bold>
       </font>
      </property>
      <property name="text">
       <string>Создать новый узел</string>
      </property>
     </widget>
     <widget class="QPushButton" name="new_node_PB">
      <property name="geometry">
       <rect>
        <x>130</x>
        <y>90</y>
        <width>150</width>
        <height>30</height>
       </rect>
      </property>
      <property name="text">
       <string>Создать узел</string>
      </property>
     </widget>
     <widget class="QLabel" name="new_duct_h_Lb">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>150</y>
        <width>200</width>
        <height>20</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>200</width>
        <height>20</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>200</width>
        <height>20</height>
       </size>
      </property>
      <property name="font">
       <font>
        <family>MS Shell Dlg 2</family>
        <pointsize>10</pointsize>
        <weight>75</weight>
        <bold>true</bold>
       </font>
      </property>
      <property name="text">
       <string>Создать новый кабель-канал</string>
      </property>
     </widget>
     <widget class="QLabel" name="start_node_Lb">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>240</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
      <property name="text">
       <string>Начальный узел</string>
      </property>
     </widget>
     <widget class="QLabel" name="end_node_Lb">
      <property name="geometry">
       <rect>
        <x>130</x>
        <y>240</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
      <property name="text">
       <string>Конечный узел</string>
      </property>
     </widget>
     <widget class="QLineEdit" name="duct_length_LE">
      <property name="geometry">
       <rect>
        <x>250</x>
        <y>220</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
     </widget>
     <widget class="QLabel" name="duct_length_Lb">
      <property name="geometry">
       <rect>
        <x>250</x>
        <y>240</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
      <property name="text">
       <string>Длина узла</string>
      </property>
     </widget>
     <widget class="QPushButton" name="new_duct_PB">
      <property name="geometry">
       <rect>
        <x>370</x>
        <y>215</y>
        <width>150</width>
        <height>30</height>
       </rect>
      </property>
      <property name="text">
       <string>Создать кабель-канал</string>
      </property>
     </widget>
     <widget class="QLabel" name="new_node_info_Lb">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>45</y>
        <width>300</width>
        <height>40</height>
       </rect>
      </property>
      <property name="text">
       <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;Введите имя узла в формате А0 или АА0, где:&lt;br&gt;А - любая латинская буква&lt;br&gt;0 - число от 0 до 1023, включительно&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
      </property>
     </widget>
     <widget class="QComboBox" name="start_node_CB">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>220</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
     </widget>
     <widget class="QComboBox" name="end_node_CB">
      <property name="geometry">
       <rect>
        <x>130</x>
        <y>220</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
     </widget>
     <widget class="QLabel" name="new_duct_info_Lb">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>180</y>
        <width>300</width>
        <height>30</height>
       </rect>
      </property>
      <property name="text">
       <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;Выберите начальный и конечный узлы из списка и укажите длину кабель-канала между ними&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
      </property>
      <property name="wordWrap">
       <bool>true</bool>
      </property>
     </widget>
     <widget class="Line" name="line_2">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>260</y>
        <width>580</width>
        <height>10</height>
       </rect>
      </property>
      <property name="orientation">
       <enum>Qt::Horizontal</enum>
      </property>
     </widget>
     <widget class="QLabel" name="graph_info_Lb">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>270</y>
        <width>200</width>
        <height>20</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>200</width>
        <height>20</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>200</width>
        <height>20</height>
       </size>
      </property>
      <property name="font">
       <font>
        <family>MS Shell Dlg 2</family>
        <pointsize>10</pointsize>
        <weight>75</weight>
        <bold>true</bold>
       </font>
      </property>
      <property name="text">
       <string>Данные о графе</string>
      </property>
     </widget>
     <widget class="QLabel" name="nodes_quantity_Lb">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>300</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
      <property name="text">
       <string>Количество узлов:</string>
      </property>
     </widget>
     <widget class="QLabel" name="ducts_quantity_Lb">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>330</y>
        <width>150</width>
        <height>20</height>
       </rect>
      </property>
      <property name="text">
       <string>Количество кабель-каналов:</string>
      </property>
     </widget>
     <widget class="QLineEdit" name="nodes_quantity_LE">
      <property name="geometry">
       <rect>
        <x>120</x>
        <y>300</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
      <property name="readOnly">
       <bool>true</bool>
      </property>
     </widget>
     <widget class="QLineEdit" name="ducts_quantity_LE">
      <property name="geometry">
       <rect>
        <x>170</x>
        <y>330</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
      <property name="readOnly">
       <bool>true</bool>
      </property>
     </widget>
     <widget class="QLabel" name="display_graph_h_Lb">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>360</y>
        <width>200</width>
        <height>20</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>200</width>
        <height>20</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>200</width>
        <height>20</height>
       </size>
      </property>
      <property name="font">
       <font>
        <family>MS Shell Dlg 2</family>
        <pointsize>10</pointsize>
        <weight>75</weight>
        <bold>true</bold>
       </font>
      </property>
      <property name="text">
       <string>Отобразить граф</string>
      </property>
     </widget>
     <widget class="QPushButton" name="display_graph_PB">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>390</y>
        <width>150</width>
        <height>30</height>
       </rect>
      </property>
      <property name="text">
       <string>Отобразить граф</string>
      </property>
     </widget>
    </widget>
    <widget class="QWidget" name="third_Tb">
     <property name="enabled">
      <bool>false</bool>
     </property>
     <attribute name="title">
      <string>Кабели</string>
     </attribute>
     <widget class="QTableWidget" name="cables_table_TW">
      <property name="geometry">
       <rect>
        <x>0</x>
        <y>0</y>
        <width>600</width>
        <height>360</height>
       </rect>
      </property>
      <property name="editTriggers">
       <set>QAbstractItemView::NoEditTriggers</set>
      </property>
     </widget>
     <widget class="QLabel" name="new_cable_h_Lb">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>365</y>
        <width>200</width>
        <height>20</height>
       </rect>
      </property>
      <property name="minimumSize">
       <size>
        <width>200</width>
        <height>20</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>200</width>
        <height>20</height>
       </size>
      </property>
      <property name="font">
       <font>
        <family>MS Shell Dlg 2</family>
        <pointsize>10</pointsize>
        <weight>75</weight>
        <bold>true</bold>
       </font>
      </property>
      <property name="text">
       <string>Добавить новый кабель</string>
      </property>
     </widget>
     <widget class="QComboBox" name="start_node_CB_2">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>410</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
     </widget>
     <widget class="QLabel" name="start_node_Lb_2">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>430</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
      <property name="text">
       <string>Начальный узел</string>
      </property>
     </widget>
     <widget class="QComboBox" name="end_node_CB_2">
      <property name="geometry">
       <rect>
        <x>130</x>
        <y>410</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
     </widget>
     <widget class="QLabel" name="end_node_Lb_2">
      <property name="geometry">
       <rect>
        <x>130</x>
        <y>430</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
      <property name="text">
       <string>Конечный узел</string>
      </property>
     </widget>
     <widget class="QComboBox" name="type_cable_CB">
      <property name="geometry">
       <rect>
        <x>250</x>
        <y>410</y>
        <width>200</width>
        <height>20</height>
       </rect>
      </property>
      <property name="editable">
       <bool>true</bool>
      </property>
     </widget>
     <widget class="QLabel" name="type_cable_Lb">
      <property name="geometry">
       <rect>
        <x>250</x>
        <y>430</y>
        <width>100</width>
        <height>20</height>
       </rect>
      </property>
      <property name="text">
       <string>Тип кабеля</string>
      </property>
     </widget>
     <widget class="QPushButton" name="new_cable_PB">
      <property name="geometry">
       <rect>
        <x>470</x>
        <y>405</y>
        <width>110</width>
        <height>30</height>
       </rect>
      </property>
      <property name="text">
       <string>Добавить кабель</string>
      </property>
     </widget>
     <widget class="QLabel" name="new_cable_info_Lb">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>385</y>
        <width>581</width>
        <height>20</height>
       </rect>
      </property>
      <property name="text">
       <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;Выберите начальный и конечный узлы из списка и укажите тип кабеля&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
      </property>
      <property name="wordWrap">
       <bool>true</bool>
      </property>
     </widget>
    </widget>
    <widget class="QWidget" name="fourth_Tb">
     <property name="enabled">
      <bool>false</bool>
     </property>
     <attribute name="title">
      <string>Итоги подсчетов</string>
     </attribute>
     <widget class="QTableWidget" name="total_table_TW">
      <property name="geometry">
       <rect>
        <x>0</x>
        <y>0</y>
        <width>600</width>
        <height>410</height>
       </rect>
      </property>
      <property name="editTriggers">
       <set>QAbstractItemView::DoubleClicked</set>
      </property>
     </widget>
     <widget class="QPushButton" name="count_total_PB">
      <property name="geometry">
       <rect>
        <x>200</x>
        <y>420</y>
        <width>200</width>
        <height>30</height>
       </rect>
      </property>
      <property name="text">
       <string>Рассчитать</string>
      </property>
     </widget>
    </widget>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>600</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

cur = 0
con = 0
csv_file_path = ''
db_file_path = ''

G = nx.Graph()


def connect_database(file_name):
    global con, cur
    global db_file_path
    try:
        con = sqlite3.connect(file_name)
        cur = con.cursor()
        db_file_path = file_name
    except Exception:
        error_dialog(-2003)


def new_database(file_name):
    global con, cur
    global db_file_path
    try:
        con = sqlite3.connect(file_name)
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS cables(
            id INT PRIMARY KEY,
            start_node TEXT,
            end_node TEXT,
            route TEXT,
            length INTEGER,
            type TEXT);
        """)
        cur.execute("""CREATE TABLE IF NOT EXISTS cable_types(
            type_name TEXT PRIMARY KEY,
            length INT);
        """)
        con.commit()
        db_file_path = file_name
    except Exception:
        error_dialog(-2003)


def check_name(name):
    if len(name) >= 2:
        if name[0] in ALPHABET and name[1] not in ALPHABET and name[1:].isdecimal():
            if int(name[1:]) >= 0 and int(name[1:]) < 1024:
                if str(int(name[1:])) == str(name[1:]):
                    return True
                else:
                    return False
            else:
                return False
        elif len(name) > 2 and name[0] in ALPHABET and name[1] in ALPHABET and name[2] not in ALPHABET and name[
                                                                                                           2:].isdecimal():
            if int(name[2:]) >= 0 and int(name[2:]) < 1024:
                if str(int(name[2:])) == str(name[2:]):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def new_node(n_name):
    name_is_ok = check_name(n_name)
    if name_is_ok and n_name not in G.nodes():
        G.add_node(n_name)
        return 0
    elif n_name in G.nodes():
        return -3001
    else:
        return -3002


def new_duct(d_start_node, d_end_node, d_length=-1):
    if d_start_node in G.nodes() and d_end_node in G.nodes():
        nodes_are_ok = True
    else:
        nodes_are_ok = False
    if str(d_length).isdecimal():
        if int(d_length) >= 0:
            length_are_ok = True
        else:
            length_are_ok = False
    else:
        length_are_ok = False
    if nodes_are_ok and length_are_ok:
        G.add_edge(d_start_node, d_end_node, length=int(d_length))
        return 0
    elif not nodes_are_ok:
        return -3003
    else:
        return -3004


def new_cable(c_start_node, c_end_node, c_type=-1):
    if c_start_node in G.nodes() and c_end_node in G.nodes() and c_type != -1 and c_type != '' and set(c_type) != {' '}:
        if nx.has_path(G, c_start_node, c_end_node):
            c_id = 0
            if len(cur.execute("SELECT id FROM cables;").fetchall()) > 0:
                c_id = max(cur.execute("SELECT id FROM cables;").fetchall())[0] + 1
            c_route = ''
            for i in nx.dijkstra_path(G, c_start_node, c_end_node, weight='length'):
                c_route += i + " -> "
            c_route = c_route[:-4]
            c_length = nx.dijkstra_path_length(G, c_start_node, c_end_node, weight='length')
            queue = f"""INSERT INTO cables(id,start_node,end_node,route,length,type)
        VALUES({c_id},'{c_start_node}','{c_end_node}','{c_route}',{str(c_length)},'{c_type}');
    """
            print(queue)
            cur.execute(queue)
            con.commit()
            return 0
        else:
            return -4001
    elif c_start_node not in G.nodes() or c_end_node not in G.nodes():
        return -4002
    elif c_type == '' or set(c_type) == {' '}:
        return -4003


def graph_open(file_name):
    global csv_file_path
    file = file_name
    G.clear()
    with open(file, 'r', newline='', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        text = list(reader)
        nodes = []
        ducts = []
        for node in text:
            if not node:
                error_dialog(-2001)
                break
            elif node[0] == '***NODES***':
                pass
            elif node[0] == 'n_name':
                pass
            elif node[0] == '***DUCTS***':
                break
            elif node[0]:
                res = int(new_node(node[0]))
                if res:
                    error_dialog(res)
                    break
            else:
                error_dialog(-2002)
        print(G.nodes())
        for duct in text[len(G.nodes()) + 2:]:
            if not duct:
                error_dialog(-2001)
                break
            elif duct[0] == '***DUCTS***':
                pass
            elif duct[0] == 'd_start_node' and duct[1] == 'd_end_node' and duct[2] == 'd_length':
                pass
            elif duct[0]:
                res = int(new_duct(duct[0], duct[1], d_length=duct[2]))
                if res:
                    error_dialog(res)
                    break
            else:
                error_dialog(-2002)
                break
        csv_file_path = file_name


def graph_save(file_name):
    file = file_name
    with open(file, 'w', newline='', encoding="utf8") as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['***NODES***'])
        writer.writerow(['n_name'])
        for nodes in nx.nodes(G):
            writer.writerow([nodes])
        writer.writerow(['***DUCTS***'])
        writer.writerow(['d_start_node', 'd_end_node', 'd_length'])
        for edges in nx.edges(G):
            writer.writerow([edges[0], edges[1], nx.get_edge_attributes(G, 'length')[edges]])


def error_dialog(err_code):
    errs = {
        -1001: 'Неизвестная ошибка: неизвестная ошибка',
        -2001: 'Ошибка чтения файла: несоответсвие формата csv-файла (пустая строка в неположенном месте)',
        -2002: 'Ошибка чтения файла: неизвестная ошибка чтения csv-файла',
        -2003: 'Ошибка чтения файла: неизвестная ошибка чтения базы данных',
        -2004: 'Ошибка чтения файла: не выбраны все требуемые файлы',
        -3001: 'Ошибка создания графа: узел с таким именем существует',
        -3002: 'Ошибка создания графа: имя узла не соответсвует требованиям',
        -3003: 'Ошибка создания графа: начальный и/или конечный узел не существует',
        -3004: 'Ошибка создания графа: неверное значение длины',
        -3005: 'Ошибка создания графа: не удалось отобразить граф',
        -4001: 'Ошибка создания кабеля: узлы не соединены кабель-каналами',
        -4002: 'Ошибка создания кабеля: начальный и/или конечный узел не существует',
        -4003: 'Ошибка создания кабеля: не указан тип кабеля',
        -5001: 'Ошибка сохранения файла: неизвестная ошибка'}

    if err_code:
        ErrDialog = QMessageBox()
        ErrDialog.setIcon(QMessageBox.Warning)
        err_text = f'Код ошибки: {err_code}\n{errs[err_code]}'
        ErrDialog.setText(err_text)
        ErrDialog.setWindowTitle('Ошибка | CableComputing')
        err_close_PB = QPushButton()
        err_help_PB = QPushButton()
        err_close_PB.setText('Закрыть')
        err_help_PB.setText('Справка')
        ErrDialog.addButton(err_close_PB, QMessageBox.AcceptRole)
        ErrDialog.addButton(err_help_PB, QMessageBox.HelpRole)
        err_help_PB.clicked.connect(help_dialog)
        ErrDialog.exec_()


def help_dialog():
    HelpDialog = QDialog()
    HelpDialog.resize(400, 300)
    HelpDialog.setMinimumSize(400, 300)
    HelpDialog.setMaximumSize(400, 300)
    HelpDialog.setWindowTitle('Справка | CableComputing')
    textBrowser_TB = QTextBrowser(HelpDialog)
    textBrowser_TB.setGeometry(QRect(0, 0, 400, 300))
    textBrowser_TB.setHtml(HELP_FILE)
    HelpDialog.exec_()


def computing_cables():
    c_dict = {}
    c_lengths_types = [(i[0], i[1]) for i in list(cur.execute("SELECT type, length FROM cables;").fetchall())]
    c_types = sorted(list(set([i[0] for i in c_lengths_types])))
    print(c_lengths_types)
    print(c_types)
    for c_length_type in c_lengths_types:
        if c_length_type[0] not in c_dict.keys():
            c_dict[c_length_type[0]] = c_length_type[1]
        else:
            c_dict[c_length_type[0]] += c_length_type[1]
    print(c_dict.keys())
    cur.execute('DELETE FROM cable_types')
    for c_type in c_types:
        queue = f"""INSERT INTO cable_types(type_name,length)
        VALUES('{c_type}',{c_dict[c_type]});
    """
        print(queue)
        cur.execute(queue)
    con.commit()
    print(c_dict)


def display_graph():
    try:
        nx.draw(G, with_labels=True)
        plt.show()
    except Exception:
        error_dialog(-3005)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(io.StringIO(UI_FILE), self)

        self.pixmap = QPixmap('logo.png').scaled(180, 120)
        self.logo_Lb.setPixmap(self.pixmap)

        self.csv_path_LE.setText('Имя файла')
        self.db_path_LE.setText('Имя файла')

        self.csv_is_picked = False
        self.db_is_picked = False
        self.csv_is_new = False
        self.db_is_new = False

        self.open_csv_PB.clicked.connect(self.open_csv)
        self.new_csv_PB.clicked.connect(self.new_csv_dir)
        self.open_db_PB.clicked.connect(self.open_db)
        self.new_db_PB.clicked.connect(self.new_db_dir)

        self.load_files_PB.clicked.connect(self.load_files)
        self.display_graph_PB.clicked.connect(self.display_graphin)
        self.new_node_PB.clicked.connect(self.make_node)
        self.new_duct_PB.clicked.connect(self.make_duct)
        self.new_cable_PB.clicked.connect(self.make_cable)
        self.count_total_PB.clicked.connect(self.total_table_load)
        self.save_PB.clicked.connect(self.save_files)
        self.total_table_TW.cellChanged.connect(self.change_value)

        print('ok')

    def change_value(self, row, column):
        if column == 1:
            print(row, column)
            print(self.total_table_TW.item(row, column).text())
            cur.execute(
                f"UPDATE cable_types SET length = '{self.total_table_TW.item(row, column).text()}' WHERE type_name = '{self.total_table_TW.item(row, 0).text()}'")

    def load_nodes_list(self):
        self.start_node_CB.clear()
        self.end_node_CB.clear()
        self.start_node_CB_2.clear()
        self.end_node_CB_2.clear()
        self.start_node_CB.addItems(G.nodes())
        self.end_node_CB.addItems(G.nodes())
        self.start_node_CB_2.addItems(G.nodes())
        self.end_node_CB_2.addItems(G.nodes())
        self.nodes_quantity_LE.setText(str(len(G.nodes())))
        self.ducts_quantity_LE.setText(str(len(G.edges())))

    def save_files(self):
        try:
            graph_save(csv_file_path)
            con.commit()
            self.save_PB.setText('Сохранить ✓')
        except Exception:
            error_dialog(-5001)

    def open_csv(self):
        self.csv_file = QFileDialog.getOpenFileName(self, 'Открыть файл графа', '', 'CSV-файл (*.csv);;Все файлы (*)')[
            0]
        self.open_csv_PB.setText('Открыть файл графа ✓')
        self.new_csv_PB.setText('Создать файл графа')
        self.csv_path_LE.setText(self.csv_file)
        self.csv_is_picked = True
        self.csv_is_new = False

    def new_csv_dir(self):
        self.csv_file = QFileDialog.getSaveFileName(self, 'Создать файл графа', '', 'CSV-файл (*.csv)')[0]
        self.new_csv_PB.setText('Создать файл графа ✓')
        self.open_csv_PB.setText('Открыть файл графа')
        self.csv_path_LE.setText(self.csv_file)
        self.csv_is_picked = True
        self.csv_is_new = True

    def open_db(self):
        self.db_file = \
        QFileDialog.getOpenFileName(self, 'Открыть базу данных', '', 'База данных SQLite (*.sqlite);;Все файлы (*)')[0]
        self.open_db_PB.setText('Открыть базу данных ✓')
        self.new_db_PB.setText('Создать базу данных')
        self.db_path_LE.setText(self.db_file)
        self.db_is_picked = True
        self.db_is_new = False

    def new_db_dir(self):
        self.db_file = QFileDialog.getSaveFileName(self, 'Создать базу данных', '', 'База данных SQLite (*.sqlite)')[0]
        self.new_db_PB.setText('Создать базу данных ✓')
        self.open_db_PB.setText('Открыть базу данных')
        self.db_path_LE.setText(self.db_file)
        self.db_is_picked = True
        self.db_is_new = True

    def load_files(self):
        if self.csv_is_picked and self.db_is_picked:
            if not self.csv_is_new:
                graph_open(self.csv_file)
                self.load_nodes_list()
            else:
                if not os.path.exists(self.csv_file):
                    file = open(f'{self.csv_file}', 'w')
                    file.close()
                else:
                    os.remove(self.csv_file)
                    file = open(f'{self.csv_file}', 'w')
                    file.close()
            if not self.db_is_new:
                connect_database(self.db_file)
            else:
                if not os.path.exists(self.db_file):
                    new_database(self.db_file)
                else:
                    os.remove(self.db_file)
                    new_database(self.db_file)
        else:
            error_dialog(-2004)
            return -2004
        self.load_files_PB.setText('Загрузить ✓')
        self.cables_table_load()
        self.total_table_load()
        self.second_Tb.setEnabled(True)
        self.third_Tb.setEnabled(True)
        self.fourth_Tb.setEnabled(True)

    def make_node(self):
        name = self.node_name_LE.text()
        error_dialog(new_node(name))
        self.load_nodes_list()

    def make_duct(self):
        start_name = self.start_node_CB.currentText()
        end_name = self.end_node_CB.currentText()
        length = self.duct_length_LE.text()
        error_dialog(new_duct(start_name, end_name, d_length=length))
        self.load_nodes_list()

    def make_cable(self):
        start_name = self.start_node_CB_2.currentText()
        end_name = self.end_node_CB_2.currentText()
        type_name = self.type_cable_CB.currentText()
        error_dialog(new_cable(start_name, end_name, c_type=type_name))
        self.cables_table_load()

    def cables_table_load(self):
        self.cables_table_TW.setColumnCount(6)
        self.cables_table_TW.setHorizontalHeaderLabels(['ID', 'Начало', 'Конец', 'Путь', 'Длина', 'Тип кабеля'])
        self.cables_table_TW.setColumnWidth(0, 50)
        self.cables_table_TW.setColumnWidth(1, 80)
        self.cables_table_TW.setColumnWidth(2, 80)
        self.cables_table_TW.setColumnWidth(4, 80)
        self.cables_table_TW.setColumnWidth(5, 190)
        data = cur.execute('SELECT * from cables').fetchall()
        self.cables_table_TW.setRowCount(len(data))
        for row_id in range(len(data)):
            for column_id in range(6):
                self.cables_table_TW.setItem(row_id, column_id, QTableWidgetItem(str(data[row_id][column_id])))
        pass

    def total_table_load(self):
        computing_cables()
        self.total_table_TW.setColumnCount(2)
        self.total_table_TW.setHorizontalHeaderLabels(['Тип кабеля', 'Общая длина'])
        self.total_table_TW.setColumnWidth(0, 480)
        self.total_table_TW.setColumnWidth(1, 100)
        data = cur.execute('SELECT * from cable_types').fetchall()
        self.type_cable_CB.addItems([i[0] for i in data])
        self.total_table_TW.setRowCount(len(data))
        for row_id in range(len(data)):
            for column_id in range(2):
                self.total_table_TW.setItem(row_id, column_id, QTableWidgetItem(str(data[row_id][column_id])))
        pass

    def display_graphin(self):
        display_graph()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = MainWindow()
        ex.show()
        sys.exit(app.exec())
    except Exception:
        error_dialog(-1001)
