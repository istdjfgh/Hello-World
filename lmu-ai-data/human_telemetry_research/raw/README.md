# raw/ — исходные файлы намеренно не сохранены

Скачанные файлы здесь не лежат. Причина: в них есть данные людей.

- `prisma/dev.db` (LMU-Tracking-Desktop/tracker): таблицы `User` и `ImportedLap` содержат имя.
- `.ld` (orion-miller/RFactor2-Motec-Workspace): в заголовке есть поле водителя (12 символов).

Коммит файлов без изменений означал бы публикацию этих данных, а вырезать поля значит изменить файл. Поэтому в git попали только производные таблицы без имён (`../derived/`) и скрипты (`../scripts/`).

## Как получить и проверить исходники

Каждый файл восстанавливается по коммиту. Сверяйте SHA-256 с таблицей.

| Файл | Репозиторий и коммит | Путь | Размер, байт | SHA-256 |
|---|---|---|---|---|
| LMU-данные (кругов с телеметрией: 25) | github.com/LMU-Tracking-Desktop/tracker @ `54a6df1508b5b490f93bd72eb22684227d1d7431` | `prisma/dev.db` | 7 688 192 | `a5b94f1d4c772a101dfec28090e3118fa456a322a0cbb58fb15a7a4344cb55a6` |
| rF2-лог (9 полных кругов, не LMU) | github.com/orion-miller/RFactor2-Motec-Workspace @ `614bac78b70a76f01cbbbaae5a7feb3e51cb0f07` | `Sample Dataset - Matsusaka (Suzuka)/2025-08-03 - 16-34-45 - Matsusaka East Circuit - P1.ld` | 15 776 355 | `9e2216ec16d13cbe3ad85eb3004d0c12a8093a039f9e80702750e8718e7c79b4` |
| rF2-лог, маркеры XML | то же | `…P1.ldx` | 8 980 | `69dffc48d1ce7acfa4e04a6d7045fca7f14ebe241329c8827056bc75451a663c` |

Пример проверки:

```
git clone https://github.com/LMU-Tracking-Desktop/tracker
git -C tracker checkout 54a6df1508b5b490f93bd72eb22684227d1d7431
sha256sum tracker/prisma/dev.db
```

Файлы в этой папке не переписаны вручную. Производные таблицы в `../derived/` получены скриптами из `../scripts/` по этим же файлам.
