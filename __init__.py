import os
from cudatext import *
from cudax_lib import get_translation
_ = get_translation(__file__)

class Command:
    def translate(self):
        try:
            from deep_translator import GoogleTranslator
            txt = ed.get_text_sel()
            if len(txt) >0:
                langs_list = GoogleTranslator().get_supported_languages()
                lst = ''
                for i in langs_list:
                    lst = lst + i + "\n"
                res = dlg_menu(DMENU_LIST, lst, 0, _('Supported languages'))
                if res is None: return
                lang = langs_list[res]
                translated = GoogleTranslator(source='auto', target=lang).translate(txt)
                file_open('')
                ed.set_text_all(translated)
        except ImportError:
            msg_box(_('Install first') + ': pip install -U deep-translator', MB_OK+MB_ICONERROR)