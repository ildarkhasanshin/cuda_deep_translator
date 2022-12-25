import os
from cudatext import *
from cudax_lib import get_translation
_ = get_translation(__file__)

try:
    from deep_translator import GoogleTranslator
    deep_translator_imported = True
except:
    deep_translator_imported = False
    msg_box(_('Install first') + ': pip install -U deep-translator', MB_OK+MB_ICONERROR)


class Command:
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

    def res2msgbox(self):
        translated = self.translate()
        if translated is not None:
            msg_box(translated, MB_OK+MB_ICONINFO)