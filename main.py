from flet import *  # type: ignore
import time
from gtts import gTTS
from pygame import mixer
import os
import librosa
import soundfile as sf

show_token = False
bot_is_work = False
language = 'ru'

try:
    with open("token", 'r') as file:
        bot_token = file.read().strip()
        file.close()
except:
    with open("token", 'w') as file:
        file.write("токен")
        bot_token = "токен"
        file.close()

try:
    with open("pitch", 'r') as file:
        audio_pitch = float(file.read().strip())
        file.close()
except:
    with open("pitch", 'w') as file:
        file.write("1.0")
        audio_pitch = 1.0
        file.close()

hear = True

def main(page:Page) -> None:
    page.title = f"TTS to Microphone - {language}"

    page.window_center()
    page.window.height = 600
    page.window.width = 500
    page.window_frameless = True
    # page.window_resizable = True

    try:
        with open("theme", 'r') as file:
            theme = file.read().strip()
            file.close()
            if theme == "ThemeMode.DARK":theme = ThemeMode.DARK
            else: theme = ThemeMode.LIGHT
            # print(theme)
        page.theme_mode = theme #type: ignore
    except:
        with open("theme", 'w') as file:
            file.write(str(ThemeMode.LIGHT))
            file.close()
        page.theme_mode = ThemeMode.LIGHT
    
    page.update()

    def toggle_dark_mode(e):
        if page.theme_mode == ThemeMode.DARK:
            ToggleTheme.name = icons.DARK_MODE_ROUNDED
            page.theme_mode = ThemeMode.LIGHT
            # print(page.theme_mode)

        else:
            ToggleTheme.name = icons.WB_SUNNY_ROUNDED
            page.theme_mode = ThemeMode.DARK
            # print(page.theme_mode)
        
        save_icon.color = "black" if page.theme_mode == ThemeMode.LIGHT else "white"
        language_icon.color = "black" if page.theme_mode == ThemeMode.LIGHT else "white"
        install_desk_icon.color = "black" if page.theme_mode == ThemeMode.LIGHT else "white"
        ToggleTheme.color = "black" if page.theme_mode == ThemeMode.LIGHT else "white"
        settings.icon_color = "black" if page.theme_mode == ThemeMode.LIGHT else "white"
        close_button.icon_color = "black" if page.theme_mode == ThemeMode.LIGHT else "white"
        icon_button.icon_color = "black" if page.theme_mode == ThemeMode.LIGHT else "white"
        show_token_button.icon_color = "black" if page.theme_mode == ThemeMode.LIGHT else "white"
        bot_api_apply.icon_color = "black" if page.theme_mode == ThemeMode.LIGHT else "white"
        bot_api_input.border_color = "black" if page.theme_mode == ThemeMode.LIGHT else "white"
        text_field.border_color= "black" if page.theme_mode == ThemeMode.LIGHT else "white"
        for i in message_container.controls:
            i.controls[0].bgcolor = "white" if page.theme_mode == ThemeMode.LIGHT else "black"
            # print(i.controls[0].border)
            i.controls[0].border.top.color ="white" if page.theme_mode == ThemeMode.DARK else "black"
            i.controls[0].content.color = "black" if page.theme_mode == ThemeMode.LIGHT else "white"

        with open("theme", 'w') as file:
            file.write(str(page.theme_mode))
            file.close()

        page.update()
    
    # print(page.theme_mode)
    ToggleTheme = Icon(
        icons.DARK_MODE_ROUNDED if page.theme_mode == ThemeMode.LIGHT else icons.WB_SUNNY_ROUNDED,
        color="black" if page.theme_mode == ThemeMode.LIGHT else "white"
    )

    
        
    # show_token =

    # Создаем контейнер для сообщений с возможностью прокрутки
    message_container = ListView(
        spacing=5,  # Расстояние между сообщениями
        padding=10,
        expand=True
    )

    # Функция для обработки нажатия кнопки
    def on_button_click(e):
        # Отключить кнопку и поле ввода
        icon_button.disabled = True
        text_field.disabled = True
        page.update()

        # Получить текст из текстового поля
        text = text_field.value

        # Создать скругленный квадрат с текстом
        message_box = Container(
            content=Text(text, color="white" if page.theme_mode == ThemeMode.LIGHT else "black"),
            padding=10,
            bgcolor="black" if page.theme_mode == ThemeMode.LIGHT else "white",
            border_radius=10,
            margin=2,
            border=border.all(2, color="black" if page.theme_mode == ThemeMode.LIGHT else "white"),
            expand=True  # Фиксированная ширина для сообщения
        )

        # Добавить новый скругленный квадрат в контейнер
        message_container.controls.append(
            Row(
                controls=[message_box],
                alignment=MainAxisAlignment.START,  # Выравнивание по горизонтали
                expand=False  # Чтобы занимал доступное пространство по горизонтали
            )
        )

        # Очистить текстовое поле
        text_field.value = ""

        # Обновить контейнер на странице
        page.update()

        # Сохранить и воспроизвести аудио
        if text != '':
            gTTS(text=text, lang=language, slow=False).save('text.mp3')
            file_path = "text.mp3"
            try:
                audio, sr = librosa.load(file_path, sr=None)
                print("Аудіофайл завантажено успішно!")
            except Exception as e:
                print("Помилка при завантаженні аудіофайлу:", e)
            
            pitch_shifted_audio = librosa.effects.pitch_shift(y=audio, sr=sr, n_steps=audio_pitch)  # Зміна тону на 2 півтона

            # Збереження зміненого аудіофайлу
            output_path = "text_pitched.mp3"
            try:
                sf.write(output_path, pitch_shifted_audio, sr)
                print("Змінений аудіофайл збережено успішно!")
            except Exception as e:
                print("Помилка при збереженні аудіофайлу:", e)
            
            mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')
            mixer.music.load('text_pitched.mp3')
            mixer.music.play()
            while mixer.music.get_busy():  # wait for music to finish playing
                time.sleep(1)
            else:
                mixer.music.unload()

        # Обновить цвет текста
        message_box.bgcolor = "white" if page.theme_mode == ThemeMode.LIGHT else "black"
        message_box.content = Text(text, color="black" if page.theme_mode == ThemeMode.LIGHT else "white")
        page.update()

        # Включить кнопку и поле ввода
        icon_button.disabled = False
        text_field.disabled = False
        page.update()




    # Создаем текстовое поле с обработчиком нажатия Enter
    text_field = TextField(
        label="Ввод Текста",
        expand=True,
        on_submit=on_button_click, border_color="black" if page.theme_mode == ThemeMode.LIGHT else "white"  # Устанавливаем функцию для события on_submit
    )

    def bot_token_change(e):
        global bot_token
        bot_token = bot_api_input.value

    def start_bot(e):
        global bot_is_work, bot_token, language
        if bot_is_work:
            os.system('taskkill /F /IM ttstm_bot.exe /T')
            bot_is_work = False
            bot_api_apply.icon=icons.CLOUD_OUTLINED
            page.update()
        else:
            os.system(f"start ttstm_bot.exe \"{bot_token}\" \"{language}\" {int(audio_pitch)}")
            bot_is_work = True
            bot_api_apply.icon=icons.CLOUD
            page.update()

    bot_api_input = TextField(
        label="Telegram Bot Token:", expand=True, value=bot_token,on_change=bot_token_change, #password=True, #can_reveal_password=True,
          border_color="black" if page.theme_mode == ThemeMode.LIGHT else "white"
    )

    bot_api_apply = IconButton(
        icon=icons.CLOUD_OUTLINED,
        icon_size=30,
        icon_color="black" if page.theme_mode == ThemeMode.LIGHT else "white",
        on_click=start_bot
    )
    
    # settings = IconButton(
    #     icon=icons.SETTINGS,
    
    # )

    def show_bot_buttons(e):
        global show_token  # Оголошуємо, що використовуємо глобальну змінну
        # print(show_token)
        if not show_token:
            bot_api_input.visible = True 
            # bot_api_apply.visible = True
            show_token_button.icon = icons.REMOVE_RED_EYE
            show_token = True
            page.update()
        else:
            bot_api_input.visible = False
            # bot_api_apply.visible = False
            show_token_button.icon = icons.REMOVE_RED_EYE_OUTLINED
            show_token = False
            page.update()

    def save_token(e):
        bot_token = bot_api_input.value
        with open("token", 'w') as file:
            file.write(str(bot_token))
            file.close()
    
    show_token_button = IconButton(
        icon=icons.REMOVE_RED_EYE_OUTLINED,
        icon_size=30,
        icon_color="black" if page.theme_mode == ThemeMode.LIGHT else "white",
        on_click= show_bot_buttons
    )

    title = Text(value=page.title, weight=FontWeight.BOLD, size=25)

    def ch_ru(e):
        global language
        language = 'ru'
        page.title = f"TTS to Microphone - {language}"
        title.value = page.title
        page.update()
    def ch_ua(e):
        global language
        language = 'uk'
        page.title = f"TTS to Microphone - {language}"
        title.value = page.title
        page.update()
    def ch_en(e):
        global language
        language = 'en'
        page.title = f"TTS to Microphone - {language}"
        title.value = page.title
        page.update()

    def driver(e):
        os.system("start vcable/VBCABLE_Setup.exe")
    def driver64(e):
        os.system("start vcable/VBCABLE_Setup_x64.exe")

    save_icon = Icon(icons.SAVE, color="black" if page.theme_mode == ThemeMode.LIGHT else "white")
    language_icon =Icon(icons.LANGUAGE, color="black" if page.theme_mode == ThemeMode.LIGHT else "white")
    install_desk_icon = Icon(icons.INSTALL_DESKTOP, color="black" if page.theme_mode == ThemeMode.LIGHT else "white")

    def update_audio_pitch(e):
        global audio_pitch
        audio_pitch = e.control.value
        print(audio_pitch)
        settings.items[0].content.value = f"Pitch: {audio_pitch}" #type: ignore
        with open("pitch", 'w') as file:
            file.write(str(audio_pitch))
            file.close()
        page.update()

    settings = PopupMenuButton(
        items=[
            PopupMenuItem(content=Text(f"Pitch: {audio_pitch}")),
            PopupMenuItem(content=Slider(value=audio_pitch, min=-4, max=4, divisions=21, label="{value}%", on_change=update_audio_pitch)),
            PopupMenuItem(),
            # PopupMenuItem(text="Item 1"),
            # PopupMenuItem(icon=icons.POWER_INPUT, text="Check power"),
            PopupMenuItem(
                content=Row(
                    [
                        save_icon,
                        Text("Save Telegram Token")
                    ]
                ), on_click=save_token
            ),
            PopupMenuItem(
                content=Row([ToggleTheme,Text("Toggle Dark Mode")]), on_click=toggle_dark_mode
            ),
            PopupMenuItem(),
            PopupMenuItem(
                content=Row([language_icon,Text("TTS Languages:")])
            ),
            PopupMenuItem(),
            PopupMenuItem(
                content=Text("Русский"), on_click=ch_ru
                ),
            PopupMenuItem(
                content=Text("Українська"), on_click=ch_ua
                ),
            PopupMenuItem(
                content=Text("English"), on_click=ch_en
                ),
            PopupMenuItem(),
            PopupMenuItem(
                content=Row([install_desk_icon,Text("Install/Remove Driver:")])
            ),
            PopupMenuItem(),
            PopupMenuItem(
                content=Text("x32"), on_click=driver
                ),
            PopupMenuItem(
                content=Text("x64"), on_click=driver64
                ),

            #     on_click=lambda _: print("Button with a custom content clicked!"),
            # PopupMenuItem(),  # divider
            # PopupMenuItem(
            #     text="Checked item", checked=False, on_click=check_item_clicked
            # ),
        ], icon=icons.SETTINGS,icon_size=30,icon_color="black" if page.theme_mode == ThemeMode.LIGHT else "white"
    )

    # Создаем кнопку с иконкой
    icon_button = IconButton(
        icon=icons.SEND,  # Выбираем иконку
        icon_size=30,  # Размер иконки
        icon_color="black" if page.theme_mode == ThemeMode.LIGHT else "white",
        on_click=on_button_click  # Присваиваем функцию обработки нажатия
    )

    def close_window(e):
        page.window_close()
        if bot_is_work:
            os.system('taskkill /F /IM ttstm_bot.exe /T')

    bot_api_input.visible = show_token
    # bot_api_apply.visible = show_token

    # Добавляем контент на страницу
    close_button = IconButton(icon=icons.CLOSE,icon_size=30, icon_color="black" if page.theme_mode == ThemeMode.LIGHT else "white", on_click=close_window)

    gTTS(text="ты", lang="ru", slow=False).save('text.mp3')
    file_path = "text.mp3"
    try:
        audio, sr = librosa.load(file_path, sr=None)
        print("Аудіофайл завантажено успішно!")
    except Exception as e:
        print("Помилка при завантаженні аудіофайлу:", e)

    page.add(
        Column(
            controls=[
                ResponsiveRow([
                    Row([settings,
                    WindowDragArea(
                        Row([
                            Container(
                                content=Row([title,Container(content=Row([VerticalDivider(width=77),close_button], alignment=MainAxisAlignment.END))])
                            )
                            ], alignment=MainAxisAlignment.CENTER, expand=True)
                        )
                        ])
                    ]),
                Row([show_token_button, bot_api_input, bot_api_apply]),
                message_container,  # Контейнер с прокруткой для сообщений
                Row(
                    controls=[
                        text_field,
                        icon_button
                    ],
                    alignment=MainAxisAlignment.END,  # Выравнивание по горизонтали
                    spacing=10  # Расстояние между элементами
                )
            ],
            expand=True,  # Занимает весь доступный пространство
            alignment=MainAxisAlignment.START,  # Выравнивание по горизонтали
        )
    )

# Запускаем приложение с функцией main
if __name__ == "__main__":
    app(target=main)
