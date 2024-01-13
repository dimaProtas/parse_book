from datetime import datetime
from ebooklib import epub
from lxml import etree
import argparse
import warnings

# Игнорирование всех предупреждений
warnings.filterwarnings("ignore")

def read_epub(file_path):
    # Открываем книгу для чтения
    book = epub.read_epub(file_path)
    # Получаем атрибуты книги и проверяем есть ли атрибут, если нет возвращаем None
    title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else None
    authors = ', '.join(author[0] for author in book.get_metadata('DC', 'creator')) if book.get_metadata('DC', 'creator') else None
    publisher = book.get_metadata('DC', 'publisher')
    name_published = ','.join(published[0] for published in publisher) if publisher else None
    date_published = book.get_metadata('DC', 'date')
    date = datetime.strptime(date_published[0][0], '%Y-%m-%dT%H:%M:%S%z').year if date_published else None

    print(f'Название книги: {title}\nАвторы: {authors}\nНазвание издательства: {name_published}\nГод издания: {date}')


def read_fb2(file_path):
    # Открываем книгу для чтения
    with open(file_path, 'r') as f:
        book = etree.parse(f)
        # Получаем атрибуты книги и проверяем есть ли атрибут, если нет возвращаем None, если есть возвращаем данные
        title = book.xpath('//fb:book-title', namespaces={'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'})[0].text

        authors = ' '.join([author.text for author in book.xpath('//fb:author/fb:first-name | //fb:author/fb:last-name',
                                                        namespaces={
                                                            'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'})])

        date_published = book.xpath('//fb:date', namespaces={'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'})[0].text

        publisher = book.xpath('//fb:publisher', namespaces={'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'})
        name_published = publisher[0].text if publisher else None

        print(f'Название книги: {title}\nАвторы: {authors}\nНазвание издательства: {name_published}\nГод издания: {date_published}' )


def read_book(file_path: str):
    # Получаем расширение книги, и в зависимости от расширения вызываем подходящий парсер
    format_book = file_path.split('.')[-1]
    print(f'Формат книги: {format_book}')
    if format_book == 'epub':
        return read_epub(file_path)
    elif format_book == 'fb2':
        return read_fb2(file_path)


# Функция для вызова в консоли
def main():
    parser = argparse.ArgumentParser(description='Скрипт для парсинга книг в формате ".epub", и ".fb2"')
    parser.add_argument('file_path', type=str, help='Полный путь к книге')

    args = parser.parse_args()

    return read_book(args.file_path)




if __name__ == '__main__':
    # path = '/home/dima_protasevich/Documents/python_proj/test_task/task_2/book/avidreaders.ru__drugoy-mir-preemnik-drevnih.epub'
    # path = '/home/dima_protasevich/Documents/python_proj/test_task/task_2/book/avidreaders.ru__brak-po-zaveschaniyu-ili-nasledstvo-s.epub'
    # read_epub(path)

    # path = '/home/dima_protasevich/Documents/python_proj/test_task/task_2/book/avidreaders.ru__drugoy-mir-preemnik-drevnih.fb2'
    # path = '/home/dima_protasevich/Documents/python_proj/test_task/task_2/book/avidreaders.ru__specgruppa-nechist.fb2'
    # read_fb2(path_fb2)

    main()