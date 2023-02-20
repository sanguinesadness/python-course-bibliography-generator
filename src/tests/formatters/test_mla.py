"""
Тестирование функций оформления списка источников по MLA 9th Edition.
"""

from formatters.base import BaseCitationFormatter
from formatters.models import (
    BookModel,
    InternetResourceModel,
    AbstractModel,
    MagazineArticleModel,
)
from formatters.styles.mla import (
    MLABook,
    MLAInternetResource,
    MLAAbstract,
    MLAMagazineArticle,
)


class TestMLA:
    """
    Тестирование оформления списка источников согласно MLA 9th Edition.
    """

    def test_abstract(self, abstract_model_fixture: AbstractModel) -> None:
        """
        Тестирование форматирования автореферата к диссертации.

        :param AbstractModel abstract_model_fixture: Фикстура автореферата к диссертации
        :return:
        """

        model = MLAAbstract(abstract_model_fixture)

        assert (
            model.formatted
            == 'Иванов И.М. Abstract of "Наука как искусство." экон., p. 199, 2020.'
        )

    def test_magazine_article(
        self, magazine_article_model_fixture: MagazineArticleModel
    ) -> None:
        """
        Тестирование форматирования статьи из журнала.

        :param AbstractModel magazine_article_model_fixture: Фикстура статьи из журнала
        :return:
        """

        model = MLAMagazineArticle(magazine_article_model_fixture)

        assert (
            model.formatted
            == 'Иванов И.М., Петров С.Н. "Наука как искусство." Образование и наука, no. 10, 2020, pp. 25-30.'
        )

    def test_book(self, book_model_fixture: BookModel) -> None:
        """
        Тестирование форматирования книги.

        :param BookModel book_model_fixture: Фикстура модели книги
        :return:
        """

        model = MLABook(book_model_fixture)

        assert (
            model.formatted
            == 'Иванов И.М., Петров С.Н. "Наука как искусство." СПб., Просвещение, 2020.'
        )

    def test_internet_resource(
        self, internet_resource_model_fixture: InternetResourceModel
    ) -> None:
        """
        Тестирование форматирования интернет-ресурса.

        :param InternetResourceModel internet_resource_model_fixture: Фикстура модели интернет-ресурса
        :return:
        """

        model = MLAInternetResource(internet_resource_model_fixture)

        assert (
            model.formatted
            == '"Наука как искусство." Ведомости, https://www.vedomosti.ru.'
        )

    def test_citation_formatter(
        self,
        book_model_fixture: BookModel,
        internet_resource_model_fixture: InternetResourceModel,
        abstract_model_fixture: AbstractModel,
        magazine_article_model_fixture: MagazineArticleModel,
    ) -> None:
        """
        Тестирование функции итогового форматирования списка источников.

        :param BookModel book_model_fixture: Фикстура модели книги
        :param InternetResourceModel internet_resource_model_fixture: Фикстура модели интернет-ресурса
        :param AbstractModel abstract_model_fixture: Фикстура модели автореферата к диссертации
        :param MagazineArticleModel magazine_article_model_fixture: Фикстура модели статьи из журнала

        :return:
        """

        models = [
            MLABook(book_model_fixture),
            MLAInternetResource(internet_resource_model_fixture),
            MLAAbstract(abstract_model_fixture),
            MLAMagazineArticle(magazine_article_model_fixture),
        ]
        result = BaseCitationFormatter(models).format()

        # тестирование сортировки списка источников
        assert result[0] == models[1]
        assert result[1] == models[2]
        assert result[2] == models[3]
        assert result[3] == models[0]
