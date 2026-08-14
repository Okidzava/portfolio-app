from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line, Ellipse, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
import webbrowser
import os
import json
import datetime
import hashlib

Window.size = (400, 750)
Window.clearcolor = (0.035, 0.035, 0.035, 1)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENT_LANG = 'ru'
CURRENT_USER = None

COLORS = {
    'bg': (0.035, 0.035, 0.035, 1),
    'bg_secondary': (0.06, 0.06, 0.06, 1),
    'bg_card': (0.08, 0.08, 0.08, 1),
    'text_primary': (1, 1, 1, 1),
    'text_secondary': (0.85, 0.85, 0.85, 1),
    'text_muted': (0.5, 0.5, 0.5, 1),
    'accent': (0.75, 0.68, 0.45, 1),
    'accent_light': (0.85, 0.78, 0.60, 1),
    'button_dark': (0.12, 0.12, 0.12, 1),
    'button_green': (0.2, 0.6, 0.2, 1),
    'button_red': (0.6, 0.2, 0.2, 1),
    'border': (0.75, 0.68, 0.45, 0.2),
    'divider': (0.75, 0.68, 0.45, 0.1),
    'white': (1, 1, 1, 1)
}

TRANSLATIONS = {
    'ru': {
        'back': 'НАЗАД',
        'about': 'О ПРИЛОЖЕНИИ',
        'versions': 'ВЕРСИИ',
        'skills': 'НАВЫКИ',
        'experience': 'ОПЫТ',
        'contacts': 'КОНТАКТЫ',
        'edit': 'ПРАВКА',
        'save': 'СОХРАНИТЬ',
        'cancel': 'ОТМЕНА',
        'new': 'СОЗДАТЬ',
        'load': 'ЗАГРУЗИТЬ',
        'delete': 'УДАЛИТЬ',
        'no_versions': 'Нет сохранённых версий',
        'add_name_first': 'Сначала добавьте имя',
        'app_name': 'Портфолио',
        'version': 'Версия 1.4',
        'author': 'Автор: Godem',
        'empty_template': 'Пустой шаблон',
        'login': 'ВХОД',
        'register': 'РЕГИСТРАЦИЯ',
        'username': 'Имя пользователя',
        'password': 'Пароль',
        'confirm_password': 'Подтвердите пароль',
        'wrong_password': 'Неверный пароль!',
        'user_exists': 'Пользователь уже существует!',
        'password_mismatch': 'Пароли не совпадают!',
        'registered': 'Регистрация успешна!',
        'logout': 'ВЫЙТИ',
        'enter': 'Войти',
        'create': 'Создать',
        'name': 'ИМЯ',
        'export_pdf': 'ЭКСПОРТ PDF',
        'upload_photo': 'ЗАГРУЗИТЬ ФОТО',
        'photo_uploaded': 'Фото загружено',
        'exported': 'PDF экспортирован',
        'fill_all': 'Заполните все поля!',
        'reg_success': 'Регистрация успешна!'
    },
    'en': {
        'back': 'BACK',
        'about': 'ABOUT',
        'versions': 'VERSIONS',
        'skills': 'SKILLS',
        'experience': 'EXPERIENCE',
        'contacts': 'CONTACTS',
        'edit': 'EDIT',
        'save': 'SAVE',
        'cancel': 'CANCEL',
        'new': 'NEW',
        'load': 'LOAD',
        'delete': 'DEL',
        'no_versions': 'No saved versions',
        'add_name_first': 'Add name first',
        'app_name': 'Portfolio',
        'version': 'Version 1.4',
        'author': 'Author: Godem',
        'empty_template': 'Empty template',
        'login': 'LOGIN',
        'register': 'REGISTER',
        'username': 'Username',
        'password': 'Password',
        'confirm_password': 'Confirm password',
        'wrong_password': 'Wrong password!',
        'user_exists': 'User already exists!',
        'password_mismatch': 'Passwords do not match!',
        'registered': 'Registration successful!',
        'logout': 'LOGOUT',
        'enter': 'Login',
        'create': 'Create',
        'name': 'NAME',
        'export_pdf': 'EXPORT PDF',
        'upload_photo': 'UPLOAD PHOTO',
        'photo_uploaded': 'Photo uploaded',
        'exported': 'PDF exported',
        'fill_all': 'Fill all fields!',
        'reg_success': 'Registration successful!'
    }
}

def tr(key):
    return TRANSLATIONS[CURRENT_LANG].get(key, key)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_file_path(filename):
    return os.path.join(APP_DIR, filename)

USERS_FILE = get_file_path('users.json')

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(username, data):
    file_name = get_file_path(f'data_{username}.json')
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data(username):
    file_name = get_file_path(f'data_{username}.json')
    if os.path.exists(file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_versions(username, versions):
    file_name = get_file_path(f'versions_{username}.json')
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(versions, f, ensure_ascii=False, indent=4)

def load_versions(username):
    file_name = get_file_path(f'versions_{username}.json')
    if os.path.exists(file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

class Toast(Widget):
    def __init__(self, text, duration=2, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (Window.width - dp(40), dp(50))
        self.pos = (dp(20), dp(20))
        self.opacity = 0
        
        with self.canvas:
            Color(0, 0, 0, 0.8)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(25)])
        
        self.label = Label(
            text=text,
            color=(1, 1, 1, 1),
            font_size='14sp',
            size=self.size,
            pos=self.pos,
            halign='center',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.add_widget(self.label)
        
        anim = Animation(opacity=1, duration=0.3)
        anim.start(self)
        Clock.schedule_once(self.hide, duration)
    
    def hide(self, *args):
        anim = Animation(opacity=0, duration=0.3)
        anim.bind(on_complete=self._remove_from_parent)
        anim.start(self)
    
    def _remove_from_parent(self, *args):
        if self.parent:
            self.parent.remove_widget(self)

class AnimatedScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
    
    def on_enter(self):
        anim = Animation(opacity=1, duration=0.3)
        anim.start(self)
    
    def on_leave(self):
        anim = Animation(opacity=0, duration=0.2)
        anim.start(self)
    
    def show_toast(self, text, duration=2):
        toast = Toast(text, duration)
        self.add_widget(toast)

class AvatarWidget(Widget):
    def __init__(self, size, pos, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (size, size)
        self.pos = pos
        self.avatar_size = size
        self.photo_path = None
        self.bind(pos=self.redraw, size=self.redraw)
        Clock.schedule_once(lambda dt: self.redraw(), 0.1)
    
    def redraw(self, *args):
        self.canvas.clear()
        x = self.x
        y = self.y
        s = self.avatar_size
        
        with self.canvas:
            if self.photo_path and os.path.exists(self.photo_path):
                try:
                    from kivy.core.image import Image as CoreImage
                    texture = CoreImage(self.photo_path).texture
                    Color(1, 1, 1, 1)
                    Ellipse(pos=(x, y), size=(s, s), texture=texture)
                except:
                    self.draw_default(x, y, s)
            else:
                self.draw_default(x, y, s)
    
    def draw_default(self, x, y, s):
        Color(*COLORS['accent'])
        Ellipse(pos=(x, y), size=(s, s))
        Color(*COLORS['bg_secondary'])
        Ellipse(pos=(x + dp(3), y + dp(3)), size=(s - dp(6), s - dp(6)))
        Color(*COLORS['accent'])
        Line(circle=(x + s/2, y + s/2, s/2), width=dp(2))
    
    def set_photo(self, path):
        self.photo_path = path
        self.redraw()
    
    def clear_photo(self):
        self.photo_path = None
        self.redraw()

class LoginScreen(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        self.build_ui()
    
    def build_ui(self):
        global CURRENT_LANG
        self.clear_widgets()
        root = FloatLayout()
        w = Window.width
        h = Window.height
        
        lang_btn = Button(
            text="RU/EN",
            font_size="12sp",
            color=COLORS['text_secondary'],
            background_normal='',
            background_color=COLORS['button_dark'],
            size_hint=(None, None),
            size=(dp(60), dp(30)),
            pos=(w - dp(80), h - dp(50))
        )
        lang_btn.bind(on_release=self.toggle_lang)
        root.add_widget(lang_btn)
        
        title = Label(
            text=tr('app_name'),
            font_size="32sp",
            bold=True,
            color=COLORS['accent'],
            size_hint=(None, None),
            size=(w, dp(60)),
            pos=(0, h - dp(150)),
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        root.add_widget(title)
        
        self.is_login = True
        self.username_input = TextInput(
            hint_text=tr('username'),
            font_size="16sp",
            foreground_color=COLORS['text_primary'],
            background_color=COLORS['bg_card'],
            cursor_color=COLORS['text_primary'],
            size_hint=(None, None),
            size=(w - dp(60), dp(50)),
            pos=(dp(30), h - dp(270)),
            multiline=False
        )
        root.add_widget(self.username_input)
        
        self.password_input = TextInput(
            hint_text=tr('password'),
            font_size="16sp",
            foreground_color=COLORS['text_primary'],
            background_color=COLORS['bg_card'],
            cursor_color=COLORS['text_primary'],
            size_hint=(None, None),
            size=(w - dp(60), dp(50)),
            pos=(dp(30), h - dp(340)),
            multiline=False,
            password=True
        )
        root.add_widget(self.password_input)
        
        self.confirm_input = TextInput(
            hint_text=tr('confirm_password'),
            font_size="16sp",
            foreground_color=COLORS['text_primary'],
            background_color=COLORS['bg_card'],
            cursor_color=COLORS['text_primary'],
            size_hint=(None, None),
            size=(w - dp(60), dp(50)),
            pos=(dp(30), h - dp(410)),
            multiline=False,
            password=True
        )
        self.confirm_input.opacity = 0
        self.confirm_input.disabled = True
        root.add_widget(self.confirm_input)
        
        self.action_btn = Button(
            text=tr('enter'),
            font_size="18sp",
            bold=True,
            color=COLORS['text_primary'],
            background_normal='',
            background_color=COLORS['button_green'],
            size_hint=(None, None),
            size=(w - dp(60), dp(50)),
            pos=(dp(30), h - dp(480))
        )
        self.action_btn.bind(on_release=self.do_action)
        root.add_widget(self.action_btn)
        
        self.switch_btn = Button(
            text=tr('register'),
            font_size="14sp",
            color=COLORS['text_secondary'],
            background_normal='',
            background_color=(0, 0, 0, 0),
            size_hint=(None, None),
            size=(w - dp(60), dp(40)),
            pos=(dp(30), h - dp(540))
        )
        self.switch_btn.bind(on_release=self.switch_mode)
        root.add_widget(self.switch_btn)
        
        self.status_label = Label(
            text='',
            font_size="14sp",
            color=COLORS['accent'],
            size_hint=(None, None),
            size=(w - dp(60), dp(30)),
            pos=(dp(30), h - dp(590))
        )
        root.add_widget(self.status_label)
        
        self.add_widget(root)
    
    def toggle_lang(self, *args):
        global CURRENT_LANG
        CURRENT_LANG = 'en' if CURRENT_LANG == 'ru' else 'ru'
        self.build_ui()
    
    def switch_mode(self, *args):
        self.is_login = not self.is_login
        self.status_label.text = ''
        if self.is_login:
            self.action_btn.text = tr('enter')
            self.switch_btn.text = tr('register')
            self.confirm_input.opacity = 0
            self.confirm_input.disabled = True
        else:
            self.action_btn.text = tr('create')
            self.switch_btn.text = tr('login')
            self.confirm_input.opacity = 1
            self.confirm_input.disabled = False
    
    def do_action(self, *args):
        global CURRENT_USER
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        if not username or not password:
            self.status_label.text = tr('fill_all')
            return
        
        users = load_users()
        
        if self.is_login:
            if username in users:
                stored = users[username]
                if isinstance(stored, str):
                    if stored == hash_password(password):
                        CURRENT_USER = username
                        self.sm.current = 'main'
                        return
                elif isinstance(stored, dict):
                    if stored.get('password') == hash_password(password):
                        CURRENT_USER = username
                        self.sm.current = 'main'
                        return
            self.status_label.text = tr('wrong_password')
        else:
            if username in users:
                self.status_label.text = tr('user_exists')
                return
            confirm = self.confirm_input.text.strip()
            if password != confirm:
                self.status_label.text = tr('password_mismatch')
                return
            users[username] = hash_password(password)
            save_users(users)
            CURRENT_USER = username
            self.sm.current = 'main'

class EditModal(ModalView):
    def __init__(self, key, current_text, callback, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.callback = callback
        self.size_hint = (0.9, 0.8)
        self.auto_dismiss = False
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        title = Label(
            text=f"{tr('edit')}: {key.upper()}",
            font_size="18sp",
            bold=True,
            color=COLORS['text_primary'],
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(title)
        
        self.text_input = TextInput(
            text=current_text,
            font_size="16sp",
            foreground_color=COLORS['text_primary'],
            background_color=(0.1, 0.1, 0.1, 1),
            cursor_color=COLORS['text_primary'],
            size_hint=(1, 1),
            multiline=True
        )
        layout.add_widget(self.text_input)
        
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(15))
        
        save_btn = Button(
            text=tr('save'),
            font_size="16sp",
            bold=True,
            color=COLORS['text_primary'],
            background_normal='',
            background_color=COLORS['button_green'],
            size_hint_x=0.5
        )
        save_btn.bind(on_release=self.save_and_close)
        btn_layout.add_widget(save_btn)
        
        cancel_btn = Button(
            text=tr('cancel'),
            font_size="16sp",
            bold=True,
            color=COLORS['text_primary'],
            background_normal='',
            background_color=COLORS['button_red'],
            size_hint_x=0.5
        )
        cancel_btn.bind(on_release=self.dismiss)
        btn_layout.add_widget(cancel_btn)
        
        layout.add_widget(btn_layout)
        self.add_widget(layout)
    
    def save_and_close(self, *args):
        self.callback(self.key, self.text_input.text)
        self.dismiss()

class EditButton(Button):
    def __init__(self, key, current_text, callback, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.current_text = current_text
        self.callback = callback
        self.background_normal = ''
        self.background_color = COLORS['button_dark']
        self.size_hint = (None, None)
        self.size = (dp(50), dp(30))
        self.text = tr('edit')
        self.font_size = '11sp'
        self.color = COLORS['text_secondary']
        self.bold = True
        self.bind(on_release=self.open_editor)
    
    def open_editor(self, *args):
        modal = EditModal(self.key, self.current_text, self.callback)
        modal.open()

class AboutScreen(AnimatedScreen):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        root = FloatLayout()
        w = Window.width
        h = Window.height
        
        back_btn = Button(
            text=tr('back'),
            font_size="14sp",
            color=COLORS['text_primary'],
            background_normal='',
            background_color=COLORS['button_dark'],
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            pos=(dp(20), h - dp(60))
        )
        back_btn.bind(on_release=lambda x: setattr(self.sm, 'current', 'main'))
        root.add_widget(back_btn)
        
        info = Label(
            text=f"{tr('app_name')}\n{tr('version')}\n{tr('author')}\n\n{tr('empty_template')}",
            font_size="16sp",
            color=COLORS['text_secondary'],
            size_hint=(None, None),
            size=(w - dp(40), dp(200)),
            pos=(dp(20), h - dp(350)),
            halign='center',
            valign='top'
        )
        info.bind(size=info.setter('text_size'))
        root.add_widget(info)
        
        self.add_widget(root)

class VersionsScreen(AnimatedScreen):
    def __init__(self, sm, update_callback, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        self.update_callback = update_callback
        self.data = {}
        self.build_ui()
    
    def on_pre_enter(self, *args):
        global CURRENT_USER
        if CURRENT_USER:
            self.data = load_data(CURRENT_USER)
            self.load_versions_list()
    
    def build_ui(self):
        self.clear_widgets()
        root = FloatLayout()
        w = Window.width
        h = Window.height
        
        back_btn = Button(
            text=tr('back'),
            font_size="14sp",
            color=COLORS['text_primary'],
            background_normal='',
            background_color=COLORS['button_dark'],
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            pos=(dp(20), h - dp(60))
        )
        back_btn.bind(on_release=lambda x: setattr(self.sm, 'current', 'main'))
        root.add_widget(back_btn)
        
        new_btn = Button(
            text=tr('new'),
            font_size="14sp",
            bold=True,
            color=COLORS['text_primary'],
            background_normal='',
            background_color=COLORS['button_dark'],
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            pos=(w - dp(110), h - dp(60))
        )
        new_btn.bind(on_release=self.save_version)
        root.add_widget(new_btn)
        
        scroll = ScrollView(
            size_hint=(None, None),
            size=(w - dp(40), h - dp(200)),
            pos=(dp(20), dp(20))
        )
        
        self.content = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            spacing=dp(10)
        )
        self.content.bind(minimum_height=self.content.setter('height'))
        
        scroll.add_widget(self.content)
        root.add_widget(scroll)
        
        self.add_widget(root)
    
    def load_versions_list(self):
        self.content.clear_widgets()
        self.versions = load_versions(CURRENT_USER)
        if not self.versions:
            label = Label(
                text=tr('no_versions'),
                font_size="15sp",
                color=COLORS['text_muted'],
                size_hint=(1, None),
                height=dp(50)
            )
            self.content.add_widget(label)
            return
        
        for i, ver in enumerate(self.versions):
            box = BoxLayout(size_hint=(1, None), height=dp(60), spacing=dp(10))
            
            name_label = Label(
                text=ver.get('name', 'Version')[:30] or 'Untitled',
                font_size="14sp",
                color=COLORS['text_primary'],
                size_hint_x=0.5
            )
            box.add_widget(name_label)
            
            date_label = Label(
                text=ver.get('date', ''),
                font_size="11sp",
                color=COLORS['text_muted'],
                size_hint_x=0.3
            )
            box.add_widget(date_label)
            
            load_btn = Button(
                text=tr('load'),
                font_size="12sp",
                color=COLORS['text_secondary'],
                background_normal='',
                background_color=COLORS['button_dark'],
                size_hint_x=0.1
            )
            load_btn.bind(on_release=lambda x, idx=i: self.load_version(idx))
            box.add_widget(load_btn)
            
            del_btn = Button(
                text=tr('delete'),
                font_size="12sp",
                color=COLORS['text_secondary'],
                background_normal='',
                background_color=COLORS['button_dark'],
                size_hint_x=0.1
            )
            del_btn.bind(on_release=lambda x, idx=i: self.delete_version(idx))
            box.add_widget(del_btn)
            
            self.content.add_widget(box)
    
    def save_version(self, *args):
        if not self.data.get('name'):
            return
        version = self.data.copy()
        version['date'] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
        self.versions.append(version)
        save_versions(CURRENT_USER, self.versions)
        self.load_versions_list()
    
    def load_version(self, idx):
        ver = self.versions[idx]
        for key in self.data:
            self.data[key] = ver.get(key, '')
        self.update_callback(self.data)
        setattr(self.sm, 'current', 'main')
    
    def delete_version(self, idx):
        del self.versions[idx]
        save_versions(CURRENT_USER, self.versions)
        self.load_versions_list()

class NameEditorModal(ModalView):
    def __init__(self, current_text, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        self.size_hint = (0.9, 0.4)
        self.auto_dismiss = False
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        title = Label(
            text=tr('name'),
            font_size="18sp",
            bold=True,
            color=COLORS['text_primary'],
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(title)
        
        self.text_input = TextInput(
            text=current_text,
            font_size="20sp",
            foreground_color=COLORS['text_primary'],
            background_color=(0.1, 0.1, 0.1, 1),
            cursor_color=COLORS['text_primary'],
            size_hint=(1, 1),
            multiline=False
        )
        layout.add_widget(self.text_input)
        
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(15))
        
        save_btn = Button(
            text=tr('save'),
            font_size="16sp",
            bold=True,
            color=COLORS['text_primary'],
            background_normal='',
            background_color=COLORS['button_green'],
            size_hint_x=0.5
        )
        save_btn.bind(on_release=self.save_and_close)
        btn_layout.add_widget(save_btn)
        
        cancel_btn = Button(
            text=tr('cancel'),
            font_size="16sp",
            bold=True,
            color=COLORS['text_primary'],
            background_normal='',
            background_color=COLORS['button_red'],
            size_hint_x=0.5
        )
        cancel_btn.bind(on_release=self.dismiss)
        btn_layout.add_widget(cancel_btn)
        
        layout.add_widget(btn_layout)
        self.add_widget(layout)
    
    def save_and_close(self, *args):
        self.callback(self.text_input.text)
        self.dismiss()

class MainScreen(AnimatedScreen):
    def __init__(self, sm, update_callback, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        self.update_callback = update_callback
        self.data = {}
        self.avatar = None
        self.build_ui()
    
    def on_pre_enter(self, *args):
        global CURRENT_USER
        if CURRENT_USER:
            self.data = load_data(CURRENT_USER)
            self.name_label.text = self.data.get('name', '')
            if self.avatar:
                if self.data.get('photo_path'):
                    self.avatar.set_photo(self.data['photo_path'])
                else:
                    self.avatar.clear_photo()
    
    def build_ui(self):
        global CURRENT_LANG
        self.clear_widgets()
        root = FloatLayout()
        w = Window.width
        h = Window.height
        
        lang_btn = Button(
            text="RU/EN",
            font_size="12sp",
            color=COLORS['text_secondary'],
            background_normal='',
            background_color=COLORS['button_dark'],
            size_hint=(None, None),
            size=(dp(60), dp(30)),
            pos=(w - dp(80), h - dp(50))
        )
        lang_btn.bind(on_release=self.toggle_lang)
        root.add_widget(lang_btn)
        
        logout_btn = Button(
            text=tr('logout'),
            font_size="12sp",
            color=COLORS['text_secondary'],
            background_normal='',
            background_color=COLORS['button_red'],
            size_hint=(None, None),
            size=(dp(70), dp(30)),
            pos=(dp(10), h - dp(50))
        )
        logout_btn.bind(on_release=self.logout)
        root.add_widget(logout_btn)
        
        user_label = Label(
            text=f"@{CURRENT_USER}" if CURRENT_USER else "",
            font_size="12sp",
            color=COLORS['text_muted'],
            size_hint=(None, None),
            size=(dp(120), dp(30)),
            pos=(dp(90), h - dp(50)),
            halign='left',
            valign='middle'
        )
        root.add_widget(user_label)
        
        avatar_size = dp(140)
        avatar_x = (w - avatar_size) / 2
        avatar_y = h - dp(210)
        
        self.avatar = AvatarWidget(size=avatar_size, pos=(avatar_x, avatar_y))
        root.add_widget(self.avatar)
        
        if self.data.get('photo_path'):
            self.avatar.set_photo(self.data['photo_path'])
        
        upload_btn = Button(
            text=tr('upload_photo'),
            font_size="10sp",
            color=COLORS['text_secondary'],
            background_normal='',
            background_color=COLORS['button_dark'],
            size_hint=(None, None),
            size=(dp(100), dp(25)),
            pos=(w/2 - dp(50), avatar_y - dp(30))
        )
        upload_btn.bind(on_release=self.open_file_chooser)
        root.add_widget(upload_btn)
        
        name_btn = Button(
            text=tr('name'),
            font_size="12sp",
            color=COLORS['text_secondary'],
            background_normal='',
            background_color=COLORS['button_dark'],
            size_hint=(None, None),
            size=(dp(80), dp(30)),
            pos=(w/2 - dp(40), avatar_y - dp(65))
        )
        name_btn.bind(on_release=self.open_name_editor)
        root.add_widget(name_btn)
        
        self.name_label = Label(
            text='',
            font_size="20sp",
            color=COLORS['text_primary'],
            size_hint=(None, None),
            size=(w, dp(40)),
            pos=(0, avatar_y - dp(100)),
            halign='center',
            valign='middle'
        )
        self.name_label.bind(size=self.name_label.setter('text_size'))
        root.add_widget(self.name_label)
        
        button_y_start = avatar_y - dp(180)
        button_spacing = dp(60)
        button_width = w - dp(80)
        button_x = dp(40)
        
        buttons = [
            (tr('skills'), "skills"),
            (tr('experience'), "experience"),
            (tr('contacts'), "contacts"),
            (tr('versions'), "versions"),
            (tr('export_pdf'), "export"),
            (tr('about'), "about")
        ]
        
        for i, (title, action) in enumerate(buttons):
            y_pos = button_y_start - (i * button_spacing)
            btn = Button(
                text=title,
                font_size="15sp",
                color=COLORS['text_secondary'],
                background_normal='',
                background_color=COLORS['button_dark'],
                size_hint=(None, None),
                size=(button_width, dp(48)),
                pos=(button_x, y_pos)
            )
            if action == "export":
                btn.bind(on_release=self.export_pdf)
            else:
                btn.bind(on_release=lambda x, s=action: setattr(self.sm, 'current', s))
            root.add_widget(btn)
        
        footer = Label(
            text=tr('app_name'),
            font_size="10sp",
            color=COLORS['text_muted'],
            size_hint=(None, None),
            size=(w, dp(20)),
            pos=(0, dp(10)),
            halign='center',
            valign='middle'
        )
        footer.bind(size=footer.setter('text_size'))
        root.add_widget(footer)
        
        self.add_widget(root)
    
    def toggle_lang(self, *args):
        global CURRENT_LANG
        CURRENT_LANG = 'en' if CURRENT_LANG == 'ru' else 'ru'
        self.build_ui()
    
    def logout(self, *args):
        global CURRENT_USER
        CURRENT_USER = None
        self.sm.current = 'login'
    
    def open_file_chooser(self, *args):
        file_chooser = FileChooserIconView(
            path=os.path.expanduser('~'),
            filters=['*.png', '*.jpg', '*.jpeg']
        )
        popup = Popup(
            title=tr('upload_photo'),
            content=file_chooser,
            size_hint=(0.9, 0.9)
        )
        file_chooser.bind(on_submit=lambda instance, selection, *args: self.load_photo(selection, popup))
        popup.open()
    
    def load_photo(self, selection, popup):
        if selection:
            self.data['photo_path'] = selection[0]
            self.avatar.set_photo(selection[0])
            self.update_callback(self.data)
            self.show_toast(tr('photo_uploaded'))
        popup.dismiss()
    
    def open_name_editor(self, *args):
        modal = NameEditorModal(
            current_text=self.data.get('name', ''),
            callback=self.update_name
        )
        modal.open()
    
    def update_name(self, new_name):
        self.data['name'] = new_name
        self.name_label.text = new_name
        self.update_callback(self.data)
    
    def export_pdf(self, *args):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph
            
            pdf_path = get_file_path(f'portfolio_{CURRENT_USER}.pdf')
            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            if self.data.get('name'):
                story.append(Paragraph(self.data['name'], styles['Title']))
            if self.data.get('skills'):
                story.append(Paragraph(tr('skills'), styles['Heading1']))
                story.append(Paragraph(self.data['skills'].replace('\n', '<br/>'), styles['Normal']))
            if self.data.get('experience'):
                story.append(Paragraph(tr('experience'), styles['Heading1']))
                story.append(Paragraph(self.data['experience'].replace('\n', '<br/>'), styles['Normal']))
            
            doc.build(story)
            self.show_toast(tr('exported'))
            webbrowser.open(pdf_path)
        except Exception as e:
            print(f'PDF error: {e}')
            self.show_toast('Export failed')

class SkillsScreen(AnimatedScreen):
    def __init__(self, sm, update_callback, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        self.update_callback = update_callback
        self.data = {}
        self.build_ui()
    
    def on_pre_enter(self, *args):
        if CURRENT_USER:
            self.data = load_data(CURRENT_USER)
            self.main_text.text = self.data.get('skills', '')
    
    def build_ui(self):
        self.clear_widgets()
        root = FloatLayout()
        w = Window.width
        h = Window.height
        
        back_btn = Button(
            text=tr('back'),
            font_size="14sp",
            color=COLORS['text_primary'],
            background_normal='',
            background_color=COLORS['button_dark'],
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            pos=(dp(20), h - dp(60))
        )
        back_btn.bind(on_release=lambda x: setattr(self.sm, 'current', 'main'))
        root.add_widget(back_btn)
        
        title = Label(
            text=tr('skills'),
            font_size="22sp",
            bold=True,
            color=COLORS['text_primary'],
            size_hint=(None, None),
            size=(w, dp(50)),
            pos=(0, h - dp(110)),
            halign='center'
        )
        root.add_widget(title)
        
        edit_btn = EditButton(key='skills', current_text='', callback=self.update_text)
        edit_btn.pos = (w - dp(70), h - dp(90))
        root.add_widget(edit_btn)
        
        scroll = ScrollView(
            size_hint=(None, None),
            size=(w - dp(40), h - dp(200)),
            pos=(dp(20), dp(20))
        )
        
        self.main_text = Label(
            text='',
            font_size="17sp",
            color=COLORS['text_secondary'],
            size_hint=(1, None),
            height=dp(200),
            halign='left',
            valign='top'
        )
        self.main_text.bind(size=self.main_text.setter('text_size'))
        scroll.add_widget(self.main_text)
        
        root.add_widget(scroll)
        self.add_widget(root)
    
    def update_text(self, key, new_text):
        self.data['skills'] = new_text
        self.main_text.text = new_text
        self.update_callback(self.data)

class ExperienceScreen(AnimatedScreen):
    def __init__(self, sm, update_callback, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        self.update_callback = update_callback
        self.data = {}
        self.build_ui()
    
    def on_pre_enter(self, *args):
        if CURRENT_USER:
            self.data = load_data(CURRENT_USER)
            self.exp_text.text = self.data.get('experience', '')
    
    def build_ui(self):
        self.clear_widgets()
        root = FloatLayout()
        w = Window.width
        h = Window.height
        
        back_btn = Button(
            text=tr('back'),
            font_size="14sp",
            color=COLORS['text_primary'],
            background_normal='',
            background_color=COLORS['button_dark'],
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            pos=(dp(20), h - dp(60))
        )
        back_btn.bind(on_release=lambda x: setattr(self.sm, 'current', 'main'))
        root.add_widget(back_btn)
        
        title = Label(
            text=tr('experience'),
            font_size="22sp",
            bold=True,
            color=COLORS['text_primary'],
            size_hint=(None, None),
            size=(w, dp(50)),
            pos=(0, h - dp(110)),
            halign='center'
        )
        root.add_widget(title)
        
        edit_btn = EditButton(key='experience', current_text='', callback=self.update_text)
        edit_btn.pos = (w - dp(70), h - dp(90))
        root.add_widget(edit_btn)
        
        scroll = ScrollView(
            size_hint=(None, None),
            size=(w - dp(40), h - dp(200)),
            pos=(dp(20), dp(20))
        )
        
        self.exp_text = Label(
            text='',
            font_size="17sp",
            color=COLORS['text_secondary'],
            size_hint=(1, None),
            height=dp(200),
            halign='left',
            valign='top'
        )
        self.exp_text.bind(size=self.exp_text.setter('text_size'))
        scroll.add_widget(self.exp_text)
        
        root.add_widget(scroll)
        self.add_widget(root)
    
    def update_text(self, key, new_text):
        self.data['experience'] = new_text
        self.exp_text.text = new_text
        self.update_callback(self.data)

class ContactsScreen(AnimatedScreen):
    def __init__(self, sm, update_callback, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        self.update_callback = update_callback
        self.data = {}
        self.build_ui()
    
    def on_pre_enter(self, *args):
        if CURRENT_USER:
            self.data = load_data(CURRENT_USER)
            for k, widget in self.contact_widgets:
                widget.text = self.data.get(k, '')
    
    def build_ui(self):
        self.clear_widgets()
        root = FloatLayout()
        w = Window.width
        h = Window.height
        
        back_btn = Button(
            text=tr('back'),
            font_size="14sp",
            color=COLORS['text_primary'],
            background_normal='',
            background_color=COLORS['button_dark'],
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            pos=(dp(20), h - dp(60))
        )
        back_btn.bind(on_release=lambda x: setattr(self.sm, 'current', 'main'))
        root.add_widget(back_btn)
        
        title = Label(
            text=tr('contacts'),
            font_size="22sp",
            bold=True,
            color=COLORS['text_primary'],
            size_hint=(None, None),
            size=(w, dp(50)),
            pos=(0, h - dp(110)),
            halign='center'
        )
        root.add_widget(title)
        
        scroll = ScrollView(
            size_hint=(None, None),
            size=(w - dp(40), h - dp(200)),
            pos=(dp(20), dp(20))
        )
        
        content = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=dp(15))
        content.bind(minimum_height=content.setter('height'))
        
        contacts = [("Telegram", 'tg'), ("Email", 'email'), ("VK", 'vk')]
        self.contact_widgets = []
        
        for label_text, key in contacts:
            label = Label(
                text=label_text,
                font_size="14sp",
                bold=True,
                color=COLORS['text_primary'],
                size_hint=(1, None),
                height=dp(25)
            )
            content.add_widget(label)
            
            row = BoxLayout(size_hint=(1, None), height=dp(40))
            
            value_btn = Button(
                text='',
                font_size="16sp",
                color=COLORS['text_secondary'],
                background_normal='',
                background_color=(0, 0, 0, 0),
                size_hint_x=0.8
            )
            row.add_widget(value_btn)
            
            edit_btn = EditButton(key=key, current_text='', callback=self.update_contact)
            edit_btn.size = (dp(50), dp(30))
            row.add_widget(edit_btn)
            
            content.add_widget(row)
            self.contact_widgets.append((key, value_btn))
        
        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)
    
    def update_contact(self, key, new_text):
        self.data[key] = new_text
        for k, widget in self.contact_widgets:
            if k == key:
                widget.text = new_text
        self.update_callback(self.data)

class PortfolioApp(App):
    def build(self):
        global CURRENT_USER
        sm = ScreenManager(transition=FadeTransition(duration=0.3))
        
        sm.add_widget(LoginScreen(sm, name='login'))
        sm.add_widget(MainScreen(sm, self.update_data, name='main'))
        sm.add_widget(SkillsScreen(sm, self.update_data, name='skills'))
        sm.add_widget(ExperienceScreen(sm, self.update_data, name='experience'))
        sm.add_widget(ContactsScreen(sm, self.update_data, name='contacts'))
        sm.add_widget(AboutScreen(sm, name='about'))
        sm.add_widget(VersionsScreen(sm, self.update_data, name='versions'))
        
        sm.current = 'login' if not CURRENT_USER else 'main'
        
        return sm
    
    def update_data(self, new_data):
        if CURRENT_USER:
            save_data(CURRENT_USER, new_data)
    
    def on_stop(self):
        if CURRENT_USER:
            data = load_data(CURRENT_USER)
            if data:
                save_data(CURRENT_USER, data)

if __name__ == "__main__":
    PortfolioApp().run()