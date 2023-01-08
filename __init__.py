import os
from cudatext import *
from pathlib import Path
import json
from cudax_lib import get_translation
_ = get_translation(__file__)

try:
    from deep_translator import GoogleTranslator
    deep_translator_imported = True
except:
    deep_translator_imported = False
    msg_box(_('Install first') + ': pip install -U deep-translator', MB_OK+MB_ICONERROR)

try:
    import pyperclip
    pyperclip_imported = True
except:
    pyperclip_imported = False
    msg_box(_('Install first') + ': pip install pyperclip. For Linux also: sudo apt-get install xsel', MB_OK+MB_ICONERROR)


class Command:
    def __init__(self):
        self.conf_file = Path(app_path(APP_DIR_SETTINGS)) / 'cuda_deep_translator.json'

    def translate(self):
        if deep_translator_imported:
            langs_list = GoogleTranslator().get_supported_languages()
            lst = ''
            for i in langs_list:
                lst = lst + i + "\n"
            res = dlg_menu(DMENU_LIST, lst, 0, _('Supported languages'))
            if res is None: return
            txt = ed.get_text_sel()
            translated = GoogleTranslator(source='auto', target=langs_list[res]).translate(txt)
            if len(txt) > 0:
                return translated
            return

    def res2tab(self):
        translated = self.translate()
        if translated is not None:
            file_open('')
            ed.set_text_all(translated)
            self.actc(translated)

    def res2msgbox(self):
        translated = self.translate()
        if translated is not None:
            msg_box(translated, MB_OK+MB_ICONINFO)
            self.actc(translated)

    def res2clipboard(self):
        if pyperclip_imported:
            translated = self.translate()
            if translated is not None:
                pyperclip.copy(translated)
                msg_status('Deep Translator: ' + _('translated text copied to clipboard.'))

    def res2statusbar(self):
        translated = self.translate()
        if translated is not None:
            msg_status('Deep Translator: ' + translated)
            self.actc(translated)

    def config(self):
        if self.conf_file.exists() == False:
            with self.conf_file.open(mode='w', encoding='utf-8') as f:
                json.dump({'automatic copy to clipboard': 0}, f, indent=2)
        file_open(str(self.conf_file))

    def check_option(self, option):
        data = {}
        if self.conf_file.exists():
            with self.conf_file.open(encoding='utf-8') as f:
                data = json.load(f)
        for param, val in data.items():
            if (param == option and val == 1):
                return True

        return False

    def actc(self, translated):
        if self.check_option('automatic copy to clipboard'):
            pyperclip.copy(translated)
            msg_status('Deep Translator: ' + _('translated text copied to clipboard (option: automatic copy to clipboard).'))
