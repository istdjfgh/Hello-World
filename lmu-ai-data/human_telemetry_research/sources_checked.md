# Где искали (sources_checked)

Дата: 2026-10-25. Среда: облачная сессия с egress-прокси (политика по хостам). Ничего не покупалось, логины не вводились, поиск по GitHub API за пределами scope не делался.

## 1. Что доступно из среды

| Хост | Ответ | Итог |
|---|---|---|
| github.com (включая raw, codeload, gist) | 200 / 301 / 302 / 400 | доступен. Репозитории читались только после `add_repo` (см. раздел 3) |
| gitlab.com | 301 | доступен, но репозитории вне scope. Не читались |
| pypi.org, files.pythonhosted.org | 200 / 404 | доступны: JSON API и файлы пакетов. Пакеты не запускались |
| registry.npmjs.org | 200 (поиск) | доступен: метаданные и tarball'ы. Код не запускался |
| crates.io | 403 | закрыт |

**Заблокированы политикой (403 на CONNECT):** lemansultimate.wiki.gg, bsimracing.com, overtake.gg, coachdaveacademy.com, zenodo.org, huggingface.co, kaggle.com, reddit.com, store.steampowered.com, steamcommunity.com, codeberg.org, archive.org, figshare.com, data.mendeley.com, osf.io, arxiv.org, doi.org, drive.google.com, dropbox.com, mega.nz, youtube.com, racedepartment.com, semanticscholar.org, pubmed.ncbi.nlm.nih.gov, dataverse.harvard.edu, cdn.jsdelivr.net, unpkg.com.

**Не отвечают (000):** lemansultimate.com, www.lemansultimate.com, community.lemansultimate.com.

**WebFetch:** `getaddrinfo ENOTFOUND` для lemansultimate.wiki.gg, bsimracing.com, overtake.gg, coachdaveacademy.com.

Обходов не делалось: ни зеркал, ни кэшей, ни web.archive. По правилам среды блокировки указаны как есть. Поэтому все «страницы» ниже известны только из сниппетов поиска и помечены как не проверенные.

## 2. Веб-поиск (WebSearch, около 60 запросов)

Режим `standard`, если не указано иное. Пустой = ничего релевантного с данными.

**A. Общие запросы (англ.)**
1. Le Mans Ultimate telemetry duckdb wheel laps download — ссылки на NikMusy, вики, changelog v1.2 (DuckDB), overtake-инструмент, Coach Dave. Файлов нет.
2. LMU telemetry UserData Telemetry duckdb file — пусто (нерелевантный DuckDB).
3. Le Mans Ultimate full list of circuits and layouts DLC — гайды трасс 2026, onlineracedriver (2024).
4. rFactor 2 telemetry dataset steering wheel lap data — только инструменты записи, гайд AiM.
5. sim racing telemetry dataset steering throttle brake zenodo OR kaggle OR huggingface — нерелевантное (CARLA, uni.lu 2017).
6. site:reddit.com Le Mans Ultimate telemetry share laps google drive — Reddit-результатов нет.
7. site:overtake.gg Le Mans Ultimate telemetry file ld motec export — только страница инструмента.
8. Garage61 Le Mans Ultimate telemetry support public laps — подтверждения LMU нет.
9. Le Mans Ultimate Kaggle OR Zenodo OR Figshare dataset telemetry — пусто.
10. Le Mans Ultimate telemetry dataset research paper driver model rFactor 2 human laps — пусто.
11. Le Mans Ultimate telemetry files shared download players laps (extended) — LMU Desktop (JSON-экспорт), LMU Trace (платно), LMU Pitwall (портал), pavva94/LMUTelemetry (недоступен).
12. LMU telemetry duckdb tables schema laps samples channels — пусто (схемы нет).
13. LMU DuckDB telemetry file location Documents Telemetry folder export — вики: `.ld`/`.csv` в Telemetry под Documents (не официально).
14. Le Mans Ultimate telemetry channels steering wheel angle degrees export column names — колонок нет; вики относит руль к группе driver inputs.
15. Le Mans Ultimate v1.3 telemetry shared memory new channels tire data plugin update — RaceControl: новые параметры в shared memory, без списка.
16. Le Mans Ultimate reference laps download free telemetry pro driver — только платное (Coach Dave).
17. driving simulator human driver dataset steering wheel angle throttle brake lap racing paper dataset available — uni.lu (Project CARS, 25 участников), IEEE DataPort (не гонки), BROOK, Learn-to-Race, SimLingo, Udacity.
18. LMU .ldx .ld lap file shared download telemetry laps — пусто по LMU.
19. reddit LeMansUltimate telemetry lap file shared laptop wheel — пусто.
20. Le Mans Ultimate community forum telemetry thread lap data export help — форум не индексируется.
21. youtube Le Mans Ultimate telemetry download laps description link file — пусто.
22. stardance hackclub Le Mans Ultimate telemetry project devlog — только devlog, данных нет.
23. Stardance LMU Telemetry Karlito github repository — пусто (не тот проект).

**B. Сервисы и инструменты (поддержка LMU)**
24. Track Titan Le Mans Ultimate support — LMU есть, через плагин, платно; статус v1.4 не подтверждён.
25. Racelab Le Mans Ultimate telemetry plugin setup docs — установка плагина, локальные данные.
26. SimHub Le Mans Ultimate rFactor 2 shared memory support export — поддержка LMU не подтверждена.
27. Crew Chief Le Mans Ultimate telemetry logging — поддержка не подтверждена.
28. mylmu Le Mans Ultimate dashboard telemetry — mylmu не найден; LMU PIT WALL, Swizzjack.
29. Garage61 ... (см. п. 8).

**C. Языки (en → de/it/es/fr/pl/ru/zh/ja/pt)**
30. Le Mans Ultimate Telemetrie Daten Download Runden Lenkwinkel (нем.) — файлов нет; Fanatec (общие статьи).
31. Le Mans Ultimate telemetria dati giri download volante (итал.) — итальянских источников нет.
32. Le Mans Ultimate telemetría vueltas descarga datos volante (исп.) — пусто.
33. Le Mans Ultimate télémétrie tours téléchargement données volant (франц.) — пусто (промо Logitech).
34. Le Mans Ultimate telemetria okrążenia pobierz dane kierownica (польск.) — пусто.
35. Le Mans Ultimate телеметрия круги скачать данные руль (рус.) — пусто (русских гайдов нет).
36. 勒芒终极赛车 Le Mans Ultimate 遥测 数据 方向盘 下载 (кит.) — пусто (спам-страница загрузки).
37. ル・マン・ウルティメイト テレメトリー データ ハンドル 公開 (яп.) — только вики.
38. Le Mans Ultimate telemetria dados volta download arquivo (португ.) — пусто.

**D. Трассы, раскладки, DLC**
39. Le Mans Ultimate Silverstone Paul Ricard Barcelona ELMS track layouts list 2026 — раскладки Silverstone (National, International, GP), Paul Ricard (1A, 1AV2, 1AV2-short, 3A), Barcelona (non-chicane, v1.3).
40. lemansultimate.com official circuits list tracks Studio 397 — официального сайта в выдаче нет.
41. Le Mans Ultimate version 1.4 US track pass Daytona Laguna Seca tracks list — v1.4 (28.07.2026): Daytona, Laguna Seca.
42. Le Mans Ultimate US Track Pass pack two circuits announced — остальные четыре трассы не названы (одна вероятная догадка в тексте, не подтверждена).
43. Le Mans Ultimate Steam DLC list app 2399420 track packs cars — Steam недоступен; 14 трасс по гайдам.

**E. Наборы, академия, резервные симуляторы**
44. Assetto Corsa Competizione telemetry dataset public csv laps download — acr_telemetry (MoTeC-логгер), публичного датасета нет.
45. iRacing telemetry dataset public ibt laps csv download research — libibt, hotlap, REC; публичного датасета нет.
46. Automobilista 2 telemetry dataset public csv laps download — AVUS (Reiza), Other Telemetry Tool (вход по аккаунту); датасета нет.
47. rFactor 2 MoTeC ld log file sample download github parser — gotzl/ldparser, motec-i2, sim-to-motec, гайд boxthislap.
48. rFactor 2 MoTeC ld laps sample telemetry files free download shared steering wheel (extended) — RFactor2-Motec-Workspace (с sample `.ld`), DAMPlugin v0.931 (2023), Lebalap, форумы (заблокированы).
49. rFactor 2 telemetry dataset steering wheel lap data (п. 4 повтор) — см. выше.
50. Le Mans Ultimate DuckDB telemetry file location Documents Telemetry folder export (см. п. 13).

**F. Репозитории и пакеты через поиск (не через GitHub API)**
51. github le mans ultimate telemetry tool duckdb reader — NikMusy, DuckF1 (F1).
52. github LMU telemetry converter motec ld csv export — пусто по LMU (конвертеры AiM, convert.guru).
53. github rFactor 2 shared memory logger csv laps steering angle — плагины SeriousOldMan, TheIronWolf, ianv1 (без данных).
54. github rFactor 2 telemetry dataset csv laps sample data — SimRacingTelemetry, гайд boxthislap.
55. github le-mans-ultimate laps csv analysis python — пусто (MotorsportDB — реальный WEC, не симулятор).
56. github rf2 telemetry duckdb parquet lap data recorder — только документация DuckDB.
57. github racing telemetry dataset csv steering wheel degrees lap sample — hack_the_track (агрегаты), pacefinderapp (Forza), kyle-dorman (Udacity ROS-бэги).
58. PoKPoK68 hypertrace github telemetry — аккаунт/репозиторий не найден.
59. kerb rust crate racing telemetry LMU rF2 parser — kerb (живая shared memory, парсера файлов нет).
60. pypi package Le Mans Ultimate telemetry duckdb reader — пусто (duck-f1 — F1).
61. pypi motec ld file parser python sample files — gotzl/ldparser (ACC-ориентир).
62. rFactor 2 MoTeC ld log sample download github parser — см. п. 47.

Итого веб-поиск: около 60 запросов, 9 языков (считая английский за базовый), 3 площадки по сайтам (reddit, overtake, kaggle/zenodo), все без файлов LMU.

## 3. Репозитории GitHub (add_repo, read)

Добавление только для проверки данных. Читались публичные репозитории, найденные через поиск. Владелец не менялся.

| Репозиторий | Статус | Что внутри | Данные? | Решение |
|---|---|---|---|---|
| NikMusy/le-mans-ultimate-telemetry (LMU PIT WALL) | read ok, клон 568 КБ, 15 файлов | live-дашборд по rF2 shared memory, demo-режим на синтетике | нет | инструмент |
| Swizzjack/lmu-pitwall | read ok, клон 5.2 МБ, 161 файл | live-дашборд (Rust bridge), описание полей shared memory | нет (только JSON-конфиги) | инструмент, поля SM |
| mcryan123/SimRacingTelemetry | read ok, 2 файла (README, LICENSE) | описание: LMU/rF2, SQLite, экспорт CSV/Parquet в планах | нет | инструмент |
| pavva94/LMUTelemetry | add_repo: «not found or no access» | по описанию читает нативные DuckDB LMU | не проверено | не читался, повтор не делался |
| **LMU-Tracking-Desktop/tracker** | read ok, клон 39 МБ | LMU Desktop: круги в SQLite, JSON-экспорт; `prisma/dev.db` | **да: 25 кругов с телеметрией** | взято: производное |
| **orion-miller/RFactor2-Motec-Workspace** | read ok, клон 34 МБ | MoTeC-шаблон rF2 и sample `.ld` + `.ldx` | **да: rF2 (не LMU), 9 кругов** | взято: производное |
| decnet100/acr_telemetry | read ok, клон 15 МБ | ACC-логгер; `motec/Sample.ld` оказался реальным автомобилем (MoTeC M800) | sample не симулятор | исключён |
| GeekyDeaks/sim-to-motec | read ok, клон 7.6 МБ | конвертер AMS2/GT7 в MoTeC; тестовые `ams2_*.bin` (24 КБ) и CSV-базы треков | только фрагменты | не декодировано |
| gotzl/ldparser | read ok, клон 280 КБ, 5 файлов | парсер `.ld` (ориентир ACC) | нет | инструмент, свой парсер |
| Novapool/hack_the_track | read ok | ML-признаки по стинтам (агрегаты) | агрегаты, не сырые | каталог: не сырые |
| Herbertmt978/MoTeC-MCP | add_repo: «not found or no access» | — | не проверено | не читался |

Не добавлялись и не читались (плагины, библиотеки или оверлеи без данных по сниппетам): TinyPedal/TinyPedal, tariknz/irdashies (iRacing-оверлей с LMU beta), SeriousOldMan/rF2SharedMemoryMapPlugin, TheIronWolfModding/rF2SharedMemoryMapPlugin, ianv1/BSTSharedMemoryMapPlugin, afonso360/motec-i2 (Rust), estetika101/pacefinderapp (Forza), TracingInsights (F1).

GitLab и Codeberg не читались: вне scope, добавить через `add_repo` нельзя.

## 4. Реестры пакетов

**PyPI (JSON API):** имена lmu-telemetry, lmutelemetry, pylmu, le-mans-ultimate, rf2-telemetry, rfactor2, rf2-shared-memory, motec-ld, ldparser, pymotec, sim-racing-telemetry, simracing-telemetry — не найдены. racing-telemetry 0.1.6 — общая библиотека, не открывалась. libibt 0.0.5: sdist содержит только код, `.ibt` нет.

**npm (поиск по registry):** запросы «le mans ultimate», «lmu telemetry», «rfactor 2 telemetry», «rf2 shared memory», «motec ld», «racing telemetry dataset», «sim racing laps». Релевантных:
- `@rflafla/motec-ld-reader` 1.0.1 (MIT): tarball содержит только код, данных нет. **Его формула масштаба неверна** (сначала сдвиг, потом умножение). Для скорости даёт около 1700 км/ч, поэтому не использовался.
- `@hotlap.ai/telemetry` 1.4.0 (MIT): tarball содержит только код, ни одного `.ibt`.
- `@haybarn/ext-motorsport_telemetry-*`: расширение DuckDB для форматов MoTeC/AiM, данных нет.

**crates.io:** 403. Информация о kerb только из docs.rs-сниппетов.

## 5. Локальные проверки (что открыто и как)

- `tracker/prisma/dev.db` (HEAD `54a6df1`): SQLite, read-only, `immutable=1`. Таблица `Lap` содержит 28 строк, из них 24 с `telemetryJson`; `ImportedLap` содержит 1 строку с телеметрией; `Session` 21; `Track` 5; `User` 1. **Имена людей** есть в таблицах `User` и `ImportedLap`, в вывод не попадали. Формат поля: JSON-массив сэмплов на круг, ключи `d`, `t`, `th`, `br`, `st`, `rpm`, `g`, `v`, `x`, `z`, `abs`, `tc`. Определения взяты из кода `src/tracker/tracker.js` (`mUnfilteredThrottle`, `mUnfilteredBrake`, `mUnfilteredSteering`, запись в цикле 20 Гц).
- `tracker/dev.db` (корень): таблица `Lap` без строк телеметрии.
- История `tracker` (`git fetch --depth=300`): у `prisma/dev.db` четыре коммита. Один из них HEAD (та же база, SHA-256 совпадает). Остальные три более ранние: 20–22 круга с телеметрией. Все их идентификаторы кругов уже есть в HEAD: дополнительных данных нет.
- `RFactor2-Motec-Workspace`: `.ld` (15.8 МБ, 245 каналов по связному списку; в заголовке поле 78) разобран собственным парсером `scripts/ld_parse.py`. Формула масштаба проверена на скорости (0–241 км/ч), газе (0–100 %) и оборотах (0–7794). `.ldx`: только числовые настройки автомобиля (131 запись), маркеров кругов нет.
- `acr_telemetry/motec/Sample.ld`: разобран тем же парсером. Признаки реального автомобиля: `M800 Err Grp`, дата 2005, «Test Session». Исключён.

## 6. Персональные данные

- В `dev.db` есть имя человека (`User.name`, `ImportedLap.ownerName`). В `.ld` в заголовке есть поле водителя (12 символов). Ни то, ни другое не записывалось в производные файлы и каталог. Проверка: в `derived/`, `scripts/`, `catalog.csv` и этих файлах строк из полей не найдено.
- Исходные файлы (`dev.db`, `.ld`, `.ldx`) в git **не коммитились**. Их можно воспроизвести по URL и SHA-256 из `catalog.csv`.
- Ник: в поле `source` указан владелец репозитория (организация LMU-Tracking-Desktop; ник RFactor2 — orion-miller). В поле `author` записано «not stated».

## 7. Не проверено или недоступно

- Официальный список трасс и Steam-DLC — не проверены (сайты недоступны). Список собран по гайдам.
- pavva94/LMUTelemetry и Herbertmt978/MoTeC-MCP — не открыты (add_repo).
- Все источники из разделов 1 и 2, помеченные 403/000/ENOTFOUND, — не открыты.
- Блок Coach Dave, LMU Trace, Track Titan, Garage61, Overtake Telemetry Tool — только описания из сниппетов; регистрации и покупки не делались.
- Reddit, Overtake, YouTube, Discord — не открывались.
