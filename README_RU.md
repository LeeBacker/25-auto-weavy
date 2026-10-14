# Seedance 2.5 — AUTO Duration (720p) for Weavy

Подготовленная пользовательская модель Replicate (Cog). Модель определяет поле **Duration: Auto / 30**, по умолчанию **Auto**. Его отображение в Weavy зависит от импортёра. Вызов уходит на `bytedance/seedance-2.5/us/reference-to-video` через fal.ai. В API передаётся **настоящее значение** `"duration": "auto"` и `"resolution": "720p"` — никаких скрытых 30 секунд.

## Что требуется для публикации

1. Аккаунт на https://replicate.com/ и созданная модель https://replicate.com/create . Модель уже создана: https://replicate.com/leebacker/25-auto-weavy, аппаратный профиль CPU. Репозиторий может быть публичным; **ключи в коде не хранятся**.
2. **Без установки Docker на Windows:** создай репозиторий GitHub и загрузи туда файлы из архива (включая скрытую папку `.github`). Добавь в Settings → Secrets and variables → Actions секрет `REPLICATE_CLI_AUTH_TOKEN` (получить у Replicate). В Actions → Publish Replicate Cog model → Run workflow запусти публикацию. Адрес `r8.im/leebacker/25-auto-weavy` уже прописан. Рабочий процесс уже включён в архив.
3. **Альтернатива с Docker:** установи Docker Desktop и Cog CLI по https://replicate.com/docs/guides/build/push-a-model . Из каталога с `cog.yaml` выполни `cog login`, затем `cog push r8.im/leebacker/25-auto-weavy`.
4. В Weavy: **Import Model** → вставить `https://replicate.com/leebacker/25-auto-weavy`.
5. В поле `fal_api_key` указать **свой** ключ fal.ai. Не вставляй ключ в сообщения и не публикуй его в коде. Секретные поля поддерживаются Replicate, но поддержку передачи через интерфейс Weavy необходимо проверить отдельно.

## Поля

- `prompt`: сценарий.
- `duration`: `Auto` / `30`; по умолчанию `Auto`.
- `aspect_ratio`: `16:9` и другие форматы.
- `generate_audio`: вкл./выкл.
- `image_1`...`image_6`: до шести загружаемых изображений; в промпте указывай `@Image1`, `@Image2` и т.д.
- `video_1`: необязательный видеореференс.
- `resolution`: **зафиксировано на 720p**, 480p исключено.

## Что НЕ гарантируется

- У модели есть страница, но запускать её нельзя до отправки первой версии Cog в Replicate.
- Мы пока не знаем, сохранит ли Weavy поле `Duration: Auto` при импорте — он может менять/ограничивать UI.
- Поскольку это прокси, fal.ai выставляет отдельный счёт; дополнительно возможна тарификация Replicate и Weavy. Нет подтверждения «5–15 кредитов».
- `Auto` определяет длительность по запросу, а **не гарантирует 30 секунд**.
- Не проверено платной генерацией: без твоего аккаунта и API-ключа нельзя проверить удалённое выполнение.

## Техническая проверка

`pytest -q tests/test_inputs.py` — тесты на соответствие `Auto → "auto"`, 720p и отсутствие 480p (pytest для локальных тестов, без оплаты генераций).

Источники: https://fal.ai/models/bytedance/seedance-2.5/us/reference-to-video/api ; https://help.weavy.ai/en/articles/12265334-importing-models ; https://replicate.com/docs/guides/build/push-a-model .


## Текущая модель пользователя

- Replicate: https://replicate.com/leebacker/25-auto-weavy
- Цель публикации: `r8.im/leebacker/25-auto-weavy`
- Репозиторий GitHub: может называться `25-auto-weavy` (не требуется совпадение имён GitHub и Replicate)

### Публикация через GitHub — подробные шаги

1. Создай новый репозиторий через https://github.com/new (можно Private).
2. Распакуй ZIP и добавь в корень GitHub-репозитория `predict.py`, `cog.yaml`, `README_RU.md` и папку `.github/workflows/publish.yml`. Можно загрузить командой `git add .` / `git commit` / `git push` или средствами GitHub Desktop (он сохраняет скрытую папку).
3. Открой https://replicate.com/auth/token и создай или скопируй токен. НИКОМУ его не отправляй.
4. GitHub-репозиторий → Settings → Secrets and variables → Actions → New repository secret: **Name** `REPLICATE_CLI_AUTH_TOKEN`, **Secret** = токен Replicate.
5. GitHub → Actions → Publish Replicate Cog model → Run workflow.
6. Дождись завершения публикации; в https://replicate.com/leebacker/25-auto-weavy/versions появится версия.
7. В Weavy → Import Model → вставь ссылку Replicate и проверь `Duration` = `Auto` (без платного запуска).
8. Для реальной генерации нужен API-ключ fal.ai, который вводится только в защищённое поле (если Weavy его поддерживает).

Проверь, что публикация/импорт работают, до оплаты генерации: при `Auto` длительность выбирает модель, не гарантируется 30 сек, и расход кредитов Weavy может не уменьшиться.
