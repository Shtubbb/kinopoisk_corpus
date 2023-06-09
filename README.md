## Описание корпуса
Корпус собран из примерно 3000 рецензий на фильмы с кинопоиска. 

## Реализация
Для обработки текстов я использовал библиотеку stanza. В ней уже готовый пайплайн обработки текстов(токенизация, лемматизация, определение части речи и вычисление зависимостей)

В директории `make_corpus/` этап сбора данных, `get_info.py` ищет по слову информацию о нем и выводит содрежащее его предложение.

## Проверка работы
Все примеры лежат в директории `examples/`:
`propast*`, `teplo*`, `vzroslie*` - примеры грамматической омонимии
`zamok*` - пример лексической омонимии
`ellipse*`, - примеры недревесных явлений

## Вывод
По моим примерам можно заметить, что с омонимией пайплайн справляется хорошо, потому что я так и не смог подобрать пример на котором часть речи определяется неправильно.
Нашелся пример плохого разбора зависимостей. В `notree.png` видно, что у нас есть словосочетание "желание отвлечься или посмотреть", в котором "посмотреть" как будто зависит от "отвлечься"
С простыми эллипсами больших проблем не возникло. В `ellipse.png` видно, что в двух словах он разобрался и не сделал глагол корнем автоматически. В `ellipse1.png` недревесное явление сбило модель и "отвага, благородство, альтруизм" стали зависимы от "доброты"

В целом меня удовлетворило качество разметки. Возможно мне просто не повезло на плохие примеры или критики на кинопоиске пишут аккуратные и структурированные рецензии (все же первое вероятней)