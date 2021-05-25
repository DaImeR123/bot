import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import time
from threading import Thread
import csv
import tkinter as tk
from ttkthemes import ThemedTk
import tkinter.ttk as ttk

#win = ThemedTk() #Ткинтер тема
win.set_theme('breeze') #Установка темы
win.geometry('500x300') #Размер окна
#win.resizable(0,0) #Отключение возможности изменения размера окна

var = tk.StringVar()

lbl_tok = ttk.Label(text = 'Введите токен: ', font = 'Times')
lbl_tok.place(x=1, y=1)

tok = ttk.Entry(width = 50)
tok.place(x=1, y=30)

file_path = ttk.Label(text='Укажите путь к файлу:', font = 'Times')
file_path.place(x=1,y=62)

path = ttk.Entry(width=50)
path.place(x=1, y=92)

ls = [] # Список для ввода


def accept():
	if tok.get() != '' and path.get() != '':
		ls.append(tok.get())
		ls.append(1) # 1 Если файл, 0 Если строка с ссылкой
		ls.append(path.get())
btn_check = ttk.Button(text='Подтвердить', command=accept)
btn_check.place(x=1,y=125)



def clear():
	ls.clear()
	path.delete(0, '')
	tok.delete(0, '')
btn_cls = ttk.Button(text='Очистить', command=clear)
btn_cls.place(x=99,y=125)




def get_post(api):
	with open('post.csv', mode='w', encoding = 'utf-8',newline='') as w_file:
		file = csv.DictWriter(w_file, delimiter = ',', fieldnames = ['URL', 'LIKES', 'COMMENTS', 'REPOSTS', 'VIEWS', 'GROUP', 'DATE'])
		file.writeheader() # Запись заголовков
	check = ls
	if check[1] == 0:
		url_raw = check[0]

		url = url_raw.replace('https://vk.com/wall', '')
		try:
			post = api.wall.getById(posts = url)
			with open('post.csv', mode='a+', encoding = 'utf-8',newline='') as ww_file:
				file = csv.writer(ww_file, delimiter = ',', lineterminator='\n')
				datau1 = post[0]['date']
				datanormal1 = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(datau1))
				file.writerows([[url_raw, post[0]['likes']['count'], post[0]['comments']['count'], post[0]['reposts']['count'], post[0]['views']['count'], f'https://vk.com/club{str(post[0]["owner_id"]).replace("-", "")}', datanormal1]])
		except Exception as e:
			with open('post.csv', mode='a+', encoding = 'utf-8',newline='') as ww_file:
				file = csv.writer(ww_file, delimiter = ',', lineterminator='\n')
				file.writerows([[url_raw, '', '', '', '', '', '']])

	elif check[1] == 1:
		path = check[2]

		with open(path, 'r') as f:
			lines = f.readlines()

		alls = 100 / len(lines)
		ss = 0

		for i in range(len(lines)):
			url_raw = lines[i].replace('\n', '')
			if url_raw.startswith('https'):
				url = url_raw.replace('https://vk.com/wall', '')
			elif url_raw.startswith('http'):
				url = url_raw.replace('http://vk.com/wall', '')
			else:
				with open('post.csv', mode='a+', encoding = 'utf-8',newline='') as ww_file:
					file = csv.writer(ww_file, delimiter = ',', lineterminator='\n')
					file.writerows([['', '', '', '', '', '','']])
				ss += alls
				continue
			try:
				post = api.wall.getById(posts = url)
				datau = post[0]['date']
				datanormal = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(datau))
				with open('post.csv', mode='a+', encoding = 'utf-8', newline='') as ww_file:
					file = csv.writer(ww_file, delimiter = ',', lineterminator='\n')
					file.writerows([[url_raw, post[0]['likes']['count'], post[0]['comments']['count'], post[0]['reposts']['count'], post[0]['views']['count'], f'https://vk.com/club{str(post[0]["owner_id"]).replace("-", "")}', datanormal]])
			
			except Exception as e:
				print(e)
				with open('post.csv', mode='a+', encoding = 'utf-8',newline='') as ww_file:
					file = csv.writer(ww_file, delimiter = ',', lineterminator='\n')
					url_without = url_raw.find('-')
					url_without2 = url_raw.rfind('_')

					#print('----',url_raw[url_without+1:url_without2])
					file.writerows([[url_raw, '', '', '', '', f'https://vk.com/club{url_raw[url_without+1:url_without2]}', '']])
			
			#Процентное значение и Progressbar
			ss += alls
			print(ss)
			por = tk.IntVar()
			por.set(0)
			por2 = tk.IntVar()
			por2.set(f"0%")
			lb = ttk.Label(textvariable = por2)
			por2.set(f"{int(ss)+7}%")
			lb.place(x = 395, y = 20)
			lb.update()
			pr = ttk.Progressbar(win, variable = por)
			por.set(ss)
			pr.place(x = 395, y = 1)
			#pr.set(ss)
			pr.update()
		

		por2.set('')
		lb.update()
		por.set(0)
		pr.update()
		


def main():
	try:
		if len(ls) < 3:
			if tok.get() != '' and path.get() != '':
				ls.clear()
				ls.append(tok.get())
				ls.append(1)
				ls.append(path.get())
			
	
		vk_session = vk_api.VkApi(token=ls[0])
		vk = vk_session.get_api()
		win.after(0, get_post(vk))
		win.update()
	except Exception as e:
		print(e)

btn_start = ttk.Button(text='Запустить', command=main)
btn_start.place(x=1, y=170)

win.mainloop()